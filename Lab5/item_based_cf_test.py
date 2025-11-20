import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# Example User–Item Matrix
# Rows = Users, Columns = Items
# Ratings: 1 = picked, 0 = not picked (can also use real ratings)
# ---------------------------
user_item_matrix = np.array([
    [1, 1, 0, 0],  # User 0
    [1, 0, 1, 0],  # User 1
    [0, 1, 1, 1],  # User 2
])

# Compute item–item similarity (cosine)
item_similarity = cosine_similarity(user_item_matrix.T)

print("Item–Item Similarity Matrix:")
print(item_similarity)

# ---------------------------
# Recommend items for a user
# ---------------------------
def recommend_items(user_id, user_item_matrix, item_similarity, top_k=2):
    user_ratings = user_item_matrix[user_id]
    
    # Predicted scores are weighted sum of similar items user already interacted with
    scores = user_ratings @ item_similarity
    
    # Exclude items already chosen
    scores[user_ratings == 1] = -1
    
    recommended_items = np.argsort(scores)[::-1][:top_k]
    return recommended_items, scores

# Test recommendation for User 0
recommended_items, scores = recommend_items(
    user_id=0,
    user_item_matrix=user_item_matrix,
    item_similarity=item_similarity,
    top_k=2
)

print("\nPredicted Scores:", scores)
print("Recommended Items:", recommended_items)