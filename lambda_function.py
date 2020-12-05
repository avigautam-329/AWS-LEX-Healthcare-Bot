import json
import boto3
from boto3.dynamodb.conditions import Key

# LOADING THE SERVICES.
__tablename__ = 'DoctorInfo'
db = boto3.resource('dynamodb',region_name='eu-west-1')
client_lex = boto3.client('lex-runtime',region_name='eu-west-1')
table = db.Table(__tablename__)
#------------------------------------------------------------------------------#

# Defining the function to pick closest pincode incase of overlap in doctor names.
def pincode_Distance(pincode_area,arr_pincode):
    
    sqr_arr_diff = []
    for i in range(len(arr_pincode)):
        diff = (int(arr_pincode[i]) - pincode_area)**2
        sqr_arr_diff.append(diff)
    max_elem = max(sqr_arr_diff)
    max_elem_index = sqr_arr_diff.index(max_elem)
    return max_elem_index

#------------------------------------------------------------------------------#

#Funtion to pick closest Doctors using pincode.
def pincode_reordering(pincode_area,location_arr):
    
    sqr_arr_diff = []
    indexes_arr = []
    
    for i in range(len(location_arr)):
        diff = (int(location_arr[i]) - int(pincode_area))**2
        sqr_arr_diff.append(diff)
        
    max_elem = max(sqr_arr_diff)
    indexes_arr.append(sqr_arr_diff.index(max_elem))
    
    for j in range(len(sqr_arr_diff)-1):
         sqr_arr_diff[indexes_arr[-1]] = -999
         max_elem = max(sqr_arr_diff)
         indexes_arr.append(sqr_arr_diff.index(max_elem))
         
    return indexes_arr

#------------------------------------------------------------------------------#

#Check the opd days.
def check_opddays(user_day,opddays_arr):
    
    count = 0
    for i in range(len(opddays_arr)):
        if user_day == opddays_arr[i]:
            return True
        else:
            count = count + 1
    if count > 0:
        return False
        
#------------------------------------------------------------------------------#

#Function to create the card for the greetings intent.
def greetings_intent(event):
    
    #Creating local variables.
    primary_column_key = 'S.No'
    primary_key = '1'
    noida_docs = []
    gurugram_docs = []
    ghaziabad_docs = []
    noida_indexes = []
    gurugram_indexes = []
    ghaziabad_indexes = []
    
    department = event["currentIntent"]["slots"]["Department"]
    age = event["currentIntent"]["slots"]["Age"]
    pincode_area = event["currentIntent"]["slots"]["Pincode"]
    
    response = table.query(
        IndexName='Department-index',
        KeyConditionExpression=Key('Department').eq(department)
        )
    
    if int(age) <= 18:
        department = "Pediatrician"
        
    for i in range(len(response['Items'])):
        if response['Items'][i]['Area'] == 'Gurugram':
            gurugram_indexes.append(response['Items'][i]['Pincode'])
            gurugram_docs.append(response['Items'][i])
        elif response['Items'][i]['Area'] == 'Noida':
            noida_indexes.append(response['Items'][i]['Pincode'])
            noida_docs.append(response['Items'][i])
        elif response['Items'][i]['Area'] == 'Ghaziabad':
            ghaziabad_indexes.append(response['Items'][i]['Pincode'])
            ghaziabad_docs.append(response['Items'][i])
        else:pass
    
    noida_indexes = pincode_reordering(pincode_area,noida_indexes)
    gurugram_indexes = pincode_reordering(pincode_area,gurugram_indexes)
    ghaziabad_indexes = pincode_reordering(pincode_area,ghaziabad_indexes)    
    
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
    
    for i in range(len(gurugram_docs)):
        ind = gurugram_indexes[i]
        dict_ = {'text':gurugram_docs[ind]['Name'],"value": gurugram_docs[ind]['Name']}
        dict_ = json.dumps(dict_)
        dict_ = json.loads(dict_)        
        return_statement["dialogAction"]["responseCard"]["genericAttachments"][0]["buttons"].append(dict_)
        
    for i in range(len(noida_docs)):
        ind = noida_indexes[i]
        dict_ = {'text':noida_docs[ind]['Name'],"value": noida_docs[ind]['Name']}
        dict_ = json.dumps(dict_)
        dict_ = json.loads(dict_)
        return_statement["dialogAction"]["responseCard"]["genericAttachments"][1]["buttons"].append(dict_)

    for i in range(len(ghaziabad_docs)):
        ind = ghaziabad_indexes[i]
        dict_ = {'text':ghaziabad_docs[ind]['Name'],"value": ghaziabad_docs[ind]['Name']}
        dict_ = json.dumps(dict_)
        dict_ = json.loads(dict_)
        return_statement["dialogAction"]["responseCard"]["genericAttachments"][2]["buttons"].append(dict_)
        
    
    return return_statement
#------------------------------------------------------------------------------#    

#Creating function for the BookAnAppointment Intent.
def bookappointment(event):
    
    response = None
    opddays_arr = []
    
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
            opddays_arr = str(doctor_info_list[doc_index]["OPD_Days"]).split(",")
            
            info_str = "{0} works in {1} , {2} and the opd days for the doctor are {3}\nThe timings are : {4}\n Do you want to make an appointment with {5} ?".format(
                doctor_info_list[doc_index]["Name"],
                doctor_info_list[doc_index]["Hospital"],
                doctor_info_list[doc_index]["Area"],
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
            opddays_arr = str(doctor_info_list[0]["OPD_Days"]).split(",")
            info_str = "{0} works in {1} , {2} and the opd days for the doctor are {3}\nThe timings are : {4}\n Do you want to make an appointment with {5} ?".format(
                doctor_info_list[0]["Name"],
                doctor_info_list[0]["Hospital"],
                doctor_info_list[0]["Area"],
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
            if event["currentIntent"]["slots"]["Confirmation_Status"] == "Yes":
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
            elif event["currentIntent"]["slots"]["Confirmation_Status"] == "No":
                
                return_statement ={             
                        "dialogAction": { 
                            
                            "type": "ElicitSlot",
                            "intentName": "BookAnAppointment",
                            "slotToElicit":"Doctor_Name",
                            "slots":{
                            },
                            "message": {
                                "contentType": "PlainText", 
                                "content": "Please choose another doctor to proceed."  
                        }
                    }
                }
                
                return return_statement
                
            
    elif event["currentIntent"]["slots"]["Confirmation_Status"] != None and event["currentIntent"]["slots"]["opd_days"] != None and event["currentIntent"]["slots"]["User_time"] == None:
        
        
        
        if check_opddays(str(event["currentIntent"]["slots"]["opd_days"]),opddays_arr) == False:
        
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
                            "content": "Please choose another day"  
                    }
                }
            }
            
            return return_statement
        
        else:
            
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