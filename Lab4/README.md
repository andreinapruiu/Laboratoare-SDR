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

Absolutely — **now that we have the REAL output from your script**, we MUST update Point 6 of your README to reflect the actual pairs your model found.

This makes your README accurate, verifiable, and perfectly aligned with the assignment requirements.

Below is **the corrected and improved Section 6**, rewritten using your **exact console output**.

You can paste this directly into your README.md.

---

# ✅ **Updated README – Section 6 (FINAL VERSION)**

*(Based on YOUR real similarity results)*

## 6. 🧠 Examples of Similar Product Pairs (Using Real Output)

Below are two product pairs identified by the cosine similarity algorithm in the electronics dataset. These examples come directly from the computed similarity matrix and illustrate meaningful relationships detected by TF–IDF and cosine similarity.

---

### 🔹 **Example Pair #1: Two MSI Modern Laptops (i5 vs i7 Variants)**

* **Product A (index 295):**
  *MSI Modern 15.6" Laptop – 12th Gen Intel Core i7-1255U – 1080p*

* **Product B (index 316):**
  *MSI Modern 15.6" Laptop – 12th Gen Intel Core i5-1235U – 1080p – Windows 11*

**Cosine Similarity: 0.9907**

**Why they are similar:**
These two products are **closely related configurations** of the same MSI Modern 15.6" laptop line. Their titles and features share the same core terminology:

* *msi*, *modern*, *laptop*, *15.6*, *12th*, *gen*, *intel*, *core*, *u*, *1080p*
* Differences are limited to CPU model (i7 vs i5) and an OS mention (Windows 11)

The strong shared vocabulary after preprocessing results in a similarity close to **0.99**.

---

### 🔹 **Example Pair #2: Two Variants of Apple Mac mini**

* **Product A (index 17):**
  *Mac mini – Apple M2 Chip 8-core CPU, 10-core GPU – 8GB Memory – 256GB SSD – Silver*

* **Product B (index 22):**
  *Mac mini – Apple M2 Pro Chip 10-core CPU, 16-core GPU – 16GB Memory – 512GB SSD – Silver*

**Cosine Similarity: 0.9958**

**Why they are similar:**
These two products are **different configurations** of the same model line (Apple Mac mini).
Their titles and feature descriptions share the same core terminology:

* *Mac mini*, *Apple*, *M2*, *CPU*, *GPU*, *Memory*, *SSD*, *Silver*

The only differences relate to hardware specifications (M2 vs M2 Pro, RAM, storage).
Since most words overlap and variations are minor, their TF–IDF vectors are extremely close, resulting in a cosine similarity of **0.9958**.

This shows the algorithm correctly identifies products that differ only by upgraded components.

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