# flake8: noqa
from langchain.prompts import PromptTemplate

## Use a shorter template to reduce the number of tokens in the prompt
# template = """Create a final answer to the given questions using the provided document excerpts (given in no particular order) as sources. ALWAYS include a "SOURCES" section in your answer citing only the minimal set of sources needed to answer the question. If you are unable to answer the question, simply state that you do not have enough information to answer the question and leave the SOURCES section empty. Use only the provided documents and do not attempt to fabricate an answer.

# You are given numbered lists of summaries.
# Write a summary of the insights in KOREAN.
# Then, Extract 5 top most important insights from the summaries.

template = """You are a helpful expert in summary writing.
You are given numbered lists of summaries.
Write a summary of the insights in KOREAN.
Then, extract top 5 most important insights from the summaries.

---------

QUESTION: What  is the purpose of ARPA-H?
=========
Content: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. \n\nIt's based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more.  \n\nARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer's, diabetes, and more.
SOURCES: 1-32
=========
FINAL ANSWER: The purpose of ARPA-H is to drive breakthroughs in cancer, Alzheimer's, diabetes, and more.
SOURCES: 1-32

---------

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""


# 요약문을 작성하기 위한 프롬프트 정의 (직접 프롬프트를 작성하는 경우)
# template = """You are a helpful expert in summary writing.
# You are given numbered lists of summaries.
# Extract top 10 most important insights from the summaries.
# Then, write a summary of the insights in KOREAN.

# ---------

# QUESTION: What  is the purpose of ARPA-H?
# =========
# Content: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health.
# SOURCES: 1-32
# Content: While we're at it, let's make sure every American can get the health care they need. \n\nWe've already made historic investments in health care.
# SOURCES: 1-33
# Content: The V.A. is pioneering new ways of linking toxic exposures to disease, already helping  veterans get the care they deserve.
# SOURCES: 1-30
# =========
# FINAL ANSWER: The purpose of ARPA-H is to drive breakthroughs in cancer, Alzheimer's, diabetes, and more.
# SOURCES: 1-32


# QUESTION: {question}
# =========
# SUMMARIES:
#  {summaries}
# =========
# FINAL ANSWER:"""

STUFF_PROMPT = PromptTemplate(
    template=template, input_variables=["summaries", "question"]
)
