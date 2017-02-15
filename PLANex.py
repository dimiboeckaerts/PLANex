"""
PROJECT PLANex

Created on Fri Sep 30 15:31:57 2016

@author: dimiboeckaerts

Notes and remarks at the end of the script.
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
    
    # werken helpers in andere helpers als ze enkel hier imported worden?
    
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
    
### TO DO
### ------------------------------------------
"""
- Time complexity plannen initieel rooster (5 individuen: 1m47s)?
- probleem dat alle vakken op dagen 1 en 2 worden gezet...?

- testcases maken om alle functies die tot nu toe geimplementeerd werden, 
    te testen. Testcase voor highestcost (simpel dat ook met de hand uit 
    te rekenen is.). Test voor thecreator.
- beter dict gebruiken voor sched als er niet gewerkt kan worden met de array?
- Daarna optimalisatie starten (functie voor toernooiselectie en
    mutatie, iteratiematrix etc...). Controle voor duur van de procedure en
    controle voor iteratie (timing).
- na optimalisatie moet ideale rooster teruggegeven worden
- evaluatie van alle functies (stap per stap) in het algoritme (met eenvoudige
    en complexe testvoorbeelden) + debugging
- extra functionaliteiten (zie onder) + closed app van maken (input van
    gebruiker vragen)
- computation time...
"""
    
    
### NOTES / REMARKS
### ------------------------------------------

"""
- file, prof en days zijn strings die verwijzen naar de excelfile die ingeladen
    moet worden en in de directory staat.
    
- logic2 kan met naam en voornaam vergelijken, die dan samengevoegd worden.

- extra functionaliteit in data prep module dat het niet 2x optelt naar
    100% maar kijkt of test 1 is of 2 is en indien 1 telt hij van 0-50%, 
    anders van 50-100%.

- extra input: lijst van welke vakken net gepland moeten worden (uit de 
    lijst die meegegeven werd).

- 1e rij in excelfile moeten kolomnamen zijn, zodat identificatie van de juiste
    kolommen mogelijk is.

- in days moet de eerste kolom vakken zijn en 2e kolom aantal dagen (integer).

- working with time (extra functionaliteit: stop als benodigde tijd groter is 
    dan 4u)
    import datetime
    t1 = datetime.datetime.today()
    t2 = datetime.datetime.today() (beetje later)
    print(t2-t1)
    print((t2-t1)*5)
    if (t2-t1).total_seconds() * (benodigde iteraties) > 14400 seconden dan stop programma

- iteratiematrix bijhouden (plot?).

- Om meerdere occurences van een item in een list te vinden is de functie IND 
    nodig, dat lijsten van het type 'list' nodig heeft, niet mogelijk om met de
    dataframe te werken, dus lst1 en lst2 bijhouden

- #array1 = np.zeros((len(lst1), 2))
  #df1 = pd.DataFrame(array1)

  Is deze manier waarop ik de inputdata bijhoud de meest efficiente manier? Data 
  die bijgehouden moet worden:
      - vak: van stu_vak combo 
      - stu: van stu_vak combo (dus niet unicorn toepassen!)
      - courses: de unique lijst van vakken, op alfabet, overeenkomend met sched
      - sched: array van populatie in de generatie, overeenkomend met courses
      - prof: dictionary 'key-value' = 'vak - lijst van dagen'
      - cost van elk vak voor het opstellen van initieel rooster (1 vector die elke
        stap overschreven kan worden.)

- dict gebruiken voor schedule/courses

- extra stop: geen rooster als enkele studenten een zeer slecht rooster hebben
    maar waar trekken we de grens? Hoeveel studenten is genoeg?
    
- parallellizatie!

- beter om direct alle mondelinge momenten te plannen eens we aan dat examen
    komen, of eerst wachten tot alle andere vakken gepland zijn, dan pas rest
    van de mondelinge momenten inplannen?
- wat als examens niet correct geprioritiseerd worden zodat examens uiteindelijk
    op een dag moeten waar ze niet meer kunnen?
    
"""
