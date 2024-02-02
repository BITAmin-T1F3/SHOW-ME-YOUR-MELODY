import streamlit as st
import base64

st.set_page_config(page_title="#SHOW_ME_YOUR_MELODY", page_icon="🌃🎧")

if 'navigate_to' not in st.session_state:
    st.session_state.navigate_to = None

def navigate():
    st.session_state.navigate_to = "genre_selection"

def autoplay_video(file_path: str):
    # Open the video file in binary read mode
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # Create the HTML string with the Base64 encoded video
        video_html = f"""
            <video width="720" height="400" controls autoplay loop muted>
            <source src="data:video/mp4;base64,{b64}" type="video/mp4">
            Your browser does not support the video tag.
            </video>
            """
        # Display the video in Streamlit using markdown with unsafe_allow_html=True
        st.markdown(video_html, unsafe_allow_html=True)

st.image('../web_logo.png', use_column_width=True)

st.markdown('''
<style>
    .instructions-box {
        border-radius: 25px;
        background: #f0f0f0;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold; /* Ensure text is bold */
    }
</style>
''', unsafe_allow_html=True)

st.markdown("""
    <style>
        .centered-header {
            text-align: center;
            padding: 10px 0;
            margin: 10px 0;
        }
    </style>
    <div class="centered-header">
        <h3><span style="color: black;">#SHOW_ME_YOUR_MELODY 에 오신 것을 환영합니다! 🌃🎧</span></h3>
    </div>
""", unsafe_allow_html=True)

st.markdown('''
<div class="instructions-box">
    <p style="font-weight: bold;">인스타그램 게시글 혹은 릴스 올리실 때, 어떠한 음악을 넣으면 좋을지 고민한 적 있으신가요? 🤔</p>
    <p style="font-weight: bold;">이 사이트를 이용하면 사진에 어울리는 + 개인의 취향을 고려한 음악을 추천해드립니다! 💡</p>
    <p style="font-weight: bold;">하단에 위치한 '음악 추천받기 🎵🎧' 버튼을 클릭하셔서 한 번 이용해보세요 😊</p>
</div>
''', unsafe_allow_html=True)

st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #f0f0f0;
            color: black;
            padding: 10px 24px;
            border-radius: 25px;
            border: 1px solid #f0f0f0;
        }
        div.stButton > button:first-child:hover {
            background-color: #e6e6e6;
            border: 1px solid #dcdcdc;
        }
    </style>""", unsafe_allow_html=True)

autoplay_video("../RPReplay_Final1706802318.mov")

st.markdown('''
<div class="instructions-box">
    <div style='text-align: center; font-size: 24px; font-weight: bold; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px;'>💻 프로젝트 배경</div>
    <p><strong>인스타그램은 전세계에서 약 20억명이 사용하는 소셜미디어 플랫폼으로, 많은 이들의 사랑을 받고있습니다. (2023년 7월 통계 📉)</strong></p>
    <p><strong>어느새 이 소셜미디어 매체를 통해 우리는 자연스레 우리의 일상을 공유할 수 있게 되었습니다.</strong></p>
    <p><strong>인스타그램은 현재 위와 같이, 게시글/릴스를 기재할 때 사용자에게 음악을 탑재할 수 있도록 제공해줍니다.</strong></p>
    <p><strong>하지만, 사진을 충분히 파악하지 못하고 사용자의 취향을 고려하지 못한 점을 발견하여</strong></p>
    <p><strong>이 프로젝트를 시작하게 되었습니다.</strong></p>
</div>
''', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1.1, 1])

with col2:
    if st.button('음악 추천받기 🎵🎧', key='select_genre'):
        navigate()

if st.session_state.navigate_to == "genre_selection":
    col1, col2, col3 = st.columns([0.2, 1, 0.2])

    with col2:
        st.write("메뉴에서 '[Step 1] Genre Selection 🎵' 페이지 클릭해주시길 바랍니다!")