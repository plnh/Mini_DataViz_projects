import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use("fivethirtyeight")

# Parse XML
tree = ET.parse('export.xml') 
root = tree.getroot()
record_list = [x.attrib for x in root.iter('Record')]

record_data = pd.DataFrame(record_list)

# Convert date columns
for col in ['creationDate', 'startDate', 'endDate']:
    record_data[col] = pd.to_datetime(record_data[col])

# Convert value to numeric
record_data['value'] = pd.to_numeric(record_data['value'], errors='coerce').fillna(1.0)

# Clean type strings
record_data['type'] = record_data['type'].str.replace('HKQuantityTypeIdentifier', '', regex=False)
record_data['type'] = record_data['type'].str.replace('HKCategoryTypeIdentifier', '', regex=False)

# Filter for ActiveEnergyBurned
burn_data = record_data[record_data['type'] == 'ActiveEnergyBurned'].copy()
burn_data['date_only'] = burn_data['startDate'].dt.date
daily_sum = burn_data.groupby('date_only')['value'].sum().reset_index()
daily_sum['date_only'] = pd.to_datetime(daily_sum['date_only'])
daily_sum = daily_sum.sort_values('date_only')

# Fill missing dates
full_range = pd.date_range(start=daily_sum['date_only'].min(), end=daily_sum['date_only'].max())
daily_sum = daily_sum.set_index('date_only').reindex(full_range, fill_value=0).rename_axis('date_only').reset_index()

# Weekly average
daily_sum = daily_sum.set_index('date_only')
weekly_avg = daily_sum.resample('W').sum().reset_index()

# Normalize for color mapping
norm = plt.Normalize(weekly_avg['value'].min(), weekly_avg['value'].max())

from matplotlib.colors import LinearSegmentedColormap

# Define your custom color palette
custom_colors = [
   '#FBEFF3', # first color
   '#FFD131',
   '#F13030' # last color
]

cmap = LinearSegmentedColormap.from_list("custom_gradient", custom_colors)
colors = ['white' if v == 0 else cmap(norm(v)) for v in weekly_avg['value']]

# Plot
fig, ax = plt.subplots(figsize=(12, 3))
ax.bar(weekly_avg['date_only'], [1] * len(weekly_avg), color=colors, width=6)  # Width=6 for weekly blocks

ax.set_yticks([])
ax.set_ylabel('')
ax.set_xlabel('')
ax.set_title(
    'Calories in Color: A Striped Story of My  Habits',
    fontsize=16,         # size of the title
    fontweight='bold',   # optional: 'normal', 'bold', 'light'
    fontname='Courier New'  # any installed font; optional
)
# Colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
#fig.colorbar(sm, ax=ax)
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Calories Burned', fontsize=10, fontweight='light', fontname='Courier New')

plt.tight_layout()
plt.show()
