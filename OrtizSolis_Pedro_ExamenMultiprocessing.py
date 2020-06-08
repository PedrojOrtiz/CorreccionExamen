#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 09:52:02 2020

@author: usuario
"""

import random

import time
 

import multiprocessing

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

 

def find_max_value(ar, send_end):
    
    maxValue = 0

    for value in ar:
        if value > maxValue:
            maxValue = value
       
    send_end.send(maxValue)

def cont_max_value(ar, maxValue):
    
    contValue = 0

    for value in ar:

        if value == maxValue:

            contValue += 1

    #cont_send_end.send(contValue)
    return contValue
    
    
    

# Complete the how_many_max_values_parallel function below.

def how_many_max_values_parallel(ar):

    """
    ar_1 = ar[0 : int(len(ar)/8)]
    ar_2 = ar[int(len(ar)/8) : int(2 * len(ar)/8)]
    ar_3 = ar[int(2 * len(ar)/8) : int(3 * len(ar)/8)]
    ar_4 = ar[int(3 * len(ar)/8 ): int(4 * len(ar)/8)]
    ar_5 = ar[int(4 * len(ar)/8) : int(5 * len(ar)/8)]
    ar_6 = ar[int(5 * len(ar)/8) : int(6 * len(ar)/8)]
    ar_7 = ar[int(6 * len(ar)/8) : int(7 * len(ar)/8)]
    ar_8 = ar[int(7 * len(ar)/8) : len(ar)]
    """
    
    ##Dividimos por lotes

    ar_1 = ar[0 : int(len(ar)/4)]
    ar_2 = ar[int(len(ar)/4) : int(2 * len(ar)/4)]
    ar_3 = ar[int(2 * len(ar)/4) : int(3 * len(ar)/4)]
    ar_4 = ar[int(3 * len(ar)/8 ): len(ar)]

    ## Maximos valores en cada lote

    maxValues = []
    
    """
    p = multiprocessing.Pool(8)
    
    maxValues.append(p.apply(find_max_value, (ar_1, )))
    maxValues.append(p.apply(find_max_value, (ar_2, )))
    maxValues.append(p.apply(find_max_value, (ar_3, )))
    maxValues.append(p.apply(find_max_value, (ar_4, )))
    """

    recv_end, send_end = multiprocessing.Pipe(False)
    recv_end2, send_end2 = multiprocessing.Pipe(False)
    recv_end3, send_end3 = multiprocessing.Pipe(False)
    recv_end4, send_end4 = multiprocessing.Pipe(False)

    process1 = multiprocessing.Process(target=find_max_value, args=(ar_1, send_end))
    process2 = multiprocessing.Process(target=find_max_value, args=(ar_2, send_end2))
    process3 = multiprocessing.Process(target=find_max_value, args=(ar_3, send_end3))
    process4 = multiprocessing.Process(target=find_max_value, args=(ar_4, send_end4))
        
    MaxValue = []
    MaxValue2 = []
    MaxValue3 = []
    MaxValue4 = []
    
    MaxValue.append(recv_end)
    MaxValue2.append(recv_end2)
    MaxValue3.append(recv_end3)
    MaxValue4.append(recv_end4)
    
    
    process1.start()
    process2.start()
    process3.start()
    process4.start()
    
    
    process1.join() 
    process2.join()
    process3.join() 
    process4.join()
   
    
    Result = [x.recv() for x in MaxValue]
    Result2 = [x.recv() for x in MaxValue2]
    Result3 = [x.recv() for x in MaxValue3]
    Result4 = [x.recv() for x in MaxValue4]
    
    maxValues.append(Result[0])
    maxValues.append(Result2[0]) 
    maxValues.append(Result3[0]) 
    maxValues.append(Result4[0]) 
    
    print(maxValues)

    #maxValue = maxValues[0]

    ## Maximo valor de los lotes

    maxValue = 0
    
    for value in maxValues:
        if value > maxValue:
            maxValue = value
    
    
            
    print('Maximo Valor: ' + str(maxValue))
    
    #Cuenta el numero de maxValue en todo el array.
    
    
    
    
    contTotal = cont_max_value(ar, maxValue) 
    
    
    return contTotal

 

if __name__ == '__main__':

    ar_count = 40000000
    #ar_count = 400000

    #Generate ar_count random numbers between 1 and 30

    ar = [random.randrange(1,30) for i in range(ar_count)]

    inicioSec = time.time()

    resultSec = how_many_max_values_sequential(ar)
    print(resultSec)

    finSec =  time.time()

   

    inicioPar = time.time()   

    resultPar = how_many_max_values_parallel(ar)
    print(resultPar)

    finPar = time.time()   

   

    print('Results are correct!\n' if resultSec == resultPar else 'Results are incorrect!\n')

    print('Sequential Process took %.3f ms with %d items\n' % ((finSec - inicioSec)*1000, ar_count))

    print('Parallel Process took %.3f ms with %d items\n' % ((finPar - inicioPar)*1000, ar_count))
