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

## Slots and Slotypes used in AWS Lex 

- **Greetings** : The slots and slotypes in this intent used are:
    - _FirstName_ : This is the slot that asks and stores the first name of the patient. The SlotType used here is **amazon.us_first_name** which is a built in slot type in amazon lex.
    - _LastName_ : This is the slot that asks and stores the last name of the patient. The SlotType used here is **amazon.us_last_name** which is a built in slot type in aws lex.
    - _Age_ : This stores the age of the patient and uses a custom SlotType **AgeGroups**.![Age Groups](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Greetings/AgeGroups.png)
    - _Department_ : This computes the medical Department based on the symptoms given by the user. It uses a custom SlotType **DepartmentName**. The synonyms contains the common symptoms for each department and these symptoms are written in layman language for the ease of the user/patient.
    <p float="left">
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Greetings/DepartmentName1.png" width="400" />
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Greetings/DepartmentName2.png" width="400" /> 
    </p>

    - _Pincode_ : The pincode contains the pincode of the user's/patient's address soo that these pincodes can be compared with the pincode of the hospital to reorder the listings of the the doctors with respect to the hospitals closest to them.It uses the custom built slotTyoe **Pincode_Area**.                     ![Pincode slot](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Greetings/Pincode_Area.png)
![Greetings Slots](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Greetings/SlotAndSlotTypes.png)

- **BookAnAppointment** : This is the intent that comes after the _Greetings_ intent. After the Greetings intent is complete , It shows a response Card that contains the names of the doctors differenciated according to the regions and the closest distance. And this intent will wait for the user to choose a doctor from the list in the response card.![BookAnAppoinmtment utterances](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/BookAnAppointment/SampleUtterances.png)The slot and slotTypes used are :
    - *Doctor_Name* : This slot is responsible for waiting for the selection of the doctor and storing the name of the doctor for further use in the currentIntent. It uses a custom built slotType **Doctor_Name**.
    ![DoctorName slot](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/BookAnAppointment/Doctor_Name.png) 
    - *Confirmation_Status* : This slot takes in the confirmation in yes or no after showing more information about the doctor that has been choosen by the patient. It uses a custom built slotType **Confirmation_status**.
    ![Confirmation_status slot](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/BookAnAppointment/Confirmation_Status.png)
    - *opd_days* : This contains the day chosen by the user with refernce to the OPD Dyas of the doctor. This uses a custom built slotType called **OPD_Days**.
    ![OPD_Days slot](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/BookAnAppointment/OPD_Days.png)
    - *User_time* : This contains the time chosen by the user with refernce to the timeing of the doctor's OPD. It uses a custom built slotType called **User_Time**.
    <p float="left">
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/BookAnAppointment/User_time1.png" width="400" />
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/BookAnAppointment/User_time2.png" width="400" /> 
    </p>

![BookAnAppoinmtment slotTypes](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/BookAnAppointment/SlotAndSlotTypes.png)

## Lambda Function and it's Usage

Lambda function is used in this project to incorporate different services of AWS , In this case I have used Lambda for 2 main reasons :
- First one is to use the Department inferred by the bot to fetch the data from the DynamoDB table called **DoctorInfo**.
- Secondly, It is used to govern the flow of theconversation and error handling.

The lambda function works on the basis of the currentIntent and the event json passed by the lex bot to the Lambda function. **Eg. of event json is**:

```
{
    "messageVersion": "1.0",
    "invocationSource": "FulfillmentCodeHook",
    "userId": "wch89kjqcpkds8seny7dly5x3otq68j3",
    "bot": {
        "name": "HealthCareBot",
        "alias": null,
        "version": "$LATEST"
    },
    "outputDialogMode": "Text",
    "currentIntent": {
        "name": "Greetings",
        "slots": {
            "FirstName": "Avi",
            "LastName": "Gautam",
            "Age": "21",
            "Department": "Cardiologist",
            "Pincode": "110029"
        },
        "confirmationStatus": "None"
    }
}

```
The lambda_handler() function takes in the event and based on the currentIntent it calls the necessary function.

The name of the lambda function used here is **DoctorInfoLambdafunction** .

Now for the intents:
- _Greetings_ : The lambda function is used for fulfillment purporses to show the response card with the names of all the doctors w.r.t the department chosen by the bot.
    - The function used to fetch the data and show the response card is *greetings_intent()*.
![Greetings lambda](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Greetings/Fulfillment.png) 
- _BookAnAppointment_ : Lambda function is used here to fill the slots using **Elicitslot** type . Hence the lambda function is used her in the DialogHook. Hence in this intent lambda function has an integeral function of controlling the flow of the dialogue and also for error handling.
    - The function used to control the flow of the dialog is _bookappointment()_.
    - The in-built function client_lex.get_session used in the function bookappointment() is used to get the information from the previous intent **Greetings**. 
![BookAnAppointment lambda](https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/BookAnAppointment/LambdaValidation.png)

Libraries used in Lambda function are *boto3*,*json* and *aws-cli* .
- **_boto3_** : Boto is the Amazon Web Services (AWS) SDK for Python. It enables Python developers to create, configure, and manage AWS services.
- **_json_** : Json is used here as all the data transmission in aws is done in json format.
- **_aws-cli_** : This package provides a unified command line interface to Amazon Web Services. This library is used to run aws services in the local system after signing in aws console using aws-cli.

## Conversation Screenshots and video presentation

<p float="left">
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Conversations/part-1.png" width="400" />
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Conversations/part-2.png" width="400" />
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Conversations/part-3.png" width="400" />
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Conversations/part-4.png" width="400" />
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Conversations/part-5.png" width="400" />
        <img src="https://github.com/avigautam-329/AWS-LEX-Healthcare-Bot/blob/master/Images/Lex/Conversations/part-6.png" width="400" />  
</p>

***

Thank you for reading this readme. For further information or any queries do contact me!!

Happy coding everyone !

