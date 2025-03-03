# Install and import OpenAI Python library
#!pip install openai --upgrade
from openai import AzureOpenAI

# Parameters
client = AzureOpenAI(
  azure_endpoint = "https://hkust.azure-api.net",
  api_version = "2024-06-01",
  api_key = "7c475fca9bb744e7ad3a44d797c2c186" #put your api key here
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




print(get_response("What would you feel if Anson Lo is going to marry?", "You are a fans who like Anson Lo."))