import json
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def getResponseFromAI(prompt):
    load_dotenv()
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    VARIATION = os.environ.get('VARIATION')
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY,temperature = VARIATION)
    tweet_prompt = PromptTemplate.from_template("{prompt}")
    tweet_chain = LLMChain(llm=llm, prompt=tweet_prompt, verbose=False)
    resp = tweet_chain.run(prompt=prompt)
    return resp

def dataAsString(sample, count):
    prompt_for_gpt = "By keeping fields like email, company, website, etc that define a person, as unique always and each generated object should be inspired from a different country also no two consecutive object should be inspired from same country, generate ",count," more objects similar to the sample object like ",sample," by understanding what each key in the object means and what value is expected for each key, act like the faker library. RETURN DATA AS ARRAY OF OBJECTS JSON FORMAT, ALSO CHECK HISTORY AND DONT GENERATE SIMILAR VALUES IN ATLEAST 10 CONSECUTIVE ITERATIONS"
    print('Gemini In Action!')
    resp = getResponseFromAI(prompt_for_gpt)
    print('Gemini Responded!')
    return resp

def dataAsJSON(sample, count):
    prompt_for_gpt = "By keeping fields like email, company, website, etc that define a person, as unique always and each generated object should be inspired from a different country also no two consecutive object should be inspired from same country, generate ",count," more objects similar to the sample object like ",sample," by understanding what each key in the object means and what value is expected for each key, act like the faker library. RETURN DATA AS ARRAY OF OBJECTS JSON FORMAT, ALSO CHECK HISTORY AND DONT GENERATE SIMILAR VALUES IN ATLEAST 10 CONSECUTIVE ITERATIONS"
    print('Gemini In Action!')
    resp = getResponseFromAI(prompt_for_gpt)
    json_response = json.dumps(resp)
    print('Gemini Responded!')
    return json_response

# sample = {'name': 'Lucas', 'Id': '6FGU890128', 'email': 'lucas@microsoft.com', 'company': 'microsoft', 'website': 'microsoft.com', 'Status': True, 'address': {'city': 'bangalore', 'pincode/zipcode': 560010}}
# sample =  "{\n    \"name\": \"Samuel\",\n    \"Id\": \"6FGU890300\",\n    \"email\": \"samuel@google.com\",\n    \"company\": \"google\",\n    \"website\": \"google.com\",\n    \"Status\": False,\n    \"address\": {\n      \"city\": \"mumbai\",\n      \"pincode/zipcode\": 560011\n    }\n  }"
# count = 5
# prompt_for_gpt = "By keeping fields like email, company, website, etc that define a person, as unique always and each generated object should be inspired from a different country also no two consecutive object should be inspired from same country, generate ",count," more objects similar to the sample object like ",sample," by understanding what each key in the object means and what value is expected for each key, act like the faker library. RETURN DATA AS ARRAY OF OBJECTS JSON FORMAT, ALSO CHECK HISTORY AND DONT GENERATE SIMILAR VALUES IN ATLEAST 10 CONSECUTIVE ITERATIONS"
# print(dataAsString(sample,count))