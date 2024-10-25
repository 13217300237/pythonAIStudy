from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(model="gpt-3.5-turbo-1106")


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | chat

result = chain.invoke(
    {
        "messages": [
            HumanMessage(
                content="Translate this sentence from English to French: I love programming."
            ),
            AIMessage(content="J'adore la programmation."),
            HumanMessage(content="What did you just say?"),
        ],
    }
)

print("ai的回答是", result.content)
