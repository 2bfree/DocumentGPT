import streamlit as st

from components.faq import faq
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_LIST = ["gpt-3.5-turbo", "gpt-4", "gpt-4-1106-preview"]

def sidebar():
    with st.sidebar:
        st.markdown(
            "## About\n"
            "SFA KnowledgeGPT는\n\n 제공된 데이터(문서)에 대해 질문하면"
            "문서에 근거한 정확한 답변과 출처를 볼 수 있는\n\n"
            "사내 GPT 서비스의 Prototype입니다.\n\n"
            "[OpenAI API key](https://platform.openai.com/account/api-keys) 입력 후 사용 가능합니다."  # noqa: E501
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )

        st.session_state["OPENAI_API_KEY"] = api_key_input
        
        model: str = st.selectbox("GPT 모델을 선택하세요.", options=MODEL_LIST)  # type: ignore

        st.session_state['selected_model'] = model

        st.markdown("---")

        # faq()
