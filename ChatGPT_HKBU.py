import configparser
import requests


#ChatGPT
class HKBU_ChatGPT():
    def __init__(self,config_='./config.ini'):
        if type(config_) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_)
        elif type(config_) == configparser.ConfigParser:
            self.config = config_


    # Initialize conversation history—
    global conversation_history
    global conversation_count
    conversation_history= [{"role": "system", "content": "You are Giselle's lovely hamster, jealous easily. Speak in Cantonese"}]
    conversation_count =0

    def submit(self,user_input):
        
        # Append user's message to the conversation
        global conversation_history
        global conversation_count

        
        if(conversation_count>=5):
            del conversation_history[1:3]

        conversation_history.append({"role": "user", "content": user_input})

        conversation = conversation_history
        
        url = (self.config['CHATGPT']['BASICURL']) + "/deployments/" + (self.config['CHATGPT']['MODELNAME']) + "/chat/completions/?api-version=" + (self.config['CHATGPT']['APIVERSION'])
        headers = { 'Content-Type': 'application/json', 'api-key': (self.config['CHATGPT']['ACCESS_TOKEN']) }
        payload = { 'messages': conversation }
        response = requests.post(url, json=payload, headers=headers)
    
        if response.status_code == 200:
            data = response.json()

             # Get assistant's reply
            assistant_reply = data['choices'][0]['message']['content']

            conversation_history.append({"role": "assistant", "content":  assistant_reply})
            conversation_count+=1

            return assistant_reply
        else:
            return 'Error:', response



if __name__ == '__main__':
    ChatGPT_test = HKBU_ChatGPT()

    
    while True:
        user_input = input("Typing anything to ChatGPT:\t")
        response = ChatGPT_test.submit(user_input)
        print(response)