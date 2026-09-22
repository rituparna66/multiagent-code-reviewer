import os
import json
import prompt as prompt
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

with open(r"/content/documents_for_embedding.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []

for item in data:
    documents.append(
        Document(
            page_content=item["content"],
            metadata=item["metadata"] | {"id": item["id"]}
        )
    )

print(len(documents))
# PR test change

api_key = os.getenv("OPENAI_API_KEY")

len(documents)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local(
    "compliance_faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
vectorstore.save_local("compliance_faiss_index")

docs = vectorstore.similarity_search(
    "Can a broker accept unredacted Aadhaar?",
    k=3
)

for d in docs:
    print(d.page_content)

vectorstore = FAISS.load_local(
    "compliance_faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 6}
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

rag_chain = (
        {
            "context": itemgetter("input") | retriever,
            "question": itemgetter("input")
        }
        | prompt
        | llm
        | StrOutputParser()
)


for d in docs:
    print(d.page_content)

docs = retriever.invoke(
    "Is Aadhaar mandatory for KYC?"
)

for d in docs:
    print(d.metadata["id"])
    print(d.page_content[:300])
    print("-" * 50)

response = rag_chain.invoke({
    "input": "Is Aadhaar mandatory for KYC under Indian regulations?"
})

print(response)

docs = retriever.invoke("Is Aadhaar mandatory for KYC?")

context = "\n".join([d.page_content for d in docs])

print("DEBUG CONTEXT ↓↓↓")
print(context)

prompt = f"""
Based on the provided regulations, answer the question: "Is Aadhaar mandatory for KYC?"

- Use the provided context ONLY.
- If the context provides a conditional answer, explain those conditions.
- If the information is truly missing, say: Not found in regulations.

Context:
{context}
"""

response = llm.invoke(prompt)
print(response.content)
