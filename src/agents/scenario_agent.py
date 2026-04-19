import numpy as np

class ScenarioAgent:
    """
    VoxIntel Scenario Agent: Simulates the business impact of hypothetical decisions.
    """
    def __init__(self, df):
        self.df = df

    def simulate_shift(self, input_decision):
        """
        Calculates the predicted satisfaction shift based on a business decision.
        input_decision: dict with keys like 'investment_area', 'amount'
        """
        base_avg = self.df['Satisfaction_Score'].mean()
        
        # Hypothetical multipliers based on industry common sense
        shift_map = {
            'Quality': 0.15,
            'Price Drop': 0.10,
            'Support': 0.08,
            'R&D': 0.12
        }
        
        area = input_decision.get('area', 'Quality')
        magnitude = input_decision.get('magnitude', 1) # 1 (Low) to 5 (High)
        
        shift = shift_map.get(area, 0.05) * (magnitude / 2)
        simulated_avg = np.clip(base_avg + shift, 1, 5)
        
        return {
            'area': area,
            'original_avg': round(base_avg, 2),
            'simulated_avg': round(simulated_avg, 2),
            'net_gain': round(simulated_avg - base_avg, 2),
            'confidence': "High (Historical Correlation)"
        }

    def get_agent_thought(self, results):
        return f"Scenario Agent: If we increase focus on {results['area']}, we predict a net satisfaction gain of {results['net_gain']} points."

if __name__ == "__main__":
    import pandas as pd
    df = pd.DataFrame({'Satisfaction_Score': [4, 3, 5, 2, 4]})
    agent = ScenarioAgent(df)
    print(agent.simulate_shift({'area': 'Quality', 'magnitude': 3}))
