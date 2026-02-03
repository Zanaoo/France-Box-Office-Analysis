# Importing the libraries
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO  

# Importing the data from the webpage into a DataFrame
url = 'https://en.wikipedia.org/wiki/List_of_2018_box_office_number-one_films_in_France'

#  'User-Agent' header so Wikipedia sees us as a browser, not a bot
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# request using the headers
req = requests.get(url, headers=headers)

# Wrap the HTML text in StringIO 
data = pd.read_html(StringIO(req.text))

# Select the first table found
df = data[1]
df.head()
print(df.head())
df.info()
#removing unnecessary characters from the Gross column
df['Gross']=df['Gross'].str.replace(r"US\$","").str.replace(r",","")
df['Gross'].head(5)

#changing the data type of the Date column to extract its components
df['Date']=df['Date'].astype('datetime64[ns]')
#creating a new column for the month
df['Month']=pd.DatetimeIndex(df['Date']).month

# dropping the unnecessary columns
df.drop(['#', 'Notes'], axis=1, inplace=True, errors='ignore')

# CLEANING: Make sure 'Gross' is a number (removes US$ and commas)
df['Gross'] = df['Gross'].str.replace(r'[^\d.]', '', regex=True).astype(float)

# Sort and take top 5
df1 = df[['Film', 'Gross']].sort_values(by='Gross', ascending=False)

# Plotting the top 5 films by revenue
plt.figure(figsize=(10, 5))

# creating a bar plot
ax = sns.barplot(x='Film', y='Gross', data=df1.head(5))

# rotating the x axis labels
ax.set_xticklabels(labels=df1.head(5)['Film'], rotation=75)

# setting the title and labels
ax.set_title("Top 5 Films per revenue")
ax.set_ylabel("Gross revenue")

# Labelling the bars (Indented correctly)
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.1f'), 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', 
                xytext = (0, 9), 
                textcoords = 'offset points')

plt.tight_layout()
plt.show()