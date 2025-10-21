import os
from dotenv import load_dotenv
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import ListUsers, DeleteUser
from recombee_api_client.exceptions import APIException

load_dotenv()

DB_ID = os.getenv("RECOMBEE_DATABASE_ID")
TOKEN = os.getenv("RECOMBEE_SECRET_TOKEN")
REGION_STR = os.getenv("RECOMBEE_REGION", "EU_WEST").upper()

if not DB_ID or not TOKEN:
    raise SystemExit("Please set RECOMBEE_DATABASE_ID and "
                     "RECOMBEE_SECRET_TOKEN in .env")

if REGION_STR not in ("EU_WEST", "US_WEST"):
    raise SystemExit("RECOMBEE_REGION must be EU_WEST or US_WEST")

client = RecombeeClient(DB_ID, TOKEN, region=getattr(Region, REGION_STR))

print(f"Connected to Recombee DB '{DB_ID}' ({REGION_STR})")
confirm = input("⚠️ This will DELETE all users (properties/schema will "
                "remain). Continue? (y/N): ").strip().lower()
if confirm not in ("y", "yes"):
    print("Aborted.")
    raise SystemExit(0)

try:
    users = client.send(ListUsers())
    print(f"Deleting {len(users)} users...")
    deleted = 0
    for user_id in users:
        try:
            client.send(DeleteUser(user_id))
            deleted += 1
            if deleted % 200 == 0:
                print(f"Deleted {deleted} users...")
        except APIException as e:
            print(f"Failed deleting user {user_id}: {e}")
    print(f"✅ Done. Deleted {deleted} users.")
except APIException as e:
    print(f"Could not list users: {e}")
