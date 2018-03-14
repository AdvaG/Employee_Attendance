#to work on:
# clear input of new employee once you click the add button
# output msg that the data was added/deleted etc.
# reports output on the GUI
# reports between dates
# errors

import datetime
import time
import csv


main_employees_file = "Employees.csv"
main_attendance_log_file = "Attendance_log.csv"

class Employee:
    def __init__(self):
        self.ID = 0
        self.name = ""
        self.phone = 0
        self.age = 0
        self.attendance = []

    def get_employee_details_manually(self):
        # gets employee's details from the user
        input_string = "Please enter the new employee's "
        self.ID = input(input_string + "ID: ")
        self.name = input(input_string + "name: ")
        self.phone = input(input_string + "phone#: ")
        self.age = input(input_string + "age: ")
        self.check_new_employee()

    def check_new_employee(self):
        try:
            self.ID = int(self.ID)
        except ValueError as e:
            print(e)
        try:
            self.age = int(self.age)
            if self.age < 0:
                raise ValueError('%s is not a valid age. Age must be positive or zero, please check the file' % self.age)
        except ValueError as e:
            print('%s is not a valid age, please check the file' % self.age)

    def get_employee_details_from_file(self, employee_to_get_file, line_index=0):
        #gets employee's details from a file
        with open(employee_to_get_file, 'r') as employees_to_add_file_open:
            #self.ID, self.name, self.phone, self.age = employees_to_add_file_open.readlines()[line_index].split(", ") ### with txt file
            self.ID, self.name, self.phone, self.age = employees_to_add_file_open.readlines()[line_index].split(",")
        self.check_new_employee()
        return self.ID, self.name, self.phone, self.age

    def add_employee_to_file(self, line_index=0, *employees_to_add_file):
        #checks if a file of new employees has provided. if not, the user enters the details manually.
        #adds 1 employee
        if employees_to_add_file:
            self.get_employee_details_from_file(str(employees_to_add_file[0]), line_index)
        else:
            self.get_employee_details_manually()
        self.enter_employee_to_Employees_file()
        print("Employee %s was added to the Employees file." %self.ID)

    def enter_employee_to_Employees_file(self):
        #enters employee to the main employees file
        with open(main_employees_file, 'a', newline='') as employees_file_write_open:
            #employees_file_write.writelines([str(self.ID) + ", " + self.name + ", " + self.phone + ", " + str(self.age) + "\n"])### for txt files
            employees_file_writer = csv.writer(employees_file_write_open, delimiter=',')
            employees_file_writer.writerow([self.ID, self.name, self.phone, self.age])

class Employees_attendance_management:

    # The class maintain the employees list
    # Handles cases of insertion or deletion a group of employees using a file
    def __init__(self):
        self.employees_dict = self.init_employee_dict_from_employees_file_and_attendance_file()

    def init_employee_dict_from_employees_file_and_attendance_file(self):
        # initialize and updates the list of employees from the main employees file --> uses to build the dictionary
        num_lines = sum(1 for line in open(main_employees_file))
        employees_dict = {}
        for line_index in range(num_lines):
            employee = Employee()
            employee.get_employee_details_from_file(main_employees_file, line_index)
            employee.check_new_employee()
            employees_dict[employee.ID] = employee
        num_lines = sum(1 for line in open(main_attendance_log_file))
        for line_index in range(num_lines):
            attendance = Attendance()
            attendance.get_attendance_from_log_by_line_index(line_index)
            attendance.ID = int(attendance.ID)
            attendance.name = attendance.name[:-1]
            employees_dict[attendance.ID].attendance.append([attendance.date, attendance.time])
        return employees_dict

    def add_employees_from_file(self, new_employees_file):
        num_lines = sum(1 for line in open(new_employees_file))
        for line_index in range(num_lines):
            employee = Employee()
            employee.add_employee_to_file(line_index, new_employees_file)
            self.employees_dict[employee.ID] = employee

    def update_main_employees_file(self):
        #updates the main employees file with current employees dict
        for key, value in self.employees_dict.items():
            self.employees_dict[key].enter_employee_to_Employees_file()

    def delete_employee_from_dict_and_main_file(self, employee_to_delete_ID):
        #deletes employee records from employees dictionary and the main employees file
        if self.is_employee_exist(employee_to_delete_ID):
            del self.employees_dict[employee_to_delete_ID]
            open(main_employees_file, 'w').close()
            self.update_main_employees_file()
            print("Employee %s was deleted from file" %employee_to_delete_ID)
        else:
            print('Employee %s is not in the employees list' %employee_to_delete_ID)

    def delete_employee_from_file(self, employees_ID_to_delete_file):
        #gets file with employees IDs to delete
        with open(employees_ID_to_delete_file, 'r') as employee_file_open:
            employees_ID_to_delete = employee_file_open.read().splitlines()
        for employee_ID in employees_ID_to_delete:
            self.delete_employee_from_dict_and_main_file(int(employee_ID))

    def is_employee_exist(self,employee_ID_to_search):
        if employee_ID_to_search in self.employees_dict.keys():
            return True
        else:
            return False

class Attendance:
    def __init__(self):
        self.ID = 0
        self.name = ''
        self.date = ''
        self.time = ''

    def new_attendance(self, employees_dict):
        if self.ID == 0:
            self.ID = int(input("Please enter your employee ID: "))
        self.date = datetime.date.today().strftime("%d/%m/%Y")
        self.time = time.strftime("%H:%M")
        self.name = employees_dict[self.ID].name
        self.enter_new_attendance_to_attendance_file_and_employees_dict(employees_dict)

    def enter_new_attendance_to_attendance_file_and_employees_dict(self, employees_dict):
        with open(main_attendance_log_file, 'a', newline='') as attendance_log_file_write_open:
            #attendance_log_file_write.writelines([str(self.date) + ", " + str(self.time) + ", " + str(self.ID) + ", " + self.name + "\n"]) ###for txt files
            attendance_log_file_writer = csv.writer(attendance_log_file_write_open, delimiter=',')
            attendance_log_file_writer.writerow([self.date, self.time, self.ID, self.name])
        employees_dict[self.ID].attendance.append([str(self.date), self.time])
        print("Attendance was entered to the system:\n" + str(self.date) + ", " + str(self.time) + ", " + str(self.ID) + ", " + self.name)

    def get_attendance_from_log_by_line_index(self, line_index):
        with open(main_attendance_log_file, 'r') as attendance_log_file_open:
            #self.date, self.time, self.ID, self.name = attendance_log_file_open.readlines()[line_index].split(", ")### for txt files
            self.date, self.time, self.ID, self.name = attendance_log_file_open.readlines()[line_index].split(",") ###for csv files
        return self.date, self.time, int(self.ID), self.name[:-1]

class Attendance_reports:
    def __init__(self, employees_dict):
        self.employees_dict = employees_dict

    def attendance_report_for_employee(self, employee_ID_for_report):
        for attendance_index in range(len(self.employees_dict[employee_ID_for_report].attendance)):
            print(self.employees_dict[employee_ID_for_report].attendance[attendance_index])

    def attendance_report_for_month(self):
        today = datetime.date.today()
        first = today.replace(day=1)
        last_month_month = (first - datetime.timedelta(days=1)).month
        last_month_year = (first - datetime.timedelta(days=1)).year
        for key, employee in self.employees_dict.items():
            for attendance_index in range(len(employee.attendance)):
                attendance_date = time.strptime(employee.attendance[attendance_index][0],"%d/%m/%Y")
                if attendance_date.tm_mon == last_month_month and attendance_date.tm_year == last_month_year:
                    print(employee.ID, employee.name, employee.attendance[attendance_index][0], employee.attendance[attendance_index][1])

    def attendance_report_for_late_employees(self):
        late_hour = datetime.time(9,30)
        for key, employee in self.employees_dict.items():
            for attendance_index in range(len(employee.attendance)):
                attendance_time = time.strptime(employee.attendance[attendance_index][1],"%H:%M")
                if (attendance_time.tm_hour, attendance_time.tm_min) >= (late_hour.hour, late_hour.minute):
                    print(employee.ID, employee.name, employee.attendance[attendance_index][0], employee.attendance[attendance_index][1])


from tkinter import *
from tkinter import ttk
from tkinter import filedialog

buttonHeight = 1
buttonWidth = 15


class EAMS_start_GUI(Frame):
    #Employee_attendance_management_system_GUI
    def __init__(self, parent):
        self.employees_attendance_management = Employees_attendance_management()
        self.employees_dict = self.employees_attendance_management.init_employee_dict_from_employees_file_and_attendance_file()
        self.attendance_reports = Attendance_reports(self.employees_dict)
        self.parent = parent

        Frame.__init__(self, parent)
        self.grid()
        self.__init_start_UI()

    def __init_start_UI(self):
        self.parent.title("Employee attendance management system")

        self.startLabel = Label(self, text="Enter as:")
        self.startLabel.grid(column=0, row=0, padx=10, pady=10)

        self.employeeButton = Button(self, text="Employee", height=buttonHeight, width=buttonWidth, command=self.open_employee_UI)
        self.employeeButton.grid(column=0, row=2, padx=10, pady=10)#, sticky=N)

        self.managerButton = Button(self, text="Manager", height=buttonHeight, width=buttonWidth, command=self.open_manager_UI)
        self.managerButton.grid(column=1, row=2, padx=10, pady=10)#, sticky=N)

    def open_employee_UI(self):
        self.employeeWindow = Toplevel(self.parent)
        self.app = EAMS_employee_GUI(self.employeeWindow, self.employees_attendance_management, self.employees_dict)

    def open_manager_UI(self):
        self.managerWindow = Toplevel(self.parent)
        self.app = EAMS_manager_GUI(self.managerWindow, self.employees_attendance_management, self.attendance_reports)

class EAMS_employee_GUI(Frame):
    def __init__(self, parent, employees_attendance_management, employee_dict):
        self.employees_attendance_management = employees_attendance_management
        self.employee_dict = employee_dict
        self.parent = parent

        Frame.__init__(self, parent)
        self.grid()
        self.__init_employee_UI()

    def __init_employee_UI(self):
        self.parent.title("Employee attendance management system")

        #self.employeeFrame = Frame(self, width=200, height=100)
        #self.employeeFrame.grid()#column=0, row=0, columnspan=5, rowspan=3)

        self.newAttendanceFrame = LabelFrame(self, text="Enter attendance:", relief='groove', borderwidth=2)
        self.newAttendanceFrame.grid(column=0, row=0, padx=10, pady=10, rowspan=3, columnspan=3)

        self.newAttendanceID = StringVar()
        self.IDEntryLabel = Label(self.newAttendanceFrame, text="ID:")
        self.IDEntryLabel.grid(column=0, row=1, stick=E, padx=10, pady=10)
        self.IDEntry = Entry(self.newAttendanceFrame, textvariable=self.newAttendanceID)
        self.IDEntry.grid(column=1, row=1, padx=10, pady=10)

        self.enterAttendanceButton = Button(self.newAttendanceFrame, text="Add attendance", height=buttonHeight, width=buttonWidth, command=self.enter_attendance)
        self.enterAttendanceButton.grid(column=1, row=2, padx=10, pady=10)

    def enter_attendance(self):
        attendance = Attendance()
        attendance.ID = int(self.newAttendanceID.get())
        attendance.new_attendance(self.employee_dict)

class EAMS_manager_GUI(Frame):
    def __init__(self, parent, employees_attendance_management, attendance_reports):
        self.employees_attendance_management = employees_attendance_management
        self.employees_dict = self.employees_attendance_management.init_employee_dict_from_employees_file_and_attendance_file()
        self.attendance_reports = attendance_reports
        self.parent = parent

        Frame.__init__(self, parent)
        self.grid()
        self.__init_manager_UI()

    def __init_manager_UI(self):
        self.parent.title("Employee attendance management system")

        ####Add new employee
        self.newEmployeeFrame = LabelFrame(self, text="Enter new employee details:", relief='groove', borderwidth=2)#, text="Enter new employee details:")
        self.newEmployeeFrame.grid(column=0, row=0, padx=10, pady=10, rowspan=3, columnspan=3)

        self.newEmployeeID = StringVar()
        self.IDEntryLabel = Label(self.newEmployeeFrame, text="ID:")
        self.IDEntryLabel.grid(column=0, row=1, stick=E, padx=10, pady=10)
        self.IDEntry = Entry(self.newEmployeeFrame, textvariable=self.newEmployeeID)
        self.IDEntry.grid(column=1, row=1, padx=10, pady=10)

        self.newEmployeeName = StringVar()
        self.nameEntryLabel = Label(self.newEmployeeFrame, text="Name:")
        self.nameEntryLabel.grid(column=0, row=2, stick=E, padx=10, pady=10)
        self.nameEntry = Entry(self.newEmployeeFrame, textvariable=self.newEmployeeName)
        self.nameEntry.grid(column=1, row=2, padx=10, pady=10)

        self.newEmployeePhone = StringVar()
        self.phoneEntryLabel = Label(self.newEmployeeFrame, text="Phone:")
        self.phoneEntryLabel.grid(column=0, row=3, stick=E, padx=10, pady=10)
        self.phoneEntry = Entry(self.newEmployeeFrame, textvariable=self.newEmployeePhone)
        self.phoneEntry.grid(column=1, row=3, padx=10, pady=10)

        self.newEmployeeAge = StringVar()
        self.ageEntryLabel = Label(self.newEmployeeFrame, text="Age:")
        self.ageEntryLabel.grid(column=0, row=4, stick=E, padx=10, pady=10)
        self.ageEntry = Entry(self.newEmployeeFrame, textvariable=self.newEmployeeAge)
        self.ageEntry.grid(column=1, row=4, padx=10, pady=10)

        self.saveNewEmployeeButton = Button(self.newEmployeeFrame, text="Save new employee", height=buttonHeight, width=buttonWidth, command=self.save_new_employee)
        self.saveNewEmployeeButton.grid(column=0, row=5, padx=10, pady=10)

        self.findFileToAddButton = Button(self.newEmployeeFrame, text="Add from file", height=buttonHeight, width=buttonWidth, command=self.find_file_to_add)
        self.findFileToAddButton.grid(column=1, row=5, padx=10, pady=10)

        ####Delete employee
        self.deleteEmployeeFrame = LabelFrame(self, text="Delete employee:", relief='groove', borderwidth=2)
        self.deleteEmployeeFrame.grid(column=0, row=6, padx=10, pady=10, rowspan=3, columnspan=3)

        self.deleteEmployeeID = StringVar()
        self.IDEntryLabel = Label(self.deleteEmployeeFrame, text="ID:")
        self.IDEntryLabel.grid(column=0, row=7, stick=E, padx=10, pady=10)
        self.IDEntry = Entry(self.deleteEmployeeFrame, textvariable=self.deleteEmployeeID)
        self.IDEntry.grid(column=1, row=7, padx=10, pady=10)

        self.deleteEmployeeButton = Button(self.deleteEmployeeFrame, text="Delete employee", height=buttonHeight, width=buttonWidth, command=self.delete_Employee)
        self.deleteEmployeeButton.grid(column=0, row=8, padx=10, pady=10)

        self.findFileToDeleteButton = Button(self.deleteEmployeeFrame, text="From file", height=buttonHeight, width=buttonWidth, command=self.find_file_to_delete)
        self.findFileToDeleteButton.grid(column=1, row=8, padx=10, pady=10)

        ###Reports
        self.reportsFrame = LabelFrame(self, text="Reports:", relief='groove', borderwidth=2)
        self.reportsFrame.grid(column=0, row=9, padx=10, pady=10, rowspan=3, columnspan=3)

        self.comboValue = StringVar()
        self.reportsCombo = ttk.Combobox(self.reportsFrame, values=("report by employee ID", "last month report", "late employees report"), textvariable=self.comboValue)
        self.reportsCombo.grid(column=0, row=10, padx=10, pady=10)
        self.reportsCombo.bind("<<ComboboxSelected>>", self.combo_choice)

        self.printReportButton = Button(self.reportsFrame, text="Print report", height=buttonHeight, width=buttonWidth, command=self.print_report)
        self.printReportButton.grid(column=1, row=10, padx=10, pady=10)

        reportEmployeeID = StringVar()
        self.reportIDLabel = Label(self.reportsFrame, text="ID:")
        self.reportIDEntry = Entry(self.reportsFrame, textvariable=reportEmployeeID)

    def save_new_employee(self):
        newEmployee = Employee()
        newEmployee.ID = self.newEmployeeID.get()
        newEmployee.name = self.newEmployeeName.get()
        newEmployee.phone = self.newEmployeePhone.get()
        newEmployee.age = self.newEmployeeAge.get()
        newEmployee.check_new_employee()
        newEmployee.enter_employee_to_Employees_file()

    def find_file_to_add(self):
        file_to_add = filedialog.askopenfile().name
        self.employees_attendance_management.add_employees_from_file(file_to_add)

    def delete_Employee(self):
        employee_ID_to_delete = int(self.deleteEmployeeID.get())
        self.employees_attendance_management.delete_employee_from_dict_and_main_file(employee_ID_to_delete)

    def find_file_to_delete(self):
        file_to_delete = filedialog.askopenfile().name
        self.employees_attendance_management.delete_employee_from_file(file_to_delete)


    def print_report(self):
        if self.comboValue.get() == 'report by employee ID' and self.reportIDEntry.get() != "":
            self.attendance_reports.attendance_report_for_employee(int(self.reportIDEntry.get()))
        elif self.comboValue.get() == 'last month report':
            self.attendance_reports.attendance_report_for_month()
        elif self.comboValue.get() == 'late employees report':
            self.attendance_reports.attendance_report_for_late_employees()

    def combo_choice(self, event):
        if self.comboValue.get() == 'report by employee ID':
            self.reportIDLabel.grid(column=0, row=11, sticky=W, padx=10, pady=10)
            self.reportIDEntry.grid(column=0, row=11, sticky=E, padx=10, pady=10)
        elif self.comboValue.get() != 'report by employee ID':
            self.reportIDLabel.grid_forget()
            self.reportIDEntry.grid_forget()



root = Tk()
app = EAMS_start_GUI(root)
root.mainloop()

