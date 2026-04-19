import pandas as pd
from textblob import TextBlob

class SentimentAgent:
    """
    VoxIntel Sentiment Agent: Processes open-ended feedback using NLP to extract emotional tone and themes.
    """
    def __init__(self, df):
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        self.df = df

    def analyze_sentiment(self):
        # Calculate sentiment polarity (-1 to 1)
        self.df['Polarity'] = self.df['Feedback'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        
        # Categorize
        def categorize(p):
            if p > 0.1: return 'Positive'
            elif p < -0.1: return 'Negative'
            else: return 'Neutral'
            
        self.df['Sentiment_Label'] = self.df['Polarity'].apply(categorize)
        return self.df

    def get_sentiment_distribution(self):
        df_analyzed = self.analyze_sentiment()
        return df_analyzed['Sentiment_Label'].value_counts(normalize=True) * 100

    def get_theme_distribution(self):
        """Extracts frequency of mentioned themes (Battery, Price, etc.)"""
        if 'Theme' in self.df.columns:
            return self.df['Theme'].value_counts(normalize=True) * 100
        return pd.Series()

    def get_top_keywords(self):
        # Simple word frequency from feedback
        from collections import Counter
        all_text = " ".join(self.df['Feedback'].astype(str)).lower()
        words = [w for w in all_text.split() if len(w) > 4] # Filter small words
        return Counter(words).most_common(10)

    def get_agent_thought(self):
        dist = self.get_sentiment_distribution().to_dict()
        top_sent = max(dist, key=dist.get)
        return f"Sentiment Agent: Public tone is predominantly {top_sent}. Analyzing primary friction points in themes..."

if __name__ == "__main__":
    # Test data
    test_df = pd.DataFrame({
        'Feedback': ["Great battery life!", "Too expensive.", "Okay performance."],
        'Theme': ['Battery', 'Price', 'Performance']
    })
    agent = SentimentAgent(test_df)
    print("Sentiment Distribution:\n", agent.get_sentiment_distribution())
    print("\nTheme Distribution:\n", agent.get_theme_distribution())
