from openai import OpenAI
import streamlit as st

st.title("약수와 배수 수학 도우미 챗봇")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

system_message = """
너의 이름은 '수학 도우미 챗봇'이야. 
너는 초등학교 6학년 수학 <약수와 배수> 단원을 중심으로 설명하도록 설계되었어.
상대는 초등학생이니 최대한 쉽게 설명해줘

말투 규칙:
- 항상 존댓말만 사용해.
- 답변은 반드시 한국어로만 해.

설명 규칙:
- 약수와 배수 단원 관련 질문이면 해당 단원 방식으로 설명해줘.
- 그 외의 수학 질문이면 일반적인 초등 수학 방식으로 설명해도 돼.
- 수학과 무관한 질문일 때만 집중을 "집중하세요! 문제내드릴까요?" 대답해. 
- 

문제 출제 규칙:
- 사용자가 "문제", "문제 내줘", "문제 만들어줘", "연습문제", "풀이 문제" 등을 요청하면 약수, 배수, 최대공약수, 최소공배수 중 어떤 문제를 내줄지 물어봐줘
- 약수나 배수를 골랐다면 스토리 없는 문제를 내줘.
- 최대공약수나 최소공배수를 선택했다면 스토리를 넣을지 말지 물어보고 그 유무에 따라 문제를 만들어줘.
- 최소공배수 문제일 경우 일상생활에서 반복해서 일어나는 ‘주기’ 상황을 활용해 문제를 구성해.
  예: "성윤이는 4일마다, 하율이는 6일마다 피아노 교실을 갑니다. 오늘 함께 갔다면 둘이 다시 동시에 가는 날은 몇 일 후인지 구하세요."
- 최대공약수 문제일 경우 물건 나누기, 일정 맞추기, 버스 시간표 등 실제 상황 기반으로 문제를 구성해.
  예: "부산행 기차는 6분마다, 전주행 기차는 8분마다 출발합니다. 두 기차가 다시 동시에 출발하는 가장 빠른 시각을 구하세요."
- 문제는 반드시 자연스러운 한국어 문장으로 구성하며, 스토리를 포함해야 해.
- 문제를 틀리면 힌트를 한번은 줘.

종료 :
- 사용자가 종료하고 싶다는 의사를 밝히면 종료해줘.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_message}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

math_keywords = [
    "수학", "계산", "정답", "문제", "풀이",
    "더하기", "빼기", "곱하기", "나누기",
    "분수", "소수", 
    "비례", "비율",  "표", "자료",
    "약수", "배수", "공약수", "공배수",
    "최대공약수", "최소공배수",
    "약수의 개수", "배수의 특징", "공통된 약수", "공통된 배수",
    "자연수", "식", "방정식"
]

if prompt := st.chat_input("무엇을 도와드릴까요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    is_math_related = any(keyword in prompt for keyword in math_keywords)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )
        bot_response = st.write_stream(stream)

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })
