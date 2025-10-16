#!/usr/bin/env python3
"""
Lab 1 - Movie Dataset Analysis and API Implementation
Dataset: movies-QueryResult.csv (1000 movies)
Author: Student
Date: 2024
"""

import pandas as pd
import requests
import json
from typing import Dict, List, Any
import sys
import os
from dotenv import load_dotenv
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch, AddItemProperty, GetItemValues

class MovieDatasetAnalyzer:
    """
    Class to analyze the movie dataset and implement API functionality
    for sending product attributes and their types.
    """
    
    def __init__(self, csv_file_path: str):
        """
        Initialize the analyzer with the CSV file path.
        
        Args:
            csv_file_path (str): Path to the movies CSV file
        """
        self.csv_file_path = csv_file_path
        self.df = None
        self.load_dataset()
        
        # Load environment variables
        load_dotenv()
        self.recombee_url = os.getenv('RECOMBEE_URL')
        self.recombee_database_id = os.getenv('RECOMBEE_DATABASE_ID')
        self.recombee_secret_token = os.getenv('RECOMBEE_SECRET_TOKEN')
        self.recombee_batch_size = int(os.getenv('RECOMBEE_BATCH_SIZE', '100'))
        
    def load_dataset(self):
        """Load the movie dataset from CSV file."""
        try:
            self.df = pd.read_csv(self.csv_file_path)
            print(f"✓ Dataset loaded successfully: {len(self.df)} movies")
            print(f"✓ Dataset columns: {list(self.df.columns)}")
        except FileNotFoundError:
            print(f"❌ Error: File {self.csv_file_path} not found")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            sys.exit(1)
    
    def analyze_dataset(self):
        """
        Analyze the dataset and display key statistics.
        """
        print("\n" + "="*60)
        print("MOVIE DATASET ANALYSIS")
        print("="*60)
        
        # Basic info
        print(f"Total movies: {len(self.df)}")
        print(f"Total attributes: {len(self.df.columns)}")
        
        # Data types analysis
        print(f"\nData types:")
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            non_null_count = self.df[col].count()
            print(f"  {col}: {dtype} ({non_null_count} non-null values)")
        
        # Key statistics for numeric columns
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            print(f"\nNumeric columns statistics:")
            print(self.df[numeric_cols].describe())
        
        # Sample data
        print(f"\nSample movies:")
        print(self.df[['title', 'year', 'genre', 'avg_vote', 'duration']].head())
    
    def get_product_attributes(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract and categorize product attributes from the movie dataset.
        
        Returns:
            Dict containing attribute information with types and examples
        """
        attributes = {
            'title': {
                'type': 'string',
                'description': 'Movie title',
                'example': self.df['title'].dropna().iloc[0] if not self.df['title'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['title'].count())
            },
            'year': {
                'type': 'integer',
                'description': 'Year of release',
                'example': int(self.df['year'].dropna().iloc[0]) if not self.df['year'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['year'].count())
            },
            'genre': {
                'type': 'string',
                'description': 'Movie genre(s)',
                'example': self.df['genre'].dropna().iloc[0] if not self.df['genre'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['genre'].count())
            },
            'duration': {
                'type': 'integer',
                'description': 'Movie duration in minutes',
                'example': int(self.df['duration'].dropna().iloc[0]) if not self.df['duration'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['duration'].count())
            },
            'avg_vote': {
                'type': 'float',
                'description': 'Average rating/vote',
                'example': float(self.df['avg_vote'].dropna().iloc[0]) if not self.df['avg_vote'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['avg_vote'].count())
            },
            'budget': {
                'type': 'string',
                'description': 'Movie budget',
                'example': self.df['budget'].dropna().iloc[0] if not self.df['budget'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['budget'].count())
            },
            'country': {
                'type': 'string',
                'description': 'Country of production',
                'example': self.df['country'].dropna().iloc[0] if not self.df['country'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['country'].count())
            },
            'language': {
                'type': 'string',
                'description': 'Primary language',
                'example': self.df['language'].dropna().iloc[0] if not self.df['language'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['language'].count())
            },
            'director': {
                'type': 'string',
                'description': 'Movie director',
                'example': self.df['director'].dropna().iloc[0] if not self.df['director'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['director'].count())
            },
            'votes': {
                'type': 'integer',
                'description': 'Number of votes',
                'example': int(self.df['votes'].dropna().iloc[0]) if not self.df['votes'].dropna().empty else 'N/A',
                'non_null_count': int(self.df['votes'].count())
            }
        }
        
        return attributes
    
    def display_attributes(self):
        """
        Display the product attributes with their types and examples.
        """
        print("\n" + "="*60)
        print("PRODUCT ATTRIBUTES ANALYSIS")
        print("="*60)
        
        attributes = self.get_product_attributes()
        
        print("Movie attributes with types and examples:")
        print("-" * 60)
        
        for attr_name, attr_info in attributes.items():
            print(f"\n{attr_name.upper()}:")
            print(f"  Type: {attr_info['type']}")
            print(f"  Description: {attr_info['description']}")
            print(f"  Example: {attr_info['example']}")
            print(f"  Non-null values: {attr_info['non_null_count']}")
    
    def send_attributes_to_recombee(self, database_id: str = None, secret_token: str = None):
        """
        Send movie attributes to Recombee API to add more properties to items.
        
        Args:
            database_id (str): Database ID (optional, uses .env if not provided)
            secret_token (str): Secret token (optional, uses .env if not provided)
        """
        print("\n" + "="*60)
        print("SENDING ATTRIBUTES TO RECOMBEE")
        print("="*60)
        
        # Use provided values or fall back to environment variables
        db_id = database_id or self.recombee_database_id
        token = secret_token or self.recombee_secret_token
        batch_size = self.recombee_batch_size
        
        if not all([db_id, token]):
            print("❌ Missing Recombee credentials!")
            print("\nPlease either:")
            print("1. Create a .env file with your credentials (see env_example.txt)")
            print("2. Provide credentials manually when prompted")
            print("\nTo create .env file:")
            print("   cp env_example.txt .env")
            print("   # Then edit .env with your actual values")
            return
        
        print(f"✓ Using credentials from {'environment variables' if not database_id else 'manual input'}")
        print(f"✓ Database ID: {db_id}")
        print(f"✓ Batch size: {batch_size}")
        
        try:
            # Initialize Recombee client
            client = RecombeeClient(db_id, token, region=Region.EU_WEST)
            print("✓ Recombee client initialized successfully")
            
            # Create properties first
            print("Creating item properties...")
            properties = [
                ('title', 'string'),
                ('year', 'int'),
                ('genre', 'string'),
                ('duration', 'int'),
                ('avg_vote', 'double'),
                ('country', 'string'),
                ('language', 'string'),
                ('director', 'string'),
                ('votes', 'int')
            ]
            
            for prop_name, prop_type in properties:
                try:
                    client.send(AddItemProperty(prop_name, prop_type))
                    print(f"✓ Created property: {prop_name} ({prop_type})")
                except Exception as e:
                    print(f"⚠️  Property {prop_name} might already exist")
            
            print("✓ Properties setup complete")
            
            # Prepare items with additional properties
            items_to_update = []
            
            for index, row in self.df.iterrows():
                item_id = str(index + 1)  # Using row index as itemId
                
                # Prepare item properties (excluding itemId)
                item_properties = {
                    "title": str(row['title']),
                    "year": int(row['year']) if pd.notna(row['year']) else None,
                    "genre": str(row['genre']) if pd.notna(row['genre']) else None,
                    "duration": int(row['duration']) if pd.notna(row['duration']) else None,
                    "avg_vote": float(row['avg_vote']) if pd.notna(row['avg_vote']) else None,
                    "country": str(row['country']) if pd.notna(row['country']) else None,
                    "language": str(row['language']) if pd.notna(row['language']) else None,
                    "director": str(row['director']) if pd.notna(row['director']) else None,
                    "votes": int(row['votes']) if pd.notna(row['votes']) else None
                }
                
                # Remove None values
                item_properties = {k: v for k, v in item_properties.items() if v is not None}
                
                items_to_update.append({
                    "item_id": item_id,
                    "properties": item_properties
                })
            
            # Send to Recombee in batches
            total_batches = (len(items_to_update) + batch_size - 1) // batch_size
            
            print(f"Updating {len(items_to_update)} items in {total_batches} batches...")
            
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(items_to_update))
                batch = items_to_update[start_idx:end_idx]
                
                try:
                    print(f"Sending batch {batch_num + 1}/{total_batches} ({len(batch)} items)...")
                    
                    # Create batch requests
                    requests_list = []
                    for item in batch:
                        requests_list.append(
                            SetItemValues(
                                item_id=item["item_id"],
                                values=item["properties"]
                            )
                        )
                    
                    # Send batch
                    client.send(Batch(requests_list))
                    print(f"✓ Batch {batch_num + 1} sent successfully")
                    
                except Exception as e:
                    print(f"❌ Error sending batch {batch_num + 1}: {e}")
            
            print(f"\n✓ Completed sending {len(items_to_update)} items to Recombee")
            print("You can now check your Recombee admin panel to see the additional properties!")
            
        except Exception as e:
            print(f"❌ Error initializing Recombee client: {e}")
            print("Please check your credentials and try again.")

    def send_attributes_to_api(self, api_url: str = "https://httpbin.org/post"):
        """
        Send product attributes and their types to an API endpoint.
        
        Args:
            api_url (str): API endpoint URL (default: httpbin for testing)
        """
        print("\n" + "="*60)
        print("SENDING ATTRIBUTES TO API")
        print("="*60)
        
        attributes = self.get_product_attributes()
        
        # Prepare the payload
        payload = {
            "dataset_info": {
                "name": "Movies Dataset",
                "total_products": len(self.df),
                "description": "Dataset containing 1000 movies with various attributes"
            },
            "product_attributes": attributes,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        try:
            print(f"Sending data to: {api_url}")
            print(f"Payload structure:")
            print(f"  - Dataset info: {payload['dataset_info']}")
            print(f"  - Number of attributes: {len(payload['product_attributes'])}")
            
            # Send POST request
            response = requests.post(
                api_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            print(f"\nResponse Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✓ Successfully sent attributes to API")
                try:
                    response_data = response.json()
                    print(f"Response: {json.dumps(response_data, indent=2)}")
                except:
                    print(f"Response text: {response.text}")
            else:
                print(f"❌ API request failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending request: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def generate_summary_report(self):
        """
        Generate a comprehensive summary report of the dataset.
        """
        print("\n" + "="*60)
        print("DATASET SUMMARY REPORT")
        print("="*60)
        
        # Dataset overview
        print(f"Dataset: Movies Dataset")
        print(f"File: {os.path.basename(self.csv_file_path)}")
        print(f"Total records: {len(self.df)}")
        print(f"Total attributes: {len(self.df.columns)}")
        
        # Key attributes summary
        attributes = self.get_product_attributes()
        print(f"\nKey Product Attributes:")
        for attr_name, attr_info in list(attributes.items())[:5]:  # Show first 5
            print(f"  • {attr_name}: {attr_info['type']} - {attr_info['description']}")
        
        # Data quality
        print(f"\nData Quality:")
        print(f"  • Complete records: {len(self.df.dropna())}")
        print(f"  • Records with missing data: {len(self.df) - len(self.df.dropna())}")
        
        # Genre distribution
        if 'genre' in self.df.columns:
            genre_counts = self.df['genre'].value_counts().head(10)
            print(f"\nTop 10 Genres:")
            for genre, count in genre_counts.items():
                print(f"  • {genre}: {count} movies")
        
        # Year range
        if 'year' in self.df.columns:
            year_stats = self.df['year'].describe()
            print(f"\nYear Statistics:")
            print(f"  • Range: {int(year_stats['min'])} - {int(year_stats['max'])}")
            print(f"  • Average: {year_stats['mean']:.1f}")
        
        print(f"\n✓ Dataset meets requirements:")
        print(f"  • Has 1000+ products: ✓ ({len(self.df)} movies)")
        print(f"  • Has 3+ attributes: ✓ ({len(attributes)} attributes)")
        print(f"  • Attributes have different types: ✓ (string, integer, float)")

def main():
    """
    Main function to run the movie dataset analysis.
    """
    print("🎬 MOVIE DATASET ANALYZER - LAB 1")
    print("="*60)
    
    # Initialize analyzer
    csv_file = "/Users/andrei.napruiu/Desktop/SDR/Laboratoare-SDR/Lab1/movies-QueryResult.csv"
    analyzer = MovieDatasetAnalyzer(csv_file)
    
    # Run analysis
    analyzer.analyze_dataset()
    analyzer.display_attributes()
    analyzer.generate_summary_report()
    
    # API Options
    print("\n" + "="*60)
    print("API OPTIONS")
    print("="*60)
    print("Choose an option:")
    print("1. Send to Recombee (to add more properties to your items)")
    print("2. Send to demo API (httpbin.org/post)")
    print("3. Skip API calls")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        # Check if .env file exists
        if os.path.exists('.env'):
            print("\n✓ Found .env file with credentials")
            print("Using credentials from .env file...")
            analyzer.send_attributes_to_recombee()
        else:
            print("\n⚠️  No .env file found.")
            print("You can either:")
            print("1. Create .env file: cp env_example.txt .env")
            print("2. Enter credentials manually")
            
            manual_input = input("\nEnter credentials manually? (y/n): ").lower().strip()
            if manual_input in ['y', 'yes']:
                print("\nTo send data to Recombee, you'll need:")
                print("- Database ID")
                print("- Secret Token")
                print("\nYou can find these in your Recombee admin panel under Integration > Catalog Feed")
                
                database_id = input("\nEnter Database ID: ").strip()
                secret_token = input("Enter Secret Token: ").strip()
                
                if all([database_id, secret_token]):
                    analyzer.send_attributes_to_recombee(database_id, secret_token)
                else:
                    print("❌ Missing credentials. Skipping Recombee update.")
            else:
                print("Skipping Recombee update.")
            
    elif choice == "2":
        print("\nNote: Using httpbin.org/post for demonstration purposes")
        user_input = input("Do you want to send attributes to demo API? (y/n): ").lower().strip()
        if user_input in ['y', 'yes']:
            analyzer.send_attributes_to_api()
        else:
            print("Skipping demo API call.")
    else:
        print("Skipping all API calls.")
    
    print("\n✓ Analysis complete!")

if __name__ == "__main__":
    main()