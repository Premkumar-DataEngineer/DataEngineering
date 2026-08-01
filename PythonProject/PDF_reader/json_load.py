import pandas as pd
import json

# Sample nested data
json_data = """
{
    {
        "id": 101,
        "name": "Alice Smith",
        "contact": {
            "email": "alice@example.com",
            "phone": "555-0199"
        },
        "company": {
            "name": "Tech Corp",
            "location": "New York"
        }
    },
    {
        "id": 102
        "name": "Alice Smith",
        "contact": {
            "email": "alice@example.com",
            "phone": "555-0199"
        },
        "company": {
            "name": "Tech Corp",
            "location": "New York"
        }
    }
}
"""

# 1. Convert JSON string to Python dictionary
data_dict = json.loads(json_data)

# 2. Flatten into a single row DataFrame
df = pd.json_normalize(data_dict)
print(df)