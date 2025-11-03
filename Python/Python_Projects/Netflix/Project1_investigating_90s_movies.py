# Importing pandas and matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Read in the Netflix CSV as a DataFrame
netflix_df = pd.read_csv("netflix_data.csv")

#descriptive
netflix_df.head()
netflix_df.info()
netflix_df.tail()
netflix_df.dtypes
netflix_df.count()

#Create a table with all the 90s movies
movies = netflix_df[netflix_df['type'].str.lower().eq('movie')].copy() #create a new table with just movies (avoid TV shows)
movies_90s = movies[(movies['release_year'] >= 1990) & (movies['release_year'] < 2000)].copy()
movies_90s[['title', 'release_year', 'duration', 'genre']].head()

#Most frequent durantion of 90s movies
mode_vals = movies_90s['duration'].mode()
duration = int(movies_90s['duration'].value_counts().idxmax())
print(duration)

# Number of short action movies released in 90s
is_action = movies_90s['genre'].str.contains('Action', case=False, na=False)
is_short  = movies_90s['duration'] < 90
short_movie_count = int((is_action & is_short).sum())
print(short_movie_count)