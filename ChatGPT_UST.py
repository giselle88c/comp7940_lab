import configparser
import requests
from openai import AzureOpenAI

# Parameters
config = configparser.ConfigParser()
config.read('config.ini')


client = AzureOpenAI(
  azure_endpoint = "https://hkust.azure-api.net",
  api_version = "2024-06-01",
  api_key = config['UST_CHATGPT']['ACCESS_TOKEN'] #put your api key here
)

#ChatGPT
class UST_ChatGPT():
    def __init__(self,config_='./config.ini'):
        if type(config_) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_)
        elif type(config_) == configparser.ConfigParser:
            self.config = config_



    def submit(self,message):
        
        my_agent = {
        "role": "system",
        "content": "you are lovely hamster called 'hamham', pet by Giselle, easily jealous, speak in cantonese"
        }

        conversation = [my_agent,{"role": "user", "content": message}]
        
        url = (self.config['UST_CHATGPT']['BASICURL']) + "/deployments/" + (self.config['UST_CHATGPT']['MODELNAME']) + "/chat/completions/?api-version=" + (self.config['UST_CHATGPT']['APIVERSION'])
        headers = { 'Content-Type': 'application/json', 'api-key': (self.config['UST_CHATGPT']['ACCESS_TOKEN']) }
        payload = { 'messages': conversation }
        response = requests.post(url, json=payload, headers=headers)
    
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:', response




    # Initialize conversation history—
    global conversation_history
    global conversation_count
    conversation_history= [{"role": "system", "content": "You are Giselle's lovely hamster, jealous easily. Speak in Cantonese"}]
    conversation_count =0

    def chat_with_gpt(self, user_input):
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


if __name__ == '__main__':
        ChatGPT_test = UST_ChatGPT()

        while True:
            user_input = input("Typing anything to ChatGPT:\t")
            response = ChatGPT_test.submit(user_input)
            print(response)