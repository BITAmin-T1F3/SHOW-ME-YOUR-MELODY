import streamlit as st
import pandas as pd
import numpy as np
import re
from IPython.display import Image, display, HTML

if 'background_result' in st.session_state:
    background_result = st.session_state.background_result
else:
    st.write("No background result found. Please complete the previous step.")

if 'emotion_result' in st.session_state:
    emotion_result = st.session_state.emotion_result
else:
    st.write("No emotion result found. Please complete the previous step.")

if 'selected_genre' in st.session_state:
    selected_genre = st.session_state.selected_genre
else:
    st.write("No selected genre found. Please complete the previous step.")

# 1. playlist 배경, 감정 거르기
playlist = pd.read_csv('../final_playlist.csv')
playlist = playlist[playlist['배경'] == background_result] #배경으로 한 번 거르고

#face_emotion으로 다시 거르기
if emotion_result == 'Happy':
    playlist = playlist[((playlist['가사 감정'] == 'love') & (playlist['템포'] == '빠름')) |
                                (playlist['가사 감정'] == 'excited')]
elif emotion_result == 'Surprising':
    playlist = playlist[playlist['가사 감정'] == 'excited']
elif emotion_result == 'Sad':
    playlist = playlist[playlist['가사 감정'] == 'missing']
elif emotion_result == 'Neutral':
    playlist = playlist[(playlist['가사 감정'] == 'love') & (playlist['템포'] != '빠름')]


# 2. 장르 거르기
selected_rows = playlist[playlist['장르'].apply(lambda x: selected_genre in x.split(','))]

if not selected_rows.empty:
    # If there is more than one row with the selected genre, select 2 random rows with that genre
    selected_rows = selected_rows.sample(n=min(2, len(selected_rows)))

    # Select 1 random row from other genres, if available
    other_rows = playlist[~playlist['장르'].apply(lambda x: selected_genre in x.split(','))]
    if not other_rows.empty:
        other_rows = other_rows.sample(n=1)
    else:
        # If no other rows are available, handle this case accordingly (e.g., select a default row)
        other_rows = pd.DataFrame(columns=playlist.columns)  # Empty DataFrame

    # Concatenate the selected rows
    final_selection = pd.concat([selected_rows, other_rows])
else:
    # If the selected genre is not present or the playlist has 3 or fewer rows, recommend the entire playlist
    if len(playlist) <= 3:
        final_selection = playlist.copy()
    else:
        # If the playlist has more than 3 rows, select 3 random rows
        final_selection = playlist.sample(n=3, replace=True)  # Use replace=True for sampling with replacement

# Create a new DataFrame with only '가수', '노래 제목', and '앨범사진' columns
display_df = final_selection[['가수', '노래 제목', '앨범사진', '장르']].copy()

# Extract URLs from HTML tags in the '앨범사진' column
display_df['앨범사진'] = display_df['앨범사진'].apply(lambda x: re.search('src=\"(.*?)\"', x).group(1) if (pd.notnull(x) and re.search('src=\"(.*?)\"', x) is not None) else x)

# Display the DataFrame with album images
if not final_selection.empty:
    for idx, row in display_df.iterrows():
        st.markdown(f"**{row['가수']}** - **{row['노래 제목']}** (장르 -{row['장르']})")

        album_image_url = row['앨범사진']
        if album_image_url:
            st.image(album_image_url)
        else:
            st.write("No album image available.")

else:
    st.write("No songs found based on the selected criteria.")