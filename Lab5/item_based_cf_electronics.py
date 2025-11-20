import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

item_names = [
    "Mac mini - Apple M2, 8GB, 256GB SSD - Silver",                # 0
    "Mac mini - Apple M2 Pro, 16GB, 512GB SSD - Silver",          # 1
    "MSI Modern 15.6\" - Intel Core i7-1255U - 1080p",            # 2
    "MSI Modern 15.6\" - Intel Core i5-1235U - 1080p - Windows 11",  # 3
    "Ooma Telo Air 2 Wireless Wi-Fi Home Phone Service",          # 4
    "Samsung Galaxy Tab S9 - 11\" AMOLED - 256GB",                # 5
    "Sony WH-1000XM5 Wireless Noise-Cancelling Headphones",       # 6
    "Apple iPad Air (M1) - 10.9\" - Wi-Fi - 256GB",               # 7
    "Apple Watch SE (2nd Gen) - GPS - 44mm",                      # 8
    "Canon EOS R50 Mirrorless Camera - 4K Video"                  # 9
]

user_names = [
    "Ana", "Bogdan", "Carmen", "Dan", "Elena",
    "Florin", "Geanina", "Horia", "Irina", "Vlad"
]

user_item_matrix = np.array([
    [5, 4, 0, 0, 3, 4, 0, 5, 5, 0],   # Ana
    [5, 5, 4, 0, 0, 3, 4, 4, 5, 0],   # Bogdan
    [0, 4, 5, 5, 0, 0, 4, 0, 3, 4],   # Carmen
    [4, 0, 4, 5, 3, 0, 3, 0, 4, 5],   # Dan
    [0, 4, 0, 5, 4, 0, 5, 0, 3, 4],   # Elena
    [3, 4, 0, 4, 5, 0, 4, 3, 0, 5],   # Florin
    [0, 0, 5, 4, 0, 5, 4, 4, 0, 3],   # Geanina
    [4, 4, 3, 0, 4, 5, 0, 5, 5, 3],   # Horia
    [5, 5, 3, 0, 0, 4, 0, 5, 5, 4],   # Irina
    [0, 3, 4, 5, 4, 0, 3, 4, 3, 5],   # Vlad
], dtype=float)

item_similarity = cosine_similarity(user_item_matrix.T)

print("Item-Item Similarity Matrix (cosine):")
print(item_similarity)
print()


def recommend_items(user_id, user_item_matrix, item_similarity, top_k=3):
    user_ratings = user_item_matrix[user_id]
    scores = user_ratings @ item_similarity

    scores = scores.copy()
    scores[user_ratings > 0] = -1  # mask rated items

    recommended_indices = np.argsort(scores)[::-1][:top_k]
    return recommended_indices, scores


target_user_id = 0
top_k = 3

recommended_items, scores = recommend_items(
    user_id=target_user_id,
    user_item_matrix=user_item_matrix,
    item_similarity=item_similarity,
    top_k=top_k
)

print(f"Target user: {user_names[target_user_id]}")
print("User ratings:", user_item_matrix[target_user_id])
print("\nPredicted scores:")
for idx, score in enumerate(scores):
    print(f"  Item {idx}: {item_names[idx]} -> score = {score:.4f}")

print(f"\nTop-{top_k} recommendations for {user_names[target_user_id]}:")
for idx in recommended_items:
    print(f"  -> {item_names[idx]} (score = {scores[idx]:.4f})")
