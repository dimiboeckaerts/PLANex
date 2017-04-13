"""
HELPERS (PROJECT PLANex)

Created on Sat Oct  8 00:26:41 2016

@author: dimiboeckaerts
"""


#%% DATA PREP
"""
Function to check input and convert the .xlsx files to lists and dictionaries.
"""

def dataprep(file, days, prof):
    
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
    
    return stu, vak, courses, profd


#%% UNICORN
"""
Function to find unique elements in a list.
"""

def unicorn(lst):
    newlst = []
    for item in lst:
        if item not in newlst: 
            # only works for individual elements, so not list of list.
            newlst.append(item)
    return newlst

    
#%% INDX
"""
Function to find multiple occurences of an item in a list. This requires a
list (type = list).
    
@author: paulmcguire
"""

def indx(lst,item):
    start = -1
    locs = []
    while True:
        try:
            loc = lst.index(item,start+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start = loc
    return locs

    
#%% BUDS
"""
Function that counts the number of common students between 2 courses. Four
inputs are needed: exam1 (string), exam2 (string), stu (a list of all 
students) and vak (a list of all courses corresponding with the list 'stu').
"""
    
def buds(exam1, exam2, stu, vak):
    index1 = indx(vak, exam1)
    index2 = indx(vak, exam2)
    count = 0
    
    for item1 in index1:
        for item2 in index2:
            if stu[item1] == stu[item2]:
                count += 1
    return count
    
    
#%% WEIGHT
"""
Function to calculate the given weight of a given distance 'd', needed for
the optimization. 
http://www.sciencedirect.com/science/article/pii/S1568494609001331
"""

def weight(d):
    if d == 0:
        return 32
    elif d == 1:
        return 16
    elif d == 2:
        return 8
    elif d == 3:
        return 4
    elif d == 4:
        return 2
    elif d == 5:
        return 1
    else:
        return 0
            

#%% HIGHEST COST
"""
Function that calculates the HC heuristic, for all exams and returns 
them in a list. 
Input needed: 
- an exam to compute the heuristic for.
- list of all students and corresponding courses 'vak' (also a list).
- the schedule itself, which consists of 'courses', a list with all unique 
    courses where oral exams could appear more then once if they need more 
    then one day.
- 'sched', a vector of the current generation with numbers (day of 
    examination) corresponding to a course in the list courses'. 
- length: length of the examination period.
    
The tricky part is that we need to account for oral exams, which could 
appear more than once in the 'courses' list. When calculating the distance,
and the course appears multiple times, we add all distances together, 
meaning that an exam that appears multiple times has a higher cost, in most
cases it is indeed more difficult to schedule an exam to multiple days 
(although the students have more options).
    
The function also incorporates saturation degree heuristic, if the count is
zero (so highest cost won't have a cost).
http://www.sciencedirect.com/science/article/pii/S1568494609001331
"""
 
def highestcost(exam, stu, vak, courses, schedlst, length, profd):
    hc = len(profd[exam])
    for item in courses:
        if (exam != item) and (buds(exam, item, stu, vak) != 0):
            index = indx(courses, item)
            for item2 in index:
                for i in range(1, length+1):
                    if schedlst[item2] != 0:
                        hc += weight(abs(schedlst[item2]-i))*buds(exam, item, stu, vak)
    return hc


#%% SATURATION DEGREE
"""
The number of periods that an examination can NOT be allocated to without
causing a clash. As input we need the prof dictionary to see when that 
particular exam can not be given due to prof absence.
    
Saturation degree still needed as seperate function for initial ordering 
(outside of for loop, which is faster).
http://www.sciencedirect.com/science/article/pii/S1568494609001331
"""

def satdegree(exam, profd):
    cost = len(profd[exam])
    return cost
    
    
#%% THEVERYBEST
"""
Function to search for the minimum cost period of a given exam.
http://www.sciencedirect.com/science/article/pii/S1568494609001331
"""

def theverybest(exam, stu, vak, courses, schedlst, length, period):
    cost = 0
    for item in courses:
        if (exam != item) and (buds(exam, item, stu, vak) != 0):
            index = indx(courses, item)
            for item2 in index:
                if schedlst[item2] != 0:
                    cost += weight(abs(schedlst[item2]-period))*buds(exam, item, stu, vak)
    return cost/len(indx(vak, exam))
    

#%% THE CREATOR
"""
Algorithm used to create the initial population of timetables. 
http://www.sciencedirect.com/science/article/pii/S1568494609001331
"""

def thecreator(stu, vak, courses, length, profd, n1):
    #now = dt.datetime.now()
    print('Starting process to compute initial generation of timetables.')
    vector = [x for x in range(1,length+1)]
    for item in vector:
        if item%7 == 0:
            vector.remove(item)
            vector.remove(item-1)
    cost = []
    sched = {}
        
    # Get the first ordering
    for item in courses:
        cost.append(satdegree(item, profd))
    order = [courses for (cost, courses) in sorted(zip(cost,courses))][::-1]
    
    for i in range(0, n1):
        sched[i] = [0] * len(courses)
        # Plan first exam for each generation (sat degree) (slow)
        firstexam = order[ran.randint(0,2)]
        # update vector list to only possible dates
        vector2 = [x for x in vector if x not in profd[firstexam]]
        cost = []
        for item in vector2:
            cost.append(theverybest(firstexam, stu, vak, courses, sched[i], length, item))    
        order_period = [vector2 for (cost, vector2) in sorted(zip(cost,vector2))]
        index = indx(courses, firstexam)
        
        # Schedule all orals directly
        for k in range(0, len(index)):
            sched[i][index[k]] = order_period[k] # dict, [][]
    
        # Plan rest of courses for each of the individuals in population
        # While exams have to be scheduled in this individu
        while (np.prod(sched[i]) == 0): #or len(unscheduled) != 0:
            # Update list to only unscheduled courses, then use heuristics
            unscheduled_index = indx(sched[i], 0)
            cost = []
            unscheduled = []
            for item in unscheduled_index:
                unscheduled.append(courses[item])
                cost.append(highestcost(courses[item], stu, vak, courses, sched[i], length, profd))
                # now unscheduled matches with cost
            neworder = [unscheduled for (cost, unscheduled) in sorted(zip(cost,unscheduled))][::-1]

            # Schedule most difficult exams (random between two most difficult)
            if len(unscheduled) == 1:
                exam = unscheduled[0]
            else:
                exam = neworder[ran.randint(0,1)]
            vector2 = [x for x in vector if x not in profd[exam]]
            cost = []
            for item in vector2:
                cost.append(theverybest(exam, stu, vak, courses, sched[i], length, item))    
            order_period = [vector2 for (cost, vector2) in sorted(zip(cost,vector2))]
            index = indx(courses, exam)
            for l in range(0, len(index)):
                sched[i][index[l]] = order_period[l]
            #print(sched[i])
            
        if (i/n1*100) % 5 == 0:
            print(str(i/n1*100) + ' %  of initial timetables done')
    #print(dt.datetime.now() - now)
    return vector, sched
                    
    
#%% FITNESS PHASE 1
"""
Function to calculate the fitness in phase 1 of optimization. This is 
defined as the number of clashes in the schedule. Th duplicate dates in the 
schedule are counted, and then checked wheter the courses involved have
students in common. If so, we count as a clash.
http://www.sciencedirect.com/science/article/pii/S1568494609001331
"""
def fitness1(schedlst, courses, stu, vak):
    counter = 0
    dups = [x for x in schedlst if schedlst.count(x) > 1]
    dups = unicorn(dups)
    lst = []
    
    # only clash if the courses have students in common
    for item in dups:
        index = indx(schedlst, item)
        count = 0
        for i in range(0, len(index)):
            exam1 = courses[index[i]]
            for j in range(i+1, len(index)):
                exam2 = courses[index[j]]
                if buds(exam1, exam2, stu, vak) != 0:
                    count += 1
                    lst.append(exam1)
                    lst.append(exam2) 
        if count > 0:
            counter += 1
    clashes = unicorn(lst)
    return counter, clashes
    

#%% OPTIMIZER PHASE 1
"""
Function for phase 1 optimization.
Count clashes for all schedules in a tournament, keep the one with least
clashes. Then optimize the schedule by mutation. Only courses in clashes 
are selected for mutation. Rescheduling to minimum cost slot.

= ONE ROUND OF TOURNAMENT SELECTION AND MUTATION

http://www.sciencedirect.com/science/article/pii/S1568494609001331
    
TESTPHASE
"""

def optimizer1(sched, vector, courses, stu, vak, profd, length):
    newsched = {}
    test = 0 # dummy to stop optimization
    
    # Tournament selection (n=10) and fitness calculation
    for i in range(0, len(sched)):
        ids = ran.sample(range(len(sched)), 10)
        fitness = 1000
        for item in ids:
            newfitness, clashes = fitness1(sched[item], courses, stu, vak)
            if newfitness < fitness: # fitness = # of clashes
                fitness = newfitness
                newschedlst = sched[item]
                newclashes = clashes
        newsched[i] = newschedlst
        
        # If clashes, then reschedule first clash to min cost period
        if len(newclashes) > 0:
            test = 1
            vector2 = [x for x in vector if x not in profd[newclashes[0]]]
            cost = []
            for item in vector2:
                cost.append(theverybest(newclashes[0], stu, vak, courses, newsched[i], length, item))
            order_period = [vector2 for (cost, vector2) in sorted(zip(cost, vector2))]
            index = indx(courses, newclashes[0])
            
            #if len(index) > 1:
            #    ...
            #else:
            newsched[i][index[0]] = order_period[0]
            
    return newsched, test
    
            
#%% FITNESS PHASE 2
"""
Function to calculate the fitness in phase 2 of optimization.
The fitness in phase 2 optimization is definded by the soft constraint
cost (proximity cost), which we want to minimize (it is a cost).
http://www.sciencedirect.com/science/article/pii/S1568494609001331
"""

def fitness2(schedlst, courses, stu, vak):
    softcost = 0
    
    for i in range(0, len(schedlst)):
        exam1 = courses[i]
        for j in range(i+1, len(schedlst)):
            exam2 = courses[j]
            if (exam1 != exam2):
                softcost += weight(abs(schedlst[i]-schedlst[j]))*buds(exam1, exam2, stu, vak)
    softcost /= len(unicorn(stu))
    
    return softcost
    
    
#%% OPTIMIZER PHASE 2
"""
Function for phase 2 optimization, using proxcost. 
    
= ONE ROUND OF TOURNAMENT SELECTION AND MUTATION

http://www.sciencedirect.com/science/article/pii/S1568494609001331
"""

def optimizer2(sched, vector, courses, stu, vak, profd, n2):
    newsched = {}

    for i in range(0, n2):
        ids = ran.sample(range(len(sched)), 10)
        softcost = 1000
        for item in ids:
            newcost = fitness2(sched[item], courses, stu, vak)
            if newcost < softcost:
                softcost = newcost
                newschedlst = sched[item]
        newsched[i] = newschedlst
        
        times = ran.randint(1, 3)
        for i in range(0, times):    
            # only feasible mutations
            fix1 = ran.randint(0, len(sched[i]))
            vector2 = [x for x in vector if x not in profd[courses[fix1]]]
            vector3 = [x for x in vector2 if x not in newsched[i]]
            
            # dummies to stop mutation
            tester = 1
            tries = 0
            
            while (tester != 0 and tries < 3):
                fix2 = ran.sample(vector3, 1)[0]
                testsched = newsched[i]
                testsched[fix1] = fix2
                testcost = fitness2(testsched, courses, stu, vak)
                # check cost after new mutation
                if testcost < softcost:
                    tester = 0 # stop if we found a better schedule
                    newsched[i] = testsched
                tries += 1 # max 3 tries
    return newsched
