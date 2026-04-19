import pandas as pd

class AnalystAgent:
    """
    VoxIntel Analyst Agent: Responsible for statistical aggregation and demographic insights.
    """
    def __init__(self, df):
        self.df = df
        if 'Timestamp' in self.df.columns:
            self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])

    def get_summary_stats(self):
        total_responses = len(self.df)
        avg_satisfaction = self.df['Satisfaction_Score'].mean()
        top_product = self.df['Product_Interests'].value_counts().idxmax()
        
        return {
            "total_responses": total_responses,
            "avg_satisfaction": round(avg_satisfaction, 2),
            "top_product": top_product
        }

    def get_market_share(self):
        return self.df['Product_Interests'].value_counts(normalize=True) * 100

    def get_regional_performance(self):
        return self.df.groupby(['Region', 'Product_Interests']).size().unstack(fill_value=0)

    def get_demographic_split(self):
        return self.df.groupby('Age_Group')['Satisfaction_Score'].mean()

    def identify_anomalies(self):
        # Identify regions where satisfaction is below 2.5
        regional_avg = self.df.groupby('Region')['Satisfaction_Score'].mean()
        anomalies = regional_avg[regional_avg < 3.0].to_dict()
        return anomalies

    def get_agent_thought(self):
        stats = self.get_summary_stats()
        return f"Analyst Agent: Monitored {stats['total_responses']} voices. Market leadership held by {stats['top_product']}."

if __name__ == "__main__":
    test_df = pd.DataFrame({
        'Satisfaction_Score': [4, 5, 3],
        'Product_Interests': ['VoxPhone Elite', 'VoxPhone Elite', 'VoxTab Air'],
        'Region': ['Europe', 'Europe', 'Asia']
    })
    agent = AnalystAgent(test_df)
    print("Market Share:\n", agent.get_market_share())
    print("\nAnomalies:\n", agent.identify_anomalies())
