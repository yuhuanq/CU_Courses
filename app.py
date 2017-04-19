#cu_courses.py
#Imani Chilongani
#!/usr/bin/env python
"""
cu_courses is a module that checks Cornell University student center
for any open spots in a particular course
"""

from time import sleep
import smtplib

from selenium import webdriver
from selenium.webdriver.support.ui import Select

def main():
	"""Returns the number of open spots in a paricular
	 course at Cornell University"""
	netid = raw_input("Thanks for trying CU_Courses, please enter your netid: ")
	password = raw_input("Please enter your password: ")
	term = raw_input("Please enter the term: ")
        department = raw_input("What department is the class you're searching "
                               + "for in (use abbreviated form. E.g. " +
                               "'Computer Science'as 'CS': ")
	number = raw_input("Please enter class number: ")
	c_index = raw_input("Please enter an index of a section of the requested" +
						" class (it is the order in which the section appears" +
						" on the search results page, starting with 0 for the" +
						" section at the top of the page), if you leave blank" +
						" then first section will be selected automatically: ")
	if c_index=='':
		c_index='0'
	spots = check_course(netid,password,term,department,int(number),int(c_index))
	print "Results: \n" +"Open spots: " + str(spots["open_seats"])
	print "\nWaitlist spots: " + str(spots["waitlist_seats"])


def check_course(netid,password,term,department,number,c_index=0):
	"""Returns: A dictionary containing the number of
				available seats and waitlist spots in a class

	Logs into Cornell's Student Center using netid and password and then
	Checks if the lecture or discussion of index number c_index  for
	the class of number in the requesteddepartment is open, then returns a
	dictionary in the form {"open_seats": number of open seats,
	"waitlist_seats": number of waitlist spots available}. For example,
	check_course("ijg43", "Computer", "Spring 2017", "CS","1110") returns
	{'open_seats': 4, 'waitlist_seats': 20} . If there is no
	waitlist then value of 'waitlist_seats' is 'no_waitlist'
        IMPORTANT: Chrome and chrome driver are required for this function to
        work

	Parameter netid: User's netid
	Precondition: netid is a string of len(netid)<=5

	Parameter password: User's password
	Precondition: password is a string of len(password)>=8

	Parameter term: Requested term
	Precondition: Term is a valid Cornell term of type String, with
                                        name of term (starting with capital
                                        latter) placed before year. E.g "Spring
                                        2017"

	Parameter department: Requested class department
	Precondition: department is a Cornell department in valid abbreviated
                                        form and type String, also
                                        len(deparment)<=5

	Parameter number: Class number
	Precondition: number is an int and is a number of a class in department,
					and len(str(number))==4

	Parameter c_index: Index of class section
	Precondition: index is an int and is a valid index of a section of the
					requested class (it is the order in which
                                        the section appears on the search
                                        results page starting with 0 for the
                                        section at the top of the page) and is
                                        >=0, default value is 0
	"""

	#assert preconditions
	assert type(netid)==type("") and len(netid)<=5
	assert type(password)==type("") and len(password)>=8
	assert type(term)==type("")
	assert type(department)==type("") and len(department)<=5
	assert type(number)==int and len(str(number))==4
	assert type(c_index)==int and c_index>=0

	#Path of chromedriver as parameter
	driver = webdriver.Chrome("/usr/bin/chromedriver")

	#get page
	driver.get('http://www.studentcenter.cornell.edu')

	#Input netid
	submit_id = driver.find_element_by_id("netid")
	submit_id.send_keys(netid)

	#Input password
	submit_password = driver.find_element_by_id("password")
	submit_password.send_keys(password)

	#submit form
	submit_id.submit()

	#go to search page
        driver.get("https://css.adminapps.cornell.edu/psc/cuselfservice/EMPLOYEE/"
                   +"HRMS/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?Page=SSR_CLSRCH_ENTR"
                   +"Y&Action=U&ExactKeys=Y&TargetFrameName=None")

	#Input term
	submit_term = Select(driver.find_element_by_id("CLASS_SRCH_WRK2_STRM$35$"))
	submit_term.select_by_visible_text(term)

	#Wait for page to update, sleep time may need to be adjusted
	#depending on internet speed
	sleep(1)

	#Input subject
        subject = Select(driver.find_element_by_id("SSR_CLSRCH_WRK_SUBJECT_SRCH$0"))
	subject.select_by_value(department)

	#Input course number
	course_number = driver.find_element_by_id("SSR_CLSRCH_WRK_CATALOG_NBR$1")
	course_number.send_keys(str(number))

	#Uncheck 'open classes only' box
	driver.find_element_by_id("SSR_CLSRCH_WRK_SSR_OPEN_ONLY$3").click()

	#Search for class
	driver.find_element_by_id("CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH").click()

	#Wait for search to load, wait time may need to be adjusted
	#depending on internet speed
	driver.implicitly_wait(3)

	#Input lecture or discussion depending on index
	class_index = "MTG_CLASSNAME$span$" + str(c_index)
	driver.find_element_by_id(class_index).click()

	#Wait for page to load, wait time may need to be adjusted
	#depending on internet speed
	driver.implicitly_wait(3)

	#Check number of open seats
	available_seats = driver.find_element_by_id("SSR_CLS_DTL_WRK_AVAILABLE_SEATS")

	#Check waitlist capacity
	waitlist_capacity = driver.find_element_by_id("SSR_CLS_DTL_WRK_WAIT_CAP")

	#Check waitlist total
	waitlist_total = driver.find_element_by_id("SSR_CLS_DTL_WRK_WAIT_TOT")

	#Waitlist spots
	waitlist_spots = int(waitlist_capacity.text)-int(waitlist_total.text)


	return {"open_seats":int(available_seats.text),
			"waitlist_seats":waitlist_spots}; driver.quit()

if __name__ == "__main__":
    main()

