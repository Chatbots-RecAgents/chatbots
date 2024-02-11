  - [Overview](#Overview)
  - [Dependencies](#Dependencies)
  - [Objectives](#Objectives)
  - [Keyresults](#KRs)
  - [Structure](#Structure)
  - [Setup](#Setup)
  - [CodeExplanation](#Code)
  - [Tests](#Tests)


# Make friends
### Product Vision Statement
  To make meeting people easier 

## Overview
  Eventually add picture of system architecture


## Dependencies
  In this project, we will be using the huggingface for the chatbot, a recommendation engine, and a data processing tool

## Objectives and Key Results
### Objectives
   Improve customer satisfaction
### KRs:
   Making the webapp easily accessible
   Maintaining recommendation speed
   Correctly processing data given to the chatbot


## Structure
* .github: CI/CD with GitHub Actions. It runs the tests every time there is a pull request to the repository, and everytime someone pushes their codes.
* docs: Documentation of the project
* tests: Python tests completed using PyTest
* xxxxxx

## Setup
* Will revisit when we continue with the project

## Code
### Chatbot creation
  We will be using the huggingface to create a chatbot. The chatbot will ask the user questions, and save their answers into a csv file.
### Data Processing
  The data will be taken from the csv file, and will go through an EDA process. After the EDA process, it will be fed into a recommendation engine
### Recommendation Engine
  Specifics on this model will be written later. After the data is fed into this model, the model will send the output back to the chatbot which will send it to the user.
  We are using KNN. More info will come later

# Tests
  The tests will be explained as we start the coding foundations
