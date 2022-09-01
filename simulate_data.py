import datetime
import patient_management_system



date = datetime.date.today()

date += datetime.delta(days=1)


'''To initiate hospital beds to be 0 at the beginning,initial_hospital_state.csv data should be taken and the value for 
ICU bed should be empty'''
'''A dictionary of the list of patients and their severity indicates the starting point of the patients coming in'''

listofpatientID ={"805c":2, "718p":2, "667g":0, "259m":2, "565f":2, "516c":3, "740r":2, "936v":1, "130t":3, "082f":0,
                  "503i":0, "761c":0, "989z":1, "457z":2, "444k":1, "707d":0, "811r":0, "432w":0, "997h":1, "541d":3}

ICU_capacity = {"Kingston":0, "Ottawa":0, "Hamilton":0}

patients_kingston = {"516c":3, "740r":2, "936v":1, "082f":0, "457z":2, "444k":1, "432w":0,}
patients_toronto = {"565f":2, "503i":0, "541d":3}
patients_hamilton = {"805c":2, "718p":2, "667g":0, "259m":2, "130t":3, "761c":0, "989z":1, "707d":0, "811r":0, "997h":1}

#1. loop for Each hospital only to admit one patient to the ICU every 7 days, except Toronto which admits 1 every 4 days
def ICU_count_7(city_patients):

    for i in range(0,91,7):
        for key in city_patients:
            pass
#range loop to count 7 days for 90 days?

def ICU_count_4():
    for i in range (0,91,4):
        pass
#range loop to count 4 days for 90 days?
'''we would need to call the function from the other file to admit the patient (using instance attribute?)'''

#2. condition to discharge Patients automatically discharged when their severity status reaches 0
def patient_status():
    pass
'''we would need to call the function from the other file to remove the patient (using instance attribute?)'''
#3. drop patient severity status from 3 to 2 after 5 days of admission if severity is 3 and 3 days if condition is 2 to 1 and only 1 day if their condition is 1 and is dropping to 0

#4. If a patient must be transferred, they are transferred to the hospital with the most available ICU beds. (use transfer function onlnew hospitalName has more ICU beds available then initial hospital
'''use transfer function from the other file?'''

#5.