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
            "**SFA KnowledgeGPT는**    \n"
            "업로드한 문서에 있는 내용만 사용하여    \n"
            "질문에 대한 정확한 답변과       \n"
            "참조한 내용의 위치를 알려주는    \n"
            "**사내 GPT 서비스의 Prototype**입니다."
            "     \n\n\n"
        )

        api_key_input = st.text_input(
            "OpenAI API key 를 입력하세요.",
            type="password",
            placeholder="sk-############",
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )

        if not api_key_input:
            st.error(
                "OpenAI API key가 없습니다."
            )

        st.session_state["OPENAI_API_KEY"] = api_key_input
        
        model: str = st.selectbox("사용할 GPT 모델을 선택하세요.", options=MODEL_LIST)  # type: ignore

        st.session_state['selected_model'] = model

        return_all_chunks = st.checkbox("벡터검색한 모든 조각을 포함합니다")
        show_full_doc = st.checkbox("업로드한 파일 내용을 봅니다.")

        # session_state에 값 저장
        st.session_state["return_all_chunks"] = return_all_chunks
        st.session_state["show_full_doc"] = show_full_doc

        st.markdown("---")

        # faq()
