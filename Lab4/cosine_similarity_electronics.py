"""
Cosine similarity project - Electronics dataset

Steps:
1. Load ElectronicsData.csv (must be in the same folder as this script).
2. Build a textual field by combining Title + Feature.
3. Full preprocessing of text:
   - lowercase
   - remove HTML tags
   - remove non-alphabetic characters
   - tokenize
   - remove English stopwords
   - lemmatize tokens
4. Compute TF-IDF vectors for all products.
5. Compute cosine similarity matrix between all products.
6. Save similarity matrix to CSV.
7. Identify and print:
   - the most similar pair (including possible duplicates)
   - the most similar NON-identical pair (similarity < ~1.0)
"""

import re
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# NLTK imports for full preprocessing
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def ensure_nltk_resources():
    """Download NLTK resources if they are not already available."""
    needed = ["stopwords", "wordnet", "omw-1.4"]
    for resource in needed:
        try:
            nltk.data.find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource)


def preprocess_text(text, stop_words, lemmatizer):
    """
    Full preprocessing pipeline:
    - convert to lowercase
    - remove HTML tags
    - keep only letters
    - tokenize
    - remove stopwords
    - lemmatize
    Returns a cleaned string.
    """
    if not isinstance(text, str):
        text = str(text)

    # lowercase
    text = text.lower()

    # remove HTML tags if any
    text = re.sub(r"<.*?>", " ", text)

    # keep only letters (replace everything else with space)
    text = re.sub(r"[^a-z]", " ", text)

    # tokenize
    tokens = text.split()

    # remove stopwords and lemmatize
    cleaned_tokens = []
    for tok in tokens:
        if tok not in stop_words:
            lemma = lemmatizer.lemmatize(tok)
            cleaned_tokens.append(lemma)

    # join back into a string
    return " ".join(cleaned_tokens)


def main():
    # 1. Load dataset
    csv_path = "ElectronicsData.csv"  # make sure this file is in the same directory
    df = pd.read_csv(csv_path)

    # We will use both Title and Feature columns as our text
    # (these are present in the uploaded ElectronicsData.csv)
    df["Title"] = df["Title"].fillna("")
    df["Feature"] = df["Feature"].fillna("")

    # combined text field
    df["text_raw"] = (df["Title"] + " " + df["Feature"]).str.strip()

    # 2. Prepare NLTK tools
    ensure_nltk_resources()
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    # 3. Apply full preprocessing to all documents
    print("Preprocessing text... This may take a few seconds.")
    df["text_clean"] = df["text_raw"].apply(
        lambda t: preprocess_text(t, stop_words, lemmatizer)
    )

    # 4. TF-IDF vectorization
    print("Computing TF-IDF matrix...")
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["text_clean"])

    print("TF-IDF matrix shape:", tfidf_matrix.shape)

    # 5. Cosine similarity matrix
    print("Computing cosine similarity matrix...")
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # zero out self-similarity on the diagonal
    np.fill_diagonal(similarity_matrix, 0.0)

    # 6. Save similarity matrix to CSV (optional, but nice for the assignment)
    print("Saving similarity matrix to similarity_matrix.csv ...")
    sim_df = pd.DataFrame(
        similarity_matrix,
        index=df["Title"],
        columns=df["Title"],
    )
    sim_df.to_csv("similarity_matrix.csv", encoding="utf-8")

    # 7. Find most similar pairs

    # 7.1 Most similar pair overall (can include near-duplicates)
    flat_index = np.argmax(similarity_matrix)
    i_any, j_any = divmod(flat_index, similarity_matrix.shape[1])
    best_any_score = similarity_matrix[i_any, j_any]

    # 7.2 Most similar NON-identical pair (ignore scores >= 0.999)
    sim_nondup = similarity_matrix.copy()
    sim_nondup[sim_nondup >= 0.999] = 0.0

    if np.all(sim_nondup == 0.0):
        # fallback if everything is < 0.999 or there are no duplicates
        i_nd, j_nd = i_any, j_any
        best_nd_score = best_any_score
    else:
        flat_index_nd = np.argmax(sim_nondup)
        i_nd, j_nd = divmod(flat_index_nd, sim_nondup.shape[1])
        best_nd_score = sim_nondup[i_nd, j_nd]

    # Extract product info
    def product_info(idx):
        return {
            "index": int(idx),
            "title": df.loc[idx, "Title"],
            "sub_category": df.loc[idx, "Sub Category"],
        }

    prod_any_1 = product_info(i_any)
    prod_any_2 = product_info(j_any)

    prod_nd_1 = product_info(i_nd)
    prod_nd_2 = product_info(j_nd)

    print("\n=== Most similar pair (including possible duplicates) ===")
    print(f"Product A (index {prod_any_1['index']}): {prod_any_1['title']}")
    print(f"   Sub-category: {prod_any_1['sub_category']}")
    print(f"Product B (index {prod_any_2['index']}): {prod_any_2['title']}")
    print(f"   Sub-category: {prod_any_2['sub_category']}")
    print(f"Cosine similarity: {best_any_score:.4f}")

    print("\n=== Most similar NON-identical pair (similarity < 0.999) ===")
    print(f"Product A (index {prod_nd_1['index']}): {prod_nd_1['title']}")
    print(f"   Sub-category: {prod_nd_1['sub_category']}")
    print(f"Product B (index {prod_nd_2['index']}): {prod_nd_2['title']}")
    print(f"   Sub-category: {prod_nd_2['sub_category']}")
    print(f"Cosine similarity: {best_nd_score:.4f}")

    print("\nDone. You can now check similarity_matrix.csv and use these results in README.txt.")


if __name__ == "__main__":
    main()
