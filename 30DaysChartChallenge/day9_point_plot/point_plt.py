import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import seaborn as sns
from highlight_text import fig_text

file_path = "WeCount-Report-8-tables.xlsx"

xls = pd.ExcelFile(file_path)
print("Available sheets:", xls.sheet_names)

sheet_name = "T1 values"
df = pd.read_excel(xls, sheet_name=sheet_name)

# Display basic info about the DataFrame
print("\nDataFrame Info:")
df.info()

print("\nColumn Names:")
print(df.columns.tolist())

# Convert Abortion col to number and check if there's null/invalid value
df['Abortions'] = pd.to_numeric(df["Abortions"], errors='coerce')
print("No data: ")
print(df[df['Abortions'].isna()])

#Check if all the state is valid
print("State: ")
print(df['State'].unique())

#Remove invalid states
invalid_state = {'All US state totals', 'Banned','Gestational limit, 6 weeks', 'Permitted','Abortions provided under shield laws to states with telehealth restrictions', 'Abortions provided under shield laws to states with total bans and 6-week bans'}
df = df[~df['State'].isin(invalid_state)]


#Check if missing record of particular month and state
df['Month'] = pd.to_datetime(df['Month'], errors = 'coerce')
min_date = df['Month'].min()
max_date = df['Month'].max()


print(F"Range {min_date.date()} to {max_date.date()}")

existing_month = df['Month'].dropna().unique()
expected_month = pd.period_range(start = min_date, end= max_date, freq='M')

missing_month = expected_month.difference(existing_month)
print("Missing months:")
print(missing_month)

#The code below is to see missing data per month and per state
#pivot = df.pivot_table(index='State', columns = 'Month', aggfunc='sum', fill_value=0)
#cmap = ListedColormap(['black', 'green'])
#bounds = [0, 1]
#norm = BoundaryNorm(bounds, cmap.N)
#                    
#plt.figure(figsize=(14,10))
#sns.heatmap(pivot, cmap=cmap , norm=norm , cbar_kws={'label': 'Sum of Abortions'})
#plt.title("Abortions Data by State and Month")
#plt.xlabel("Month")
#plt.ylabel("State")
#plt.xticks(rotation=45, ha="right")
#plt.tight_layout()
#plt.show()

#From the heatmap, there's missing data from middle of 2022 to 2023. For illustration purpose, I use average per month for available datap point
df['Year'] = df['Month'].dt.year
state_sum = df.groupby(['State', 'Year']).agg(
            Total_abortions = ('Abortions', 'sum'),
            Availble_month= ('Abortions', 'count')
)

state_sum["Avg_Abortions_PerMonth"] = (state_sum["Total_abortions"] / state_sum["Availble_month"]).round(1)
state_sum = state_sum.reset_index()

state = state_sum['State'].unique()
rate_2022 = state_sum[ state_sum['Year']== 2022]['Avg_Abortions_PerMonth']
rate_2024 = state_sum[ state_sum['Year']== 2024]['Avg_Abortions_PerMonth']


#plot
fig, ax = plt.subplots(figsize=(10, 10), dpi=200)

colors = ['#9fbded', '#81ebb9']

plt.scatter(rate_2022, state, color=colors[0], s=20, label='2022')
plt.scatter(rate_2024, state, color=colors[1], s=20, label= '2024')

for i in range(len(state)):
    arrow_color = '#81ebb9' if rate_2024.iloc[i] > rate_2022.iloc[i]  else '#7e8694'
    plt.annotate(
        ''
        ,xy=(rate_2024.iloc[i], state[i])
        ,xytext=(rate_2022.iloc[i], state[i])
        , arrowprops=dict(arrowstyle='-|>', color=arrow_color , lw=1.5)
        )
    
# Titles and labels
text = 'Did U.S. Abortion Rate Decreased after the abortion ban?\n<Data from ><2022>< to ><2024>< disagrees.>'
fig_text(
    s=text,
    x=.1, y=0.98,ha='left',
    fontsize=14,
    color='black',
    highlight_textprops=[{"color": 'grey', 'fontsize': '9'},
                         {"color": colors[0],  'fontsize': '10'},
                         {"color": 'grey', 'fontsize': '9'},
                         {"color": colors[1],  'fontsize': '10'},
                         {"color": 'grey', 'fontsize': '9'}]
)

plt.xlabel("Average Abortions per month", fontsize=6,  fontstyle='italic', family='monospace')
plt.ylabel("State", fontsize=6, fontstyle='italic', family='monospace')

# Get current axis
ax = plt.gca()

# Set font for tick labels
ax.set_xticklabels(ax.get_xticklabels(), fontdict={'fontsize': 4, 'family': 'monospace'})
ax.set_yticklabels(ax.get_yticklabels(), fontdict={'fontsize': 4, 'family': 'monospace'})

# Layout and show
plt.tight_layout()
plt.show()