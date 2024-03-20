import re
import streamlit as st

from components.sidebar import sidebar

from ui import (
    wrap_doc_in_html,
    is_query_valid,
    is_file_valid,
    is_open_ai_key_valid,
    display_file_read_error,
)

from core.caching import bootstrap_caching

from core.parsing import read_file
from core.chunking import chunk_file
from core.embedding import embed_files
from core.qa import query_folder
from core.utils import get_llm


EMBEDDING = "openai"
VECTOR_STORE = "faiss"
# MODEL_LIST = ["gpt-3.5-turbo", "gpt-4", "gpt-4-1106-preview"]

# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="SFA KnowledgeGPT - beta", page_icon="📖", layout="wide")
st.header("SFA KnowledgeGPT - beta")

# Enable caching for expensive functions
bootstrap_caching()

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")


if not openai_api_key:
    st.warning(
        "OpenAI API key를 사이드바에 입력하셔야. 시작됩니다. API key는"
        " https://platform.openai.com/account/api-keys.에서 발급 받을 수 있습니다."
    )


uploaded_file = st.file_uploader(
    "검색할 파일을 업로드 하세요. (현재는 pdf, docx, txt만 가능합니다.)",
    type=["pdf", "docx", "txt"],
    help="스캔한 문서 분석은 아직 못합니다.",
)

# model: str = st.selectbox("GPT 모델 선택", options=MODEL_LIST)  # type: ignore

with st.expander("세부 옵션 보기"):
    return_all_chunks = st.checkbox("벡터 검색에서 검색된 모든 조각(chunks) 보기")
    show_full_doc = st.checkbox("업로드한 파일 내용 보기")


if not uploaded_file:
    st.stop()

try:
    file = read_file(uploaded_file)
except Exception as e:
    display_file_read_error(e, file_name=uploaded_file.name)

chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)

if not is_file_valid(file):
    st.stop()

model = sidebar.model

if not is_open_ai_key_valid(openai_api_key, model):
    st.stop()


with st.spinner("문서를 인덱싱하고 있습니다. 시간이 조금 거릴 수 있습니다."):
    folder_index = embed_files(
        files=[chunked_file],
        embedding=EMBEDDING if model != "debug" else "debug",
        vector_store=VECTOR_STORE if model != "debug" else "debug",
        openai_api_key=openai_api_key,
    )

with st.form(key="qa_form"):
    query = st.text_area("등록한 문서에 대해 물어보세요.")
    submit = st.form_submit_button("질문하기")


if show_full_doc:
    with st.expander("문서 자세히 보기"):
        # Hack to get around st.markdown rendering LaTeX
        st.markdown(f"<p>{wrap_doc_in_html(file.docs)}</p>", unsafe_allow_html=True)


if submit:
    if not is_query_valid(query):
        st.stop()

    # Output Columns
    answer_col, sources_col = st.columns(2)

    llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0.2)
    result = query_folder(
        folder_index=folder_index,
        query=query,
        return_all=return_all_chunks,
        llm=llm,
    )

    # 문장으로 나누기
    sentences_answer = re.split('(?<=\.)\s', result.answer)

    with answer_col:
        st.markdown("#### 결과")
        # st.markdown(result.answer)
        for sentences_answer in sentences_answer :
            st.markdown(sentences_answer)

    with sources_col:
        st.markdown("#### 출처")
        for source in result.sources:
            st.markdown(source.page_content)
            st.markdown(source.metadata["source"])
            st.markdown("---")
