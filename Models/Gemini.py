import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from rich.console import Console

# create a console object
console = Console()

# load the .env file
load_dotenv()

# set the api key
api_key = os.getenv("Google_Auth_Key")

genai.configure(api_key=api_key)

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

# define the model to use
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
)

messages = []

# override the print function
def print(*args, **kwargs):
    console.print(*args, **kwargs)

def get_current_unix_timestamp():
    return int(time.time())

def build_conversation(role, message):
    # build a conversation
    obj = {
        "role": role,
        'parts': [message]
        
    }

    # append to messages
    messages.append(obj)

def count_tokens_in_response(sentence):
    return len(sentence.split())

# def OpenAi Wrapper function.  
def OpenAIWrapper(prompt, response, index=0):

    # current time.
    current_time = get_current_unix_timestamp()

    # tokens in the response
    promptTokens = count_tokens_in_response(prompt)

    # response tokens
    ResponseTokens = count_tokens_in_response(response)

    #total tokens
    totalTokens = promptTokens + ResponseTokens

    return {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": current_time,
            "model": "custom_model",
            "system_fingerprint": "fp_alfie_module",
            "choices": [{
                    "index": index,
                    "message": {
                        "role": "assistant",
                        "content": response,
                    },
                    "logprobs": None,
                    "finish_reason": "stop"
                }],
            "usage": {
                "prompt_tokens": ResponseTokens,
                "completion_tokens": promptTokens,
                "total_tokens": totalTokens
            }
        }


def _Query(prompt):
    # buid the conversation
    build_conversation("user", prompt)
    
    # generate the response
    response = model.generate_content(messages)

    # build the conversation
    build_conversation("model", response.text)

    # we need to return an OpenAI structure response
    wrapperObj = OpenAIWrapper(prompt, response.text)

    return wrapperObj