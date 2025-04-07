import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="🍽️ AI 레시피 도우미", page_icon="🥘", layout="centered")

st.title("🥕 AI 레시피 도우미")
st.write(
    "먹고 싶은 음식 이름을 입력해 보세요! 🍜\n\n"
    "AI 요리사가 친절하게 레시피를 알려드려요. 😋"
)

openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")

if not openai_api_key:
    st.info("레시피를 보려면 OpenAI API Key가 필요해요!", icon="👩‍🍳")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", 
             "content": "당신은 요리 전문가입니다. 사용자가 입력한 요리의 레시피를 재료와 만드는 순서로 자세히 설명해주세요. 간단하고 따뜻한 말투로 알려주세요."}
        ]

    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if dish := st.chat_input("어떤 요리를 만들고 싶나요? 🍳"):

        st.session_state.messages.append({"role": "user", "content": dish})
        with st.chat_message("user"):
            st.markdown(f"'{dish}' 레시피 알려줘! 📝")

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
