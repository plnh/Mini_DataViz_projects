import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from highlight_text import fig_text, ax_text

plt.style.use('Solarize_Light2')


file_path = "KIDB.csv"
df = pd.read_csv(file_path)

#df['Indicator'] = df['Indicator'].str.strip()

df =df[['Indicator', 'Economy', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']]
df_long = pd.melt(df, id_vars=['Indicator','Economy'], var_name='Year', value_name='Value')
df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')
df_long = df_long.dropna()

df_pivot = pd.pivot(data=df_long,index=['Economy', 'Year'], columns='Indicator', values='Value').reset_index()

years = ['2012', '2015', '2019', '2022'] #df_pivot['Year'].unique()


fig, axes = plt.subplots(2, 2,figsize=(2 * 2, 3 * 2))
axes = axes.flatten()  

for idx, year in enumerate(years):
    ax = axes[idx]
    sns.scatterplot(data= df_pivot[df_pivot['Year'] == year]
                    , x='Government Expenditure (% of GDP)'
                    , y='Internet Users (per 100 People)'
                    , ax = ax
    )
    ax.set_title(f"Year {year}", fontweight='medium', color = 'gray', fontsize='10', horizontalalignment='center')
    ax.set_xlabel('Government Expenditure (GDP)', fontweight='medium', color = 'gray', fontsize='6', horizontalalignment='center')
    ax.set_ylabel('Internet Users (per 100 People)', fontweight='medium', color = 'gray', fontsize='6', horizontalalignment='center')
    ax.tick_params(axis='x', color = 'gray', labelsize=5)
    ax.tick_params(axis='y', color='gray', labelsize=5)

# Titles and labels
fig_text(
    s='                      Government Expenditure and Internet Usage in Asia\n'
      '<The chart below compares internet usage with government expenditure (% of GDP). Each dot represents a country.>',
    x=0.5, y=0.97,
    ha='center',
    fontsize=15,
    color='#3f4245',
    highlight_textprops=[
        {"color": "grey", "fontsize": 10}
        ]
)


plt.subplots_adjust(
    left=0.05,
    right=0.95,
    top=0.8,
    bottom=0.1,
    wspace=0.5,
    hspace=0.5
)
plt.show()