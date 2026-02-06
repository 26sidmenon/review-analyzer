# This imports libraries we need (like tools in a toolbox)
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# The G2 product page we want to scrape
# You'll change this to whatever product you want to analyze
url = "https://www.g2.com/products/slack/reviews"

print("Starting to scrape reviews...")
print(f"Target URL: {url}")

# Send a request to get the webpage
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)

# Check if we successfully got the page
if response.status_code == 200:
    print("✓ Successfully connected to G2!")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find review elements (this is where we extract the actual reviews)
    # G2's structure: reviews are in specific div classes
    reviews = soup.find_all('div', class_='paper paper--white paper--box mb-2 position-relative')
    
    print(f"Found {len(reviews)} reviews on this page")
    
    # Let's extract data from the first 5 reviews to start
    review_data = []
    
    for i, review in enumerate(reviews[:5]):  # [:5] means "first 5 only"
        try:
            # Extract the rating (stars)
            rating_elem = review.find('div', class_='stars')
            rating = rating_elem.get('class')[1].replace('stars-', '') if rating_elem else "N/A"
            
            # Extract review title
            title_elem = review.find('h3')
            title = title_elem.text.strip() if title_elem else "No title"
            
            # Extract review text
            text_elem = review.find('div', itemprop='reviewBody')
            text = text_elem.text.strip() if text_elem else "No review text"
            
            # Store the data
            review_data.append({
                'rating': rating,
                'title': title,
                'text': text[:200]  # First 200 characters only for now
            })
            
            print(f"\nReview {i+1}:")
            print(f"Rating: {rating} stars")
            print(f"Title: {title}")
            print(f"Text preview: {text[:100]}...")
            
        except Exception as e:
            print(f"Error processing review {i+1}: {e}")
    
    # Save to CSV file
    if review_data:
        with open('reviews.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['rating', 'title', 'text'])
            writer.writeheader()
            writer.writerows(review_data)
        print(f"\n✓ Saved {len(review_data)} reviews to reviews.csv")
    
else:
    print(f"✗ Failed to connect. Status code: {response.status_code}")