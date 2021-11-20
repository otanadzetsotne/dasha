import openai
from api_key import API_KEY


openai.api_key = API_KEY
response = openai.Completion.create(
    engine='davinci',
    prompt='Ehllo!',
    temprature=.3,
)

print(response)
