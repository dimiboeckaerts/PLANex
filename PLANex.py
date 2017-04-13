"""
PROJECT PLANex (Genetic Algorithm)

Created on Fri Sep 30 15:31:57 2016

@author: dimiboeckaerts

Notes and remarks in seperate script.
"""

### The PLANex Scheduling Algorithm 
### ------------------------------------------

def PLANex(file=0, prof=0, days=0, startdate, length=28):
    
    # IMPORT LIBRARIES
    # ----------------------------------------
    import openpyxl as oxl
    import numpy as np
    import random as ran
    from helpers import dataprep
    from helpers import unicorn
    from helpers import indx
    from helpers import buds
    from helpers import weight
    from helpers import highestcost
    from helpers import satdegree
    from helpers import theverybest
    from helpers import thecreator
    from helpers import fitness1
    from helpers import optimizer1
    from helpers import fitness2
    from helpers import optimizer2
    
    
    # INTRO
    # ----------------------------------------
    print('Hi, I\'m PLANex, you\'re exam timetabeling assistant.')
    
    if file == 0 or prof == 0 or days == 0 or type(file) != str or type(prof) != str or type(days) != str:
        print('Oops, it seems that you have not given me the correct input.\
        Please try again.')
        return
    elif (len(startdate) != 7 or len(startdate) != 8 or type(startdate) != str):
        print('Oops, please input the correct date format: dd/m/yy or dd/mm/yy as a string.')
        return
    else:
        print('Data prep on it\'s way.')
                
        
    # DATA PREP
    # ----------------------------------------
    stu, vak, courses, profd = dataprep(file, days, prof)      
    
    
    # GENETIC ALGORITHM - PHASE 1
    # ----------------------------------------
    # Creating initial schedule
    n1 = 1000
    vector, sched = thecreator(stu, vak, courses, length, profd, n1)
    n_generations_1 = 0
    test = 1
    
    # Phase 1 optimization
    while (test != 0 and n_generations_1 < 50):
        sched, test = optimizer1(sched, vector, courses, stu, vak, profd, length)
        n_generations_1 += 1
        
    if n_generations_1 == 50:
        print('Very difficult schedule... full optimization probably impossible.')
    
        
    # GENETIC ALGORITHM - PHASE 2
    # ----------------------------------------
    n2 = 500
    n_generations_2 = 1000
    
    for i in range(0, n_generations_2):
        sched = optimizer2(sched, vector, courses, stu, vak, profd, n2)
        
        
    # WORKING WITH DATETIME
    # ----------------------------------------
    thedate = dt.datetime.strptime(startdate, "%d/%m/%y")
    final_sched = []
    softcost = 10000
    
    for i in range(0, len(sched)):
        newcost = fitness2(sched[i], courses, stu, vak)
        if newcost < softcost:
            softcost = newcost
            newschedlst = sched[i]
        
    for i in range(0, len(newschedlst)):
        date = thedate + dt.timedelta(days = newschedlst[i]-1)
        final_sched.append(date.strftime('%d/%m'))
    
    print('Final schedule:')
    for i in range(0, len(final_sched)):
        print(courses[i], ':', final_sched[i])
        
    return
                
