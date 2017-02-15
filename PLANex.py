"""
PROJECT PLANex

Created on Fri Sep 30 15:31:57 2016

@author: dimiboeckaerts

"""

### The PLANex Scheduling Algorithm 
### ------------------------------------------

def PLANex(file=0, prof=0, days=0, length=28):
    
    # IMPORT LIBRARIES
    # ----------------------------------------
    import openpyxl as oxl
    import pandas as pd
    import numpy as np
    import random as ran
    from helpers import unicorn
    from helpers import indx
    from helpers import buds
    from helpers import weight
    from helpers import highestcost
    from helpers import satdegree
    from helpers import theverybest
    from helpers import thecreator
    

    # INTRO
    # ----------------------------------------
    print('Hi, I\'m PLANex, you\'re exam timetabeling assistant.')
    
    if file == 0 or prof == 0 or days == 0 or type(file) != str or type(prof) != str or type(days) != str:
        print('Oops, it seems that you have not given me the correct input.\
        Please try again.')
        return
    else:
        print('Data prep on it\'s way.')
            
        
    # DATA PREP
    # ----------------------------------------
    
    # FILE
    wb = oxl.load_workbook(file)
    lst = wb.get_sheet_names()
    sheet = wb.get_sheet_by_name(lst[0])
    test = 0
    
    for j in range(1, sheet.max_column):
        sheetvalue = sheet.cell(row=1, column=j).value
        logic1 = sheetvalue in ['VAK', 'Vak', 'vak', 'CURSUS', 'Cursus', 'cursus', 'CURSUSNAAM', 'Cursusnaam', 'cursusnaam']
        logic2 = sheetvalue in ['EMAIL', 'Email', 'email', 'MAIL', 'Mail', 'mail', 'EMAILADRES', 'Emailadres', 'emailadres']
        if logic1 == True:
            test += 1
            lst1 = []
            for i in range(2, sheet.max_row+1):
                lst1.append(sheet.cell(row=i, column=j).value)
                if (i/sheet.max_row*100) % 10 == 0:
                    print(str(i/sheet.max_row*100) + ' % done (1/4)')
        elif logic2 == True:
            test += 1
            lst2 = []
            for k in range(2, sheet.max_row+1):
                lst2.append(sheet.cell(row=k, column=j).value)
                if (k/sheet.max_row*100) % 10 == 0:
                    print(str(k/sheet.max_row*100) + ' % done (2/4)')
    if test != 2:
        print('Oops, it seems that you have not given me the correct input.\
        Please try again.')
        return
    else:
        vak = lst1
        stu = lst2
        courses = unicorn(vak)
        
    # DAYS
    wb = oxl.load_workbook(days)
    lst = wb.get_sheet_names()
    sheet = wb.get_sheet_by_name(lst[0])
    
    if (type(sheet.cell(row=1, column=2).value) != int) and (type(sheet.cell(row=1, column=1).value) != str):
        print('Oops, there is something wrong with your \'days\' file. Please try again.')
        return
            
    for i in range(1, sheet.max_row+1):
        sheetvalue = sheet.cell(row=i, column=2).value
        if sheetvalue > 1:
            for j in range(1,sheetvalue):
                # range to sheetvalue, not sheetvalue+1 because we already have
                # the course one time in the list.
                courses.append(sheet.cell(row=i, column=1).value)
        if (i/sheet.max_row*100) % 10 == 0:
            print(str(i/sheet.max_row*100) + ' % done (3/4)')
        
    courses = sorted(courses)
    
    # PROF
    wb = oxl.load_workbook(prof)
    lst = wb.get_sheet_names()
    sheet = wb.get_sheet_by_name(lst[0])
    
    if (type(sheet.cell(row=1, column=2).value) != int) and (type(sheet.cell(row=1, column=1).value) != str):
        print('Oops, there is something wrong with your \'prof\' file. Please try again.')
        return
    else:
        profd = {}
        for i in range(1, sheet.max_row+1):
            lijst = []
            for j in range(2, sheet.max_column+1):
                if sheet.cell(row=i, column=j).value != 0:
                    lijst.append(sheet.cell(row=i, column=j).value)
                    
            profd[sheet.cell(row=i, column=1).value] = lijst

            if (i/sheet.max_row*100) % 10 == 0:
                print(str(i/sheet.max_row*100) + ' % done (4/4)')
                
    print('Data prep done. Now let\'s get scheduling.')
        
    
    # GENETIC ALGORITHM
    # ----------------------------------------
    n1 = 1000
    
    sched = thecreator(stu, vak, courses, length, profd, n1)
    
