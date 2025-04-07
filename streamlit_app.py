import streamlit as st
import openai
from openai import OpenAI

st.set_page_config(page_title="AI 레시피 도우미", page_icon="🍳", layout="centered")

st.title("🍽️ AI 레시피 도우미")
st.markdown("요리 이름을 입력하면 만드는 방법을 알려드릴게요!")

openai_api_key = st.secrets['REPLICATE_KEY']['API_KEY']
client = OpenAI(api_key=openai_api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", 
         "content": "당신은 요리 전문가입니다. 사용자가 입력한 요리의 레시피를 재료와 만드는 순서로 자세히 설명해주세요. 친절하고 명확하게, 마치 요리책처럼 써주세요."}
    ]

dish_name = st.text_input("요리 이름을 입력하세요", key="dish_input")

if st.button("레시피 알려줘") and dish_name:
    st.session_state.messages.append({"role": "user", "content": f"{dish_name} 레시피 알려줘"})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    dish_name = ""

st.divider()
for message in st.session_state.messages[1:]:
    if message["role"] == "user":
        st.markdown(f"👤 **{message['content']}**")
    else:
        st.markdown(f"👩‍🍳 {message['content']}")

if st.button("처음부터 다시"):
    st.session_state.messages = [
        {"role": "system", 
         "content": "당신은 요리 전문가입니다. 사용자가 입력한 요리의 레시피를 재료와 만드는 순서로 자세히 설명해주세요. 친절하고 명확하게, 마치 요리책처럼 써주세요."}
    ]
