import json
import boto3
from boto3.dynamodb.conditions import Key

# LOADING THE SERVICES.
__tablename__ = 'DoctorInfo'
db = boto3.resource('dynamodb',region_name='eu-west-1')
client_lex = boto3.client('lex-runtime',region_name='eu-west-1')
table = db.Table(__tablename__)
#------------------------------------------------------------------------------#

# Defining the function to pick closest pincode.
def pincode_Distance(pincode_area,arr_pincode):
    
    sqr_arr_diff = []
    for i in range(len(arr_pincode)):
        diff = (int(arr_pincode[i]) - pincode_area)**2
        sqr_arr_diff.append(diff)
    max_elem = max(sqr_arr_diff)
    max_elem_index = sqr_arr_diff.index(max_elem)
    return max_elem_index

#------------------------------------------------------------------------------#

#Function to create the card for the greetings intent.
def greetings_intent(event):
    
    #CREATING THE PRIMARY KEY NAME AND NUMBER.
    primary_column_key = 'S.No'
    primary_key = '1'
    
    department = event["currentIntent"]["slots"]["Department"]
    age = event["currentIntent"]["slots"]["Age"]
    
    response = table.query(
        IndexName='Department-index',
        KeyConditionExpression=Key('Department').eq(department)
        )
    
    if int(age) <= 18:
        department = "Pediatrician"
    
    return_statement = { 
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": "The department to refer is " + department 
            },
            "responseCard": {
              "version":"1",
              "contentType": "application/vnd.amazonaws.card.generic",
              "genericAttachments": [
                  {
                     "title":"Doctor in Gurugram:",
                     "subTitle":department,
                     "buttons":[

                     ]
                  },
                  {
                      "title":"Doctor in Noida:",
                      "subTitle":department,
                      "buttons":[
                          
                      ]
                  },
                  {
                      "title":"Doctor in Ghaziabad:",
                      "subTitle":department,
                      "buttons":[
                          
                    
                      ]
                  }
              ] 
            }
         }
    }
    return_statement = json.dumps(return_statement)
    return_statement = json.loads(return_statement)
    
    for i in range(len(response['Items'])):
        dict_ = {'text':response['Items'][i]['Name'],"value": response['Items'][i]['Name']}
        dict_ = json.dumps(dict_)
        dict_ = json.loads(dict_)
        if response['Items'][i]['Area'] == 'Gurugram':
            return_statement["dialogAction"]["responseCard"]["genericAttachments"][0]["buttons"].append(dict_)
        elif response['Items'][i]['Area'] == 'Noida':
            return_statement["dialogAction"]["responseCard"]["genericAttachments"][1]["buttons"].append(dict_)
        elif response['Items'][i]['Area'] == 'Ghaziabad':
            return_statement["dialogAction"]["responseCard"]["genericAttachments"][2]["buttons"].append(dict_)
        else:pass
    
    return return_statement
#------------------------------------------------------------------------------#    

#Creating function for the BookAnAppointment Intent.
def bookappointment(event):
    
    response = None
    
    if event["currentIntent"]["slots"]["Confirmation_Status"] == None:
        
        greetings_sess = client_lex.get_session(
            botName=event["bot"]["name"],
            botAlias=event["bot"]["alias"],
            userId=event["userId"]
            )
        
        for i in range(len(greetings_sess["recentIntentSummaryView"])):
            
            if greetings_sess["recentIntentSummaryView"][i]["intentName"] == "Greetings":
                department = greetings_sess["recentIntentSummaryView"][i]["slots"]["Department"]
                response = table.query(
                IndexName='Department-index',
                    KeyConditionExpression=Key('Department').eq(department)
                )
            
        doctor_name = event["currentIntent"]["slots"]["Doctor_Name"]
        doctor_info_list = []
        doctor_pincode_list = []
        
        for j in range(len(response['Items'])):
            
            if response['Items'][j]['Name'] == doctor_name:
                doctor_info_list.append(response['Items'][j])
                doctor_pincode_list.append(int(response['Items'][j]['Pincode']))
        
        if len(doctor_info_list) >= 2 :
            
            patient_pincode = greetings_sess["recentIntentSummaryView"][i]["slots"]["Pincode"]
            patient_pincode = int(patient_pincode)
            doc_index = pincode_Distance(patient_pincode,doctor_pincode_list)
            
            info_str = "{0} works in {1} and the opd days for the doctor are {2}\nThe timings are : {3}\n Do you want to make an appointment with {4} ?".format(
                doctor_info_list[doc_index]["Name"],
                doctor_info_list[doc_index]["Hospital"],
                doctor_info_list[doc_index]["OPD_Days"],
                doctor_info_list[doc_index]["Timings"],
                doctor_info_list[doc_index]["Name"]
                )
                
            return_statement ={             
                    "dialogAction": { 
                        
                        "type": "ElicitSlot",
                        "intentName": "BookAnAppointment",
                        "slotToElicit":"Confirmation_Status",
                        "slots":{
                          "Doctor_Name":doctor_name
                        },
                        "message": {
                            "contentType": "PlainText", 
                            "content": info_str   
                    }
                }
            }
            
            return return_statement
            
        else:
            
            info_str = "{0} works in {1} and the opd days for the doctor are {2}\nThe timings are : {3}\n Do you want to make an appointment with {4} ?".format(
                doctor_info_list[0]["Name"],
                doctor_info_list[0]["Hospital"],
                doctor_info_list[0]["OPD_Days"],
                doctor_info_list[0]["Timings"],
                doctor_info_list[0]["Name"]
                )
                
            return_statement ={             
                    "dialogAction": { 
                        
                        "type": "ElicitSlot",
                        "intentName": "BookAnAppointment",
                        "slotToElicit":"Confirmation_Status",
                        "slots":{
                          "Doctor_Name":doctor_name
                        },
                        "message": {
                            "contentType": "PlainText", 
                            "content": info_str   
                    }
                }
            }
            
            return return_statement
            
    elif event["currentIntent"]["slots"]["Confirmation_Status"] != None and event["currentIntent"]["slots"]["opd_days"] == None and event["currentIntent"]["slots"]["User_time"] == None:   
            return_statement ={             
                    "dialogAction": { 
                        
                        "type": "ElicitSlot",
                        "intentName": "BookAnAppointment",
                        "slotToElicit":"opd_days",
                        "slots":{
                          "Doctor_Name":event["currentIntent"]["slots"]["Doctor_Name"],
                          "Confirmation_Status":event["currentIntent"]["slots"]["Confirmation_Status"]
                        },
                        "message": {
                            "contentType": "PlainText", 
                            "content": "Which day is comfortable with the patient ?"  
                    }
                }
            }
            
            return return_statement
            
    elif event["currentIntent"]["slots"]["Confirmation_Status"] != None and event["currentIntent"]["slots"]["opd_days"] != None and event["currentIntent"]["slots"]["User_time"] == None:
        return_statement ={             
            "dialogAction": { 
                        
                "type": "ElicitSlot",
                "intentName": "BookAnAppointment",
                "slotToElicit":"User_time",
                "slots":{
                    "Doctor_Name":event["currentIntent"]["slots"]["Doctor_Name"],
                    "Confirmation_Status":event["currentIntent"]["slots"]["Confirmation_Status"],
                    "opd_days": event["currentIntent"]["slots"]["opd_days"]
                    },
                    "message": {
                        "contentType": "PlainText", 
                        "content": "What time is comfortable with you with reference to the OPD Timings ?"   
                    }
                }
            }
            
        return return_statement
    
    elif event["currentIntent"]["slots"]["Confirmation_Status"] != None and event["currentIntent"]["slots"]["opd_days"] != None and event["currentIntent"]["slots"]["User_time"] != None and event["currentIntent"]["confirmationStatus"] == "None":
        
        result = "Appointment for {0} on {1} at {2}?".format(
            event["currentIntent"]["slots"]["Doctor_Name"],
            event["currentIntent"]["slots"]["opd_days"],
            event["currentIntent"]["slots"]["User_time"]
            )
        return_statement ={             
            "dialogAction": { 
                "type": "ConfirmIntent",
                "intentName": "BookAnAppointment",
                "slots":{
                    "Doctor_Name":event["currentIntent"]["slots"]["Doctor_Name"],
                    "Confirmation_Status":event["currentIntent"]["slots"]["Confirmation_Status"],
                    "opd_days": event["currentIntent"]["slots"]["opd_days"],
                    "User_time":event["currentIntent"]["slots"]["User_time"]
                    },"responseCard": {
                 "genericAttachments": [
                {
                    "buttons": [
                        {
                            "text": "Yes",
                            "value": "yes"
                        },
                        {
                            "text": "No",
                            "value": "no"
                        }
                    ],
                    "subTitle": result,
                    "title": "Confirm Appointment"
                }
            ],
                "version": 1,
                "contentType": "application/vnd.amazonaws.card.generic"
                }
            }
        }
        return return_statement
    
    elif event["currentIntent"]["slots"]["Confirmation_Status"] != None and event["currentIntent"]["slots"]["opd_days"] != None and event["currentIntent"]["slots"]["User_time"] != None and event["currentIntent"]["confirmationStatus"] == "Confirmed":
        return_statement = {
            "dialogAction": {
                "type": "Close",
                "message": {
                    "content": "Okay, I have booked your appointment.  Thank you for you co-operation. Get well soon !",
                    "contentType": "PlainText"
                },
                "fulfillmentState": "Fulfilled"
            }
        }
        
        return return_statement
    
    elif event["currentIntent"]["slots"]["Confirmation_Status"] != None and event["currentIntent"]["slots"]["opd_days"] != None and event["currentIntent"]["slots"]["User_time"] != None and event["currentIntent"]["confirmationStatus"] == "Denied":
        return_statement = {
            "dialogAction": {
                "type": "Close",
                "message": {
                    "content": "Okay. It was nice talking to you !",
                    "contentType": "PlainText"
                },
                "fulfillmentState": "Fulfilled"
            }
        }
        
        return return_statement

#------------------------------------------------------------------------------#

def lambda_handler(event, context):

    
    if event["currentIntent"]["name"] == 'Greetings':
        
        return_statement1 = greetings_intent(event)
        return return_statement1
    
    elif event["currentIntent"]["name"] == 'BookAnAppointment' and event["invocationSource"] == "DialogCodeHook":
        
        return_statement2 = bookappointment(event)
        return return_statement2
    
        
#------------------------------------------------------------------------------#