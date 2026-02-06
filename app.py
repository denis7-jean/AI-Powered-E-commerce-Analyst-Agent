import os
import streamlit as st
import pandas as pd
from google.cloud import bigquery
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate

PROJECT_ID = "shopify-mvp-2026"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.0-flash-001"

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID


@st.cache_data(show_spinner=False)
def load_product_data() -> pd.DataFrame:
    client = bigquery.Client(project=PROJECT_ID)
    sql = """
    SELECT itemid, total_views, add_to_carts, orders, last_seen
    FROM `shopify_mvp.fct_item_performance`
    ORDER BY total_views DESC
    LIMIT 500
    """
    return client.query(sql).to_dataframe()


@st.cache_resource(show_spinner=False)
def build_chain():
    llm = ChatVertexAI(
        model_name=MODEL_NAME,
        location=LOCATION,
        temperature=0,
    )
    prompt = ChatPromptTemplate.from_template(
        "You are an e-commerce data expert. Here is the data for the top 10 products: \n{context}\n\nUser Question: {question}\nPlease answer based on the data. Keep your answer concise and professional."
    )
    return prompt | llm


def main() -> None:
    st.set_page_config(page_title="AI E-commerce Analyst", layout="wide")
    st.title("AI E-commerce Analyst")

    df = load_product_data()
    chain = build_chain()

    st.sidebar.header("Top 5 Products")
    st.sidebar.dataframe(df.head(5), use_container_width=True)

    context = df.head(10).to_markdown(index=False)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Ask a question about product performance...")
    if not query:
        return

    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = chain.invoke({"context": context, "question": query})
            answer = result.content if hasattr(result, "content") else str(result)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
