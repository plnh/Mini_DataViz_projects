import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from pypalettes import load_cmap, get_hex
from highlight_text import fig_text


file_path = 'Spotify Global Chart 2024_1.xlsx'

xls = pd.ExcelFile(file_path)
print("Available sheets:", xls.sheet_names)

sheet_name = "Spotify Global Chart 2024"
df = pd.read_excel(xls, sheet_name=sheet_name)

# Display basic info about the DataFrame
print("\nDataFrame Info:")
df.info()

print("\nColumn Names:")
print(df.columns.tolist())

# Group by artist and track, and get the max weeks_on_chart for each combination
df_summary = df.groupby(['Type','artist_names', 'track_name'])['weeks_on_chart'].max().reset_index()

df_count = df_summary.groupby(['Type','weeks_on_chart'])['track_name'].count().reset_index()
df_count = df_count.rename(columns={'track_name': 'track_count', 'Type': 'Do I Know This Artist?'})
# Show the result
print(df_count.head())


palette = get_hex('AndyWarhol_2', keep_first_n=5)

fig, ax = plt.subplots(figsize=(10,10))

fig.patch.set_facecolor('#f7f3f0')  # Whole figure background
ax.set_facecolor('#fefcfb')         # Plot (axes) background

sns.kdeplot(data=df_count, x="weeks_on_chart", hue="Do I Know This Artist?",  fill=True, common_norm=False, alpha=0.4, palette=palette, ax=ax)

text = 'Time on the Charts by Familiarity'
fig_text(
    s=text,
    x=.1, y=0.95,ha='left',
    fontsize=25,
    color='#2F191BFF'
)



plt.show()