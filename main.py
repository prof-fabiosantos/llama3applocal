from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
]

# Flag to control the introduction message
intro_sent = False

while True:
    if not intro_sent:
        intro_message = {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."}
        history.append(intro_message)
        intro_sent = True

    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)

    print()
    user_input = input("> ")
    if user_input.lower() == 'exit':
        break
    history.append({"role": "user", "content": user_input})
