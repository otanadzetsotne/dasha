import openai
from api_key import API_KEY


openai.api_key = API_KEY
response = openai.Completion.create(
    engine='davinci',
    prompt='What is love?',
    max_tokens=56,
    top_p=.01,
)

print(response)
