import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------------------------------
# Item-Based Collaborative Filtering - Electronics
# ----------------------------------------------------
# Rows = Users, Columns = Items
# Ratings on a 1-5 scale (0 = no interaction)
#
# Users:
#   0: Ana
#   1: Bogdan
#   2: Carmen
#   3: Dan
#   4: Elena
#
# Items (Electronics products):
#   0: Mac mini - Apple M2, 8GB, 256GB SSD - Silver
#   1: Mac mini - Apple M2 Pro, 16GB, 512GB SSD - Silver
#   2: MSI Modern 15.6" - Intel Core i7-1255U - 1080p
#   3: MSI Modern 15.6" - Intel Core i5-1235U - 1080p - Windows 11
#   4: Ooma Telo Air 2 Wireless Wi-Fi Home Phone Service
# ----------------------------------------------------

item_names = [
    "Mac mini - Apple M2, 8GB, 256GB SSD - Silver",                 # item 0
    "Mac mini - Apple M2 Pro, 16GB, 512GB SSD - Silver",           # item 1
    "MSI Modern 15.6\" - Intel Core i7-1255U - 1080p",             # item 2
    "MSI Modern 15.6\" - Intel Core i5-1235U - 1080p - Windows 11",  # item 3
    "Ooma Telo Air 2 Wireless Wi-Fi Home Phone Service",           # item 4
]

user_names = ["Ana", "Bogdan", "Carmen", "Dan", "Elena"]

# Ratings matrix: rows = users, cols = items
# 0 means no rating / no interaction yet
user_item_matrix = np.array([
    [5, 4, 0, 0, 3],  # Ana: loves Mac mini, also uses Ooma
    [5, 5, 4, 0, 0],  # Bogdan: strong Apple fan, also likes MSI i7 laptop
    [0, 4, 5, 5, 0],  # Carmen: mostly on MSI laptops and Mac mini Pro
    [4, 0, 4, 5, 3],  # Dan: MSI laptops + Mac mini + Ooma
    [0, 4, 0, 5, 4],  # Elena: Mac mini Pro + MSI i5 + Ooma
], dtype=float)

# ----------------------------------------------------
# 1. Compute item-item similarity (cosine)
# ----------------------------------------------------
item_similarity = cosine_similarity(user_item_matrix.T)

print("Item-Item Similarity Matrix (cosine):")
print(item_similarity)
print()


# ----------------------------------------------------
# 2. Recommend items for a user using Item-Based CF
# ----------------------------------------------------
def recommend_items(user_id, user_item_matrix, item_similarity, top_k=2):
    """
    Item-based Collaborative Filtering recommendation.

    Predicted score for an item j is:
        score_j = sum_over_i( rating_user_i * sim(i, j) )
    where i are items already rated by the user.

    We then:
    - Set scores for already-rated items to -1 (to avoid recommending them)
    - Return the indices of the top_k items with highest predicted score
    """
    user_ratings = user_item_matrix[user_id]        # vector of size [num_items]
    scores = user_ratings @ item_similarity         # weighted sum over similar items

    # Exclude already rated items from recommendations
    scores = scores.copy()
    scores[user_ratings > 0] = -1

    # Get indices of items sorted by score (descending)
    recommended_indices = np.argsort(scores)[::-1][:top_k]
    return recommended_indices, scores

# ----------------------------------------------------
# 3. Example: Top-K recommendations for Ana (user 0)
# ----------------------------------------------------


target_user_id = 0
top_k = 2

recommended_items, scores = recommend_items(
    user_id=target_user_id,
    user_item_matrix=user_item_matrix,
    item_similarity=item_similarity,
    top_k=top_k
)

print(f"Target user: {target_user_id} - {user_names[target_user_id]}")
print("User ratings:", user_item_matrix[target_user_id])
print("\nPredicted scores for all items (after CF):")
for idx, score in enumerate(scores):
    print(f"  Item {idx}: {item_names[idx]} -> score = {score:.4f}")

print(f"\nTop-{top_k} recommended items for {user_names[target_user_id]}:")
for idx in recommended_items:
    print(f"  -> Item {idx}: {item_names[idx]} (score = {scores[idx]:.4f})")
