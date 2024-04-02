# hIngE
### Product Vision Statement
  To make meeting people easier 
  
  - [Overview](#Overview)
  - [What is this project about?](#Whatisthisprojectabout?)
  - [Objectives](#Objectives)
  - [Keyresults](#KRs)
  - [Structure](#Structure)
  - [Setup](#Setup)
  - [CodeExplanation](#Code)
  - [Tests](#Tests)



## Overview
<img width="560" alt="Screenshot 2024-04-02 at 22 54 01" src="https://github.com/Chatbots-RecAgents/chatbots/assets/145041682/31ac7923-97e2-4279-8e1d-cae491c14454">



## What is this project about?
  First of all, the goal of our project is to connect people. Meeting new people can be a problem for a lot of people around the world, which is why we created this product. How does it work? The user starts by communicating with the chatbot. The goal of the chatbot is to humanise the process where the user enters their data. The user will type in their answers normally. After that, the data will be sent to a recommendation engine. The recommendation engine will take all the info the user gave to the chatbot, and recommend other users who share similarities to the user.


## Objectives and Key Results
### Objectives
   * Facilitate communication and socialisation between users
   * Allow users to speak to a chatbot to facilitate giving information
   * Connecting like-minded people
### KRs:
   * Making the webapp easily accessible through the internet
   * Maintaining recommendation speed
   * Correctly processing data given to the chatbot(bot to csv, csv to reco, reco to bot)
   * Restricting chatbot abilities to stay in context


## Structure
* .github: CI/CD with GitHub Actions. It runs the tests every time there is a pull request to the repository, and everytime someone pushes their codes.
* docs: Documentation of the project
* tests: Python tests completed using PyTest. 
* Firebase: Hosting the databse on Firebase and using it as a general dataset for all users

## Setup
* Will revisit when we continue with the project

## Code
### Chatbot creation
  We will be using the streamlit and the openai API to create a chatbot. Our chatbot is limited: the questions we want to ask stay as they are. We create a list of these questions, and have our chatbot iterate through them. We utilise the openai API when the chatbot reacts to the user responses.

  To summarise: The chatbot asks questions to the user from the list. The user responds with info. The chatbot reacts to that info without asking any more questions. After the chatbot reaction, the next question from the list gets asked. This helps in humanising the process.  
  
### Data Processing
  The data will be taken from the csv file, and will go through an EDA process. After the EDA process, it will be fed into a recommendation engine. After that, the engine will send the user the recommendations
  
### Recommendation Engine
  Cosine similarity is a measure used to determine how similar two vectors are irrespective of their size. It calculates the cosine of the angle between the two vectors.

# Test
  Using pytest, we created a unit test for the save_to_csv function. This will test how this function enters the data into the csv file
  More tests will come later

## To run the hIngE:
1. Do: 'pip install .' in the root directory to install all libraries
2. Change directories into chatbot
3. Run streamlit (streamlit run app.py)
