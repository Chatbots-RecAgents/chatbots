# hIngE
### Product Vision Statement
  To make meeting people easier 
  
  - [Overview](#Overview)
  - [Dependencies](#Dependencies)
  - [Objectives](#Objectives)
  - [Keyresults](#KRs)
  - [Structure](#Structure)
  - [Setup](#Setup)
  - [CodeExplanation](#Code)
  - [Tests](#Tests)



## Overview
  Eventually add picture of system architecture


## Dependencies
  In this project, we will be using the streamlit for the chatbot, a recommendation engine using cosine similarity, and a data processing tool

## Objectives and Key Results
### Objectives
   * Improve customer satisfaction
   * Facilitate communication and socialisation between users
### KRs:
   * Making the webapp easily accessible through the internet
   * Maintaining recommendation speed
   * Correctly processing data given to the chatbot(bot to csv, csv to reco, reco to bot)


## Structure
* .github: CI/CD with GitHub Actions. It runs the tests every time there is a pull request to the repository, and everytime someone pushes their codes.
* docs: Documentation of the project
* tests: Python tests completed using PyTest. One unit test alread is running, while testing the way the chatbot takes the data to the csv
* xxxxxx

## Setup
* Will revisit when we continue with the project

## Code
### Chatbot creation
  We will be using the streamlit and langchain to create a chatbot. The chatbot will ask the user questions, and save their answers into a csv file. The goal is to have the chatbot also give a natural reaction to all the answers given bh the users
### Data Processing
  The data will be taken from the csv file, and will go through an EDA process. After the EDA process, it will be fed into a recommendation engine. After that, the engine will send the user the recommendations
### Recommendation Engine
  Cosine similarity is a measure used to determine how similar two vectors are irrespective of their size. It calculates the cosine of the angle between the two vectors.

# Test
  Using pytest, we created a unit test for the save_to_csv function. This will test how this function enters the data into the csv file
  More tests will come later

## For the chatbot:
1. Install llama-cpp-python
2. Install langchain
3. Install streamlit
4. Run streamlit (streamlit run main.py)

Also make sure to work using a venv. 
