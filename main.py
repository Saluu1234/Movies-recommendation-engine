import streamlit as st
import pandas as pd

# dataset path

PATH_DATASET = 'rotten_tomatoes_top_movies_2019-01-15.csv'

# import data
df = pd.read_csv(PATH_DATASET)

# get initial df columns
list_df_raw_columns = list(df.columns)

# get list of unique genres
list_genres = [i.split('|') for i in df['Genres'].unique()]
list_genres = [i for sub_genres in list_genres for i in sub_genres]
list_genres = list(dict.fromkeys(list_genres))

# clean df
df['Genres'] = df['Genres'].str.replace('|', ', ')
for genre in list_genres:
    df[genre] = [int(genre in x) for x in df['Genres']]

# set title & caption
st.title('Movies Reccomendation')
st.write('Filter Movies Reccomendation Data')

# create checkboxes for each genre
st.sidebar.title('Select Genres')
list_checkbox = [st.sidebar.checkbox(genre) for genre in list_genres]
list_true = [int(i) for i in list_checkbox]
list_genres_checked = [list_genres[i] for i in range(len(list_genres)) if list_true[i] == 1]

# filter df by checkbox selection
df_filtered = pd.DataFrame()
list_df_genre = [df.loc[df[genre] == 1] for genre in list_genres_checked]
for df_genre in list_df_genre:
    df_filtered = pd.concat([df_filtered, df_genre])
if len(df_filtered) > 0:
    df_filtered.columns = df.columns
    df_filtered = df_filtered[list_df_raw_columns]
    df_filtered = df_filtered.drop_duplicates()

# filter by top 10 rank
st.sidebar.title('Filter by Top 10 Rank')
checkbox_top_10_rank = st.sidebar.checkbox('Top 10 Rank')
if checkbox_top_10_rank == True and len(df_filtered) > 0:
    df_filtered = df_filtered.loc[df_filtered['Rank'] <= 10]

# filter by top 10
st.sidebar.title('Filter by Top 10 Results')
checkbox_top_10 = st.sidebar.checkbox('Top 10 Results')
if checkbox_top_10 == True and len(df_filtered) > 0:
    df_filtered = df_filtered.sort_values('Rank').head(10)

# display df
st.dataframe(data=df_filtered)
