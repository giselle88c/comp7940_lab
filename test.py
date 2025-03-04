# Install and import OpenAI Python library
#!pip install openai --upgrade
from openai import AzureOpenAI
#import openai
import configparser

# Parameters
config = configparser.ConfigParser()
config.read('config.ini')


client = AzureOpenAI(
  azure_endpoint = "https://hkust.azure-api.net",
  api_version = "2024-06-01",
  api_key = config['UST_CHATGPT']['ACCESS_TOKEN'] #put your api key here
)

# Function
def get_response(message, instruction):
    response = client.chat.completions.create(
		model = 'gpt-4o-mini',
        temperature = 1,
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": message}
        ]
    )
    
    # print token usage
    print(response.usage)
    # return the response
    return response.choices[0].message.content




#print(get_response("What would you feel if Anson Lo is going to marry?", "You are a fans who like Anson Lo."))


# Initialize conversation history
global conversation_history
conversation_history= [{"role": "system", "content": "You are Giselle's lovely hamster who is Anson Lo's big fans. Speak in Cantonese"}]

def chat_with_gpt(user_input):
    # Append user's message to the conversation
    global conversation_history
    conversation_history.append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
		model = 'gpt-4o-mini',
        temperature = 1,
        messages = conversation_history
    )

    # Get assistant's reply
    assistant_reply = response.choices[0].message.content
    
    # Append assistant's response to conversation history
    #global conversation_history
    
    conversation_history.append({"role": "assistant", "content":  assistant_reply})

    return assistant_reply

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = chat_with_gpt(user_input)
    print("ChatGPT:", response)