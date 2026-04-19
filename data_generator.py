import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Configuration
REGIONS = ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East']
AGE_GROUPS = ['18-24', '25-34', '35-44', '45-54', '55+']
GENDERS = ['Male', 'Female', 'Non-binary', 'Prefer not to say']
PRODUCTS = ['VoxPhone Elite', 'VoxTab Air', 'VoxWatch Pro']

# Theme-based feedback templates
FEEDBACK_LIB = {
    'Positive': {
        'Battery': ["The battery life is revolutionary.", "Lasts all day even with heavy use.", "Incredible power management."],
        'Performance': ["Absolutely love the performance!", "Seamless integration with my workflow.", "Blazing fast speeds."],
        'Price': ["Premium feel and worth every penny.", "Great value for a flagship device.", "A smart investment."],
        'Support': ["Exceptional customer support experience.", "Helpful and quick response times."]
    },
    'Neutral': {
        'Battery': ["Battery is average.", "Does the job but needs daily charging.", "Standard battery performance."],
        'Performance': ["It's okay, does the job.", "Standard performance.", "Good for basic tasks."],
        'Price': ["Good value for money but nothing special.", "Fairly priced.", "Regular market pricing."],
        'Support': ["Standard support quality.", "Took some time but solved."]
    },
    'Negative': {
        'Battery': ["Battery drains way too fast.", "Poor battery life compared to competitors.", "Needs constant charging."],
        'Performance': ["Extremely disappointed with the build.", "Frequent software glitches.", "Laggy and slow."],
        'Price': ["Overpriced for what it offers.", "Hidden costs and expensive repairs.", "Not worth the premium."],
        'Support': ["Support was unhelpful.", "Long wait times and no solution."]
    }
}

def generate_single_record(record_id=0, timestamp=None, bias_satisfaction=0):
    """Generates a single industry-grade opinion record."""
    region = random.choice(REGIONS)
    age = random.choice(AGE_GROUPS)
    product = random.choice(PRODUCTS)
    
    # Artificial bias: Asia-Pacific likes VoxPhone Elite more
    if region == 'Asia-Pacific' and random.random() > 0.4:
        product = 'VoxPhone Elite'
        
    # Satisfaction based on product performance + external bias
    if product == 'VoxPhone Elite':
        base_satisfaction = np.random.choice([4, 5], p=[0.3, 0.7])
    elif product == 'VoxTab Air':
        base_satisfaction = np.random.choice([3, 4, 5], p=[0.2, 0.5, 0.3])
    else:
        base_satisfaction = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.4, 0.2, 0.1])

    # Apply bias (capped at 1-5)
    satisfaction = int(np.clip(base_satisfaction + bias_satisfaction, 1, 5))

    # Match feedback to satisfaction and theme
    label = 'Positive' if satisfaction >= 4 else ('Neutral' if satisfaction == 3 else 'Negative')
    theme = random.choice(['Battery', 'Performance', 'Price', 'Support'])
    feedback = random.choice(FEEDBACK_LIB[label][theme])

    if timestamp is None:
        timestamp = datetime.now()

    return {
        'Record_ID': f"VOX-{10000 + record_id}",
        'Timestamp': timestamp,
        'Region': region,
        'Age_Group': age,
        'Gender': random.choice(GENDERS),
        'Product_Interests': product,
        'Satisfaction_Score': satisfaction,
        'Feedback': feedback,
        'Theme': theme
    }

def generate_voxintel_data(num_records=1000):
    print(f"Generating {num_records} industry-grade opinion records...")
    
    data = []
    start_date = datetime.now() - timedelta(days=90)

    for i in range(num_records):
        # Evenly spread timestamps over last 90 days
        timestamp = start_date + timedelta(
            days=random.randint(0, 89),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        data.append(generate_single_record(i, timestamp))

    df = pd.DataFrame(data)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/raw_poll_data.csv', index=False)
    print("Success: Synthetic dataset saved to 'data/raw_poll_data.csv'")
    return df

if __name__ == "__main__":
    generate_voxintel_data()
