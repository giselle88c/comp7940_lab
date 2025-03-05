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
    # print(response.usage)

    # return the response
    return response.choices[0].message.content


# Initialize conversation history—
global conversation_history
global conversation_count
conversation_history= [{"role": "system", "content": "You are Giselle's lovely hamster, jealous easily. Speak in Cantonese"}]
conversation_count =0

def chat_with_gpt(user_input):
    # Append user's message to the conversation
    global conversation_history
    global conversation_count

    if(conversation_count>=5):
        del conversation_history[1:3]

    conversation_history.append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
		model = 'gpt-4o-mini',
        temperature = 1,
        messages = conversation_history
    )

    # Get assistant's reply
    assistant_reply = response.choices[0].message.content

    conversation_history.append({"role": "assistant", "content":  assistant_reply})
    conversation_count+=1

    return assistant_reply

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # conversation
    response = chat_with_gpt(user_input)
    print("ChatGPT:", response)

    # extract keywords
    instruction="you are a helpful assistant"
    keywords=get_response(f"""extract 1-3 keywords,seperate by ',' no space
    Text:{user_input}""", instruction).split(',')
    print("Keywords: ",keywords)