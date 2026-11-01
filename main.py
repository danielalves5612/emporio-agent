from google.genai import errors

from src.agent import ask_agent, create_chat

chat = create_chat()

while True:
    text = input("> ").strip()
    if text == "":
        continue
    if text.lower() == "sair":
        break
    print("Daniel está digitando...")
    try:
        answer = ask_agent(chat, text)
    except errors.APIError:
        print(
            "O sistema está com instabilidade, por favor, tente novamente em alguns minutos."
        )
        continue
    print(answer)
