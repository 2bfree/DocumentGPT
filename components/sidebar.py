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
            "SFA KnowledgeGPT를 사용하면 문서에 대한 질문을 하고 즉각적인 인용과 함께 정확한 답변을 받을 수 있습니다. "
            "   "
            "아래에 [OpenAI API key](https://platform.openai.com/account/api-keys) 입력하세요.n"  # noqa: E501
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
        
        model: str = st.selectbox("GPT 모델 선택", options=MODEL_LIST)  # type: ignore

        st.markdown("---")

        # faq()
