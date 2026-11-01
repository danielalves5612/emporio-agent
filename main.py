from src.agent import ask_agent, create_chat

chat = create_chat()
print(ask_agent(chat, "Quanto custa o Yamaha C40?"))
print(ask_agent(chat, "E tem em estoque?"))
