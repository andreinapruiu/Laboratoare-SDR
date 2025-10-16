#!/usr/bin/env python3
"""
Recombee URL Finder
This script helps you determine your exact Recombee database URL.
"""

def find_recombee_url():
    """
    Help user determine their Recombee database URL.
    """
    print("🔍 FINDING YOUR RECOMBEE DATABASE URL")
    print("="*50)
    print()
    
    print("Based on your screenshot, I can see you're using the 'LaboratoareSdr' project.")
    print()
    
    print("Your Recombee database URL is likely:")
    print("   https://laboratoaresdr.recombee.com")
    print()
    
    print("However, let's verify this step by step:")
    print()
    
    print("1. Go to: https://admin.recombee.com")
    print("2. Log in to your account")
    print("3. Look at the top-left corner - you should see 'LaboratoareSdr'")
    print("4. Navigate to: Integration > Catalog Feed")
    print("5. Look for the API URL field")
    print()
    
    print("Common URL patterns:")
    print("   - https://laboratoaresdr.recombee.com")
    print("   - https://laboratoaresdr-dev.recombee.com")
    print("   - https://laboratoaresdr-prod.recombee.com")
    print()
    
    print("If you see a 'Limited Dev Database' toggle:")
    print("   - If it's ON: URL might be https://laboratoaresdr-dev.recombee.com")
    print("   - If it's OFF: URL might be https://laboratoaresdr.recombee.com")
    print()
    
    print("Still can't find it? Try these steps:")
    print("1. Check the browser URL bar when you're in the admin panel")
    print("2. Look for any 'API Documentation' or 'Developer' sections")
    print("3. Check if there's a 'Settings' or 'Account' section")
    print()
    
    print("💡 Quick test: Try running this command to test the URL:")
    print("   curl -I https://laboratoaresdr.recombee.com")
    print("   (If it returns HTTP 200, the URL is correct)")

if __name__ == "__main__":
    find_recombee_url()
