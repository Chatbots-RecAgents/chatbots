# We will create a client object using the OpenAI api to make requests
# For this we need to use the keys so that is is authenticated and charges can be made

import os
from openai import OpenAI

# These keys is needed to "login" and "authenticate"
# Read keys so they are not written in the code

#Both keys are not generated yet. 
#This is a skeleton of how the openai API works and how we can make the user interact with it
filename = 'api_key.txt'
with open(filename, 'r') as file: 
    api_key = file.read().strip() #apikey
    
filename = 'api_org.txt'
with open(filename, 'r') as file:
    api_key2 = file.read().strip() #organization
    
myclient = OpenAI(api_key = api_key, organization=api_key2)

# Lets get an answer?
while True:
    # Let's get an answer
    q = input('What do you want to know: ')

    if not q:
        # If the user doesn't input anything, exit the loop
        break

    ans = myclient.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": q}
        ]
    )

    print(ans['choices'][0]['message']['content'])