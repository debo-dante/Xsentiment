# 🐦 Xsentiment - Twitter Sentiment Analysis Tool

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Twitter sentiment analysis tool that continuously collects tweets, performs sentiment analysis, and generates beautiful visualizations.

## 🌟 Features

- **📊 Real-time Tweet Collection**: Continuously scrapes tweets for specified keywords
- **🧠 Sentiment Analysis**: Uses TextBlob for sentiment classification (Positive/Negative/Neutral)
- **📈 Beautiful Visualizations**: Multiple chart types including pie charts, bar charts, timelines, and word clouds
- **🌐 Interactive Dashboard**: Web-based dashboard with interactive Plotly charts
- **⚡ Continuous Operation**: Runs indefinitely until keyboard interrupt
- **🔄 Duplicate Prevention**: Automatically filters out duplicate tweets
- **📝 Data Persistence**: Saves data to CSV for long-term analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Twitter Bearer Token (from Twitter Developer Account)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/xsentiment.git
   cd xsentiment
   ```

2. **Install dependencies**
   ```bash
   # For basic functionality
   pip3 install tweepy textblob pandas
   
   # For visualizations
   pip3 install -r requirements_viz.txt
   ```

3. **Set up Twitter API credentials**
   - Get your Bearer Token from [Twitter Developer Portal](https://developer.twitter.com/)
   - Update the `BEARER_TOKEN` in `script.py`

### Usage

#### 1. Collect Tweets
```bash
python3 script.py
```
- Runs continuously, collecting tweets every 5 minutes
- Press `Ctrl+C` to stop gracefully
- Data saved to `tweets_sentiment.csv`

#### 2. Visualize Data
```bash
python3 visualize_tweets.py
```
Choose from multiple visualization options:
- Sentiment distribution charts
- Timeline analysis
- Word clouds
- Interactive dashboard

## 📁 Project Structure

```
xsentiment/
├── script.py              # Main tweet collection script
├── visualize_tweets.py     # Visualization generation script
├── requirements_viz.txt    # Visualization dependencies
├── tweets_sentiment.csv    # Generated data file (ignored by git)
├── README.md              # This file
├── .gitignore             # Git ignore rules
└── generated_files/       # Charts and visualizations (ignored by git)
    ├── *.png             # Static charts
    └── *.html            # Interactive dashboards
```

## 🔧 Configuration

### Tweet Collection Settings
Edit `script.py` to customize:

```python
KEYWORD = "OpenAI"           # Search keyword
MAX_RESULTS = 10             # Tweets per cycle
SLEEP_INTERVAL = 300         # Seconds between cycles (5 minutes)
```

### API Rate Limits
- Twitter API v2 allows 300 requests per 15-minute window
- Current settings respect rate limits automatically
- Increase `SLEEP_INTERVAL` if you encounter rate limiting

## 📊 Visualization Types

### Static Charts (PNG)
- **Pie Chart**: Sentiment distribution percentages
- **Bar Chart**: Sentiment counts with values
- **Timeline**: Sentiment trends over time
- **Word Clouds**: Most common words by sentiment

### Interactive Dashboard (HTML)
- Multi-panel dashboard with hover effects
- Zoomable and interactive elements
- Sentiment distribution, tweet lengths, timeline, and top words

## 🛠️ Advanced Usage

### Custom Keywords
Modify the search keyword in `script.py`:
```python
KEYWORD = "ChatGPT OR GPT-4 OR OpenAI"
```

### Running as Background Service
```bash
# Run in background
nohup python3 script.py > tweet_collector.log 2>&1 &

# Check process
ps aux | grep script.py

# Stop process
kill [PID]
```

### Analyzing Existing Data
If you have existing tweet data, ensure it has columns:
- `Text`: Tweet content
- `Sentiment`: Positive/Negative/Neutral
- `Created_At`: Tweet timestamp (optional)
- `Collection_Time`: When data was collected (optional)

## 📈 Sample Output

```
==================================================
DATASET SUMMARY
==================================================
Total tweets: 150
Columns: ['Text', 'Sentiment', 'Created_At', 'Collection_Time']

Sentiment Distribution:
  Positive: 89 (59.3%)
  Neutral: 45 (30.0%)
  Negative: 16 (10.7%)

Date range: 2025-06-14 to 2025-06-15
```

## 🔒 Security Notes

- **Never commit API keys** to version control
- The `.gitignore` file excludes sensitive data files
- Consider using environment variables for API credentials:
  ```python
  import os
  BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
  ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Tweepy](https://github.com/tweepy/tweepy) for Twitter API integration
- [TextBlob](https://github.com/sloria/TextBlob) for sentiment analysis
- [Plotly](https://github.com/plotly/plotly.py) for interactive visualizations
- [WordCloud](https://github.com/amueller/word_cloud) for word cloud generation

## 📧 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/xsentiment/issues) page
2. Create a new issue with detailed description
3. Include error messages and environment details

---

**Happy Analyzing! 🎉**

