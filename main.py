from src.agent import ask_agent, create_chat

chat = create_chat()

while True:
    text = input("> ").strip()
    if text == "":
        continue
    if text.lower() == 'sair':
        break
    print("Daniel está digitando...")
    answer = ask_agent(chat, text)
    print(answer)
