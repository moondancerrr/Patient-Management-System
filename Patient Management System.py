###

def createHospitals(ICUCapacity):

    class Hospital:
        def __init__(self, ICUCapacity):
            self.bedsFilled = 0
            self.ICUCapacity = ICUCapacity

    hospital = Hospital(ICUCapacity)
    return hospital


def assignPatientID(ListOfPatientIDs):

    number1 = 0
    patientIDmatch = True
    while patientIDmatch == True:
        while number1 <= 9:
            number2 = 0
            while number2 <= 9:
                number3 = 0
                #number2 += 1
                while number3 <= 9:
                    letter = "a"
                    #number3 += 1
                    while letter <= "z":
                        temp_patientID = str(number1)+str(number2)+str(number3)+str(letter)
                        if temp_patientID in ListOfPatientIDs:
                            letter = chr(ord(letter)+1)
                        else:
                            patientIDmatch = False
                            patientID = temp_patientID
                            return patientID
                    number3 += 1
                number2 += 1
            number1 += 1


def ICUBedStatuses():
    global Kingston_Hospital
    global Ottawa_Hospital
    global Toronto_Hospital

    Kingston_beds = Kingston_Hospital.ICUCapacity - Kingston_Hospital.bedsFilled
    Ottawa_beds = Ottawa_Hospital.ICUCapacity - Ottawa_Hospital.bedsFilled
    Toronto_beds = Toronto_Hospital.ICUCapacity - Toronto_Hospital.bedsFilled

    beds_available = "There are currently {} bed(s) available in Kingston, {} bed(s) available in Ottawa, and {} bed(s) available in Toronto.".format(Kingston_beds, Ottawa_beds, Toronto_beds)
    return beds_available


def checkHospitals(hospitalToCheck):
    global Kingston_Hospital
    global Ottawa_Hospital
    global Toronto_Hospital

    if (Kingston_Hospital.ICUCapacity - Kingston_Hospital.bedsFilled == 0) and (Ottawa_Hospital.ICUCapacity - Ottawa_Hospital.bedsFilled == 0) and (Toronto_Hospital.ICUCapacity - Toronto_Hospital.bedsFilled == 0):
        print("Unfortunately there are currently no ICU beds available in any hospitals. Please discharge a patient before adding a new one.")
        return "0 beds"

    hospitalToCheck = hospitalToCheck.title()
    if hospitalToCheck == "Kingston":
        if Kingston_Hospital.ICUCapacity - Kingston_Hospital.bedsFilled > 0:
            Kingston_Hospital.bedsFilled += 1
            return Kingston_Hospital
        else:
            beds_available = ICUBedStatuses()
            print("There are not enough beds to move your patient to the Kingston Hospital. "
                  "Please choose a different hospital.")
            print(beds_available)
            return "not available"
    elif hospitalToCheck == "Ottawa":
        if Ottawa_Hospital.ICUCapacity - Ottawa_Hospital.bedsFilled > 0:
            Ottawa_Hospital.bedsFilled += 1
            return Ottawa_Hospital
        else:
            beds_available = ICUBedStatuses()
            print("There are not enough beds to move your patient to the Ottawa Hospital. "
                  "Please choose a different hospital.") #need to display all beds available in all hospitals
            print(beds_available)
            return "not available"
    elif hospitalToCheck == "Toronto":
        if Toronto_Hospital.ICUCapacity - Toronto_Hospital.bedsFilled > 0:
            Toronto_Hospital.bedsFilled += 1
            return Toronto_Hospital
        else:
            beds_available = ICUBedStatuses()
            print("There are not enough beds to move your patient to the Toronto Hospital. "
                  "Please choose a different hospital.") #need to display all beds available in all hospitals
            print(beds_available)
            return "not available"
    else:
        print("That is not a valid hospital.")
        return False


def checkSeverity(severity_to_check, lower_bound):
    try:
        int(severity_to_check)
        try:
            if lower_bound <= int(severity_to_check) <= 3:
                return True
            else:
                print("The patient's severity must be an integer value in the range {}-3.".format(lower_bound))
                return False
        except ValueError:
            print("You must input a severity value between {} and 3.".format(lower_bound))
            return False
    except ValueError:
        print("You must input an integer value for severity.")
        return False


def checkCovid(patientID, covid_to_check):
    global ListOfPatients

    covid_to_check = covid_to_check.lower()
    if covid_to_check == "yes" or covid_to_check == "no":
        for patient in ListOfPatients:
            if patient.patientID == patientID:
                patient.covidPositive = covid_to_check
    else:
        print("That is not a valid answer.")
        return False


def addPatient(patientID, hospitalName, sevStatus, covidPositive):

    #class to make each patient an object with their attributes
    class Patient:
        """A class that represents the patients in the hospital system"""
        def __init__(self, patientID, hospitalName, sevStatus, covidPositive):
            self.patientID = patientID
            self.sevStatus = sevStatus
            self.covidPositive = covidPositive
            self.hospitalName = hospitalName
            self.lengthOfStay = 0
            self.insystem = True #true if patient is in the system, false if patient has been discharged

    new_patient = Patient(patientID, hospitalName, sevStatus, covidPositive)
    return new_patient


def checkPatientsInSystem(patientList):
    ListOfPatientIDsInSystem = []
    for patient in patientList:
        if patient.insystem == True:
            ListOfPatientIDsInSystem.append(patient.patientID)

    return ListOfPatientIDsInSystem


def transferPatient(patientID, newHospitalName, currentHospitalName):
    global Kingston_Hospital
    global Ottawa_Hospital
    global Toronto_Hospital
    global ListOfPatients

    #Add one bed filled to the hospital the user is being transferred to
    if newHospitalName == Kingston_Hospital:
        Kingston_Hospital.bedsFilled += 1
    elif newHospitalName == Ottawa_Hospital:
        Ottawa_Hospital.bedsFilled += 1
    else:
        Toronto_Hospital.bedsFilled += 1

    #Remove one bed filled from the hospital the user is being transferred from
    if currentHospitalName == Kingston_Hospital:
        Kingston_Hospital.bedsFilled -= 1
    elif currentHospitalName == Ottawa_Hospital:
        Ottawa_Hospital.bedsFilled -= 1
    else:
        Toronto_Hospital.bedsFilled -= 1

    #Find the patient in our list of patients, and update their hospital
    for patient in ListOfPatients:
        if patient.patientID == patientID:
            patient.hospitalName = newHospitalName

    successful_transfer = "Patient {} has been successfully transfered.\n".format(patientID)
    return successful_transfer


def dischargePatient(patientID, currentHospitalName):
    global ListOfPatients

    #Remove one bed filled from the hospital the user is being transferred from
    if currentHospitalName == Kingston_Hospital:
        Kingston_Hospital.bedsFilled -= 1
    elif currentHospitalName == Ottawa_Hospital:
        Ottawa_Hospital.bedsFilled -= 1
    else:
        Toronto_Hospital.bedsFilled -= 1

    #Find the patient in our list of patients, and set them to "not in system"
    for patient in ListOfPatients:
        if patient.patientID == patientID:
            patient.insystem = False

    successful_discharge = "Patient {} has been successfully discharged.\n".format(patientID)
    return successful_discharge


def updateStatus(patientID, newStatus):
    global ListOfPatients

    #Find the patient in our list of patients, and update their severity status
    for patient in ListOfPatients:
        if patient.patientID == patientID:
            patient.sevStatus = newStatus

    successful_update = "Patient {}'s status has been successfully updated.\n".format(patientID)
    return successful_update


def main():

    #Create hospital objects
    global Kingston_Hospital
    Kingston_Hospital = createHospitals(8)
    global Ottawa_Hospital
    Ottawa_Hospital = createHospitals(17)
    global Toronto_Hospital
    Toronto_Hospital = createHospitals(20)

    #Starting list of patient IDs that have been assigned, and list of patients currently in the hospital system
    global ListOfPatientIDs
    ListOfPatientIDs = [] #won't actually start as empty, as we will need to read in the file
    global ListOfPatients
    ListOfPatients = [] #won't actually start as empty, as we will need to read in the file

    #Setting up the user program
    user_input = True

    while user_input == True:
        #Ask the user what action they would like to make
        UserAction = input("Would you like to Add, Transfer, Update or Discharge a patient? ")

        ##Adding a patient
        if UserAction.lower() == "add":
            add_patient = True

            while add_patient == True:

                #Assign the patient an ID
                patientID = assignPatientID(ListOfPatientIDs)
                ListOfPatientIDs.append(patientID) #add the patient to our current list of patients, to avoid giving duplicate IDs
                print("Your patient's ID is: {}.\n".format(patientID))

                #Check which hospital the user wants to add the patient to
                hospital = input("Which hospital would you like to add patient {} to (Kingston, Ottawa, or Toronto)? ".format(patientID))
                hospital_check = checkHospitals(hospital)
                while hospital_check == False or hospital_check == "not available":
                    hospital = input("Would you like to add patient {} to 'Kingston', 'Ottawa', or 'Toronto' hospital? ".format(patientID))
                    hospital_check = checkHospitals(hospital)
                if hospital_check == "no beds":
                    break #or UserAction.lower() != "add"
                else:
                    hospital = hospital_check

                #Check the severity of the patient
                severity = input("On a scale of 1-3, how severe is patient {}? ".format(patientID))
                severity_check = checkSeverity(severity, 1)
                while severity_check == False:
                    severity = input("On a scale of 1-3, how severe is patient {}? ".format(patientID))
                    severity_check = checkSeverity(severity, 1)
                severity = int(severity)

                #Check the covid status of the patient
                covid = input("Does patient {} have covid (yes or no)? ".format(patientID))
                covid_check = checkCovid(patientID, covid)
                while covid_check == False:
                    covid = input("Does patient {} have covid? Please type 'yes' or 'no'. ".format(patientID))
                    covid_check = checkCovid(patientID, covid)

                #Create a new patient object
                new_patient = addPatient(patientID, hospital, severity, covid)

                #Add patient to list of patients currently in system, and let user know the patient was successfully added
                ListOfPatients.append(new_patient)
                print("Thank you, patient {} has been successfully added.\n".format(patientID))

                #End the loop for the add function and let the user pick their next action
                add_patient = False

        ##Transferring a patient
        elif UserAction.lower() == "transfer":

            transfer_patient = True

            #Check which patient the user wants to transfer
            while transfer_patient == True:

                ListOfPatientIDsInSystem = checkPatientsInSystem(ListOfPatients)

                patient_to_transfer = input("{}\nAbove are the IDs of the patients in our system. Which patient would you like to transfer? ".format(ListOfPatientIDsInSystem))
                if patient_to_transfer not in ListOfPatientIDsInSystem:
                    patient_to_transfer = False
                    while patient_to_transfer == False:
                        patient_to_transfer = input("{}\nThat patient is not in our system. Which of the above patients would you like to transfer? ".format(ListOfPatientIDsInSystem))
                        if patient_to_transfer not in ListOfPatientIDsInSystem:
                            patient_to_transfer = False

                #Find the current hospital and current severity status for this patient
                for patient in ListOfPatients:
                    if patient.patientID == patient_to_transfer:
                        current_hospital = patient.hospitalName
                        current_severity = patient.sevStatus

                #Deny transfer if patient's severity is 3
                if current_severity == 3:
                    print("Sorry, patient {} is too unstable to trasnfer.\n".format(patient_to_transfer))

                    lowest_severity = 0
                    while lowest_severity < 3:
                        for patient in ListOfPatients:
                            if patient.sevStatus == lowest_severity:
                                if patient.insystem == True:
                                    if patient.hospitalName == current_hospital:
                                        correct_input = False
                                        while correct_input == False:
                                            want_to_transfer = input("Patient {} is stable enough to transfer. Would you like to transfer them instead (yes or no)? ".format(patient.patientID))
                                            if want_to_transfer.lower() == "no":
                                                print("Okay.")
                                                correct_input = True
                                                transfer_patient = False
                                            elif want_to_transfer.lower() == "yes":
                                                correct_input = True
                                                lowest_severity = 3
                                                patient_to_transfer = patient.patientID
                                            else:
                                                print("I don't understand. Please type 'yes' or 'no'.")
                        lowest_severity += 1

                                #else:
                                    #print("Unfortunately, there are currently no patients in this hospital that are stable enough to transfer.")
                                    # patient_found = False


                # Check which hospital the user wants to add the patient to
                hospital = input("Which hospital would you like to add patient {} to (Kingston, Ottawa, or Toronto)? ".format(patient_to_transfer))
                hospital_check = checkHospitals(hospital)
                while hospital_check == False or hospital_check == "not available":
                    hospital = input("Would you like to add patient {} to 'Kingston', 'Ottawa', or 'Toronto' hospital? ".format(patient_to_transfer))
                    hospital_check = checkHospitals(hospital)
                if hospital_check == "no beds":
                    break  # or UserAction.lower() != "transfer"
                else:
                    new_hospital = hospital_check

                #Transfer the patient and let user know it was successful
                transferring_patient = transferPatient(patient_to_transfer, new_hospital, current_hospital)
                print(transferring_patient)

                #End the loop for the transfer function and let the user pick their next action
                transfer_patient = False

        ##Updating a patient's status
        elif UserAction.lower() == "update":
            update_status = True

            while update_status == True:
                ListOfPatientIDsInSystem = checkPatientsInSystem(ListOfPatients)

                patient_to_update = input(
                    "{}\nAbove are the IDs of the patients in our system. Which patient would you like to update? ".format(
                        ListOfPatientIDsInSystem))

                if patient_to_update not in ListOfPatientIDsInSystem:
                    patient_to_update = False
                    while patient_to_update == False:
                        patient_to_update = input("{}\nThat patient is not in our system. Which of the above patients would you like to transfer? ".format(ListOfPatientIDsInSystem))
                        if patient_to_update not in ListOfPatientIDsInSystem:
                            patient_to_update = False

                #Get new severity status from user
                new_patient_severity = input("On a scale of 0-3, what is the new severity status for patient {}? ".format(patient_to_update))
                severity_check = checkSeverity(new_patient_severity, 0)
                while severity_check == False:
                    new_patient_severity = input("On a scale of 0-3, how severe is patient {}? ".format(patient_to_update))
                    severity_check = checkSeverity(new_patient_severity, 0)
                new_patient_severity = int(new_patient_severity)

                #Update patient status and let user know the update was successful
                updating_status = updateStatus(patient_to_update, new_patient_severity)
                print(updating_status)

                #End the loop for the update function and let the user pick their next action
                update_status = False

        ##Discharging a patient
        elif UserAction.lower() == "discharge":
            discharge_patient = True

            while discharge_patient == True:
                ListOfPatientIDsInSystem = checkPatientsInSystem(ListOfPatients)

                patient_to_discharge = input("{}\nAbove are the IDs of the patients in our system. Which patient would you like to discharge? ".format(ListOfPatientIDsInSystem))

                ###Need to fix the below block of code. Could run into an infinite loop if there are no patients to transfer
                if patient_to_discharge not in ListOfPatientIDsInSystem:
                    patient_to_discharge = False
                    while patient_to_discharge == False:
                        patient_to_discharge = input("{}\nThat patient is not in our system. Which of the above patients would you like to transfer? ".format(ListOfPatientIDsInSystem))
                        if patient_to_discharge not in ListOfPatientIDsInSystem:
                            patient_to_discharge = False

                for patient in ListOfPatients:
                    if patient.patientID == patient_to_discharge:
                        patient_severity = patient.sevStatus
                        patient_hospital = patient.hospitalName

                if patient_severity != 0:
                    print("Patient {} is not stable enough to discharge.".format(patient_to_discharge)) #Should probably show a list of patients that can be discharged
                else:
                    patient_discharge = dischargePatient(patient_to_discharge, patient_hospital)
                    print(patient_discharge)

                #End the loop for the discharge function and let the user pick their next action
                discharge_patient = False

        #Exiting the program
        elif UserAction.lower() == "exit":
            print("Thank you. Have a nice day!")
            user_input = False

        #Invalid entry for a user action
        else:
            print("{} is not valid. Please type 'Add', 'Transfer', 'Update', or 'Discharge' to make changes, or type 'Exit' to exit the program.".format(UserAction))


#Start the program
main()