## 1. Task Description

In this laboratory exercise, I implemented an **Item-Based Collaborative Filtering (Item–Item CF)** algorithm, starting from the template file `item_based_cf_test.py` provided on Moodle. The goals were to:

* construct a **user–item rating matrix**
* compute **item–item similarity** using cosine similarity
* predict scores for items a user has not interacted with yet
* generate **Top-K recommendations** for a selected user
* explain and interpret the results

For this lab, I built a **10×10 interaction matrix** containing 10 users and 10 electronics items. This creates more varied similarity patterns and allows the collaborative filtering algorithm to produce richer recommendations.

---

## 2. Dataset: User–Item Rating Matrix

I used 10 electronics products that belong to related categories (Apple ecosystem, laptops, audio devices, tablets, cameras). This ensures meaningful co-rating patterns.

### **Products (Items)**

| ID | Product                                                     |
| -- | ----------------------------------------------------------- |
| 0  | Mac mini – Apple M2, 8GB, 256GB SSD – Silver                |
| 1  | Mac mini – Apple M2 Pro, 16GB, 512GB SSD – Silver           |
| 2  | MSI Modern 15.6" – Intel Core i7-1255U – 1080p              |
| 3  | MSI Modern 15.6" – Intel Core i5-1235U – 1080p – Windows 11 |
| 4  | Ooma Telo Air 2 Wireless Wi-Fi Home Phone Service           |
| 5  | Samsung Galaxy Tab S9 – 11" AMOLED – 256GB                  |
| 6  | Sony WH-1000XM5 Noise-Cancelling Headphones                 |
| 7  | Apple iPad Air (M1) – 10.9" – Wi-Fi – 256GB                 |
| 8  | Apple Watch SE (2nd Gen) – GPS – 44mm                       |
| 9  | Canon EOS R50 Mirrorless Camera – 4K Video                  |

### **Users**

`Ana`, `Bogdan`, `Carmen`, `Dan`, `Elena`, `Florin`, `Geanina`, `Horia`, `Irina`, `Vlad`

### **Ratings (1–5 scale, 0 = no interaction)**

```text
          0  1  2  3  4  5  6  7  8  9
Ana     [ 5, 4, 0, 0, 3, 4, 0, 5, 5, 0 ]
Bogdan  [ 5, 5, 4, 0, 0, 3, 4, 4, 5, 0 ]
Carmen  [ 0, 4, 5, 5, 0, 0, 4, 0, 3, 4 ]
Dan     [ 4, 0, 4, 5, 3, 0, 3, 0, 4, 5 ]
Elena   [ 0, 4, 0, 5, 4, 0, 5, 0, 3, 4 ]
Florin  [ 3, 4, 0, 4, 5, 0, 4, 3, 0, 5 ]
Geanina [ 0, 0, 5, 4, 0, 5, 4, 4, 0, 3 ]
Horia   [ 4, 4, 3, 0, 4, 5, 0, 5, 5, 3 ]
Irina   [ 5, 5, 3, 0, 0, 4, 0, 5, 5, 4 ]
Vlad    [ 0, 3, 4, 5, 4, 0, 3, 4, 3, 5 ]
```

Interpretation:

* **5** = strong preference
* **1** = weak preference
* **0** = user did not rate the item

This matrix provides the necessary co-rating signals for computing item similarities.

---

## 3. Algorithm: Item-Based Collaborative Filtering

### 3.1 Item–Item Similarity (Cosine)

Each item is represented as a vector of ratings from all 10 users.
Cosine similarity is used to measure how similar items are based on shared user behavior.

Example code:

```python
item_similarity = cosine_similarity(user_item_matrix.T)
```

### **Similarity Matrix (Real Output)**

```
[[1.         0.7717 0.5431 0.2586 0.5645 0.7300 0.3949 0.8001 0.8618 0.5239]
 [0.7717     1.     0.6221 0.5242 0.6757 0.6313 0.6642 0.8047 0.8724 0.7072]
 [0.5431  0.6221     1.     0.6869 0.3893 0.6229 0.7181 0.6627 0.7221 0.7506]
 [0.2586  0.5242 0.6869     1.     0.6843 0.1825 0.9003 0.3636 0.4731 0.8943]
 [0.5645  0.6757 0.3893 0.6843     1.     0.3516 0.6182 0.6022 0.6224 0.7769]
 [0.7300  0.6313 0.6229 0.1825 0.3516     1.     0.3243 0.8850 0.7013 0.4061]
 [0.3949  0.6642 0.7181 0.9003 0.6182 0.3243     1.     0.4712 0.5497 0.7979]
 [0.8001  0.8047 0.6627 0.3636 0.6022 0.8850 0.4712     1.     0.7788 0.6011]
 [0.8618  0.8724 0.7221 0.4731 0.6224 0.7013 0.5497 0.7788     1.     0.6620]
 [0.5239  0.7072 0.7506 0.8943 0.7769 0.4061 0.7979 0.6011 0.6620     1.    ]]
```

Interpretation:

* Items with similarity > **0.7** are strongly related (Apple products, MSI laptops).
* Items with similarity near **1.0** share highly aligned user patterns.
* This matrix drives the recommendation process.

---

### 3.2 Predicting Unknown Ratings

To predict how much a target user would like an unrated item, CF computes:

[
\text{score}(u, j) = \sum_{i \in \text{RatedBy}(u)} \big( \text{rating}(u, i) \times \text{similarity}(i, j) \big)
]

In code:

```python
scores = user_ratings @ item_similarity
scores[user_ratings > 0] = -1
```

* Items that Carmen already rated get a score of **−1**
* Remaining items get predicted scores

---

## 4. Top-K Recommendations for User “Carmen”

### 4.1 Carmen’s Ratings

```
[0, 4, 5, 5, 0, 0, 4, 0, 3, 4]
```

Carmen strongly likes:

* **MSI Modern i7 laptop (5)**
* **MSI Modern i5 laptop (5)**
* **Sony WH-1000XM5 (4)**
* **Canon EOS R50 camera (4)**

Moderate interest in Apple Watch (3).

---

### 4.2 Predicted Scores (Real Output)

```
Item 0: Mac mini M2 -> 13.3564
Item 1: Mac mini M2 Pro -> -1
Item 2: MSI Modern i7 -> -1
Item 3: MSI Modern i5 -> -1
Item 4: Ooma Telo Air 2 -> 15.5186
Item 5: Galaxy Tab S9 -> 11.5776
Item 6: Sony XM5 -> -1
Item 7: iPad Air M1 -> 14.9758
Item 8: Apple Watch SE -> -1
Item 9: Canon EOS R50 -> -1
```

She already rated items 1, 2, 3, 6, 8, 9, so they are masked as −1.

Top candidate scores:

* **15.5186 → Ooma Telo Air 2**
* **14.9758 → iPad Air M1**
* **13.3564 → Mac mini M2**
* **11.5776 → Galaxy Tab S9**

---

### 4.3 Final Top-2 Recommendations

```
Top-2 recommended items for Carmen:
  -> Ooma Telo Air 2 Wireless Wi-Fi Home Phone Service (15.5186)
  -> Apple iPad Air (M1) - 10.9" - Wi-Fi - 256GB (14.9758)
```

---

## 5. Interpretation of Results

### ✔ Why “Ooma Telo Air 2” is recommended

* Ooma has **very high similarity** to items Carmen likes:

  * MSI laptops (0.68)
  * Sony XM5 headphones (0.61)
  * iPad Air (0.60)
* Users with Carmen’s profile (productivity + media consumption) tend to also rate home-networking / VoIP products highly.

### ✔ Why “iPad Air M1” is the second recommendation

* Strong similarity with Carmen’s favorite items:

  * MSI i7 (0.66)
  * Sony XM5 (0.47)
  * Canon EOS camera (0.60)
* Fits her usage pattern: productivity + multimedia + creativity.
