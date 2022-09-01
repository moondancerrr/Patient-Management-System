# Group 3 Project
# Student Name & ID: Hannah Driver (10090525), Sarah Salloum (20368321), Suruthy Sivanathan (20368339), Wenhuan Zhu (20368341)
# Program: Part 1 Patient Management System: Creating a hospital management system with patients and hospitals, and
#                                            allowing users to alter the patients in the system.

import pandas as pd
from collections import namedtuple
import csv


# class to make each patient an object with their attributes
class Patient:
    """A class that represents the patients in the hospital system"""

    def __init__(self, patientID, hospitalName, sevStatus, covidPositive):
        self.patientID = patientID
        self.sevStatus = sevStatus
        self.covidPositive = covidPositive
        self.hospitalName = hospitalName
        self.lengthOfStay = 0
        self.insystem = True  # true if patient is in the system, false if patient has been discharged


class Hospital:
    """A class that represents the hospitals in the hospital system"""
    def __init__(self, name, ICUCapacity):
        self.bedsFilled = 0
        self.name = name
        self.ICUCapacity = ICUCapacity


class ManagementSystem:
    """A class that allows patients and hospitals within the system to be manipulated"""
    def __init__(self):
        self.hospitals = {"Kingston": Hospital("Kingston", 8), "Ottawa": Hospital("Ottawa", 17),
                          "Toronto": Hospital("Toronto", 20)}
        self.patients = []

    def addPatient(self, hospitalName, sevStatus, covidPositive):
        """
        add patient to hospital system
        :param hospitalName: name of hospital to add patient to
        :param sevStatus: severity status of patient
        :param covidPositive: True if patient is positive for covid, False otherwise
        :return: True if patient was successfully added to the system, False otherwise
        """
        check_hospital_capacity = self.checkHospitalCapacities(hospitalName)
        if check_hospital_capacity == False:
            print("\nSorry {} currently has no beds available.".format(hospitalName))
            self.displayAvailableHospitals()
            return False
        else:
            patient_ID = self.generatePatientID()
            new_patient = Patient(patient_ID, hospitalName, sevStatus, covidPositive)
            self.patients.append(new_patient)
            hospital = self.hospitals[hospitalName]
            hospital.bedsFilled += 1
            return True

    def transferPatient(self, patientID, currentHospitalName, newHospitalName):
        """
        transfer a patient within the hospital system
        :param patientID: ID of the patient to be transferred
        :param currentHospitalName: name of the hospital the patient is currently in
        :param newHospitalName: name of the hospital the patient is being transferred to
        :return: True if patient was successfully transferred to the system, False otherwise
        """
        capacity_check = self.checkHospitalCapacities(newHospitalName)
        if capacity_check == False:
            print("\nSorry {} currently has no beds available.".format(newHospitalName))
            self.displayAvailableHospitals()
            return False
        else:
            old_hospital = self.hospitals[currentHospitalName]
            old_hospital.bedsFilled -= 1
            new_hospital = self.hospitals[newHospitalName]
            new_hospital.bedsFilled += 1
            for patient in self.patients:
                if patient.patientID == patientID:
                    patient.hospitalName = newHospitalName
            return True

    def updateStatus(self, patientID, newStatus):
        """
        update a patient's severity status
        :param patientID: ID of the patient to be transferred
        :param newStatus: new patient severity score
        :return: True if patient was successfully updated to the system, False otherwise
        """
        for patient in self.patients:
            if patient.patientID == patientID:
                patient.sevStatus = newStatus
        return True

    def setInitialStateFromCSV(self, csv_df):
        """
        set up management system with the patients that are currently in hospital
        :param csv_df: a dataframe with information about the patients' IDs, hospital names, severity statuses, and covid statuses
        """
        initial_list_of_patients = [Patient(patient.Patient_ID, patient.Hospital, int(patient.Status), patient.Covid_Positive) for patient in csv_df.itertuples()]
        for patient in initial_list_of_patients:
            self.patients.append(patient)
            patient_hospital = patient.hospitalName
            hospital = self.hospitals[patient_hospital]
            hospital.bedsFilled += 1

    def checkHospitalCapacities(self, hospital_name):
        """
        check whether beds are available within a hospital
        :param hospital_name: the name of the hospital to check
        :return: False if there are no beds available
        """
        hospital = self.hospitals[hospital_name]
        available_beds = hospital.ICUCapacity - hospital.bedsFilled
        if available_beds == 0:
            return False

    def displayAvailableHospitals(self):
        """
        display the beds available in each hospital
        :return: a print statement indicating the beds available in each hospital in the system
        """
        current_beds_available = {}
        Kingston_hospital = self.hospitals["Kingston"]
        Ottawa_hospital = self.hospitals["Ottawa"]
        Toronto_hospital = self.hospitals["Toronto"]
        list_of_hospitals = [Kingston_hospital, Ottawa_hospital, Toronto_hospital]
        current_beds_available = []
        for hospital in list_of_hospitals:
            beds_available = hospital.ICUCapacity - hospital.bedsFilled
            current_beds_available.append(beds_available)
        print("Kingston has {} beds available, Ottawa has {} beds available, and Toronto has {} beds available.\n".format(current_beds_available[0], current_beds_available[1], current_beds_available[2]))

    def generatePatientID(self):
        """
        generate IDs for new patients
        :return: a 3-number, 1-letter ID for the patient
        """
        list_of_patient_IDs = []
        for patient in self.patients:
            list_of_patient_IDs.append(patient.patientID)
        number1 = 0
        patientIDmatch = True
        while patientIDmatch == True:
            while number1 <= 9:
                number2 = 0
                while number2 <= 9:
                    number3 = 0
                    while number3 <= 9:
                        letter = "a"
                        while letter <= "z":
                            temp_patientID = str(number1) + str(number2) + str(number3) + str(letter)
                            if temp_patientID in list_of_patient_IDs:
                                    letter = chr(ord(letter) + 1)
                            else:
                                patientIDmatch = False
                                patientID = temp_patientID
                                list_of_patient_IDs.append(patientID)
                                return patientID
                        number3 += 1
                    number2 += 1
                number1 += 1

    def dischargePatient(self, patientID, patientHospital):
        """
        remove a patient from the hospital system
        :param patientID: ID of the patient being discharged
        :param patientHospital: name of hospital patient being discharged is currently in
        :return: True if patient was successfully discharged
        """
        #remove one bed from the hospital
        hospital = self.hospitals[patientHospital]
        hospital.bedsFilled -= 1
        #remove patient
        for patient in self.patients:
            if patient.patientID == patientID:
                self.patients.remove(patient)
        return True


def userAction():
    """
    input function for user to let the program know what action they would like to take
    :return: the inputted user string
    """
    """ask the user what they want? exit, add, update, discharge or transfer"""
    user_action = input("Would you like to Add, Transfer, Update or Discharge a patient? (note: you may also type 'Exit' to exit the program) ")
    return user_action.lower()


def getHospital(task):
    """
    input function to get the name of a hospital from the user
    :param task: the task the user wants to execut (add, transfer, update, discharge)
    :return: the inputted user string with a hospital name
    """
    name_of_hospital = False
    while name_of_hospital == False:
        hospital_name = input("Would you like to {} your patient to 'Kingston', 'Ottawa', or 'Toronto' hospital? ".format(task))
        if hospital_name.lower() == "kingston" or hospital_name.lower() == "ottawa" or hospital_name.lower() == "toronto":
            name_of_hospital = True
        else:
            print("That is not a valid hospital name.\n")
    return hospital_name.title()

def getSeverity(lower_bound):
    """
    input function to get the severity of a patient from the user
    :param lower_bound: the lowestr value the patient severity can be
    :return: the patient's severity value as an integer
    """
    severity_input = False
    while severity_input == False:
        patient_severity = input("How severe is your patient on a scale of {}-3? ".format(lower_bound))
        try:
            int(patient_severity)
            if lower_bound <= int(patient_severity) <= 3:
                severity_input = True
            else:
                print("The patient's severity value must be between {} and 3, inclusive.\n".format(lower_bound))
        except:
            print("The patient's severity value must be an integer between {} and 3, inclusive.\n".format(lower_bound))
    return int(patient_severity)


def getCovidStatus():
    """
    input function to get a patient's covid status from the user
    :return: True if the patient is covid positive, False otherwise
    """
    covid_input = False
    while covid_input == False:
        covid_input = input("Does your patient have covid, 'yes' or 'no'? ")
        if covid_input.lower() == "yes":
            covid_input = True
            return True
        elif covid_input.lower() == "no":
            covid_input = True
            return False
        else:
            print("I don't understand. You must input 'yes' or 'no'.\n")
            covid_input = False


def addPatient(management_system):
    """
    adding a patient to the management system
    :param management_system: the instance of the Management System the patient is being added to
    """
    # get hospital from user
    patient_hospital = getHospital("add")
    # get severity from user
    patient_severity = getSeverity(1)
    # get covid status from user
    patient_covid = getCovidStatus()
    # call management system's add patient function
    adding_patient = management_system.addPatient(patient_hospital, patient_severity, patient_covid)
    if adding_patient == True:
        print("Your patient has been successfully added.\n")

def findNewTransfer(management_system, current_hospital):
    """
    find a new patient to transfer if the original patient to transfer is too unstable
    :param management_system: the instance of the Management System the patient is being added to
    :param current_hospital: the hospital the original patient to transfer is in
    :return: the ID of the patient in the current hospital that has the lowest severity status
    """
    lowest_severity = 0
    while lowest_severity < 3:
        for patient in management_system.patients:
            if patient.sevStatus == lowest_severity:
                if patient.hospitalName == current_hospital:
                    correct_input = False
                    while correct_input == False:
                        want_to_transfer = input(
                            "Patient {} is stable enough to transfer. Would you like to transfer them instead (yes or no)? ".format(
                                patient.patientID))
                        if want_to_transfer.lower() == "no":
                            print("Okay.\n")
                            correct_input = True
                            return False
                        elif want_to_transfer.lower() == "yes":
                            correct_input = True
                            lowest_severity = 3
                            return patient.patientID
                        else:
                            print("I don't understand. Please type 'yes' or 'no'.")
        lowest_severity += 1


def transferPatient(management_system):
    """
    transferring a patient in the management system
    :param management_system: the instance of the Management System the patient is being added to
    """
    #get patient ID
    patient_to_transfer = getPatientID(management_system, "transfer")
    #get patient hospital
    for patient in management_system.patients:
        if patient.patientID == patient_to_transfer:
            current_hospital = patient.hospitalName
    #get severity status of patient
    patient_severity = checkSeverity(patient_to_transfer, management_system)
    if patient_severity == 3:
        print("Sorry, patient {} is too unstable to transfer.\n".format(patient_to_transfer))
        patient_to_transfer = findNewTransfer(management_system, current_hospital)

    if patient_to_transfer != False:
        #get hospital they want to transfer to
        hospital_to_transfer_to = getHospital("transfer")
        #call transfer function
        transferring_patient = management_system.transferPatient(patient_to_transfer, current_hospital, hospital_to_transfer_to)
        if transferring_patient == True:
            print("Patient {} has been successfully transferred.\n".format(patient_to_transfer))


def getPatientID(management_system, task):
    """
    get the ID of the patient the user wants to alter
    :param management_system: the instance of the Management System the patient is being added to
    :param task: the task the user wishes to perform (add, transfer, update, or discharge)
    :return: the string ID of the patient the user wishes to alter
    """
    list_of_patients = []
    for patient in management_system.patients:
        list_of_patients.append(patient.patientID)
    input_patientID = input("What is ID of the patient that you want to {}? ".format(task))
    ID_input = False
    while ID_input == False:
        for patient in management_system.patients:
            if input_patientID in list_of_patients:
                ID_input = True
                return input_patientID
            else:
                print("\nThat patient is not in our system. Please choose a patient from the following list:\n{}\n.".format(list_of_patients))
                input_patientID = input("What is ID of the patient that you want to {}? ".format(task))

def updatePatient(management_system):
    """
    updating the severity status of a patient in the management system
    :param management_system: the instance of the Management System the patient is being added to
    """
    verified_patientID = getPatientID(management_system, "update")
    new_severity = getSeverity(0)
    updating_patient = management_system.updateStatus(verified_patientID,new_severity)
    if updating_patient == True:
        print("Patient {} has been successfully updated.\n".format(verified_patientID))

def checkSeverity(patientID, management_system):
    """
    check the current severity status of a patient
    :param patientID: the ID of the patient who's severity status should be checked
    :param management_system: the instance of the Management System the patient is being added to
    :return: the severity value for the patient
    """
    for patient in management_system.patients:
        if patient.patientID == patientID:
            patient_severity = patient.sevStatus
    return patient_severity

def dischargePatient(management_system):
    """
    discharging a patient from the management system
    :param management_system: the instance of the Management System the patient is being discharged from
    """
    verified_patientID = getPatientID(management_system, "discharge")
    # get hospital from user
    for patient in management_system.patients:
        if patient.patientID == verified_patientID:
            patient_hospital = patient.hospitalName
    # get severity from user
    patient_severity = checkSeverity(verified_patientID, management_system)
    if patient_severity == 0:
    # call management system's remove patient function
        discharging_patient = management_system.dischargePatient(verified_patientID, patient_hospital)
        if discharging_patient == True:
            print("Patient {} has been successfully discharged\n.".format(verified_patientID))
    else:
        print("Sorry patient {} is too unstable to discharge.\n".format(verified_patientID))


def printCSV(management_system):
    """
    print the current state of the management system to a csv file
    :param management_system: the instance of the Management System the patient is being added to
    :return: a csv file
    """
    with open('final_hospital_state.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        header = namedtuple('Patient', ['Patient_ID', 'Hospital', 'Status', 'Covid_Positive'])
        writer.writerow(header._fields)
        for patient in management_system.patients:
            writer.writerow([patient.patientID, patient.hospitalName, patient.sevStatus, patient.covidPositive])


def main():
    """
    This function creates an instance of a hospital management system, including both the hospitals and the patients
    within it. Users are able to add new patients to the system, update patient severity statuses, transfer patients
    to other hospitals, or discharge patients.
    """
    system_state = ManagementSystem()
    # Read in the csv file with the initial state
    csv_file = pd.read_csv("C:/Users/User/Documents/Biomedical_Informatics/BMIF801/initial_hospital_state.csv")
    system_state.setInitialStateFromCSV(csv_file)
    # Ask user what action to take
    user_action = userAction()
    # while user input != exit continue to ask for actions (like above)
    while user_action != "exit":
        if user_action == "add":
            addPatient(system_state)
            printCSV(system_state)
        elif user_action == "transfer":
            transferPatient(system_state)
            printCSV(system_state)
        elif user_action == "update":
            updatePatient(system_state)
            printCSV(system_state)
        elif user_action == "discharge":
            dischargePatient(system_state)
            printCSV(system_state)
        else:
            print("I don't understand. Please type: 'Add', 'Transfer', 'Update', or 'Discharge'\n")
        user_action = userAction()

    print("Thank you, have a nice day!")


if __name__ == "__main__":
    main()