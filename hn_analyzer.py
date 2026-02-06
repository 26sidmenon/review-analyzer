import requests
import json
from datetime import datetime
import csv

# Keywords to track (customize these for your product category)
KEYWORDS = {
    'pricing': ['expensive', 'cheap', 'pricing', 'price', 'cost', 'affordable', 'free'],
    'ease_of_use': ['easy', 'simple', 'intuitive', 'user-friendly', 'complicated', 'confusing', 'difficult'],
    'features': ['feature', 'functionality', 'capabilities', 'integration', 'integrations'],
    'support': ['support', 'customer service', 'help', 'documentation', 'docs'],
    'bugs': ['bug', 'broken', 'error', 'crash', 'issue', 'problem', 'glitch'],
    'performance': ['fast', 'slow', 'performance', 'speed', 'lag', 'responsive']
}

def analyze_keywords(comments_list):
    """Count how many comments mention each keyword category"""
    
    keyword_counts = {category: 0 for category in KEYWORDS.keys()}
    keyword_details = {category: [] for category in KEYWORDS.keys()}
    
    for comment_data in comments_list:
        comment_text = comment_data['comment'].lower()
        
        for category, keywords in KEYWORDS.items():
            for keyword in keywords:
                if keyword in comment_text:
                    keyword_counts[category] += 1
                    keyword_details[category].append({
                        'keyword': keyword,
                        'comment_preview': comment_data['comment'][:100]
                    })
                    break  # Count each comment only once per category
    
    return keyword_counts, keyword_details

print("🔍 Hacker News Product Analyzer")
print("=" * 50)

# What product or keyword do you want to search for?
search_term = input("Enter a product or keyword to search (e.g., 'ChatGPT', 'Notion', 'Stripe'): ")

print(f"\nSearching Hacker News for: {search_term}")
print("This might take a moment...\n")

# Hacker News Algolia API for searching
api_url = f"https://hn.algolia.com/api/v1/search?query={search_term}&tags=comment"

# Get the search results
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    hits = data['hits']
    
    print(f"✓ Found {len(hits)} comments mentioning '{search_term}'")
    
    # Extract and save comment data
    comments_data = []
    
    for i, hit in enumerate(hits[:20]):  # First 20 comments
        comment_text = hit.get('comment_text', 'N/A')
        author = hit.get('author', 'Unknown')
        created_at = hit.get('created_at', 'N/A')
        story_title = hit.get('story_title', 'N/A')
        
        comments_data.append({
            'author': author,
            'date': created_at,
            'story': story_title,
            'comment': comment_text[:300]  # First 300 characters
        })
        
        # Print preview
        if i < 5:  # Show first 5 in terminal
            print(f"\n--- Comment {i+1} ---")
            print(f"Author: {author}")
            print(f"Story: {story_title}")
            print(f"Comment: {comment_text[:150]}...")
    
    # Save to CSV
    filename = f'hn_{search_term.replace(" ", "_")}_comments.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['author', 'date', 'story', 'comment'])
        writer.writeheader()
        writer.writerows(comments_data)
    
    print(f"\n✓ Saved {len(comments_data)} comments to {filename}")
    # Analyze keywords
    print("\n" + "=" * 50)
    print("📊 KEYWORD ANALYSIS")
    print("=" * 50)
    
    keyword_counts, keyword_details = analyze_keywords(comments_data)
    
    # Display results
    print(f"\nAnalyzed {len(comments_data)} comments:")
    for category, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(comments_data)) * 100
        print(f"  {category.upper()}: {count} mentions ({percentage:.1f}%)")
    
    # Show examples for top category
    top_category = max(keyword_counts, key=keyword_counts.get)
    if keyword_counts[top_category] > 0:
        print(f"\n💡 Top mentions are about: {top_category.upper()}")
        print("Sample comments:")
        for detail in keyword_details[top_category][:3]:
            print(f"  - '{detail['keyword']}': {detail['comment_preview']}...")

    print(f"\nYou can open {filename} in Excel or Google Sheets to analyze!")
    
else:
    print(f"✗ Error: Status code {response.status_code}")
