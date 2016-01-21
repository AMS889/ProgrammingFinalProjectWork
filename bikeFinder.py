"""
Date: December 15, 2015
Author: Laura Buchanan

This is the main program, where the other features of the project are accessed
"""

import main_funcs as func

if __name__ == "__main__": 
    try:
        func.intro_sequence()
        end_program = 0
        while end_program == 0:
            (weekday,month,time) = func.when_check()
            zip_code = func.where_check()
            func.bike_lookup(weekday,month,time,zip_code)
            end_program = func.search_again()
            func.goodbye()

    except KeyboardInterrupt:
        func.goodbye()
