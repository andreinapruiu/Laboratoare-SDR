# Lab 1 – Movie Dataset and Recombee Integration

## Overview
This lab demonstrates how to use the **Recombee API** to register item properties and upload dataset items.  
The chosen dataset contains movie information, where each movie is treated as a “product” with multiple attributes.  
The goal is to define item properties, send their types to Recombee, and upload up to 1000 items.

---

## Dataset Information
- **File:** `movies-QueryResult.csv`  
- **Source:** IMDb movie database  
- **Entries:** 1000 movies (limited to the required maximum of 1000)  
- **Attributes:** 22 columns with various properties such as title, genre, year, duration, country, language, director, etc.  
- **Purpose:** Each movie acts as a dataset item with several attributes of different data types (string, integer, float).

---

## Properties Sent to Recombee
The script defines and uploads the following movie attributes to the Recombee database:

| Property | Type | Description |
|-----------|------|-------------|
| `title` | string | Movie title |
| `year` | int | Year of release |
| `genre` | string | Movie genre |
| `duration` | int | Movie duration in minutes |
| `avg_vote` | double | Average rating |
| `country` | string | Country of production |
| `language` | string | Primary language |
| `director` | string | Director of the movie |
| `votes` | int | Number of votes |

All properties are created using the **AddItemProperty** API call and filled using **SetItemValues** with `cascadeCreate=True`.

---

## Files
- `lab1.py` – Main Python script (analysis + Recombee API implementation)  
- `movies-QueryResult.csv` – Dataset of 1000 movies  
- `requirements.txt` – Python dependencies  
- `env_example.txt` – Example `.env` file template  
- `README.md` – This documentation file  

---

## Installation and Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
````

### 2. Create a `.env` file

```
RECOMBEE_DATABASE_ID=your_database_id
RECOMBEE_SECRET_TOKEN=your_private_token
RECOMBEE_BATCH_SIZE=100
CSV_PATH=movies-QueryResult.csv
```
---

## Running the Script

```bash
python lab1.py
```

When executed, the script will:

1. Load and analyze the movie dataset
2. Display dataset statistics and attribute types
3. Show key movie attributes with examples
4. Generate a summary report
5. Ask what API action to take:

   * **Option 1:** Send properties and items to Recombee
   * **Option 2:** Send a demo request to httpbin.org
   * **Option 3:** Skip API calls


