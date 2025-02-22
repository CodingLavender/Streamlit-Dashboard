import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv('./low_popularity_spotify_data.csv')


st.header('Welcome to explore Low Popularity Spotify dataframe!')

st.write('Here is the whole dataset (Well .head() of it..). Pretty janky looking, eh? ')
st.dataframe(df)

st.divider()
st.header("Let's turn it in to many different plots now!")

st.title('Pie plot')
st.write('Biggest playlists and how big they are!')

playlists = df['playlist_name'].value_counts()
total = playlists.sum()
threshold = 0.027 * total

large_playlists = playlists[playlists >= threshold]
small_playlists = playlists[playlists <= threshold]

if not small_playlists.empty:
    large_playlists['Other'] = small_playlists.sum()


def autopct_format(pct, all_values):
    absolute = int(round(pct / 100. * all_values.sum()))
    return f'{absolute} songs\n({pct:.1f}%)'

fig_pie, ax_pie = plt.subplots()

ax_pie.pie(
    large_playlists, 
    labels=large_playlists.index, 
    autopct=lambda pct: autopct_format(pct, large_playlists),
    colors=plt.cm.Paired.colors, 
    startangle=90,
    textprops={'fontsize': 6},
    wedgeprops={'edgecolor': 'black', 'linewidth': 0.5}, 
    pctdistance=0.8
    )

st.pyplot(fig_pie)
st.write("Don't blame me for the plot looking like that, it would be too cramped!")

st.divider()

st.title('Scatter plot')
st.write('The Louder the Song, the More Danceable It Is')

fig_scatter, ax_scatter = plt.subplots()
ax_scatter.scatter(df['loudness'], df['danceability'], color='blue', marker='o')
ax_scatter.set_xlabel('Loudness of a song')
ax_scatter.set_ylabel('Danceability of a song')
ax_scatter.set_title('Scatter Plot about loudness and danceability of songs')

st.pyplot(fig_scatter)

st.divider()

st.title('Bar chart')

fig_bar, ax_bar = plt.subplots()

genre_distribution = df['playlist_genre'].value_counts()
ax_bar.bar(genre_distribution.index, genre_distribution.values)

ax_bar.set_xlabel('Playlist Genre')
ax_bar.set_ylabel('Number of Songs')
ax_bar.set_title("Genre Distribution in Playlists")
ax_bar.tick_params(axis='x', rotation=90, labelsize=6)


st.pyplot(fig_bar)
st.write('Again, the crampness won and now it looks like that.')
st.divider()

fig_bar2, ax_bar2 = plt.subplots()

df['track_album_release_date'] = df['track_album_release_date'].apply(
    lambda x: f'{x}-01-01' if len(x) == 4 else x
)

df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], errors='coerce')
df['year'] = df['track_album_release_date'].dt.year

album_count = df['year'].value_counts().sort_index()

ax_bar2.bar(album_count.index, album_count.values)
ax_bar2.set_xlabel('Year')
ax_bar2.set_ylabel('Number of Albums Released')
ax_bar2.set_title('Number of Albums Released Each Year')


ax_bar2.tick_params(axis='x')
st.title('Another bar chart!')
st.write('But this time it tells us how many albums were released each year!')
st.pyplot(fig_bar2)

st.divider()

st.write("And here's for you for reaching the end.")
st.button(label='Reward', on_click=st.balloons)