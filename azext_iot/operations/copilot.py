import os
import json
from azext_iot.operations.constants import SYSTEM_INSTRUCTION
import openai

# Load config values
with open(r'azext_iot/operations/config.json') as config_file:
    config_details = json.load(config_file)
    
# Setting up the deployment name
chatgpt_model_name = config_details['CHAT_GPT_MODEL']

# This is set to `azure`
openai.api_type = "azure"

# The API key for your Azure OpenAI resource.
openai.api_key = os.getenv("OPENAI_API_KEY")

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
openai.api_base = config_details['OPENAI_API_BASE']

# Currently OPENAI API have the following versions available: 2022-12-01
openai.api_version = config_details['OPENAI_API_VERSION']

# This will correspond to the custom name you chose for your deployment when you deployed a model.
deployment_id='gpt-35-turbo'

def iot_copilot_ask(
    cmd,
    prompt
):
    # Ask Azure OpenAI
    response = openai.ChatCompletion.create(
        engine=deployment_id,
        messages = [
            {
                "role":"system",
                "content":SYSTEM_INSTRUCTION
            },
            {
                "role":"user",
                "content":"How do I route IoT device message using iot hub and save them into azure storage?"
            },
            {
                "role":"assistant",
                "content":"To route IoT device messages to Azure Storage using IoT Hub, the following Azure CLI commands might be useful: (Disclaimer: the result is powered by OpenAI model, it's only for reference and might not be correct, for more information, please look into https://learn.microsoft.com/en-us/cli/azure/iot?view=azure-cli-latest)\n1. az iot hub routing-endpoint create\n2. az iot hub route create\n3. az iot device send-d2c-message"
            },
            {
                "role":"user",
                "content":"create an iot hub"
            },
            {
                "role":"assistant",
                "content":"To create an IoT Hub, the following Azure CLI commands might be useful: (Disclaimer: the result is powered by OpenAI model, it's only for reference and might not be correct, for more information, please look into https://learn.microsoft.com/en-us/cli/azure/iot?view=azure-cli-latest)\n- az iot hub create"
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0,
        max_tokens=800,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    airesponse = response['choices'][0]["message"]["content"]

    # get az commands from airesponse
    azcommands = []
    for line in airesponse.splitlines():
        if line.startswith('az'):
            azcommands.append(line)

    print(airesponse)
    # ask user to execute commands
    choice = input("Do you want to execute the commands? (y/n): ")
    if choice == 'y':
        for azcommand in azcommands:
            print("executing: " + azcommand)
            os.system(azcommand)

    