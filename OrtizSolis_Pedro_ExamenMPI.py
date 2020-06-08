#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 09:53:05 2020

@author: usuario
"""


import random

import time

from mpi4py import MPI 
 

def how_many_max_values_sequential(ar):

    #find max value of the list

    maxValue = 0

    for i in range(len(ar)):

        if i == 0:

            maxValue = ar[i]

        else:

            if ar[i] > maxValue:

                maxValue = ar[i]

    #find how many max values are in the list

    contValue = 0

    for i in range(len(ar)):

        if ar[i] == maxValue:

            contValue += 1

 

    return contValue

 

# Complete the how_many_max_values_parallel function below.

def how_many_max_values_parallel(ar):
    
    #start_time = time.time()
        
    MASTER = 0
    FROM_MASTER = 1
    FROM_WORKER = 2
   
    source = 0
    rows = 0
    
    #arC = []
    
    maxValue = 0
    
    contValue = 0
    
    maxValues = []
    
    comm = MPI.COMM_WORLD
    
    #Obtener tamano de grupo de proceso
    numtasks = comm.size
    
    #Obtener el id de procesos
    taskid = comm.Get_rank()
    
    
        
    numworkers = numtasks - 1
    
    #Mastertask
    #print('Llego hasta aqui 1')
    
    if taskid == MASTER:
        
        #print('Llego hasta aqui 2')
        
    
        print("Numero de tareas de trabajo",numworkers)
        
        
        
        averow = len(ar)//numworkers
        extra = len(ar)%numworkers
        offset = 0
        mtype = FROM_MASTER
        
        for dest in range(numworkers):
            
            if dest+1 <= extra:
                rows = averow + 1
            else:
                rows = averow
                
            comm.send(offset, dest=dest+1, tag=mtype)
            comm.send(rows, dest=dest+1, tag=mtype)
            comm.send(ar[offset:rows+offset], dest=dest+1, tag=mtype)
            
            #comm.send(matrizB, dest=dest+1, tag=mtype)
            
            offset = offset + rows
            
        mtype = FROM_WORKER
        
        concat = []
        for n in range(numworkers):
            
            source = n
            
            offset = comm.recv(source=source+1, tag=mtype)
            rows = comm.recv(source=source+1, tag=mtype)
            aux = comm.recv(source=source+1, tag=mtype)
            aux = aux[:rows]
            concat = concat + aux
        
        
        
        
        for value in concat:
            
            if value > maxValue:
                
                maxValue = value

        for value in ar:
    
            if value == maxValue:
    
                contValue += 1
                
        #print(concat)
            
        #end_time = time.time()
        
        #print("Time MPI: ", end_time - start_time)

        
        
        
    if(taskid > MASTER):
        #print('Llego hasta aqui 3')
        mtype = FROM_MASTER
        offset = comm.recv(source=MASTER,tag=mtype)
        rows = comm.recv(source=MASTER,tag=mtype)
        ar = comm.recv(source=MASTER,tag=mtype)
        #matrizB = comm.recv(source=MASTER,tag=mtype)
        
        maxEach = 0;
        for value in ar:
            if value > maxEach:
                maxEach = value
                
        maxValues.append(maxEach)
                    
        mtype = FROM_WORKER
        comm.send(offset,dest=MASTER,tag=mtype)
        comm.send(rows,dest=MASTER,tag=mtype)
        comm.send(maxValues,dest=MASTER,tag=mtype)
        #print(matrizC)
    
    
    return contValue  

 

if __name__ == '__main__':

    ar_count = 40000000

    #Generate ar_count random numbers between 1 and 30

    ar = [random.randrange(1,30) for i in range(ar_count)]

    inicioSec = time.time()

    resultSec = how_many_max_values_sequential(ar)

    finSec =  time.time()

   

    inicioPar = time.time()   

    resultPar = how_many_max_values_parallel(ar)

    finPar = time.time()   

   

    print('Results are correct!\n' if resultSec == resultPar else 'Results are incorrect!\n')

    print('Sequential Process took %.3f ms with %d items\n' % ((finSec - inicioSec)*1000, ar_count))

    print('Parallel Process took %.3f ms with %d items\n' % ((finPar - inicioPar)*1000, ar_count))