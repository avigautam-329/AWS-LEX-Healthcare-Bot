# AWS-LEX-Healthcare-Bot

![AWS LEX BADGE](https://img.shields.io/badge/AWS%20-Lex-orange)
![AWS LAMBDA BADGE](https://img.shields.io/badge/AWS%20-lambda-orange)
![AWS DYNAMO DB](https://img.shields.io/badge/AWS%20-DyanmoDB-blue)
![Python Badge](https://img.shields.io/badge/Python-v3.7.8-yellowgreen)
![Python Boto3](https://img.shields.io/badge/Boto3-v1.15.12-lightgrey)
![Python Json](https://img.shields.io/badge/Json-v.2.0.9-lightgrey)
![Python aws-cli](https://img.shields.io/badge/aws--cli-v1.18.153-lightgrey)
-------------

## What is AWS ?

Amazon Web Services (AWS) is the world's most comprehensive and broadly adopted cloud platform, offering over 175 fully featured services from data centers globally.
-------------

### What all services are used in this project ?

- **AWS LEX** - Amazon Lex is a service for building conversational interfaces into any application using voice and text. With Amazon Lex, you can build bots to increase contact centre productivity, automate simple tasks, and drive operational efficiencies across the enterprise. The two main components of AWS LEX are:
    - _Intents_:  An intent represents an action that the user wants to perform.
    - _Slots_: For each intent, you can specify parameters that indicate the information that the intent needs to fulfill the user's request. These parameters, or slots, have a type. A slot type is a list of values that Amazon Lex uses to train the machine learning model to recognize values for a slot.
- **AWS LAMBDA** - AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the underlying compute resources for you. The Lambda function is written in Python language.
- **DYNAMO DB** - Amazon DynamoDB is a key-value and document database that delivers single-digit millisecond performance at any scale. It's a fully managed, multi-region, multi-active, durable database with built-in security, backup and restore, and in-memory caching for internet-scale applications.

### What is the motivation behind the project ?

This project was created while doing an intership at _DCM InfoTech_. The chatbot was created in order to provide medical services to people sitting at home in these troubling times and help them find a doctor suitable to their requirenments and book an appointment using the chatbot.

### How do all the services work together ?

![Flow of AWS](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/ServicesUsage.png)

- **User** - The user interacts with the AWS Lex bot and starts the conversation by using the Sample Utterances to invoke the intent "**_Greetings_**".And the user further converses with the bot to feed it information about the patient or user. Based on the information the lex bot further computes which medical department does the user need to refer to.
![Greetings Fullfilment](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Greetings/SampleUtterances.png)

- **Lex** - The Lex bot has 2 intents namely **_Greetings_** and **_BookAnAppointment_**. The first intent to get invoked is "**Greetings**".
    - _Greetings_ : The main job of this intent is to know the details of the patient and try to detect the medical Department that the user needs to refer to based on the answers given by the user.
    - _BookAnAppointment_ : The main job of this intent is to Book the appointemnt for the user after the user has choosen the doctor they want to see.

- **Lambda** - Lambda is an integeral part of this project as it has the job of fetching the data from the DynamoDB based on the medical Department inferred by the bot. The other main part of the lambda function is to determine the flow of the conversation and handling the intent switching. The lambda function is written in **Python** and The **IAM Roles** given to the lambda function are:
![IAM Roles](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/IAM_ROLES/IamRoles.png)

- **DynamoDB** - It is the database that is used to store the information about the doctors and which area are they based in. Soo , There are three main regions _Gurugram_,_Noida_ and _Ghaziabad_. There are 10 medical departments which are :
    - Cardiology
    - Dermatology
    - General Surgery
    - Gynecology
    - Neurology
    - Oncology
    - Opthamology
    - Orthopedics
    - Pedriatics
    - Physician
Each department has information about 10 doctors distributed across the three regions.
![DynamoDB](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/DynamoDB/TablePic.png)

**The index used to search the DynamoDB are:**
![DynamoDB-Indexes](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/DynamoDB/IndexesPic.png) 

### Slots and Slotypes used in AWS Lex 

