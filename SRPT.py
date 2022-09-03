import pandas as pd 
import matplotlib.pyplot as plt
#import math
import random
import matplotlib
import matplotlib.colors as mcolor 


def SRTN ( df ) : # df est le data frame  avec arrive / dispo temps 
    colors = list ( mcolor.TABLEAU_COLORS.keys ())
    queue = []
    cpu , cur_pdf = None , None 
    alloc , dalloc = {} , {}
    total = 0
    time = 0
    H = [ 'A' , 'B' , 'C']
    BR = [15 , 5 , 10]
    DI = [3,5,11,12]
    fig , gnt  = plt.subplots()
    gnt.set_ylim (0,5)
    gnt.set_ylim(0,20)
    gnt.set_xlabel('TEMPS')
    gnt.set_ylabel('TACHE')
    gnt.set_yticks ([1,2,3,4,5])
    gnt.set_yticklabels(['1','2','3','4','5'])
    gnt.set_xticks([0,2,4,6,8,10,12,14,16,18,20,22])
    gnt.set_xticklabels(['0','2','4','6','8','10','12','14','16','18','20','22'])
    
    gnt.grid (True)


    while True :  # On simule l'algo
        # verifie si la tache  a terminer l'execution
        if df ['RemainingTime'].max() == 0 :
            break

        # avoir  la tache actuelle , si existe
        if cpu :
            cur_pdf = df[df.Process == cpu]

        # verifie si la tache arrive et mettre en attente 
        pdf = df[df.ArrivalTime == time ]

        if len (pdf) > 0:
            for p in pdf ['Process'].values :
                queue.append(p)

        if len (queue) > 0:
            pdf = df [df['Process'].isin(queue)]

        #Trouver la tache avec le plus court temps restant 
        if len (pdf) > 0:
            pdf = pdf [pdf['RemainingTime' ]==pdf['RemainingTime' ].min()]

        #Commencer la tache , preempt si necessaire 
        if (cpu is None ) or (len(pdf) > 0 and pdf ['RemainingTime'].values[0]< cur_pdf['RemainingTime'].values[0]):
            if cpu :
                # preemprt la tache actuelle 
                dalloc[cpu ] = dalloc.get(cpu, [])+ [time]
                queue.append (cpu)
                print ('La tache {} sort de la machine a t = {}'.format(cpu , time ))
            cur_pdf = pdf
            cpu = cur_pdf['Process'].values[0]
            queue.remove(cpu)
            print ('La tache {} entre a la machine a t = {}'.format(cpu,time))
            gnt.broken_barh([(time , BR [H.index(cpu)])], (0 , 1) , facecolors = ('{}'.format(colors[H.index(cpu)])))
            alloc [cpu] = alloc.get(cpu , []) + [time]
        df.loc[df['Process'] == cpu , 'RemainingTime'] -=1
        time += 1  # incrementer le temps 
        # enlever la tache
        if df [df['Process'] == cpu]['RemainingTime'].values[0] == 0 :
            print ( ' La tache {} sort de  la machine a t = {}'.format(cpu , time ))
            dalloc[cpu]= dalloc.get(cpu , []) + [time]
            cpu = cur_pdf = None
            total += time 

    print (" La somme de fin d'execution est {}".format(total))
    plt.savefig("gantt1.png")
    plt.show()
    return alloc , dalloc





#-------------------------------MAIN------------------------------
df = pd.DataFrame({'Process': ['A', 'B' , 'C'], 'BurstTime':[15,5,10],'ArrivalTime':[5,6,0]})
df.sort_values('ArrivalTime', inplace= True)
df['RemainingTime'] = df.BurstTime

SRTN (df)






         




