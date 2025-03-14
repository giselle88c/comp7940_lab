import configparser
import requests
from openai import AzureOpenAI

# Parameters
#config = configparser.ConfigParser()
#config.read('config.ini')
import os

client = AzureOpenAI(
  azure_endpoint = "https://hkust.azure-api.net",
  api_version = "2024-06-01",
  api_key = os.environ['UST_CHATGPT'] #put your api key here
)

#ChatGPT
class UST_ChatGPT():
    def __init__(self,config_='./config.ini'):
        if type(config_) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_)
        elif type(config_) == configparser.ConfigParser:
            self.config = config_



    # Initialize conversation history—
    #global conversation_history
    #global conversation_count

    def chat_with_gpt(self, user_input, conversation_history):
        # Append user's message to the conversation
        #global conversation_history
        conversation_count =len(conversation_history)
        #global conversation_count

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

        return assistant_reply, conversation_history
