# 📘 Cosine Similarity – Electronics Dataset

## 1. 📊 Dataset Description

For this project, I used a dataset called **`ElectronicsData.csv`**, which contains **643 electronics products**.
Each row represents a product, with the following relevant columns:

* **Sub Category** – product category (e.g., *Batteries*, *Smart Watches*, *Cameras*)
* **Price** – numeric price
* **Discount** – discount text
* **Rating** – product rating (if available)
* **Title** – product name/title
* **Currency** – currency symbol
* **Feature** – textual description/feature list

To perform text similarity, I used the **Title + Feature** fields concatenated into a single text document per product.

---

## 2. 🧹 Text Preprocessing

Before computing similarity, I applied **full preprocessing** to clean and normalize the text.
The following steps were performed:

### 🔤 1. Lowercasing

All text was converted to lowercase to avoid treating `"Battery"` and `"battery"` as different words.

### 🧼 2. Removing HTML + non-alphabetic characters

Although the dataset is clean, the script removes any possible:

* HTML tags
* punctuation
* digits
* special characters

This helps reduce noisy tokens.

### ✂️ 3. Tokenization

Each cleaned text was split into individual tokens.

### 🛑 4. Stopword Removal

Using **NLTK stopwords**, I removed common English words (e.g., *the*, *and*, *for*, *with*).
These words do not contribute meaningful information for text comparison.

### 🧩 5. Lemmatization

Tokens were lemmatized using `WordNetLemmatizer`, reducing words to their base form:

* *batteries* → *battery*
* *running* → *run*

This ensures that TF–IDF treats different forms of the same word consistently.

### 🧾 Output of preprocessing

Each product ends up with a clean, lemmatized description containing only meaningful content words.

---

## 3. 📐 TF–IDF Vectorization

To represent each product as a numerical vector, I used **TF–IDF** (`TfidfVectorizer` from scikit-learn).

### Why TF–IDF?

* **TF** → word frequency in that product description
* **IDF** → downweights words that appear in many products
* Produces a sparse, high-dimensional vector for each item

The resulting TF–IDF matrix had shape:

```
(643, N)
```

Where **N** is the size of the vocabulary after preprocessing.

---

## 4. 🔄 Cosine Similarity Matrix

Then, I computed the full **pairwise cosine similarity** matrix:

```
cosine_similarity(tfidf_matrix)
```

Cosine similarity ranges from:

* **1.0** → identical text
* **0.0** → no shared terms

I replaced the diagonal with 0 to avoid comparing each item with itself.

The final matrix (**643 × 643**) was saved as:

📄 **`similarity_matrix.csv`**

Rows and columns are indexed by the product titles.

---

## 5. 🔍 Most Similar Product Pairs

Using the similarity matrix, I extracted:

### ✔ 1. The *most similar pair overall*

(Can include near-duplicates or variants)

### ✔ 2. The *most similar non-identical pair*

(Filtered by excluding values ≥ 0.999)

The script prints both pairs, including:

* product titles
* sub-categories
* similarity score

---

## 6. 🧠 Examples of Similar Product Pairs (Not Only the Most Similar Ones)

### 🔹 **Example Pair #1: Smartwatches with Similar Features**

* **Product A:**
  *Apple Watch SE (2nd Generation) (GPS) Sport Loop*

* **Product B:**
  *Apple Watch SE (2nd Generation) (GPS + Cellular) Sport Loop*

**Why they are similar:**

* Both descriptions highlight **health tracking**, **fitness activity**, **sleep monitoring**, and **integration with iPhone**.
* The only feature difference is the presence of **cellular connectivity** in the second model.
* After preprocessing (lemmatization + stopwords removal), both items share a nearly identical set of informative keywords such as:
  *apple, watch, generation, sport, loop, track, workout, active, health, goal, monitor*.

This leads to a cosine similarity score close to **0.99**, which correctly reflects that they are two variants of the same product line.

---

### 🔹 **Example Pair #2: Home Security Cameras with Overlapping Functionality**

* **Product A:**
  *Ring Indoor Cam (2nd Gen) Plug-In, Compact Indoor Security Camera*

* **Product B:**
  *Blink Mini – Compact Indoor Plug-In HD Security Camera*

**Why they are similar:**

* Both products are **indoor plug-in security cameras**, designed for home monitoring.
* Their feature descriptions emphasize similar capabilities:

  * *HD video*
  * *motion detection*
  * *smart home compatibility*
  * *indoor surveillance*
* After cleaning the text, both descriptions heavily focus on terms like:
  *indoor, camera, plug, security, motion, detection, video, home, compact*
* They belong to the same functional category even though they are different brands (Ring vs. Blink).

Their cosine similarity score is high because the TF–IDF representation captures that they describe almost identical **use cases** and **attributes**.

---

## 7. 📁 Output Files

The project produces:

### **1.** `similarity_matrix.csv`

A full cosine similarity matrix between all product descriptions.

### **2.** Console output:

* Most similar pair (including duplicates)
* Most similar non-identical pair
* Their similarity scores
* Product titles and sub-categories

---

## 8. 🧩 Technologies Used

* **Python 3**
* **Pandas** – dataset loading
* **NLTK** – tokenization, stopwords, lemmatization
* **scikit-learn** – TF–IDF, cosine similarity
* **NumPy** – matrix operations