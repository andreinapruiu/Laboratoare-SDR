import hashlib
import os
import random
import re
import unicodedata
import uuid
from typing import Dict, Tuple

import pandas as pd
from dotenv import load_dotenv
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import (
    AddUser,
    AddUserProperty,
    SetUserValues,
)
from recombee_api_client.exceptions import APIException

load_dotenv()

R_URL = os.getenv("RECOMBEE_URL", "").strip()
R_DB = os.getenv("RECOMBEE_DATABASE_ID", "").strip()
R_TOKEN = os.getenv("RECOMBEE_SECRET_TOKEN", "").strip()
R_REGION_STR = os.getenv("RECOMBEE_REGION", "EU_WEST").strip().upper()

CSV_PATH = os.getenv("USERS_CSV_PATH", "people.csv").strip()
MAX_USERS = os.getenv("MAX_USERS", "").strip()
MAX_USERS = int(MAX_USERS) if MAX_USERS.isdigit() else None

SINGLE_DOMAIN = os.getenv("EMAIL_DOMAIN", "").strip()
EMAIL_DOMAINS = [
    d.strip()
    for d in os.getenv("EMAIL_DOMAINS", "").split(",")
    if d.strip()
]

if not R_DB or not R_TOKEN:
    raise SystemExit(
        "Please set RECOMBEE_DATABASE_ID and RECOMBEE_SECRET_TOKEN "
        "in .env"
    )

if R_REGION_STR not in ("EU_WEST", "US_WEST"):
    raise SystemExit("RECOMBEE_REGION must be 'EU_WEST' or 'US_WEST'.")

R_REGION = getattr(Region, R_REGION_STR)
print(f"Recombee DB: {R_DB} | Region: {R_REGION_STR}")
if R_URL:
    print(f"(Info) RECOMBEE_URL provided: {R_URL}")

client = RecombeeClient(R_DB, R_TOKEN, region=R_REGION)


def slug_prop(name: str) -> str:
    """Convert a string into a valid property name slug.

    Args:
        name (str): The string to convert into a property name slug.

    Returns:
        str: A valid property name that only contains lowercase letters,
        numbers, and underscores.
    """
    norm = unicodedata.normalize('NFKD', str(name))
    base = "".join(ch for ch in norm if not unicodedata.combining(ch)).lower()
    base = re.sub(r"[^a-z0-9_]+", "_", base)
    base = re.sub(r"_+", "_", base).strip("_")
    if not base:
        base = "field"
    if base[0].isdigit():
        base = f"f_{base}"
    return base


def infer_type(series) -> str:
    """Infer the data type of a pandas Series.

    Args:
        series: A pandas Series to analyze.

    Returns:
        str: One of 'string', 'boolean', 'int', or 'double'.
    """
    s = series.dropna()
    if s.empty:
        return "string"
    low = s.astype(str).str.lower().str.strip()
    bool_vals = {"true", "1", "yes", "y", "t", "false", "0", "no", "n", "f"}
    if low.isin(bool_vals).mean() > 0.95:
        return "boolean"
    as_num = pd.to_numeric(s, errors="coerce")
    if as_num.notna().mean() > 0.9:
        if (as_num.dropna() % 1 == 0).mean() > 0.99:
            return "int"
        return "double"
    return "string"


def ascii_slug(text: str) -> str:
    """Convert text to ASCII slug format.

    Args:
        text (str): The text to convert.

    Returns:
        str: ASCII-safe slug version of the text.
    """
    if not text:
        return ""
    norm = unicodedata.normalize('NFKD', str(text))
    clean = "".join(ch for ch in norm if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9._-]+", "", clean)


def split_first_last(full_name: str) -> Tuple[str, str]:
    """Split a full name into first and last names.

    Args:
        full_name (str): The full name to split.

    Returns:
        Tuple[str, str]: A tuple of (first_name, last_name).
    """
    if not full_name:
        return "", ""
    parts = [p for p in re.split(r"\s+", str(full_name).strip()) if p]
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[-1]


def pick_domain() -> str:
    """Pick an email domain from the configured domains.

    Returns:
        str: A domain name to use for email generation.
    """
    if SINGLE_DOMAIN:
        return SINGLE_DOMAIN
    return random.choice(EMAIL_DOMAINS) if EMAIL_DOMAINS else "example.com"


def build_email_from_name(full_name: str, existing: set) -> str:
    """Build a unique email address from a person's full name.

    Args:
        full_name (str): The full name to use as a base for the email.
        existing (set): Set of existing email addresses to avoid duplicates.

    Returns:
        str: A unique email address based on the name.
    """
    first, last = split_first_last(full_name)
    first_slug = ascii_slug(first)
    last_slug = ascii_slug(last)
    candidates = []
    if first_slug and last_slug:
        candidates += [
            f"{first_slug}.{last_slug}",
            f"{first_slug}_{last_slug}",
            f"{first_slug}{last_slug}",
            f"{first_slug[0]}{last_slug}"
        ]
    elif first_slug:
        candidates += [first_slug, f"{first_slug}1"]
    elif last_slug:
        candidates += [last_slug, f"{last_slug}1"]
    else:
        candidates += ["user"]

    domain = pick_domain()
    for base in candidates:
        email = f"{base}@{domain}"
        if email not in existing:
            existing.add(email)
            return email

    base = candidates[0]
    i = 2
    while True:
        email = f"{base}{i}@{domain}"
        if email not in existing:
            existing.add(email)
            return email
        i += 1


def generate_random_user_id() -> str:
    """Generate a short random user ID (12-hex digest).

    Returns:
        str: A random 12-character hexadecimal string.
    """
    return hashlib.sha1(uuid.uuid4().bytes).hexdigest()[:12]


df = pd.read_csv(CSV_PATH)
if MAX_USERS:
    df = df.head(MAX_USERS)

if len(df) < 20:
    print(f"⚠️ Only {len(df)} rows found. The lab expects at least 20 users.")

if "Sales person" in df.columns and "sales_person" not in df.columns:
    df["sales_person"] = df["Sales person"]

if "name" not in df.columns:
    df["name"] = df.get("sales_person", "").fillna("")
    for i, row in df.iterrows():
        if not str(row.get("name") or "").strip():
            if "fullname" in df.columns and pd.notna(row.get("fullname")):
                df.at[i, "name"] = str(row["fullname"]).strip()
            else:
                df.at[i, "name"] = f"user{i+1}"

if "email" not in df.columns:
    df["email"] = None

existing_emails = set(str(e).lower() for e in df["email"].dropna().astype(str))
for i, row in df.iterrows():
    if pd.isna(row.get("email")) or not str(row.get("email")).strip():
        full = row.get("sales_person") or row.get("name") or ""
        df.at[i, "email"] = build_email_from_name(full, existing_emails)

prop_map: Dict[str, str] = {}
if "sales_person" in df.columns:
    prop_map["sales_person"] = "sales_person"
prop_map["name"] = "name"
prop_map["email"] = "email"

for col in df.columns:
    if col in prop_map:
        continue
    prop_map[col] = slug_prop(col)

created = set()
for orig, prop in prop_map.items():
    if prop in created:
        continue
    typ = infer_type(df[orig]) if orig in df.columns else "string"
    try:
        client.send(AddUserProperty(prop, typ))
        print(f"[schema:user] {prop}: {typ}")
    except APIException:
        pass
    created.add(prop)

count = 0
for i, row in df.iterrows():
    user_id = generate_random_user_id()

    try:
        client.send(AddUser(user_id))
    except APIException:
        pass

    values = {}
    for orig, prop in prop_map.items():
        val = row.get(orig)
        if pd.isna(val):
            continue
        typ = infer_type(df[orig]) if orig in df.columns else "string"
        try:
            if typ == "int":
                values[prop] = int(val)
            elif typ == "double":
                values[prop] = float(val)
            elif typ == "boolean":
                values[prop] = str(val).strip().lower() in {
                    "true", "1", "yes", "y", "t"
                }
            else:
                values[prop] = str(val)[:512]
        except Exception:
            values[prop] = str(val)[:512]

    try:
        client.send(SetUserValues(user_id, values, cascade_create=True))
        count += 1
        if count % 200 == 0:
            print(f"[users] imported {count}…")
    except APIException as e:
        print(f"[warn] user {user_id} failed: {e}")

print(f"✅ Done. Imported/updated {count} users.")
