from flask import Flask, request, jsonify
from flask_restful import Resource, Api

# import the Models to use.
from Models.Gemini import _Query as GeminiQuery

app = Flask(__name__)
api = Api(app)


apiStructure = """
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-3.5-turbo-0613",
  "system_fingerprint": "fp_44709d6fcb",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "logprobs": null,
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}

"""

# class for the default route of the API
class WrapperHome(Resource):
    def get(self):
        return {
            "Message": "This is A.L.F.I.E's OPEN APO Wrapper. ",
            "OpenAI Structure": apiStructure

        }
    

# class for the default route of the API
class ApiQuery(Resource):
    def get(self, prompt):
        return GeminiQuery(prompt)


class ChatCompletions(Resource):
    def post(self):
        data = request.get_json()
        messages = data.get('messages')
        stop = data.get('stop')
        temperature = data.get('temperature')
        max_tokens = data.get('max_tokens')
        stream = data.get('stream')

        # we need to pass the messages to the model
        # generate the response
        return GeminiQuery(messages)




# expose the API endpoints
api.add_resource(WrapperHome, '/')

# model call route
api.add_resource(ApiQuery, '/ModelCall/v1/<string:prompt>')

# chat completions route
api.add_resource(ChatCompletions, '/v1/chat/completions')

# run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=12000)