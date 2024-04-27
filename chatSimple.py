from langchain_community.llms import Ollama

user_input = input("What is your question? ")
llm = Ollama(model="llama3")
res = llm.invoke(user_input)
print(res)
