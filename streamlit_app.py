import streamlit as st
from openai import OpenAI
import os

# 페이지 설정
st.set_page_config(page_title="🍽️ AI 레시피 도우미", page_icon="🥘", layout="centered")

# 타이틀 (가운데 정렬)
st.markdown("<h1 style='text-align: center;'>🥕 AI 레시피 도우미</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>먹고 싶은 음식 이름을 입력해 보세요! 🍜<br>AI 요리사가 친절하게 레시피를 알려드려요. 😋</p>", unsafe_allow_html=True)

# API 키 설정 (사용자가 입력한 API 키 사용)
openai_api_key = st.secrets['REPLICATE_KEY']['API_KEY']
client = OpenAI(api_key=openai_api_key)

# 사이드바에 언어 선택 기능 추가
st.sidebar.subheader("언어 선택")
languages = {
    "한국어": "ko",
    "영어": "en",
    "일본어": "ja",
    "중국어": "zh"
}

selected_languages = st.sidebar.multiselect("레시피를 볼 언어를 선택하세요:", 
                                   list(languages.keys()), default=["한국어"])

# 초기 대화 상태 설정
if "messages" not in st.session_state:
    language_list = ", ".join(selected_languages)
    st.session_state.messages = [
        {"role": "system", 
         "content": f"당신은 요리 전문가입니다. 사용자가 입력한 요리의 레시피를 재료와 만드는 순서로 자세히 설명해주세요. "
                   f"간단하고 따뜻한 말투로 알려주세요. 답변은 다음 언어로 제공해주세요: {language_list}. "
                   f"각 언어별로 답변 앞에 [언어명]을 표시해주세요. 예: [한국어] 레시피..."}
    ]

# 대화 초기화 버튼
if st.sidebar.button("대화 초기화", use_container_width=True):
    language_list = ", ".join(selected_languages)
    st.session_state.messages = [
        {"role": "system", 
         "content": f"당신은 요리 전문가입니다. 사용자가 입력한 요리의 레시피를 재료와 만드는 순서로 자세히 설명해주세요. "
                   f"간단하고 따뜻한 말투로 알려주세요. 답변은 다음 언어로 제공해주세요: {language_list}. "
                   f"각 언어별로 답변 앞에 [언어명]을 표시해주세요. 예: [한국어] 레시피..."}
    ]
    st.experimental_rerun()

# 이전 대화 표시
for message in st.session_state.messages[1:]:  # 시스템 메시지 제외
    role = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"]):
        st.markdown(f"<div style='text-align: center;'>{role}: {message['content']}</div>", unsafe_allow_html=True)

# 사용자 입력 처리
if dish := st.chat_input("어떤 요리를 만들고 싶나요? 🍳"):
    # 언어 목록 업데이트 (사용자가 언어 선택을 변경했을 경우)
    language_list = ", ".join(selected_languages)
    # 시스템 메시지 업데이트
    st.session_state.messages[0] = {
        "role": "system", 
        "content": f"당신은 요리 전문가입니다. 사용자가 입력한 요리의 레시피를 재료와 만드는 순서로 자세히 설명해주세요. "
                  f"간단하고 따뜻한 말투로 알려주세요. 답변은 다음 언어로 제공해주세요: {language_list}. "
                  f"각 언어별로 답변 앞에 [언어명]을 표시해주세요. 예: [한국어] 레시피..."
    }
    
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": f"{dish} 레시피 알려줘!"})
    with st.chat_message("user"):
        st.markdown(f"<div style='text-align: center;'>👤: '{dish}' 레시피 알려줘! 📝</div>", unsafe_allow_html=True)

    # AI 응답 생성 및 표시
    with st.chat_message("assistant"):
        # 응답을 저장할 변수
        full_response = ""
        
        # 로딩 상태 표시
        with st.spinner("AI 요리사가 레시피를 준비하고 있어요..."):
            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.7
            )
            
            # 응답 가져오기
            full_response = response.choices[0].message.content
        
        # 응답 표시 (가운데 정렬)
        st.markdown(f"<div style='text-align: center;'>🤖: {full_response}</div>", unsafe_allow_html=True)
        
        # 최종 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# 사이드바에 도움말 추가
with st.sidebar:
    st.markdown("### 사용 방법")
    st.markdown("1. 원하는 요리 이름을 입력하세요.")
    st.markdown("2. AI가 선택한 언어로 레시피를 알려드립니다.")
    st.markdown("3. 대화 초기화 버튼을 눌러 새로운 대화를 시작할 수 있습니다.")
    
    st.markdown("### 팁")
    st.markdown("- 구체적인 요리 이름을 입력하면 더 정확한 레시피를 받을 수 있어요.")
    st.markdown("- 여러 언어를 선택하면 해당 언어로 모두 레시피를 받을 수 있어요.")
