import pandas as pd
from plotnine import *
from mizani.palettes import brewer_pal

# Load and clean data
df = pd.read_csv("english_monarchs_marriages_df.csv")
df['king_age'] = pd.to_numeric(df['king_age'], errors='coerce')
df['consort_age'] = pd.to_numeric(df['consort_age'], errors='coerce')
df['year_of_marriage'] = pd.to_numeric(df['year_of_marriage'], errors='coerce')
df = df.dropna(subset=['year_of_marriage', 'king_age', 'consort_age'])

df_long = pd.melt(df, id_vars='year_of_marriage', value_vars=['king_age', 'consort_age'],
                  var_name='who', value_name='age')

# Rename for nicer labels
df_long['who'] = df_long['who'].map({
    'king_age': 'King Age',
    'consort_age': 'Consort Age'
})

# Get palette
palette_fn = brewer_pal(type='qual', palette='Set2')
colors = palette_fn(2)

# Build plot
plot = (
    ggplot(df_long) +
    geom_point(aes(x='year_of_marriage', y='age', color='who'), size=3) +
    geom_smooth(aes(x='year_of_marriage', y='age', color='who'), method='loess', span=0.5, se=True) +
    scale_color_manual(values=colors) +
    scale_fill_manual(values=colors) +
    theme_light() +
    labs(
        title="English Monarchs and Age of Marriage",
        color="Legend",
        x="Year of Marriage",
        y="Age"
    )
)

plot.show()
