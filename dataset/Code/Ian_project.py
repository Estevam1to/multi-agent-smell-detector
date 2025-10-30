# I used Github Copilot for some code and text suggestions in the assignment
# I also used some online tutorials on use of libraries as guidance for the assignment. 
# In the analysis for the specific dataset chosen not all the functions of pandas or python are used, but to demonstrate the 
# knowledge examples are shown of how to use them on the dataset. 
# I used visual studio code and related extensions to produce the visualizations and coding. 

# 1.  Real World Scenario:

# I am using a real world dataset regarding the international football results from 1872 to 2021. The
# dataset This dataset includes 42,899 results of international football matches starting from the very first official match in 1972 up to 2019. 
# It is taken from the Kaggle website : https://www.kaggle.com/martj42/international-football-results-from-1872-to-2017
# More details about the dataset can be found on the website.

#2   Importing data from Web (Web Scraping)

# The requests module allows us to send HTTP requests using Python.
from email.errors import FirstHeaderLineIsContinuationDefect
import requests   

# Beautiful Soup is a Python library for pulling data out of HTML and XML files. 
from bs4 import BeautifulSoup

# We use the requests library to download the webpage and the Beautiful Soup library to parse the HTML.

# In case this I am using the accweather website to access the weather inforation on Dublin. 
page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.YfVTuerP1PY")

# When we go to the website and click on inspect in browser, it shows us the HTML of page and we are interested
# in div tags on the page. 

soup = BeautifulSoup(page.content, 'html.parser')

# Print the Tile without html tags
print(soup.title.text)

# Print all the links on this page along with its attributes such as href, text, etc.
#for link in soup.find_all("a"):
#    print("Inner Text: {}".format(link.text))
#    print("Title: {}".format(link.get("title")))
#    print("href: {}".format(link.get("href")))

#2  Import a CSV file into a Pandas DataFrame

# I am using the above mentioned football results to import in Pandas dataframe.

ind= 0; 
max=10

import pandas as pd
import os
import sys

abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)


df = pd.read_csv('results.csv' , sep = ',')
print(df.head())

# 3 Analyzing the data

# 3.1  Sorting the data by names of Countries in Alphabetical order. 
df.sort_values(by=['country'], inplace=True)
print(df.head())

#3.2  Let's do the Grouping of data by type of tournament.
g_by_tour = df.groupby('tournament')
  
print("*********************************")
print("Count matches by tournament:")
print("*********************************")
print(g_by_tour.get_group('Friendly').count())

#3.3 Indexing
# If we are only interested in two columns of dataframe we can index them as follows: 
print(df[['home_team', 'country', 'neutral']].head())

#3.4 Replace missing values or duplicates

# Checking for any missing values in the dataframe.
print("\n***********************************************************************************")
print("Checking for missing values in the dataframe")
print(df.isnull().values.any())

# The CSV file we downloaded has 'NA' at places where there is no data, pandas automatically converts it to NaN when reading.

print("\n***********************************************************************************")
print("In our there are missing values as well, but we are only interested in the home_score and away_score columns NAN values")
print("\n***********************************************************************************")

print("Home score missing value Row index. In python index starts with 0 and not 1")
import numpy as np
index = df['home_score'].index[df['home_score'].apply(np.isnan)]
print(index)

print("Away score missing value Row index. In python index starts with 0 and not 1")

index = df['away_score'].index[df['away_score'].apply(np.isnan)]
print(index)

# replacing missing values in score
# I have decide to fill missing values of home and away score with zero.

# Apply the function
df['home_score'] = df['home_score'].fillna(0)
df['away_score'] = df['away_score'].fillna(0)

# If wanted we can use the following to do the replacment using mean or median.

#df['away_score'] = df['away_score'].fillna(data['away_score'].mean())
  
# replacing missing values in score column
# with median of that column
#df['away_score'] = df['away_score'].fillna(df['away_score'].median())

#3.4   Slicing, Loc and iloc 
print("***********************************************************************************")
print("Rows where home team was Scotland and their score was greater then away team score:")
print("***********************************************************************************")
print(df.loc[(df.home_team == 'Scotland') & (df.home_score > df.away_score )])

#3.5  Looping  
print("\nIterating over rows using index attribute of Pandas dataframe:\n")
  
for index in df.index:
    if ind <= max: 
        print(df['tournament'][index], df['neutral'][index]) 
        ind=ind+1

ind=0;

#3.6 :iterrows
# It is build in pandas function providing more flexiblity then tradtional looping.

# iterate through each row and select 
# 'date' and 'tournament' column respectively.
print("\nIterating over rows using iterrows of Pandas dataframe:\n")
for index, row in df.iterrows():
    if ind <= max: 
        print (row["date"], row["tournament"])
        ind=ind+1
ind=0;

#3.7 Merge DataFrames
# In the dataset I have chosen it is single CSV file which is loaded in a dataframe. So there is no need to merge. 

#4. Define a custom function to create reusable code. 

# The function will take a dataframe and a team value and print the average, min, max for that team

def score_stats(df, team):
    print("\n***********************************************************************************")
    print(f"The home_score mean   of  {team} is {df.loc[df.home_team == team, 'home_score'].mean()} ")
    print(f"The home_score median of  {team} is {df.loc[df.home_team == team, 'home_score'].median()} ")
    print(f"The home_score min    of  {team} is {df.loc[df.home_team == team, 'home_score'].min()}  ")
    print(f"The home_score max    of  {team} is {df.loc[df.home_team == team, 'home_score'].max()}  ")
    print(f"The away_score mean   of  {team} is {df.loc[df.home_team == team, 'away_score'].mean()} ")
    print(f"The away_score median of  {team} is {df.loc[df.home_team == team, 'away_score'].median()} ")
    print(f"The away_score min    of  {team} is {df.loc[df.home_team == team, 'away_score'].min()}  ")
    print(f"The away_score max    of  {team} is {df.loc[df.home_team == team, 'away_score'].max()}  ")
    print("\n***********************************************************************************")


#Use of function
score_stats(df, 'Scotland')
score_stats(df, 'England')

# Numpy 
# Numpy is a Python package for scientific computing. It provides a high-performance multidimensional array object, and tools for working with these arrays.
# Pandas is already build on top of Numpy.  So calculations I did above in pandas, similar applies to numpy. 


# Dictionary or Lists 
# When we calculate the mode of data values in frame it is returned as a list by the function if there are multiple values. 
 
# Following I am iterating over the list and printing the mode values for selected options. 
k=1; 
for i in df.loc[df.home_team == 'Scotland', 'home_score'].mode():
    print(f"The {k} mode value for Scotland is  {i} ")
    k=k+1
k=1; 
for i in df.loc[df.home_team == 'England', 'home_score'].mode():
    print(f"The {k} mode value for England is  {i} ")
    k=k+1


# 5. Visualization

# %%
# importing the required library
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('results.csv' , sep = ',')

away_teams = df['away_team'].unique()
home_teams = df['home_team'].unique()

print("\n***********************************************************************************")
print(f"There are  {len(away_teams)}  unqiue away teams in the database and are listed below")
print(away_teams)

print("\n***********************************************************************************")
print(f"There are  {len(home_teams)}  unqiue home  teams in the database")
print(home_teams)
print("\n***********************************************************************************")

# Since there are lot of teams in the dataset, I am just 
# using subset of data to make the visualization more readable.

subset_teams = df[(df['home_team'] == 'Scotland') | (df['home_team'] == 'England') | (df['home_team'] == 'Wales') | (df['home_team'] == 'Northern Ireland')]


sns.barplot(x = 'home_team',
           y = 'home_score',
           data = subset_teams)
 
# Show the plot
plt.show()

# %%
# importing the required library
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('results.csv' , sep = ',')
subset_teams = df[(df['away_team'] == 'Scotland') | (df['away_team'] == 'England') | (df['away_team'] == 'Wales') | (df['away_team'] == 'Northern Ireland')]


# away_team vs away_score plot
sns.barplot(x = 'away_team',
            y = 'away_score',
            data = subset_teams)
 
# Show the plot
plt.show()


def win_loss_ratio (df, teams):

    played =[]
    won =[]
    lost =[]

    for i in teams: 
        num_play=len(df[(df['home_team'] == i ) | (df['away_team'] == i)])
        played.append(num_play)
        won_count=0;
        won_count = won_count +len(df[(df['home_team'] == i ) & (df['home_score'] > df['away_score'])])
        won_count = won_count +len(df[(df['away_team'] == i ) & (df['home_score'] < df['away_score'])])
        won.append(won_count)
        lost.append(num_play-won_count)

        win_loss_ratio  = {"Played": played,
                           "won": won,
                           "lost" :lost};

    df_sub_teams       = pd.DataFrame(data = win_loss_ratio);
    df_sub_teams.index = teams;
    df_sub_teams.plot.barh(rot=15, title="Win/Loss Ratio of selected teams");
    plt.show(block=True);

# Test the function
teams = ['Scotland', 'England', 'Wales', 'Northern Ireland'];
win_loss_ratio(df, teams)
teams = ['Belgium', 'France', 'Netherlands', 'Hungary'];
win_loss_ratio(df, teams)


# %%
# importing the required library
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


tour_nament = df['tournament'].unique()

print("\n***********************************************************************************")
print(f"There are  {len(tour_nament)} tournament in the database and are listed below")
print(tour_nament)

print("\n***********************************************************************************")
print("Match count table by Tournament")
print("\n***********************************************************************************")


match_count =[]

for i in tour_nament: 
    match_count.append(len(df[df['tournament'] == i]))

data_tuples = list(zip(tour_nament,match_count))

match_count_df = pd.DataFrame(data_tuples, columns=['tournament','Mach_count'])
match_count_df= match_count_df.sort_values('Mach_count', ascending=False)
print(match_count_df)

# From above match count print it is clear that most number of matches are played friendly tournaments

# Number of teams (just using home_teams names)
home_teams = df['home_team'].unique()
friendly_count =[]

for i in home_teams :
    friendly_count.append(len(df[ (df['home_team'] == i)| (df['away_team'] == i) & (df['tournament'] == 'Friendly')]))

data_tuples_1 = list(zip(home_teams,friendly_count))

friendly_count_df = pd.DataFrame(data_tuples_1, columns=['team','Friendly_Match_count'])
friendly_count_df=friendly_count_df.sort_values('Friendly_Match_count',  ascending=False)
print(friendly_count_df)
