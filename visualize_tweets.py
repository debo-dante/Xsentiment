import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import numpy as np
from datetime import datetime, timedelta
import os
from collections import Counter
import re

# Set style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TweetVisualizer:
    def __init__(self, csv_file="tweets_sentiment.csv"):
        self.csv_file = csv_file
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load tweet data from CSV file"""
        if not os.path.exists(self.csv_file):
            print(f"Error: {self.csv_file} not found!")
            print("Make sure to run script.py first to collect tweet data.")
            return False
        
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"Loaded {len(self.df)} tweets from {self.csv_file}")
            
            # Convert Created_At to datetime if it exists
            if 'Created_At' in self.df.columns:
                self.df['Created_At'] = pd.to_datetime(self.df['Created_At'], errors='coerce')
            
            # Convert Collection_Time to datetime if it exists
            if 'Collection_Time' in self.df.columns:
                self.df['Collection_Time'] = pd.to_datetime(self.df['Collection_Time'], errors='coerce')
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def print_summary(self):
        """Print basic statistics about the dataset"""
        if self.df is None or len(self.df) == 0:
            print("No data available")
            return
        
        print("\n" + "="*50)
        print("DATASET SUMMARY")
        print("="*50)
        print(f"Total tweets: {len(self.df)}")
        print(f"Columns: {list(self.df.columns)}")
        
        if 'Sentiment' in self.df.columns:
            print("\nSentiment Distribution:")
            sentiment_counts = self.df['Sentiment'].value_counts()
            for sentiment, count in sentiment_counts.items():
                percentage = (count / len(self.df)) * 100
                print(f"  {sentiment}: {count} ({percentage:.1f}%)")
        
        if 'Created_At' in self.df.columns:
            valid_dates = self.df['Created_At'].dropna()
            if len(valid_dates) > 0:
                print(f"\nDate range: {valid_dates.min()} to {valid_dates.max()}")
        
        print("\nSample tweets:")
        for i, row in self.df.head(3).iterrows():
            sentiment = row.get('Sentiment', 'Unknown')
            text = row.get('Text', '')[:100] + '...' if len(row.get('Text', '')) > 100 else row.get('Text', '')
            print(f"  [{sentiment}] {text}")
    
    def create_sentiment_pie_chart(self):
        """Create a pie chart showing sentiment distribution"""
        if 'Sentiment' in self.df.columns:
            sentiment_counts = self.df['Sentiment'].value_counts()
            
            plt.figure(figsize=(8, 6))
            colors = ['#ff9999', '#66b3ff', '#99ff99']
            plt.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
            plt.title('Tweet Sentiment Distribution', fontsize=16, fontweight='bold')
            plt.axis('equal')
            plt.tight_layout()
            plt.savefig('sentiment_pie_chart.png', dpi=300, bbox_inches='tight')
            plt.show()
            print("Saved: sentiment_pie_chart.png")
    
    def create_sentiment_bar_chart(self):
        """Create a bar chart showing sentiment distribution"""
        if 'Sentiment' in self.df.columns:
            sentiment_counts = self.df['Sentiment'].value_counts()
            
            plt.figure(figsize=(10, 6))
            bars = plt.bar(sentiment_counts.index, sentiment_counts.values, 
                          color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
            plt.title('Tweet Sentiment Distribution', fontsize=16, fontweight='bold')
            plt.xlabel('Sentiment', fontsize=12)
            plt.ylabel('Number of Tweets', fontsize=12)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{int(height)}', ha='center', va='bottom', fontsize=12)
            
            plt.tight_layout()
            plt.savefig('sentiment_bar_chart.png', dpi=300, bbox_inches='tight')
            plt.show()
            print("Saved: sentiment_bar_chart.png")
    
    def create_timeline_chart(self):
        """Create a timeline chart showing sentiment over time"""
        if 'Created_At' in self.df.columns and 'Sentiment' in self.df.columns:
            # Filter out rows with invalid dates
            df_with_dates = self.df.dropna(subset=['Created_At'])
            
            if len(df_with_dates) == 0:
                print("No valid dates found for timeline chart")
                return
            
            # Group by date and sentiment
            df_with_dates['Date'] = df_with_dates['Created_At'].dt.date
            timeline_data = df_with_dates.groupby(['Date', 'Sentiment']).size().unstack(fill_value=0)
            
            plt.figure(figsize=(12, 6))
            timeline_data.plot(kind='line', marker='o', linewidth=2, markersize=6)
            plt.title('Tweet Sentiment Over Time', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Number of Tweets', fontsize=12)
            plt.legend(title='Sentiment')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('sentiment_timeline.png', dpi=300, bbox_inches='tight')
            plt.show()
            print("Saved: sentiment_timeline.png")
    
    def create_word_cloud(self):
        """Create word clouds for each sentiment"""
        if 'Text' not in self.df.columns or 'Sentiment' not in self.df.columns:
            print("Cannot create word cloud: missing Text or Sentiment columns")
            return
        
        sentiments = self.df['Sentiment'].unique()
        
        for sentiment in sentiments:
            # Get all text for this sentiment
            sentiment_texts = self.df[self.df['Sentiment'] == sentiment]['Text'].tolist()
            all_text = ' '.join(sentiment_texts)
            
            # Clean text (remove URLs, mentions, etc.)
            cleaned_text = re.sub(r'http\S+|www\S+|@\w+|#\w+', '', all_text)
            
            if len(cleaned_text.strip()) > 0:
                plt.figure(figsize=(10, 6))
                wordcloud = WordCloud(width=800, height=400, 
                                    background_color='white',
                                    colormap='viridis',
                                    max_words=100).generate(cleaned_text)
                
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.title(f'Word Cloud - {sentiment} Tweets', fontsize=16, fontweight='bold')
                plt.tight_layout()
                
                filename = f'wordcloud_{sentiment.lower()}.png'
                plt.savefig(filename, dpi=300, bbox_inches='tight')
                plt.show()
                print(f"Saved: {filename}")
    
    def create_interactive_dashboard(self):
        """Create an interactive Plotly dashboard"""
        if self.df is None or len(self.df) == 0:
            print("No data available for dashboard")
            return
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Sentiment Distribution', 'Tweet Length Distribution', 
                          'Sentiment Over Time', 'Top Words'),
            specs=[[{'type': 'pie'}, {'type': 'histogram'}],
                   [{'type': 'scatter'}, {'type': 'bar'}]]
        )
        
        # Pie chart for sentiment distribution
        if 'Sentiment' in self.df.columns:
            sentiment_counts = self.df['Sentiment'].value_counts()
            fig.add_trace(
                go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values,
                      name="Sentiment"),
                row=1, col=1
            )
        
        # Histogram for tweet length
        if 'Text' in self.df.columns:
            tweet_lengths = self.df['Text'].str.len()
            fig.add_trace(
                go.Histogram(x=tweet_lengths, name="Tweet Length", nbinsx=30),
                row=1, col=2
            )
        
        # Timeline if dates are available
        if 'Created_At' in self.df.columns and 'Sentiment' in self.df.columns:
            df_with_dates = self.df.dropna(subset=['Created_At'])
            if len(df_with_dates) > 0:
                for sentiment in df_with_dates['Sentiment'].unique():
                    sentiment_data = df_with_dates[df_with_dates['Sentiment'] == sentiment]
                    sentiment_counts = sentiment_data.groupby(sentiment_data['Created_At'].dt.date).size()
                    
                    fig.add_trace(
                        go.Scatter(x=sentiment_counts.index, y=sentiment_counts.values,
                                 mode='lines+markers', name=f'{sentiment}'),
                        row=2, col=1
                    )
        
        # Top words
        if 'Text' in self.df.columns:
            all_text = ' '.join(self.df['Text'].tolist())
            words = re.findall(r'\b\w+\b', all_text.lower())
            # Filter out common words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'rt', 'https', 'http'}
            filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
            word_counts = Counter(filtered_words).most_common(10)
            
            if word_counts:
                words, counts = zip(*word_counts)
                fig.add_trace(
                    go.Bar(x=list(counts), y=list(words), orientation='h', name="Top Words"),
                    row=2, col=2
                )
        
        # Update layout
        fig.update_layout(
            height=800,
            title_text="Tweet Sentiment Analysis Dashboard",
            title_x=0.5,
            showlegend=True
        )
        
        # Save and show
        fig.write_html("tweet_dashboard.html")
        fig.show()
        print("Saved: tweet_dashboard.html")
    
    def create_all_visualizations(self):
        """Create all visualizations at once"""
        print("Creating all visualizations...\n")
        
        self.print_summary()
        
        print("\nCreating charts...")
        self.create_sentiment_pie_chart()
        self.create_sentiment_bar_chart()
        self.create_timeline_chart()
        
        print("\nCreating word clouds...")
        try:
            self.create_word_cloud()
        except Exception as e:
            print(f"Could not create word clouds: {e}")
            print("You might need to install wordcloud: pip install wordcloud")
        
        print("\nCreating interactive dashboard...")
        try:
            self.create_interactive_dashboard()
        except Exception as e:
            print(f"Could not create interactive dashboard: {e}")
            print("You might need to install plotly: pip install plotly")
        
        print("\n" + "="*50)
        print("VISUALIZATION COMPLETE!")
        print("="*50)
        print("Generated files:")
        print("  - sentiment_pie_chart.png")
        print("  - sentiment_bar_chart.png")
        print("  - sentiment_timeline.png")
        print("  - wordcloud_[sentiment].png")
        print("  - tweet_dashboard.html")

def main():
    """Main function to run visualizations"""
    print("Tweet Sentiment Visualization Tool")
    print("=" * 40)
    
    visualizer = TweetVisualizer()
    
    if visualizer.df is None:
        return
    
    while True:
        print("\nSelect visualization option:")
        print("1. Print summary")
        print("2. Sentiment pie chart")
        print("3. Sentiment bar chart")
        print("4. Timeline chart")
        print("5. Word clouds")
        print("6. Interactive dashboard")
        print("7. Create all visualizations")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            visualizer.print_summary()
        elif choice == '2':
            visualizer.create_sentiment_pie_chart()
        elif choice == '3':
            visualizer.create_sentiment_bar_chart()
        elif choice == '4':
            visualizer.create_timeline_chart()
        elif choice == '5':
            visualizer.create_word_cloud()
        elif choice == '6':
            visualizer.create_interactive_dashboard()
        elif choice == '7':
            visualizer.create_all_visualizations()
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

