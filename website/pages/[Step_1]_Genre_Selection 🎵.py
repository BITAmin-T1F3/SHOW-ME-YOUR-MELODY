import streamlit as st

st.set_page_config(page_title="#SHOW_ME_YOUR_MELODY", page_icon="🌃🎧")

def select_genre(genre, index):
    st.session_state.selected_genre = genre
    st.session_state.genre_index = index  # Store the index/number
    st.session_state.page = 'picture_upload'  # Assuming you're using a method to navigate pages
    st.markdown(f"<strong><p class='big-font' style='text-align: center;'>선택한 장르: {genre}</p></strong>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'><br>'[Step 2] Upload Picture 📸📲'<br>페이지로 넘어가주시길 바랍니다!</div>", unsafe_allow_html=True)

# Genre Selection Page
st.markdown("""
    <style>
        .big-font {
            font-size:20px !important;
            text-align: center;
        }
        div.stButton > button:first-child {
            background-color: #f0f0f0;
            color: black;
            padding: 10px 24px;
            border-radius: 25px;
            border: 1px solid #f0f0f0;
            width: 100%;
            margin: 5px 0; /* Add some margin between the buttons */
        }
        div.stButton > button:first-child:hover {
            background-color: #e6e6e6;
            border: 1px solid #dcdcdc;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h2 style="text-align:center;">[Step 1] Pick "Your" Genre 🎵</h2>', unsafe_allow_html=True)

genres = [
    "OST", "뉴에이지", "댄스/팝", "락", "락/메탈", "랩/힙합",
    "메탈", "발라드", "알앤비/소울", "월드뮤직", "인디",
    "일렉트로닉", "팝", "포크/어쿠스틱"
]

# Display buttons for each genre in a centered column
col1, col2, col3 = st.columns([1,2,1])
with col2:
    for i, genre in enumerate(genres, start=1):
        if st.button(genre, key=f'genre_{i}'):
            select_genre(genre, i)

