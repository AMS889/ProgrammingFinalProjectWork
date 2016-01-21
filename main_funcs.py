"""
Date: December 15, 2015
Author: Laura Buchanan and Alex Simonoff

This module set all the functions and helper functions used by the main program.
"""


import time
import datetime
from Visualization import *

weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
hours = ['Midnight - 1AM', '1AM - 2AM', '2AM - 3AM', '3AM - 4AM', '4AM - 5AM', '5AM - 6AM', '6AM - 7AM', '7AM - 8AM', '8AM - 9AM',
        '9AM - 10AM', '10AM - 11AM', '11AM - 12PM', '12PM - 1PM', '1PM - 2PM', '2PM - 3PM', '3PM - 4PM', '4PM - 5PM', '5PM - 6PM',
        '6PM - 7PM', '7PM - 8PM', '8PM - 9PM', '9PM - 10PM', '10PM - 11PM', '11PM - Midnight']

short_months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
short_days = ['mon','tue','wed','thu','fri','sat','sun']
short_times = range(24)

valid_zips = [10001, 10002, 10003, 10004, 10005, 10007, 10009, 10010, 10011,
       10012, 10013, 10014, 10016, 10017, 10018, 10019, 10021, 10022,
       10023, 10024, 10028, 10036, 10038, 10069, 10103, 10119, 10128,
       10167, 10168, 10199, 10278, 10280, 10282, 11101, 11201, 11205,
       11206, 11211, 11213, 11216, 11217, 11221, 11222, 11233, 11238]

sleep_time = .2

# This function says goodbye and ends the program
def goodbye():
    break_line()
    print "OK! Have a nice day!\n"

# This function asks the user if they would like to perform another search
def search_again():
    break_line()
    print "Would you like to perform another search?"        
    status = 0 
    while status == 0:    
        again_input = raw_input("Please type 'yes' or 'no' and hit 'Enter'\n")
        again_input = clean_input(again_input)
        if again_input == 'yes' or again_input == 'y':
            end_program = 0
            break_line()                        
            print "OK!"
            status = 1
        elif again_input == 'no' or again_input == 'n' or again_input == 'exit' or again_input == 'quit':
            end_program = 1
            status = 1
        else:
            break_line()        
            print "Sorry! I didn't understand that."
            status = 0        
    return end_program

## This function asks the user if they would like to save the graphs
def save_check():
    break_line()
    print "Would you like to save the results of the bike availability search?"
    print "Please type 'yes' or 'no' and hit 'Enter'"
    status = 0
    while status == 0:
        saveVal = raw_input("Save:")
        saveVal = clean_input(saveVal)
        if saveVal == 'yes' or saveVal == 'y':
            saveVal = 'Y'
            return saveVal
        elif saveVal == 'no' or saveVal == 'n':
            saveVal = 'N'
            return saveVal
        else: 
            print "\nOops! Didn't understand that."
            print "Would you like to save the results?."
            break_line()
            status = 0

# This function does the bike availibility look up and 
# prints the vizulization to the screen
def bike_lookup(weekday,month,time,zip_code):
    saveVar = save_check()
    break_line()        
    print "Awesome!"
    print "Please wait while the graphs load..." 
    #print "\nHere are the probable number of bikes at the stations in zip code " + str(zip_code) + ":\n"
    
    visual = visualization(zip_code, month, weekday, time)	
    visual.barPlot(saveVar)
    print "Plotting, please wait ..."
    plt.clf()
    visual.basemapPlot(saveVar)
    plt.show()

# This function determines zip_code to look over
def where_check():
	print "Now, what is your 5-digit zip code?"
	status = 0
	while status == 0:
        	try:
        		zip_code = input("Zip Code:\n")
                	if len(str(zip_code))==5:
                		if zip_code in valid_zips:
                  			status = status_good()
					return zip_code      	        
				else:
                			status = data_error()        
			else:
				status = len_error()
        	except ValueError:
			status = int_error()
        	except NameError:
			status = int_error()
        	except SyntaxError:
			status = int_error()

# Add a visual division on screen
def break_line():
	print "\n***********************************\n"

# Error message when input is an integer as needed
def int_error():
	break_line()
	print "Oops! Make sure you format your zip code as an integer."
	return status_error()

# Error message when we don't have data requested
def data_error():
	break_line()
	print "I'm sorry! We don't have data for that zip code."
	print "Try one of these NYC zip codes with Citi Bike data:"
        print "e.g. 10001, 10014, 10036, 10168, or 11222"
	return status_error()

# Error message when zip code isn't 5 digits
def len_error():
	break_line()
	print "\nOops! Make sure your zip code is 5 digits."
	return status_error()

# Sets status value when there is an error
def status_error():
	status = 0
        return status

# Sets status value when user input collected correctly
def status_good():
	status = 1
        return status


# This function determines which day of the week we should search over 
def day_check():
	break_line()
        print "OK! What day of the week do you want to ride a Citi Bike?"
        print "Please type the first 3 letter of the day you're interested in."
        status = 0
        while status == 0:
        	day = raw_input("Day of the Week:\n")
		day = clean_input(day)
		day = day[0:3]
        	if day in short_days:
                	status = 1
                	day = short_days.index(day)
			return day
		else:
			break_line() 
			print "\nOops! Didn't understand that."
			print "Please type just the first 3 letters of the weekday you're interested in."
			break_line()
			status = 0

# This function determines which month we should search over
def month_check():
	break_line()
	print "OK! What month do you want to ride a Citi Bike?"
        print "Please type the first 3 letter of the month you're interested in."
        status = 0
        while status == 0:
		month = raw_input("Month:\n")
		month = clean_input(month)
		month = month[0:3]
        	if month in short_months:
                	status = 1
                	month = short_months.index(month)
                	return month
        	else:
			break_line()
                	print "\nOops! Didn't understand that."
                	print "Please type just the first 3 letters of the month you're interested in."
                	break_line()
                	status = 0

# This function determines which hour we should search over
def time_check():
        break_line()        
	print "OK! What time do you want to ride a Citi Bike?"
        print "We will search over a given hour, in military time."
        print "e.g. Type '0' for Midnight - 1AM, '10' for 10AM - 11AM, or '14' for 2PM - 3PM"
        status = 0
        while status == 0:
        	time = raw_input("Time:\n")
		time = time.strip()
        	try:
                	time = int(time)
                	if time in short_times:
                        	status = 1
                        	time = short_times.index(time)
                        	return time
                	else:
				break_line()
                        	print "\nOops! Didn't understand that."
                        	print "Please type the hour you're interested in, in military time."
                        	break_line()
                        	status = 0
        	except:
                	print "\nOops! Didn't understand that."
                	print "Please type the hour you're interested in, in military time."
                	break_line()
                	status = 0

# This function determines whether we should look up bike availability
# now or at some other time
def when_check():
	when_status = 0
	while when_status == 0:
		print "Are you checking how many bikes might be availible right now?"
        	now_input = raw_input("Please type 'yes' or 'no' and hit 'Enter' \n")
        	now_input = clean_input(now_input)
		if now_input == 'yes' or now_input == 'y':
			time_info = datetime.datetime.now()
			weekday = weekdays[datetime.datetime.today().weekday()]
			month = time_info.strftime("%B")
			time = hours[time_info.hour]
			break_line()
                	print ("\nGreat! We will look up probable bike availibility near you on " +  weekdays[datetime.datetime.today().weekday()] +
                        	"s, in " + time_info.strftime("%B") + ", between " + hours[time_info.hour] + ".\n")
			break_line()
			when_status = 1
			month = months.index(month)+1
			time = hours.index(time)
			return (weekday,month,time)
		elif now_input == 'no' or now_input == 'n':
                	weekday = day_check()
			month = month_check()+1
                	time = time_check()
			break_line()
			print ("\nGreat! We will look up probable bike availibility near you on " +  weekdays[weekday] +
                        	"s, in " + months[month] + ", between " + hours[time] + ".\n")
			break_line()
			when_status = 1
			weekday = weekdays[weekday]
                        return (weekday,month,time)
		else:
			print "Hmm, didn't quite understand that..."
                        when_status = 0

# This function removes whitespace and lowercasese input from user
def clean_input(user_input):
	user_input = user_input.strip()
	user_input = user_input.lower()
	return user_input

# This function welcomes the user to the program, asks if they would like 
# to read and introduction, and prints an introduction if they type 'yes'
def intro_sequence():
	break_line()
	break_line()
	print "Welcome to Citi Bike Station Check!"
	break_line()
	break_line()
	time.sleep(sleep_time)
	print "Is this your first time using Citi Bike Station Check?\n"
	print "Please type 'yes' if you would like to read an introduction"
	print "or 'no' to proceed to the program.\n"
	intro = 1
	while intro == 1:
		intro_input = raw_input("Please type 'yes' or 'no' and hit 'Enter' \n")
        	intro_input = clean_input(intro_input)
		break_line()
		if intro_input == 'yes' or intro_input == 'y':
                	time.sleep(sleep_time)
			print "Welcome!\n"
                	print "This program let's you check how many Citi Bikes are likely"
                	print "to be available at your local Citi Bike stations...\n"
                	time.sleep(sleep_time)
                	print "This way, if there are probably no bikes availible, you don't"
                	print "even have to leave your apartment before you know whether you"
                	print "can bike! ...\n"
                	time.sleep(sleep_time)
                	print "This program is especially useful if you plan to bike with a"
                	print "group of people, you will have an idea if enough bikes will"
                	print "be available! ...\n"
                	time.sleep(sleep_time)
                	print "The output of this program are the locations of your nearby"
                	print "bike stations and how many bikes we expect to be available"
                	print "based on past data. Past weather data has been incorporated"
                	print "into our prediction...\n"
                	time.sleep(sleep_time)
                	print "We hope you find this product useful!"
                	break_line()
			time.sleep(sleep_time)
                	intro = 0

        	elif intro_input == 'no' or intro_input == 'n':
                	intro = 0
		
		else:
			print "Hmm, didn't quite understand that..."
			print "Is this your first time using Citi Bike Station Check?"
			print "Enter 'yes' if you would like to read an introduction."
			intro = 1

	print "OK! Let's begin!\n"
