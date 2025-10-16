#!/usr/bin/env python3
"""
Recombee Credentials Helper
This script helps you find your Recombee API credentials.
"""

def print_recombee_instructions():
    """
    Print detailed instructions on how to find Recombee credentials.
    """
    print("🔑 HOW TO FIND YOUR RECOMBEE CREDENTIALS")
    print("="*60)
    print()
    print("1. Go to your Recombee admin panel:")
    print("   https://admin.recombee.com")
    print()
    print("2. Log in to your account")
    print()
    print("3. Navigate to: Integration > Catalog Feed")
    print("   (This is usually in the left sidebar)")
    print()
    print("4. You'll find three important values:")
    print()
    print("   📍 API URL:")
    print("      - Look for 'API URL' or 'Endpoint URL'")
    print("      - Format: https://[your-database-name].recombee.com")
    print("      - Example: https://my-movies-db.recombee.com")
    print()
    print("   📍 Database ID:")
    print("      - Look for 'Database ID' or 'Database Name'")
    print("      - This is usually the same as your database name")
    print("      - Example: my-movies-db")
    print()
    print("   📍 Secret Token:")
    print("      - Look for 'Secret Token' or 'API Key'")
    print("      - This is a long string of characters")
    print("      - Example: ZNeKdnmeGLR560s5g7sr0uUcnRs53wOGTkVrnk0Hee4gYpS0HvDRdpU1Exu5mrDP")
    print()
    print("5. Alternative locations to check:")
    print("   - Dashboard > API Information")
    print("   - Settings > API Keys")
    print("   - Account > API Configuration")
    print()
    print("6. If you can't find the credentials:")
    print("   - Check if you're in the correct database")
    print("   - Look for a 'Limited Dev Database' toggle")
    print("   - Make sure you have admin permissions")
    print()
    print("💡 TIP: The API URL is usually:")
    print("   https://[your-database-name].recombee.com")
    print()
    print("🔒 Keep your Secret Token secure and don't share it!")
    print()
    print("📞 Need help? Contact Recombee support if you can't find these values.")

if __name__ == "__main__":
    print_recombee_instructions()
