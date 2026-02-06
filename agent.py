import os
import pandas as pd
from google.cloud import bigquery
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate

os.environ["GOOGLE_CLOUD_PROJECT"] = "shopify-mvp-2026"

client = bigquery.Client(project="shopify-mvp-2026")
sql = """
SELECT itemid, total_views, add_to_carts, orders, last_seen
FROM shopify_mvp.fct_item_performance
ORDER BY total_views DESC
LIMIT 10
"""

df = client.query(sql).to_dataframe()
print(f"Successfully loaded {len(df)} product records")

context = df.to_markdown(index=False)

llm = ChatVertexAI(
    model_name="gemini-2.0-flash-001",
    location="us-central1",
    temperature=0,
)

prompt = ChatPromptTemplate.from_template(
    "You are an e-commerce data expert. Here is the data for the top 10 products: \n{context}\n\nUser Question: {question}\nPlease answer based on the data. Keep your answer concise and professional."
)

chain = prompt | llm

while True:
    query = input("\nAsk E-commerce Agent (type exit to quit): ")
    if query.strip().lower() == "exit":
        break

    print("Thinking...")
    result = chain.invoke({"context": context, "question": query})
    print(result.content)
