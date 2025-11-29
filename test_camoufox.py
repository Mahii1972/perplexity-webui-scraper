"""
Use camoufox (stealth Firefox) to bypass Cloudflare and make requests to Perplexity.
This gets fresh cookies that work with the API.
"""
import json
from camoufox.sync_api import Camoufox

def main():
    print("Starting camoufox browser...")
    
    with Camoufox(headless=False) as browser:
        page = browser.new_page()
        
        # Navigate to Perplexity and let Cloudflare challenge pass
        print("Navigating to Perplexity...")
        page.goto("https://www.perplexity.ai/")
        
        # Wait for the page to fully load (Cloudflare challenge should auto-solve)
        print("Waiting for page to load...")
        page.wait_for_load_state("networkidle")
        
        # Check if we're past Cloudflare
        title = page.title()
        print(f"Page title: {title}")
        
        if "Just a moment" in title:
            print("Still on Cloudflare challenge, waiting more...")
            page.wait_for_timeout(5000)
        
        # Get all cookies
        cookies = page.context.cookies()
        print(f"\nGot {len(cookies)} cookies:")
        
        # Format cookies for use with httpx
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']
            print(f"  {cookie['name']}: {cookie['value'][:50]}...")
        
        # Save cookies to file
        with open("cookies.json", "w") as f:
            json.dump(cookie_dict, f, indent=2)
        print("\nCookies saved to cookies.json")
        
        # Now try to make a request using the page
        print("\nTrying to send a query...")
        
        # Type in the search box and submit
        search_input = page.locator('textarea[placeholder*="Ask"]').first
        if search_input:
            search_input.fill("What is 2+2?")
            search_input.press("Enter")
            
            # Wait for response
            page.wait_for_timeout(10000)
            print("Query sent! Check the browser window.")
        
        input("\nPress Enter to close browser...")

if __name__ == "__main__":
    main()
