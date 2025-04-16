import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.style.use('fivethirtyeight')


file_path = "mental health Dataset.csv"
df = pd.read_csv(file_path)
print(df.columns.tolist())

print(df.info())

depression_cols = [col for col in df.columns if "Depression" in col]
burnoout_cols = [col for col in df.columns if "Burnout" in col]
anxiety_cols = [col for col in df.columns if "Anexity" in col]


for col in depression_cols + burnoout_cols + anxiety_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

for col in depression_cols:
    df['Total_Depresion'] = df[depression_cols].sum(axis=1) 
for col in burnoout_cols:
    df['Total_Burnout'] = df[burnoout_cols].sum(axis=1)
for col in anxiety_cols:
    df['Total_Anxiety'] = df[anxiety_cols].sum(axis=1)    


sex_name = df['Sex'].unique()
sex_labels = {sex_name[0] : "Female", sex_name[1] : "Male"}
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
print(colors)  
#sns.histplot(df['Total_Anxiety'], bins=10, kde= False, label= "Anxity")   
#sns.histplot(df['Total_Depresion'], bins=10, kde= False, label="Depresion")

for i, sex in enumerate(sex_name):
    ax = df[df['Sex']==sex]['Total_Burnout'].hist(figsize=(8,4)
                                            ,label = sex_labels[sex]        
                                            ,edgecolor = 'gray'
                                            ,bins=5
                                            ,color=colors[i]  
                                            ,alpha=0.7
                                            )

csfont = {'fontname':'Arial'}
hfont = {'fontname':'Noto Sans'}


plt.legend(title='Sex')
plt.title('Perceived Burnout among Iranian Healthcare Workers during COVID', **csfont)
plt.xlabel('Total Score')
plt.ylabel('Hospital Nurses')
plt.tight_layout()
plt.show()