### Make friends
#Product Vision Statement
To make meeting people easier 

# Dependencies
In this project, we will be using the OpenAi API, a recommendation engine, and a data processing tool

# OKRs
 * Objectives:
 *   Improve customer satisfaction
 * Key results:
 *   Making the webapp easily accessible
 *   Maintaining recommendation speed
 *   Correctly processing data given to the chatbot


# Structure
* .github: CI/CD with GitHub Actions. It runs the tests every time there is a pull request to the repository, and everytime someone pushes their codes.
* docs: Documentation of the project
* tests: Python tests completed using PyTest
* xxxxxx

# Setup
* Will revisit when we continue with the project

# Code explanation
* Chatbot creation
We will be using the OpenAI API to create a chatbot. The chatbot will ask the user questions, and save their answers into a txt file.
* Data Processing
The data will be taken from the txt file, and will go through an EDA process. After the EDA process, it will be fed into a recommendation engine
* Recommendation Engine
Specifics on this model will be written later. After the data is fed into this model, the model will send the output back to the chatbot which will send it to the user.

# Tests
The tests will be explained as we start the coding foundations
