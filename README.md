# hIngE
### Product Vision Statement
  To make meeting people easier 
  
  - [Overview](#Overview)
  - [About](#About)
  - [Objectives](#Objectives)
  - [Keyresults](#KRs)
  - [Structure](#Structure)
  - [CodeExplanation](#Code)
  - [Tests](#Tests)
  - [Run](#Run)



## Overview
<img width="560" alt="Screenshot 2024-04-02 at 22 54 01" src="https://github.com/Chatbots-RecAgents/chatbots/assets/145041682/31ac7923-97e2-4279-8e1d-cae491c14454">



## About
What is this project about?
  First of all, the goal of our project is to connect people. Meeting new people can be a problem for a lot of people around the world, which is why we created this product. How does it work? The user starts by communicating with the chatbot. The goal of the chatbot is to humanise the process where the user enters their data. The user will type in their answers normally. After that, the data will be sent to a recommendation engine. The recommendation engine will take all the info the user gave to the chatbot, and recommend other users who share similarities to the user.


## Objectives and Key Results
### Objectives
   * Facilitate communication and socialisation between users
   * Allow users to speak to a chatbot to facilitate giving information
   * Connecting like-minded people
### KRs:
   * Making the webapp easily accessible through the internet
   * Maintaining recommendation speed
   * Correctly processing data given to the chatbot
   * Restricting chatbot abilities to stay in context


## Structure
* .github: CI/CD with GitHub Actions. It runs the tests every time there is a pull request to the repository, and everytime someone pushes their codes.
* docs: Documentation of the project
* tests: Python tests completed using PyTest. 
* dataset: The dataset used was retrieved from Kaggle. it is a dataset about friends


## Code
### Chatbot creation
  We will be using the streamlit and the openai API to create a chatbot. Our chatbot is limited: the questions we want to ask stay as they are. We create a list of these questions, and have our chatbot iterate through them. We utilise the openai API when the chatbot reacts to the user responses. Also, we used a GRU layer to better understand the context and perform sentiment analysis to better understand the user

  To summarise: The chatbot asks questions to the user from the list. The user responds with info. The chatbot reacts to that info without asking any more questions. After the chatbot reaction, the next question from the list gets asked. This helps in humanising the process.  

### The Data 
  The data is collected from a dataset on Kaggle. The dataset was too big to upload to github, but the link can be found below:
https://www.kaggle.com/datasets/subhamyadav580/dating-site


### EDA
  During the EDA process, the data goes several steps:
  1. Removing Duplicate rows
  2. Encoding categorical data (one-hot encoding for Gender and label encoding for the rest of the categorical variables)
  3. Build the model using lightgbm. 
  
### Recommendation Engine
  For the recommendation engine we decided to use a LightGBM model, and another 

# Test
  Using pytest, we created unit tests for both folders chatbot and chatlib. Unit tests are essential to ensure a good code quality

## Run:
This will help you in running our project
1. Do: 'pip install .' in the root directory to install all libraries
2. Change directories into chatbot
3. Run streamlit (streamlit run gru_app.py)

[chatbot_rating · Streamlit.pdf](https://github.com/Chatbots-RecAgents/chatbots/files/14933471/chatbot_rating.Streamlit.pdf)


