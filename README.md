# HN Product Analyzer

AI-powered product intelligence tool that analyzes Hacker News discussions to extract sentiment, topics, and key insights.

## Features

- **Keyword Analysis** - Categorizes comments by predefined topics (pricing, features, support, etc.)
- **Sentiment Analysis** - VADER-based emotional tone detection (positive/neutral/negative)
- **Topic Modeling** - LDA-based automatic theme discovery
- **TF-IDF Extraction** - Identifies most distinctive vocabulary
- **Data Visualization** - Generates professional charts automatically

## Output

- **Terminal**: Detailed text analysis with all insights
- **CSV Export**: `hn_{product}_comments.csv` - Raw data for further analysis
- **Visual Report**: `hn_{product}_analysis.png` - 4-chart dashboard

## Installation

```bash
git clone https://github.com/YOUR-USERNAME/review-analyzer.git
cd review-analyzer
pip install -r requirements.txt
python3 -c "import nltk; nltk.download('vader_lexicon')"
```

## Usage

```bash
python3 hn_analyzer.py
# Enter product name when prompted (e.g., "Notion", "ChatGPT", "AWS")
```

## Sample Output

**Search: "AWS"**
Sentiment: 85% positive, 10% neutral, 5% negative
Topics: 45% usage, 35% hiring, 20% infrastructure
Key Terms: engineer, cloud, services, onsite, product
Categories: Support 25%, Pricing 10%, Performance 5%

Plus a 2x2 visualization showing all insights visually.

## Tech Stack

- Python 3.14
- scikit-learn (LDA, TF-IDF)
- NLTK (sentiment, tokenization)
- matplotlib (visualization)
- requests (API calls)

## Project Structure
review-analyzer/
├── hn_analyzer.py          # Main analyzer
├── fundamentals.py         # Learning exercises
├── requirements.txt        # Dependencies
└── hn_*.csv / *.png       # Generated outputs

## Learning Journey

This project was built as a learning exercise to understand:
- Python fundamentals
- Machine learning (supervised & unsupervised)
- Natural language processing
- Data visualization
- API integration

See the [pm-tech-portfolio](https://github.com/YOUR-USERNAME/pm-tech-portfolio) for detailed project documentation.

## Dependencies
requests
beautifulsoup4
nltk
scikit-learn
matplotlib
numpy

## License

MIT