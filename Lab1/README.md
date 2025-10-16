# Lab 1 - Movie Dataset Analysis and API Implementation

## Overview
This project implements a Python script that analyzes a movie dataset and demonstrates API functionality for sending product attributes and their types.

## Dataset Information
- **File**: `movies-QueryResult.csv`
- **Size**: 1000 movies (meets the requirement of 100+ products, limited to max 1000)
- **Source**: IMDB movie database
- **Attributes**: 22 columns with various movie properties

## Requirements Met
✅ **Dataset Requirements**:
- Has 1000+ products (1000 movies)
- Each movie has multiple attributes/properties
- Minimum 3+ properties per movie
- Different data types (string, integer, float)

✅ **API Functionality**:
- Sends product attribute names and their types
- Demonstrates proper API communication
- Includes error handling and response processing

## Key Product Attributes
The script analyzes and sends the following movie attributes with their types:

1. **title** (string) - Movie title
2. **year** (integer) - Year of release  
3. **genre** (string) - Movie genre(s)
4. **duration** (integer) - Movie duration in minutes
5. **avg_vote** (float) - Average rating/vote
6. **budget** (string) - Movie budget
7. **country** (string) - Country of production
8. **language** (string) - Primary language
9. **director** (string) - Movie director
10. **votes** (integer) - Number of votes

## Files
- `lab1.py` - Main Python script
- `movies-QueryResult.csv` - Movie dataset
- `requirements.txt` - Python dependencies
- `get_recombee_credentials.py` - Helper script for finding Recombee credentials
- `setup_env.py` - Interactive script to create .env file
- `env_example.txt` - Example .env file template
- `README.md` - This documentation file

## Installation and Usage

### Prerequisites
- Python 3.7+
- pip package manager

### Installation
```bash
# Install required dependencies
pip3 install -r requirements.txt
```

### Running the Script
```bash
python3 lab1.py
```

The script will:
1. Load and analyze the movie dataset
2. Display comprehensive statistics
3. Show product attributes with types and examples
4. Generate a summary report
5. Offer API options:
   - Send to Recombee (to add more properties to your items)
   - Send to demo API (httpbin.org/post)
   - Skip API calls

### Recombee Integration
To add more properties to your Recombee items:

#### Option 1: Using .env file (Recommended)
1. **Setup your credentials**:
   ```bash
   python3 setup_env.py
   ```
   This will create a `.env` file with your Recombee credentials.

2. **Run the main script**:
   ```bash
   python3 lab1.py
   ```

3. **Choose option 1** when prompted for API options

#### Option 2: Manual setup
1. **Create .env file manually**:
   ```bash
   cp env_example.txt .env
   # Then edit .env with your actual values
   ```

2. **Get your credentials**:
   ```bash
   python3 get_recombee_credentials.py
   ```

3. **Run the main script**:
   ```bash
   python3 lab1.py
   ```

4. **Choose option 1** and enter credentials manually if .env file is not found

#### Required Credentials
You'll need these from your Recombee admin panel (Integration > Catalog Feed):
- **API URL** (e.g., `https://your-database.recombee.com`)
- **Database ID**
- **Secret Token**

The script will then add these properties to your 1000 movie items:
- `year` (integer)
- `genre` (string) 
- `duration` (integer)
- `avg_vote` (float)
- `country` (string)
- `language` (string)
- `director` (string)
- `votes` (integer)

### API Demonstration
The script also offers a demo option using `httpbin.org/post` for testing purposes.

## Features

### Dataset Analysis
- Loads CSV data using pandas
- Analyzes data types and statistics
- Shows sample data and distributions
- Calculates data quality metrics

### Product Attributes
- Extracts key movie attributes
- Categorizes by data type (string, integer, float)
- Provides examples and non-null counts
- Formats data for API transmission

### API Communication
- Sends structured JSON payload
- Includes dataset metadata
- Handles HTTP responses and errors
- Provides detailed logging

## Sample Output
```
🎬 MOVIE DATASET ANALYZER - LAB 1
============================================================
✓ Dataset loaded successfully: 1000 movies
✓ Dataset columns: ['imdb_title_id', 'title', 'original_title', ...]

Total movies: 1000
Total attributes: 22

✓ Dataset meets requirements:
  • Has 1000+ products: ✓ (1000 movies)
  • Has 3+ attributes: ✓ (10 attributes)
  • Attributes have different types: ✓ (string, integer, float)
```

## Technical Details
- **Language**: Python 3
- **Libraries**: pandas, requests, json
- **Data Format**: CSV
- **API Format**: JSON
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: Detailed console output

## Future Enhancements
This script serves as the foundation for future laboratory work and can be extended with:
- Additional data analysis features
- More sophisticated API endpoints
- Data visualization capabilities
- Machine learning integration
- Real-time data processing
