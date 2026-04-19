class StrategyAgent:
    """
    VoxIntel Strategy Agent: Generates autonomous business recommendations based on cross-agent analysis.
    """
    def __init__(self, analyst_results, sentiment_results, prediction_trend):
        self.stats = analyst_results
        self.sentiment = sentiment_results
        self.trend = prediction_trend

    def generate_recommendations(self):
        recommendations = []

        # Logic based on Satisfaction
        if self.stats['avg_satisfaction'] < 3.5:
            recommendations.append("🚨 URGENT: Quality audit required for lower-performing product tiers.")
        
        # Logic based on Sentiment
        neg_sent = self.sentiment.get('Negative', 0)
        if neg_sent > 20:
            recommendations.append(f"💬 PR ALERT: Negative sentiment is at {round(neg_sent, 1)}%. Deploy damage control in identified regions.")
            
        # Logic based on Trend
        if self.trend < 0:
            recommendations.append("📉 PREDICTIVE ALERT: Satisfaction drift is negative. Review software stability immediately.")
        else:
            recommendations.append("🚀 GROWTH OPPORTUNITY: Sentiment is trending upward. Ideal window for new feature rollout.")

        # Product specific
        recommendations.append(f"🎯 FOCUS: {self.stats['top_product']} remains the market leader. Scale production to meet demand.")

        return recommendations

    def get_agent_thought(self):
        if self.trend < 0:
            return "Strategy Agent: Critical drift detected. Synthesizing defensive maneuvers and quality benchmarks."
        return "Strategy Agent: Growth cycle confirmed. Optimizing resource allocation for market dominance."

if __name__ == "__main__":
    # Mock data for testing
    stats = {"avg_satisfaction": 3.2, "top_product": "VoxPhone Elite"}
    sent = {"Negative": 25}
    strat = StrategyAgent(stats, sent, -0.01)
    print("Strategy Output:\n", strat.generate_recommendations())
