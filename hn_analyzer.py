import requests
import json
from datetime import datetime
import csv
import re
import html
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Keywords to track (customize these for your product category)
KEYWORDS = {
    'pricing': ['expensive', 'cheap', 'pricing', 'price', 'cost', 'affordable', 'free'],
    'ease_of_use': ['easy', 'simple', 'intuitive', 'user-friendly', 'complicated', 'confusing', 'difficult'],
    'features': ['feature', 'functionality', 'capabilities', 'integration', 'integrations'],
    'support': ['support', 'customer service', 'help', 'documentation', 'docs'],
    'bugs': ['bug', 'broken', 'error', 'crash', 'issue', 'problem', 'glitch'],
    'performance': ['fast', 'slow', 'performance', 'speed', 'lag', 'responsive']
}

def preprocess_comment(text):
    """Strip HTML, tokenize, remove stopwords and short tokens"""
    text = html.unescape(text)                     # decode &#x27; → ' etc.
    text = re.sub(r'<[^>]+>', ' ', text)          # strip HTML tags
    text = re.sub(r'[^a-zA-Z\s]', '', text)       # keep only letters
    tokens = nltk.word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    return [t for t in tokens if t not in stop_words and len(t) >= 3]

def analyze_topics(comments_list, num_topics=3):
    """Extract latent topics from comments using LDA"""

    # Phase 2: Build corpus
    preprocessed = [' '.join(preprocess_comment(c['comment'])) for c in comments_list]

    vectorizer = CountVectorizer(
        min_df=2,        # token must appear in at least 2 documents
        max_df=0.8,      # ignore tokens in more than 80% of docs
        max_features=500
    )
    doc_term_matrix = vectorizer.fit_transform(preprocessed)
    vocab = vectorizer.get_feature_names_out()

    # Phase 3: Train LDA
    lda = LatentDirichletAllocation(
        n_components=num_topics,
        max_iter=10,
        learning_method='batch',
        random_state=42
    )
    doc_topic_matrix = lda.fit_transform(doc_term_matrix)
    # doc_topic_matrix shape: (n_comments, num_topics) — each row sums to 1.0

    # Phase 4: Extract top words and dominant topic per comment
    top_words_per_topic = []
    for topic_weights in lda.components_:
        top_indices = topic_weights.argsort()[-10:][::-1]
        top_words_per_topic.append([vocab[i] for i in top_indices])

    dominant_topics = doc_topic_matrix.argmax(axis=1)
    topic_counts = [0] * num_topics
    for t in dominant_topics:
        topic_counts[t] += 1

    # Display
    total = len(comments_list)
    print("\n" + "=" * 50)
    print("🧠 TOPIC MODELING (LDA)")
    print("=" * 50)
    for i, words in enumerate(top_words_per_topic):
        pct = (topic_counts[i] / total) * 100
        print(f"\n  Topic {i + 1}  ({topic_counts[i]} comments, {pct:.1f}%)")
        print(f"  Top words: {', '.join(words)}")

    return topic_counts, top_words_per_topic

def extract_key_terms(comments_list, search_term, top_n=10):
    """Identify the most distinctive terms in this result set using TF-IDF"""
    preprocessed = [' '.join(preprocess_comment(c['comment'])) for c in comments_list]

    vectorizer = TfidfVectorizer(min_df=2, max_df=0.8)
    tfidf_matrix = vectorizer.fit_transform(preprocessed)
    vocab = vectorizer.get_feature_names_out()

    mean_scores = tfidf_matrix.mean(axis=0).A1  # collapse to 1-D array of per-term means
    scored = sorted(zip(vocab, mean_scores), key=lambda x: x[1], reverse=True)

    # Drop any variant of the search term so it doesn't crowd out real signal
    stop_terms = {t.lower() for t in search_term.split()}
    top_terms = [(term, score) for term, score in scored if term not in stop_terms][:top_n]

    print("\n" + "=" * 50)
    print("🔑 TF-IDF KEY TERMS")
    print("=" * 50)
    print(f"\n  Most distinctive terms in these comments:\n")
    for rank, (term, score) in enumerate(top_terms, 1):
        print(f"  {rank:>2}. {term:<20} {score:.3f}")

    return top_terms

def generate_visualizations(sentiment_counts, keyword_counts,
                            topic_counts, top_words_per_topic, top_terms, search_term):
    """Save a 2x2 PNG of all four analysis charts"""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"HN Analysis: {search_term}", fontsize=16, fontweight='bold', y=1.01)

    # Chart 1 — Sentiment pie (top-left)
    ax1 = axes[0, 0]
    labels = ['Positive', 'Neutral', 'Negative']
    sizes  = [sentiment_counts['positive'], sentiment_counts['neutral'], sentiment_counts['negative']]
    colors = ['#4CAF50', '#9E9E9E', '#F44336']
    non_zero = [(l, s, c) for l, s, c in zip(labels, sizes, colors) if s > 0]
    ax1.pie(
        [s for _, s, _ in non_zero],
        labels=[l for l, _, _ in non_zero],
        colors=[c for _, _, c in non_zero],
        autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10}
    )
    ax1.set_title('Sentiment Distribution', fontweight='bold')

    # Chart 2 — Topic distribution bar (top-right)
    ax2 = axes[0, 1]
    topic_labels = [f"Topic {i + 1}\n({', '.join(words[:3])}...)"
                    for i, words in enumerate(top_words_per_topic)]
    bar_colors = ['#5C6BC0', '#42A5F5', '#26C6DA']
    bars = ax2.bar(topic_labels, topic_counts, color=bar_colors[:len(topic_counts)], width=0.5)
    for bar, count in zip(bars, topic_counts):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 str(count), ha='center', va='bottom', fontsize=10)
    ax2.set_ylabel('Comments')
    ax2.set_title('Topic Distribution', fontweight='bold')
    ax2.set_ylim(0, max(topic_counts) + 2)

    # Chart 3 — TF-IDF horizontal bar (bottom-left)
    ax3 = axes[1, 0]
    terms  = [t for t, _ in top_terms][::-1]   # reverse so rank 1 is at top
    scores = [s for _, s in top_terms][::-1]
    cmap   = cm.Blues(np.linspace(0.4, 0.9, len(terms)))
    ax3.barh(terms, scores, color=cmap)
    ax3.set_xlabel('Mean TF-IDF Score')
    ax3.set_title('TF-IDF Key Terms', fontweight='bold')

    # Chart 4 — Keyword categories bar (bottom-right)
    ax4 = axes[1, 1]
    sorted_kw = sorted(
        [(cat, cnt) for cat, cnt in keyword_counts.items() if cnt > 0],
        key=lambda x: x[1], reverse=True
    )
    if sorted_kw:
        kw_labels = [cat.replace('_', '\n') for cat, _ in sorted_kw]
        kw_counts = [cnt for _, cnt in sorted_kw]
        kw_bars = ax4.bar(kw_labels, kw_counts, color='#FF7043', width=0.5)
        for bar, count in zip(kw_bars, kw_counts):
            ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                     str(count), ha='center', va='bottom', fontsize=10)
        ax4.set_ylabel('Mentions')
        ax4.set_ylim(0, max(kw_counts) + 2)
    else:
        ax4.text(0.5, 0.5, 'No keyword matches', ha='center', va='center',
                 transform=ax4.transAxes, fontsize=12, color='grey')
    ax4.set_title('Keyword Categories', fontweight='bold')

    plt.tight_layout()
    filename = f'hn_{search_term.replace(" ", "_")}_analysis.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✓ Saved visualization to {filename}")

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

def analyze_sentiment(comments_list):
    """Score each comment as positive, negative, or neutral using VADER"""
    sia = SentimentIntensityAnalyzer()
    results = []
    counts = {'positive': 0, 'negative': 0, 'neutral': 0}

    for comment_data in comments_list:
        scores = sia.polarity_scores(comment_data['comment'])
        compound = scores['compound']
        if compound >= 0.05:
            label = 'positive'
        elif compound <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        counts[label] += 1
        results.append({**comment_data, 'sentiment': label, 'sentiment_score': round(compound, 3)})

    return results, counts

print("🔍 Hacker News Product Analyzer")
print("=" * 50)

# What product or keyword do you want to search for?
search_term = input("Enter a product or keyword to search (e.g., 'ChatGPT', 'Notion', 'Stripe'): ")

print(f"\nSearching Hacker News for: {search_term}")
print("This might take a moment...\n")

# Hacker News Algolia API for searching
api_url = f"https://hn.algolia.com/api/v1/search?query={search_term}&tags=comment"

# Get the search results
try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
except requests.exceptions.ConnectionError:
    print("✗ Error: Could not connect to Hacker News. Check your internet connection.")
    exit(1)
except requests.exceptions.Timeout:
    print("✗ Error: Request timed out after 10 seconds.")
    exit(1)
except requests.exceptions.HTTPError as e:
    print(f"✗ Error: HTTP {response.status_code} - {e}")
    exit(1)
except requests.exceptions.RequestException as e:
    print(f"✗ Error: {e}")
    exit(1)

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
        
        clean_text = re.sub(r'<[^>]+>', ' ', html.unescape(comment_text))
        comments_data.append({
            'author': author,
            'date': created_at,
            'story': story_title,
            'comment': clean_text[:300]
        })
        
        # Print preview
        if i < 5:  # Show first 5 in terminal
            print(f"\n--- Comment {i+1} ---")
            print(f"Author: {author}")
            print(f"Story: {story_title}")
            print(f"Comment: {re.sub(r'<[^>]+>', ' ', html.unescape(comment_text[:150]))}...")
    
    filename = f'hn_{search_term.replace(" ", "_")}_comments.csv'

    # Run sentiment analysis
    comments_data, sentiment_counts = analyze_sentiment(comments_data)

    # Save to CSV (sentiment scores included)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['author', 'date', 'story', 'comment', 'sentiment', 'sentiment_score'])
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

    # Sentiment summary
    print("\n" + "=" * 50)
    print("😊 SENTIMENT ANALYSIS")
    print("=" * 50)
    total = len(comments_data)
    for label in ['positive', 'neutral', 'negative']:
        count = sentiment_counts[label]
        pct = (count / total) * 100
        print(f"  {label.upper():<10} {count:>2}  ({pct:.1f}%)")

    most_positive = max(comments_data, key=lambda c: c['sentiment_score'])
    most_negative = min(comments_data, key=lambda c: c['sentiment_score'])
    print(f"\nMost positive (score: {most_positive['sentiment_score']}):")
    print(f"  \"{most_positive['comment'][:120]}...\"")
    print(f"\nMost negative (score: {most_negative['sentiment_score']}):")
    print(f"  \"{most_negative['comment'][:120]}...\"")

    topic_counts, top_words_per_topic = analyze_topics(comments_data)
    top_terms = extract_key_terms(comments_data, search_term)
    generate_visualizations(sentiment_counts, keyword_counts,
                            topic_counts, top_words_per_topic, top_terms, search_term)

else:
    print(f"✗ Error: Status code {response.status_code}")


