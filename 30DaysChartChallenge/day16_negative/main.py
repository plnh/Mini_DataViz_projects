# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
from highlight_text import fig_text
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import numpy as np
plt.style.use('fivethirtyeight')

# Data
data = {
    "Period": [2014, 2016, 2018,  2020, 2021, 2022, 2023, 2024],
    "Smoking": [25.7, 24.1,  22.4,  20.2, 20.6, 18.9, 19.0, 18.2],
    "Alcohol consumption": [9.9, 8.8,  8.2,  6.9, 7.3, 6.5, 6.7, 5.5],
    "Excess body weight": [49.4, 49.2,  50.2,  50.0, 50.0, 50.2, 50.0, 50.4]
}
df = pd.DataFrame(data)

# Radar setup
categories = list(df.columns[1:])
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
selected_years = data["Period"]

cmap = cm.get_cmap('Blues')
colors = cmap(np.linspace(0.3, 0.9, len(selected_years)))

# Create one figure with two subplots (radar chart and color bar)
fig = plt.figure(figsize=(10, 12))
gs = fig.add_gridspec(2, 1, height_ratios=[8, 1])

# --- Radar chart (top)
radar_ax = fig.add_subplot(gs[0], polar=True)
radar_ax.set_theta_offset(pi / 2)
radar_ax.set_theta_direction(-1)
radar_ax.set_rlabel_position(0)
radar_ax.set_ylim(0, 60)
radar_ax.set_xticks(angles[:-1])
radar_ax.set_xticklabels(categories, color ="grey", size=7)
radar_ax.set_yticks([10, 20, 30, 40, 50])
radar_ax.set_yticklabels(["10", "20", "30", "40", "50"], color="grey", size=7)

# Plot each year with matching color
for idx, year in enumerate(selected_years):
    row = df[df["Period"] == year].iloc[0]
    values = row.drop("Period").values.flatten().tolist()
    values += values[:1]
    radar_ax.plot(angles, values, linewidth=2, linestyle='solid', label=str(year), color=colors[idx])
    radar_ax.fill(angles, values, color=colors[idx], alpha=0.1)


# --- Color gradient bar (bottom)

color_ax = fig.add_subplot(gs[1])
pos = color_ax.get_position()

# Set a new position with reduced width
color_ax.set_position([pos.x0 + 0.2, pos.y0, pos.width * 0.6, pos.height])

color_ax.set_xlim(0, len(selected_years))
color_ax.set_ylim(0, 1)
color_ax.axis('off')

for idx, year in enumerate(selected_years):
    rect = mpatches.Rectangle((idx, 0), 1, 0.5, color=colors[idx])
    color_ax.add_patch(rect)
    color_ax.text(idx + 0.5, 0.25, str(year), ha='center', va='center', fontsize=7,
                  color='white')



plt.subplots_adjust(

    top=0.7,
    bottom=0.1,
    wspace=0.5,
    hspace=0.5
)

fig_text(
    s='Fewer people in <the Netherlands> are smoking and drinking since 2014,\n'
    'but obesity levels haven’t changed.',
    x=.1, y=0.95,ha='left',
    fontsize=18,
    color='#255973',
    highlight_textprops=[
        {"color": "#FF9B00", "fontsize": 18}
        ]
)

plt.show()
