import os
from time import sleep
import openai

# This is set to `azure`
openai.api_type = "azure"

# The API key for your Azure OpenAI resource.
openai.api_key = "98244fc8e26c41f697940af3cf792583"

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
openai.api_base = "https://jiacjuopenai2.openai.azure.com/"

# Currently OPENAI API have the following versions available: 2022-12-01
openai.api_version = "2023-03-15-preview"

# This will correspond to the custom name you chose for your deployment when you deployed a model.
deployment_id="gpt-35-turbo" 

# Prompts Azure OpenAI with a request and synthesizes the response.
def generate_openai_explain(cmd, language):
    try:
        # Ask Azure OpenAI
        response = openai.ChatCompletion.create(
            engine=deployment_id,
            messages = [
                {
                    "role":"system",
                    "content":"You are an professional AI assistant in Azure IoT Azure CLI"
                },
                {
                    "role":"user",
                    "content":"Explain " + cmd + " in " + language
                }
            ],
            temperature=0,
            max_tokens=800,
            top_p=0,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None)
        print(response['choices'][0]["message"]["content"])
    except Exception as err:
        print("Encountered exception. {}".format(err))
