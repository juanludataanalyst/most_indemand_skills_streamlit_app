import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import json
import numpy as np  # Import numpy for vectorized operations

# Read the CSV of skills
skills_df = pd.read_csv('output_data/skills_data_table.csv')

# Create a binary table where each row is a title and each column a skill
skills_encoded = (
    skills_df.groupby(['title', 'skills']).size().unstack(fill_value=0)
    .transform(lambda x: np.where(x > 0, 1, 0))  # Convert to binary format using map
)

# Apply the Apriori algorithm
frequent_itemsets = apriori(skills_encoded, min_support=0.1, use_colnames=True)

# Generate the rules of association, specifying num_itemsets (e.g., 10)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1, num_itemsets=10)

print(rules)

# Create a simplified structure for the JSON
simplified_rules = []
for _, row in rules.iterrows():
    antecedents = list(row['antecedents'])
    consequents = list(row['consequents'])

    # Add to the JSON simplified
    simplified_rules.append({
        "antecedents": antecedents,
        "consequents": consequents,
        "support": row['support'],
        "confidence": row['confidence'],
        "lift": row['lift']
    })

# Save the JSON simplified
with open('output_data/summary_association_rules.json', 'w') as f:
    json.dump(simplified_rules, f, indent=4)

print("Archivo JSON simplificado creado.")