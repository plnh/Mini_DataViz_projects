import pandas as pd
import matplotlib.pyplot as plt
from mizani.palettes import brewer_pal

data = [
    {"Hazard/Type": "Collision - Building Glass", "Source": "Loss et al. 2014a", "Min Range": 365000000, "Max Range": 988000000, "Median/Avg. Estimated": 599000000},
    {"Hazard/Type": "Collisions - Communication towers", "Source": "Longcore et al. 2012", "Min Range": None, "Max Range": None, "Median/Avg. Estimated": 6600000},
    {"Hazard/Type": "Collisions - Electrical lines", "Source": "Loss et al. 2014c", "Min Range": 8000000, "Max Range": 57300000, "Median/Avg. Estimated": 25500000},
    {"Hazard/Type": "Collision - Vehicles", "Source": "Loss et al. 2014b", "Min Range": 89000000, "Max Range": 340000000, "Median/Avg. Estimated": 214500000},
    {"Hazard/Type": "Collisions - Land-based Wind Turbines", "Source": "Loss et al. 2013b", "Min Range": 140438, "Max Range": 327586, "Median/Avg. Estimated": 234012},
    {"Hazard/Type": "Electrocutions", "Source": "Loss et al. 2014c", "Min Range": 900000, "Max Range": 11600000, "Median/Avg. Estimated": 5600000},
    {"Hazard/Type": "Poison", "Source": None, "Min Range": None, "Max Range": None, "Median/Avg. Estimated": 72000000},
    {"Hazard/Type": "Cats", "Source": "Loss et al. 2013a", "Min Range": 1400000000, "Max Range": 3700000000, "Median/Avg. Estimated": 2400000000},
    {"Hazard/Type": "Oil Pits", "Source": "Trail 2006", "Min Range": 500000, "Max Range": 1000000, "Median/Avg. Estimated": 750000},
]

df = pd.DataFrame(data)
print(df)

df['Type'] = df['Hazard/Type'].apply(lambda x: 'Collisions' if 'Collisions' in str(x) else x)
print(df)

# Clean/prepare numeric data (ensure NAs are handled)
df['Min Range'] = pd.to_numeric(df['Min Range'], errors='coerce')
df['Max Range'] = pd.to_numeric(df['Max Range'], errors='coerce')
df['Median/Avg. Estimated'] = pd.to_numeric(df['Median/Avg. Estimated'], errors='coerce')

# Filter only rows where all values are present
df_candle = df.dropna(subset=['Min Range', 'Max Range', 'Median/Avg. Estimated'])

# Set figure
fig, ax = plt.subplots(figsize=(10, 6))

# X positions for each hazard
x = range(len(df_candle))


# Set background colors
fig.patch.set_facecolor(color='#CDD3CE')      # Light gray for the figure
ax.set_facecolor('#F9F8F8')   

# Draw wicks and body
for i, (_, row) in enumerate(df_candle.iterrows()):
    # Wick: from min to max
    ax.plot([i, i], [row['Min Range'], row['Max Range']], color='#AA6DA3')

    # Body: a small box around the median value
    box_height = 0.02 * (df_candle['Max Range'].max())  # adjustable size
    ax.add_patch(plt.Rectangle((i - 0.2, row['Median/Avg. Estimated'] - box_height / 2), 0.4, box_height, color='#B118C8'))  # Median = _5

# Labels and styling
ax.set_xticks(list(x))
ax.set_xlabel("Hazard Source", color="#AA6DA3", size=10)
ax.set_xticklabels(df_candle['Hazard/Type'], color="#AA6DA3", size=7, rotation=45)
ax.set_ylabel("Number of Bird Deaths", color="#AA6DA3", size=10)
ax.tick_params(axis='y', labelcolor="#AA6DA3", labelsize=7)

ax.set_title("Bird Mortality Estimates by Hazard Type (As of 2017)", color="#AA6DA3", size=15)
plt.tight_layout()
plt.show()