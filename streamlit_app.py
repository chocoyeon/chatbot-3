import streamlit as st
from openai import OpenAI
import time

# 페이지 설정
st.set_page_config(page_title="🍽️ AI 레시피 도우미", page_icon="🥘", layout="centered")

# 제목과 설명을 가운데 정렬
st.markdown("<h1 style='text-align: center;'>🥕 AI 레시피 도우미</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>먹고 싶은 음식 이름을 입력해 보세요! 🍜<br>AI 요리사가 친절하게 레시피를 알려드려요. 😋</p>", unsafe_allow_html=True)

# API 키 설정
try:
    openai_api_key = st.secrets['REPLICATE_KEY']['API_KEY']
    client = OpenAI(api_key=openai_api_key)
except Exception as e:
    st.markdown("<p style='text-align: center; color: red;'>API 키를 불러오는 데 문제가 발생했습니다.</p>", unsafe_allow_html=True)
    st.stop()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", 
         "content": "당신은 요리 전문가입니다. 사용자가 입력한 요리의 레시피를 재료와 만드는 순서로 자세히 설명해주세요. 간단하고 따뜻한 말투로 알려주세요."}
    ]

# 이전 메시지 표시
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(f"<div style='text-align: center;'>{message['content']}</div>", unsafe_allow_html=True)

# 사용자 입력 처리
dish = st.chat_input("어떤 요리를 만들고 싶나요? 🍳")
if dish:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": dish})
    with st.chat_message("user"):
        st.markdown(f"<div style='text-align: center;'>'{dish}' 레시피 알려줘! 📝</div>", unsafe_allow_html=True)

    # 스트리밍 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 스트리밍 응답 시작
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )
        
        # 응답 스트리밍 처리
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(f"<div style='text-align: center;'>{full_response}</div>", unsafe_allow_html=True)
        
        # 완성된 응답을 세션 상태에 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
# 푸터 추가
