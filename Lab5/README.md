# Item-Based Collaborative Filtering – Electronics Recommendations

## 1. Task Description

In this laboratory exercise, I implemented an **Item-Based Collaborative Filtering (Item–Item CF)** algorithm, starting from the template file `item_based_cf_test.py` provided on Moodle. The goals were to:

* construct a **user–item rating matrix**
* compute **item–item similarity** using cosine similarity
* predict scores for items a user has not interacted with yet
* generate **Top-K recommendations** for a selected user
* explain and interpret the results

The entire implementation has been adapted to a small but realistic dataset of **electronics products**, ensuring consistency with previous labs.

---

## 2. Dataset: User–Item Rating Matrix

I used 5 real users and 5 real electronics products extracted from the earlier cosine-similarity dataset:

### **Products (Items)**

| ID | Product                                                     |
| -- | ----------------------------------------------------------- |
| 0  | Mac mini – Apple M2, 8GB, 256GB SSD – Silver                |
| 1  | Mac mini – Apple M2 Pro, 16GB, 512GB SSD – Silver           |
| 2  | MSI Modern 15.6" – Intel Core i7-1255U – 1080p              |
| 3  | MSI Modern 15.6" – Intel Core i5-1235U – 1080p – Windows 11 |
| 4  | Ooma Telo Air 2 Wireless Wi-Fi Home Phone Service           |

### **Users**

`Ana`, `Bogdan`, `Carmen`, `Dan`, `Elena`

### **Ratings (1–5 scale, 0 = no interaction)**

```text
          Item 0   Item 1   Item 2   Item 3   Item 4
Ana       [  5       4        0        0        3  ]
Bogdan    [  5       5        4        0        0  ]
Carmen    [  0       4        5        5        0  ]
Dan       [  4       0        4        5        3  ]
Elena     [  0       4        0        5        4  ]
```

Interpretation:

* **5** → strong preference / frequent use
* **1** → weak preference
* **0** → no interaction (missing data)

The matrix is small enough to interpret manually but structured enough for collaborative filtering.

---

## 3. Algorithm: Item-Based Collaborative Filtering

### 3.1 Item–Item Similarity (Cosine)

Each item is represented as a vector of ratings given by all users.

Similarity is computed as:

```python
item_similarity = cosine_similarity(user_item_matrix.T)
```

The resulting similarity matrix was:

```
[[1.         0.64830462 0.58693919 0.28426762 0.56997045]
 [0.64830462 1.         0.62009915 0.5405899  0.56202695]
 [0.58693919 0.62009915 1.         0.6882472  0.27258651]
 [0.28426762 0.5405899  0.6882472  1.         0.69310328]
 [0.56997045 0.56202695 0.27258651 0.69310328 1.        ]]
```

This matrix indicates how similar each product is to every other product based on user co-ratings.

---

### 3.2 Predicting Unknown Ratings

For a user **u** and an unrated item **j**, the predicted score is:

```
score(u, j) = Σ_i rating(u, i) × similarity(i, j)
```

where **i** are the items user **u** has already rated.

In code:

```python
user_ratings = user_item_matrix[user_id]
scores = user_ratings @ item_similarity
scores[user_ratings > 0] = -1  # mask already rated items
```

This produces a score for each unrated item, allowing us to rank and recommend them.

---

## 4. Top-K Recommendations for User “Ana”

### 4.1 Ana’s ratings:

```
Ana: [5, 4, 0, 0, 3]
```

She strongly prefers:

* **Mac mini (M2)**
* **Mac mini (M2 Pro)**

And moderately likes:

* **Ooma Telo Air 2**

She has *no ratings yet* for the two MSI laptops.

---

### 4.2 Predicted Scores (Real Output)

```
Predicted scores for all items (after CF):
  Item 0: Mac mini – Apple M2 -> score = -1.0000
  Item 1: Mac mini – Apple M2 Pro -> score = -1.0000
  Item 2: MSI Modern 15.6" (i7) -> score = 6.2329
  Item 3: MSI Modern 15.6" (i5) -> score = 5.6630
  Item 4: Ooma Telo Air 2 -> score = -1.0000
```

Items with existing ratings receive `-1` to prevent recommending them again.

---

### 4.3 Top-2 Recommendations

```
Top-2 recommended items for Ana:
  -> MSI Modern 15.6" – Intel Core i7-1255U – 1080p (score = 6.2329)
  -> MSI Modern 15.6" – Intel Core i5-1235U – 1080p – Windows 11 (score = 5.6630)
```

---

## 5. Interpretation of Results (Extended Explanation)

### ✔ Why MSI laptops are recommended for Ana

1. **Users with similar taste patterns**
   Users who love the same Apple products as Ana (Bogdan, Carmen, Dan) also rated MSI laptops very highly.

2. **High item–item similarity**
   In the similarity matrix:

   * MSI laptops have similarities around **0.6–0.68** with both Mac minis
   * They also show strong mutual similarity (0.688)

3. **Collaborative filtering effect**
   The algorithm essentially says:

   > “Users who like Mac mini (M2/M2 Pro) also tend to like MSI Modern laptops.”

4. **Weighted scoring ranks the MSI i7 first**
   Because:

   * It is the closest match to the items Ana rated highly
   * It has strong endorsement across multiple users
   * It shares similar “premium productivity device” characteristics

5. **Prediction values are realistic**
   A score of **6.23** is high, but interpretable — it comes from weighted contributions of her strong ratings (5 and 4) multiplied by ~0.6 similarity values.

---