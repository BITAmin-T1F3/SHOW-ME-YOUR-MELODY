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
display_df = final_selection[['가수', '노래 제목', '앨범사진', '장르', 'first video link']].copy()

# Extract URLs from HTML tags in the '앨범사진' column
display_df['앨범사진'] = display_df['앨범사진'].apply(lambda x: re.search('src=\"(.*?)\"', x).group(1) if (pd.notnull(x) and re.search('src=\"(.*?)\"', x) is not None) else x)


st.markdown("""
    <style>
        .title-style {
            font-size: 20px;
        }
        .artist-style {
            font-size: 20px;
        }
        .genre-style {
            font-size: 15px;
        }
        /* Targeting Streamlit's primary buttons */
        button.stButton>button {
            border: 1px solid #f0f0f0;
            color: black; /* Adjust text color as needed */
            background-color: #f0f0f0;
        }
        /* Adjust hover state as well */
        button.stButton>button:hover {
            border: 1px solid #e6e6e6;
            background-color: #e6e6e6;
        }
    </style>
    """, unsafe_allow_html=True)


if not final_selection.empty:

    st.markdown("""
        <h2 style='text-align: center;'>추천 결과 🎧😝</h2>
        <div style='margin:auto; margin-bottom: 20px; width: 50%; border-bottom: 2px solid #f0f0f0;'></div>
    """, unsafe_allow_html=True)

    for idx, row in display_df.iterrows():
        col1, col2 = st.columns([1, 3])

        with col1:
            album_image_url = row['앨범사진']
            if album_image_url:
                st.image(album_image_url, use_column_width=True)
            else:
                st.write("No album image available.")

        # Displaying song title, artist, and genre in the second column
        col2.markdown(f"<span class='title-style'>**Title:** **{row['노래 제목']}**</span>", unsafe_allow_html=True)
        col2.markdown(f"<span class='artist-style'>**Artist:** **{row['가수']}**</span>", unsafe_allow_html=True)
        col2.markdown(f"<span class='genre-style'>**Genre:** **{row['장르']}**</span>", unsafe_allow_html=True)

        # Buttons for liking or disliking the recommendation
        like_button, dislike_button = col2.columns([1, 4])
        if like_button.button('좋아요 👍', key=f"like_{idx}"):
            # Handle the like action here
            st.session_state[f"liked_{idx}"] = True  # Example of setting session state
            st.success("You liked this recommendation!")

        if dislike_button.button('싫어요 👎', key=f"dislike_{idx}"):
            # Handle the dislike action here
            st.session_state[f"disliked_{idx}"] = False  # Example of setting session state
            st.error("You disliked this recommendation!")

        # Display the video below the genre and like/dislike buttons
        st.video(row['first video link'])
        
        # Separator for each recommendation
        st.markdown("---")
else:
    st.write("No songs found based on the selected criteria.")
