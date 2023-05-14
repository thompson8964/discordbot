import toml
import openai

with open('config.toml', 'r') as f:
    data = toml.load(f)
key = data['openAItoken']

#openai.organization = "org-P11Velr3yd83kB9Ps5PTqei8"
openai.api_key = key
def gptbot(userInput):
    print("Chatbot: ")
    print(f"Userinput: {userInput}")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userInput}
        ]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    bot_message = gptbot("Hello can you hear me?")
    print(f"bot_message: {bot_message}")

