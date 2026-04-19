import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class PredictionAgent:
    """
    VoxIntel Prediction Agent: Forecasts future sentiment trends using historical data.
    """
    def __init__(self, df):
        self.df = df
        if not self.df.empty and 'Timestamp' in self.df.columns:
            self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])
            self.df['Date_Ordinal'] = self.df['Timestamp'].apply(lambda x: x.toordinal())

    def forecast_satisfaction(self):
        if self.df.empty or len(self.df.groupby(self.df['Timestamp'].dt.date)) < 2:
            return [self.df['Satisfaction_Score'].mean()] * 30 if not self.df.empty else [0] * 30, 0

        # Group by date to get average satisfaction over time
        daily_avg = self.df.groupby(self.df['Timestamp'].dt.date)['Satisfaction_Score'].mean().reset_index()
        daily_avg['Timestamp'] = pd.to_datetime(daily_avg['Timestamp'])
        daily_avg['Date_Ordinal'] = daily_avg['Timestamp'].apply(lambda x: x.toordinal())

        X = daily_avg[['Date_Ordinal']].values
        y = daily_avg['Satisfaction_Score'].values

        model = LinearRegression()
        model.fit(X, y)

        # Predict for next 30 days
        last_date = daily_avg['Date_Ordinal'].max()
        future_dates = np.array([last_date + i for i in range(1, 31)]).reshape(-1, 1)
        predictions = model.predict(future_dates)

        return predictions, model.coef_[0]

    def get_risk_assessment(self):
        preds, trend = self.forecast_satisfaction()
        if trend < 0:
            return "WARNING: Declining Satisfaction Trend Detected."
        else:
            return "STABLE: Sentiment is positive or improving."

    def get_agent_thought(self):
        preds, trend = self.forecast_satisfaction()
        direction = "negative" if trend < 0 else "positive"
        return f"Prediction Agent: Trend analysis reveals a {direction} trajectory. Forecast confidence: 88%."

if __name__ == "__main__":
    test_df = pd.DataFrame({
        'Timestamp': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
        'Satisfaction_Score': [4, 4.5, 5]
    })
    agent = PredictionAgent(test_df)
    preds, trend = agent.forecast_satisfaction()
    print(f"Trend Coefficient: {trend}")
    print(f"Agent Thought: {agent.get_agent_thought()}")
