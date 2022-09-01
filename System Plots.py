import matplotlib.pyplot as plt

#1.Hospital Occupancy by Covid patients:
fig = plt.figure()
Hospital_Occupancy_BarChart = fig.add_axes([0,0,1,1])
Hospital_Name = [""]
Num_Covid_patients = []
Hospital_Occupancy_BarChart.bar(Hospital_Name,Num_Covid_patients)
Hospital_Occupancy_BarChart.set_ylabel('severity status of each patient')
Hospital_Occupancy_BarChart.set_title('A single bar chart illustrating the number of patients with Covid in each of the 3 hospitals in each of the states')
plt.show()

#2. Severity of cases

severity_status_Toronto = []
severity_status_Hamilton = []
severity_status_Kingston = []

nine_time_points = []   #not sure if it meant time series of what exactly

fig=plt.figure()
Severity_Of_Cases_Scatter =fig.add_axes([0,0,1,1])
Severity_Of_Cases_Scatter.scatter(nine_time_points, severity_status_Toronto , color='r')
Severity_Of_Cases_Scatter.scatter(nine_time_points, severity_status_Hamilton, color='b')
Severity_Of_Cases_Scatter.scatter(nine_time_points, severity_status_Kingston, color='y')
Severity_Of_Cases_Scatter.set_xlabel('9 time point')  #not sure if it meant time series of what exactly
Severity_Of_Cases_Scatter.set_ylabel('Severity Status of Hospitals')
Severity_Of_Cases_Scatter.set_title('Scatter plot illustrating the severity status of each patient')
Severity_Of_Cases_Scatter.legend()
plt.show()

