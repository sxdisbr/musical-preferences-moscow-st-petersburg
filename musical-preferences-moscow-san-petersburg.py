#!/usr/bin/env python
# coding: utf-8

# # Yandex Music

# Yandex Music is a musical app similar to Apple Music or Spotify.
# The goal of this study is to compare the musical preferences of two audiences in Moscow and San Petersburg.

# We are going to test three hypotheses:
# 
# The user's activity depends on the weekday, and in Moscow and St. Petersburg, there are differences.
#     
# In Moscow, on Monday morning people listen to some genres, and in St. Petersburg others. Similarly, on Friday evening, different genres are listened to depending on the city.
#     
# Moscow and St. Petersburg prefer different music genres. In Moscow, people prefer pop music, in St. Petersburg, Russian rap.

# ## Data Overview

# In[2]:


# import library
import pandas as pd


# In[3]:


# reading from the file
df = pd.read_csv(r'C:\Users\pinos\Desktop\yandex_music_project.csv')


# In[4]:


display(df.head(10))


# In[5]:


# info about the table
df.info()


# In[6]:


# cleaning up the variable's name
df = df.rename(columns={'  userID': 'user_id', 'Track': 'track', '  City  ': 'city', 'Day': 'day'})
display(df.head())


# In[8]:


# detecting missing values
display(df.isna().sum())


# In[9]:


# replacing missing values with 'unknown'
columns_to_replace = ['track', 'artist', 'genre']
for column in columns_to_replace:
    df[column] = df[column].fillna('unknown')


# In[10]:


# just checking
display(df.isna().sum())


# In[11]:


# duplicated values
print(df.duplicated().sum())


# In[12]:


# deleting duplicates values
df = df.drop_duplicates() 


# In[13]:


# just checking
print(df.duplicated().sum())


# In[14]:


# unique values in the column genres
df['genre'].sort_values().unique()


# In[15]:


# we are going to replace these hip, hop, hip-hop by hiphop.
# to do that we create a function:
def replace_wrong_values(wrong_values, correct_value): 
    for wrong_value in wrong_values: 
        df['genre'] = df['genre'].replace(wrong_value, correct_value) 

duplicates = ['hip', 'hop', 'hip-hop'] 
name = 'hiphop' 
replace_wrong_values(duplicates, name) 


# In[16]:


# just checking if everything is allright
df['genre'].sort_values().unique()


# ## Hypothesis testing

# ### User behavior comparison between cities

# The first hypothesis states that music preferences differ in Moscow and St. Petersburg. We will check this assumption based on the data about three days of the week: Monday, Wednesday, and Friday.

# In[17]:


# counting listenings in each city 
df.groupby('city')['genre'].count()


# In[18]:


# counting listenings for each day
df.groupby('day')['genre'].count()


# In[19]:


# we write a function that counts the listenings for a given day and city.
def number_tracks(day, city):
    track_list = df[(df['day'] == day)  &  (df['city'] == city)]
    track_list_count = track_list['user_id'].count()
    return track_list_count


# In[20]:


# calling the function
# number of listenings in Moscow on Monday.
number_tracks('Monday', 'Moscow')


# In[21]:


# number of listenings in St. Petersburg on Monday.
number_tracks('Monday', 'Saint-Petersburg')


# In[22]:


# number of listenings in Moscow on Wednesday.
number_tracks('Wednesday', 'Moscow')


# In[23]:


# number of listenings in St. Petersburg on Wednesday.
number_tracks('Wednesday', 'Saint-Petersburg')


# In[24]:


# number of listenings in Moscow on Friday.
number_tracks('Friday', 'Moscow') 


# In[25]:


# number of listenings in St. Petersburg on Friday.
number_tracks('Friday', 'Saint-Petersburg')


# In[27]:


# outcome table
info = pd.DataFrame(data=[['Moscow', 15740, 11056, 
15945], ['St. Petersburg', 5614, 7003, 5895]], columns=['city', 'monday', 'wednesday', 'friday'])
info


# The data shows the difference in user behavior: In Moscow, the peak of auditions falls on Monday and Friday, and on Wednesday there is a noticeable decline. In St. Petersburg, on the contrary, they listen to music more on Wednesdays. Activity on Monday and Friday is almost equally inferior to Wednesday here. So, the data speak in favor of the first hypothesis.
# 
# According to the second hypothesis, on Monday morning some genres prevail in Moscow and others in St. Petersburg. Similarly, on Friday evening, different genres prevail, depending on the city. Now, we are going to test that.

# In[28]:


# new variables
moscow_general = df[df['city'] == 'Moscow']
spb_general = df[df['city'] == 'Saint-Petersburg']


# In[29]:


# we create the function that check the second hypothesis
def genre_weekday(df, day, time1, time2):
    genre_df = df[(df['day'] == day) & (df['time'] > time1) & (df['time'] < time2)]
    genre_df_grouped = genre_df.groupby('genre')['genre'].count()
    genre_df_sorted = genre_df_grouped.sort_values(ascending=False)
    return genre_df_sorted[:10]


# In[30]:


# calling the function for Monday morning in Moscow
genre_weekday(moscow_general, 'Monday', '07:00', '11:00')


# In[31]:


# calling the function for Monday morning in St. Petersburg
genre_weekday(spb_general, 'Monday', '07:00', '11:00')


# In[32]:


# the same for Moscow on Friday evening
genre_weekday(moscow_general, 'Friday', '17:00', '23:00')


# In[33]:


# Petersburg on Friday evening
genre_weekday(spb_general, 'Friday', '17:00', '23:00')


# If we compare the top 10 genres on Monday morning, we can draw the following conclusions:
# 
# In Moscow and St. Petersburg, they listen to similar music. The only difference is that the “world” genre entered the Moscow rating, and jazz and classical music entered the St. Petersburg rating.
# 
# In Moscow, there were so many missing values that the value of 'unknown' took tenth place among the most popular genres. This means that the missing values occupy a significant share of the data and threaten the reliability of the study.
# 
# Friday night doesn't change that picture. Some genres rise a little higher, others go down, but overall the top 10 remains.

# ### Preferences by genre in Moscow and St. Petersburg

# Hypothesis: St. Petersburg is the capital of rap, music of this genre listens to there more often than in Moscow. And Moscow is a city of contrasts, in which, nevertheless, pop music prevails.

# In[36]:


# grouping and sorting genres in Moscow
moscow_grouping = moscow_general.groupby('genre')['genre'].count()
moscow_genres = moscow_grouping.sort_values(ascending=False)


# In[35]:


display(moscow_genres.head(10))


# In[37]:


# the same for St. Petersburg
spb_grouping = spb_general.groupby('genre')['genre'].count()
spb_genres = spb_grouping.sort_values(ascending=False)


# In[38]:


display(spb_genres.head(10))


# The hypothesis was partially confirmed:
# 
# Pop music is the most popular genre in Moscow, as the hypothesis suggested. Moreover, in the top 10 genres, there is a similar genre: Russian popular music.
# 
# Contrary to expectations, rap is equally popular in Moscow and St. Petersburg.

# ### Conclusions

# The day of the week has different effects on user activity in Moscow and St. Petersburg.
# The first hypothesis was fully confirmed.
# 
# Musical preferences don't change much during the week — whether it's Moscow or St. Petersburg. Small differences are noticeable at the beginning of the week, on Mondays:
# in Moscow, they listen to the music of the genre “world”,
# in St. Petersburg — jazz and classical.
# Thus, the second hypothesis was only partially confirmed. This result could have been different if not for the omissions in the data.
# 
# The tastes of users in Moscow and St. Petersburg have more in common than differences. Contrary to expectations, genre preferences in St. Petersburg resemble those in Moscow.
# The third hypothesis was not confirmed. If there are differences in preferences, they are invisible to the majority of users.
