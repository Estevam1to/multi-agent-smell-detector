#this code was written by github copilot, I just wrote the comments.

#webscraper for the website github.com.
#gather information about the user: surtarso.
#make a graph with public repositories and languages.

#import libraries
import requests
import json
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import seaborn as sns


#scrape the data from the website
url = 'https://api.github.com/users/surtarso/repos'
r = requests.get(url)
data = r.json()

#create a dataframe with the data
df = pd.DataFrame(data)

#create a pie graph with the languages used in the repositories
sns.set(style="whitegrid")
sns.countplot(x="language", data=df)
plt.show()

