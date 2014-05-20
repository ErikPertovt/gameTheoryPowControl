#GAME EXAMPLE - POWER CONTROL GAME

from gainCalculations import GainCalculations
#from noise import getInstantNoise
from noise import Noise
from datetime import datetime as DateTime
from myQueue import MyQueue
#import noise
# noise import getInstantNoise
import math
from matplotlib import pyplot as plot
import matplotlib
import datetime
import os

def main():
    # You can play a game with two players: one players is represented by a node pair consisting of a transmitter and receiver
    # You have to specify both players' coordinator_id , transmitter's node id, receiver's node id
    # Optional you can specify at which frequency to measure(2420Mhz default) , to or not to save the results, and how long should the generator transmit a signal (recommended to be at least 5 seconds, default value=10)
	
    listIndex=[]
    listpTransmitted1=[]	
    listpTransmitted2=[]	

    # VESNA power generating list. This must be sorted. Powers are in dBm
    available_generating_powers = [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30]
	
    # PLAYER 1
    Transmitter1=51
    Receiver1=52	

    # PLAYER 2
    Transmitter2=54
    Receiver2=58		
	
    # Desired increase of the players' lower SINR
    #IncreaseOfSINR=2 
    #IncreaseOfSINR=1.1
    IncreaseOfSINR=1.1	
    #IncreaseOfSINR=4 # for demonstrating that it is possible po increase the SINR for higher factors	
    #IncreaseOfSINR=2.5 	
	
    # TYPE OF USE: when real transmission power levels of VESNA are used or not
    # 1 - measuring gains only once at the beginning and setting transmission power at the end according to "available_generating_powers"
    # 2 - gains are continuously measured and discrete values for p1 and p2 set during the game. NOTICE: only used, when the gains are measured in real time, and not in advance (or set manually)
    TypeOfUse=1 # now not in use

    # TRANSMISSION POWER for gains calculation
    pTransmittedGainCalcdBm=-15
    #pTransmittedGainCalcdBm=0		
	
    pTransmitGainCalculation1dBm=pTransmittedGainCalcdBm
    pTransmitGainCalculation2dBm=pTransmittedGainCalcdBm	

    # REQUIRED UTILITY TO END ITERATION
    #TargetUtility=-1.0e-020
    TargetUtility=-1.0e-013
    #TargetUtility=-1.0e-012	
	
    # SAVE RESULTS
    saveresults= True
    #saveresults= False	
	
	
    # INITIAL TRANSMISSION POWER (reasonable to be set at the same level as for gains calculation)
    pTransmitteddBm=pTransmittedGainCalcdBm
    #pTransmitteddBm=-30	

    pTransmitted1dBm=pTransmitteddBm
    pTransmitted2dBm=pTransmitteddBm	

    # Maximum number of iterations in the game to prevent that, in the case that the game does not converge, it is not played infinite time	
    #MaxNrOfIterations=100
    MaxNrOfIterations=1000
    #MaxNrOfIterations=5	
	
	# Counting the number of iterations during the game
    index=1	

    listIndex.append(index)
    listpTransmitted1.append(pTransmitted1dBm)
    listpTransmitted2.append(pTransmitted2dBm)	
	
    # EXPECTED NOISE	
    #Noise1=3.38672324669e-12
    #Noise1=2.2512786538e-10 # to demonstrate the increase with IncreaseOfSINR=4
    #Noise2=3.35732111544e-12
    #Noise2=1.37506518321e-11 # to demonstrate the increase with IncreaseOfSINR=4
	
	# MEASURING NOISE IN THE OFFICE
    Noise1=Noise.getInstantNoise(9501, Receiver1)
    Noise2=Noise.getInstantNoise(9501, Receiver2)	
	
	
	# MEASURING GAINS IN THE JSI OFFICE
	#h11
    h11 = GainCalculations.calculateInstantGainForSINR(9501, Transmitter1, Receiver1, pTransmitGainCalculation1dBm, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)
    #h11 = GainCalculations.calculateInstantGainForSINR(9501, 51, 52, 0, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)	
    #h11 =0.000457079604928 # to demonstrate the increase with IncreaseOfSINR=4
    #h11 =0.000269415326193
    #h11 =1.17914835642e-06	# for testing the required convergence condition
	#h21	
    h21 = GainCalculations.calculateInstantGainForSINR(9501, Transmitter2, Receiver1, pTransmitGainCalculation2dBm, measuring_freq=2422e6, saveresults=True, transmitting_duration=5) 
    #h21 = GainCalculations.calculateInstantGainForSINR(9501, 54, 52, 0, measuring_freq=2422e6, saveresults=True, transmitting_duration=5) 	
    #h21 =1.17914835642e-06 # to demonstrate the increase with IncreaseOfSINR=4
    #h21 =1.4646903564e-05
    #h21 =0.000457079604928 # for testing the required convergence condition	
	#h22
    h22 = GainCalculations.calculateInstantGainForSINR(9501, Transmitter2, Receiver2, pTransmitGainCalculation2dBm, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)
    #h22 = GainCalculations.calculateInstantGainForSINR(9501, 54, 58, 0, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)	
    #h22 =1.30015521864e-04 # to demonstrate the increase with IncreaseOfSINR=4
    #h22 =4.83003296862e-06
    #h22 =2.91873033877e-06 # for testing the required convergence condition	
	#h12	
    h12 = GainCalculations.calculateInstantGainForSINR(9501, Transmitter1, Receiver2, pTransmitGainCalculation1dBm, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)
    #h12 = GainCalculations.calculateInstantGainForSINR(9501, 51, 58, 0, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)	
    #h12 =2.91873033877e-06 # to demonstrate the increase with IncreaseOfSINR=4
    #h12 =5.08980966629e-07
    #h12 =1.30015521864e-04 # for testing the required convergence condition	
	
    print Noise1
    print "Noise1: %.3f dBm" %(10.00*math.log10(Noise1/0.001))	
	
    print Noise2
    print "Noise2: %.3f dBm" %(10.00*math.log10(Noise2/0.001))	

    #returned gain is in linear scale. 
    print h11
    print "h11: %.3f dB" %(10.00*math.log10(h11))
    print h21
    print "h21: %.3f dB" %(10.00*math.log10(h21))
    print h22
    print "h22: %.3f dB" %(10.00*math.log10(h22))
    print h12
    print "h12: %.3f dB" %(10.00*math.log10(h12))

    # Checking if received signals are higher than interference
    if not ((h11>h21) and (h22>h12)):
       print "THE REQUIRED CONVERGENCE CONDITION IS NOT SATISFIED"
       print "The game is not played as it can not converge."		   
       return	   

    # Transmission powers of both players		   
    pTransmitted1=math.pow(10, pTransmitted1dBm/10.00) * 0.001
    pTransmitted2=math.pow(10, pTransmitted2dBm/10.00) * 0.001

    # Signal-to-noise ratio for both players	
    SINR1 = (pTransmitted1 * h11) / (pTransmitted2 * h21 + Noise1)	
    SINR2 = (pTransmitted2 * h22) / (pTransmitted1 * h12 + Noise2)

    print SINR1
    print "SINR1: %.3f dB" %(10.00*math.log10(SINR1))	

    print SINR2
    print "SINR2: %.3f dB" %(10.00*math.log10(SINR2))	
	
    # Interference for both players	
    I1=pTransmitted2 * h21
    I2=pTransmitted1 * h12

    # Defininf the rule of the game: we want to increas the SINR of the player with the lower SINR by factor of parameter TargetUtility		
    if SINR1 > SINR2:
       SINR2Required=SINR2 * IncreaseOfSINR
       SINR1Required=SINR1	 
	
    if SINR2 >= SINR1:
       SINR1Required=SINR1*IncreaseOfSINR
       SINR2Required=SINR2

    print SINR1Required	
    print "SINR1Required: %.3f dB" %(10.00*math.log10(SINR1Required))
	
    print SINR2Required	
    print "SINR2Required: %.3f dB" %(10.00*math.log10(SINR2Required))	

    # Required received powers for desired SINRs for both players	
    pReceivedrequired1=(I1+Noise1) * SINR1Required	
    pReceivedrequired2=(I2+Noise2) * SINR2Required	

    # Required transmission powers for desired SINRs for both players	
    pTransmittedrequired1=pReceivedrequired1/h11
    pTransmittedrequired2=pReceivedrequired2/h22

    print pTransmittedrequired1
    print "pTransmittedrequired1: %.3f dBm" %(10.00*math.log10(pTransmittedrequired1/0.001))	

    print pTransmittedrequired2
    print "pTransmittedrequired2: %.3f dBm" %(10.00*math.log10(pTransmittedrequired2/0.001))	

    # Utilities of both players	
    Utility1=-math.pow((pTransmittedrequired1-pTransmitted1), 2)
    Utility2=-math.pow((pTransmittedrequired2-pTransmitted2), 2)

    print Utility1
    print "Utility1: %.f" %(Utility1)		

    print Utility2
    print "Utility2: %.f" %(Utility2)
	
    index=index+1	
	
    # For TypeOfUse is equal 2
    if TypeOfUse==2:	

       if(saveresults):	   
          results_list = [pTransmitGainCalculation1dBm, 10.00*math.log10(h11), 10.00*math.log10(h21), datetime.datetime.now()]	   
          printResultsInAFileSINR(results_list, Transmitter1)	   

       if(saveresults):	   
          results_list = [pTransmitGainCalculation2dBm, 10.00*math.log10(h22), 10.00*math.log10(h12), datetime.datetime.now()]	   
          printResultsInAFileSINR(results_list, Transmitter2)
		  
       min_diferrence = float("inf")	   
       nearest_power = None	

       for i in range(0, len(available_generating_powers)):
           if (math.fabs(10.00*math.log10(pTransmittedrequired1/0.001)-available_generating_powers[i]) < min_diferrence):
               min_diferrence = math.fabs(10.00*math.log10(pTransmittedrequired1/0.001)-available_generating_powers[i])
               nearest_power = available_generating_powers[i]			
	
       print nearest_power
       print "pTransmittedrequired1: %.3f dBm" %(nearest_power)
	   
       pTransmittedGainCalcdBm1=nearest_power	   

       pTransmittedrequired1=math.pow(10, nearest_power/10.00) * 0.001	   
       print "pTransmittedrequired1: %.3f W" %(pTransmittedrequired1)		   

       min_diferrence = float("inf")
       nearest_power = None	
	
       for i in range(0, len(available_generating_powers)):
           if (math.fabs(10.00*math.log10(pTransmittedrequired2/0.001)-available_generating_powers[i]) < min_diferrence):
               min_diferrence = math.fabs(10.00*math.log10(pTransmittedrequired2/0.001)-available_generating_powers[i])
               nearest_power = available_generating_powers[i]			
	
       print nearest_power
       print "pTransmittedrequired2: %.3f dBm" %(nearest_power)	
	   
       pTransmittedGainCalcdBm2=nearest_power
	   
       pTransmittedrequired2==math.pow(10, nearest_power/10.00) * 0.001	
       print "pTransmittedrequired2: %.3f W" %(pTransmittedrequired2)

       listIndex.append(index)
       listpTransmitted1.append(pTransmittedGainCalcdBm1)	   
       listpTransmitted2.append(pTransmittedGainCalcdBm2)	   
	
    pTransmitted1=pTransmittedrequired1
    pTransmitted2=pTransmittedrequired2

    # For TypeOfUse is equal 1	
    if TypeOfUse==1:
       listIndex.append(index)	
       listpTransmitted1.append(10.00*math.log10(pTransmitted1/0.001))
       listpTransmitted2.append(10.00*math.log10(pTransmitted2/0.001))	

    # Iterations in while loop to set the transmission powers according to the desired SINRs
    # The procedure in the while loop is similar as at the first setting of transmission powers according to the desired SINRS (see above)	
    while Utility1<TargetUtility or Utility2<TargetUtility:

       # For TypeOfUse is equal 2, we continuously measure gains	
       if TypeOfUse==2:
          h11 = GainCalculations.calculateInstantGainForSINR(9501, Transmitter1, Receiver1, pTransmittedGainCalcdBm1, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)	
          h21 = GainCalculations.calculateInstantGainForSINR(9501, Transmitter2, Receiver1, pTransmittedGainCalcdBm2, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)	
          h22 = GainCalculations.calculateInstantGainForSINR(9501, Transmitter2, Receiver2, pTransmittedGainCalcdBm2, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)	
          h12 = GainCalculations.calculateInstantGainForSINR(9501, Transmitter1, Receiver2, pTransmittedGainCalcdBm1, measuring_freq=2422e6, saveresults=True, transmitting_duration=5)	
		  
          if not ((h11>h21) and (h22>h12)):	
             print "THE REQUIRED CONVERGENCE CONDITION IS NOT SATISFIED"
             print "The game is stopped as it can not converge."			 
             return			 
		  
       SINR1 = (pTransmitted1 * h11) / (pTransmitted2 * h21 + Noise1)	
       SINR2 = (pTransmitted2 * h22) / (pTransmitted1 * h12 + Noise2) 	     
	   
       I1=pTransmitted2 * h21
       I2=pTransmitted1 * h12

       pReceivedrequired1=(I1+Noise1) * SINR1Required
       pReceivedrequired2=(I2+Noise2) * SINR2Required

       pTransmittedrequired1=pReceivedrequired1/h11
       pTransmittedrequired2=pReceivedrequired2/h22

       Utility1=-math.pow((pTransmittedrequired1-pTransmitted1), 2)
       Utility2=-math.pow((pTransmittedrequired2-pTransmitted2), 2)	   

       index=index+1	

       if index >= MaxNrOfIterations:
	      Utility1=0
	      Utility2=0
         
       if TypeOfUse==2:	

          if(saveresults):		  
             results_list = [pTransmittedGainCalcdBm1, 10.00*math.log10(h11), 10.00*math.log10(h21), datetime.datetime.now()]
             printResultsInAFileSINR(results_list, Transmitter1)

          if(saveresults):		  
             results_list = [pTransmittedGainCalcdBm2, 10.00*math.log10(h22), 10.00*math.log10(h12), datetime.datetime.now()]
             printResultsInAFileSINR(results_list, Transmitter2)
			 
          min_diferrence = float("inf")		  
          nearest_power = None	

          for i in range(0, len(available_generating_powers)):
              if (math.fabs(10.00*math.log10(pTransmittedrequired1/0.001)-available_generating_powers[i]) < min_diferrence):
                  min_diferrence = math.fabs(10.00*math.log10(pTransmittedrequired1/0.001)-available_generating_powers[i])
                  nearest_power = available_generating_powers[i]			
	
          print nearest_power
          print "pTransmittedrequired1: %.3f dBm" %(nearest_power)
		  
          pTransmittedGainCalcdBm1=nearest_power		  
	   
          pTransmittedrequired1=math.pow(10, nearest_power/10.00) * 0.001	 
          print "pTransmittedrequired1: %.3f W" %(pTransmittedrequired1)		   

          min_diferrence = float("inf")
          nearest_power = None	
	
          for i in range(0, len(available_generating_powers)):
              if (math.fabs(10.00*math.log10(pTransmittedrequired2/0.001)-available_generating_powers[i]) < min_diferrence):
                  min_diferrence = math.fabs(10.00*math.log10(pTransmittedrequired2/0.001)-available_generating_powers[i])
                  nearest_power = available_generating_powers[i]			
	
          print nearest_power
          print "pTransmittedrequired2: %.3f dBm" %(nearest_power)

          pTransmittedGainCalcdBm2=nearest_power		  
	   
          pTransmittedrequired2==math.pow(10, nearest_power/10.00) * 0.001	
          print "pTransmittedrequired2: %.3f W" %(pTransmittedrequired2)

          listIndex.append(index)	
          listpTransmitted1.append(pTransmittedGainCalcdBm1)
          listpTransmitted2.append(pTransmittedGainCalcdBm2)		  
		  
       pTransmitted1=pTransmittedrequired1
       pTransmitted2=pTransmittedrequired2
	   
       if TypeOfUse==1:
          listIndex.append(index)	   
          listpTransmitted1.append(10.00*math.log10(pTransmitted1/0.001))		   
          listpTransmitted2.append(10.00*math.log10(pTransmitted2/0.001))

    # END OF THE GAME
	
    # Displaying some parameters at the end of the game	
		  
    if TypeOfUse==2:
       if(saveresults):
          results_list = [pTransmittedGainCalcdBm1, 10.00*math.log10(h11), 10.00*math.log10(h21), datetime.datetime.now()]
          printResultsInAFileSINR(results_list, Transmitter1)

       if(saveresults):
          results_list = [pTransmittedGainCalcdBm2, 10.00*math.log10(h22), 10.00*math.log10(h12), datetime.datetime.now()]
          printResultsInAFileSINR(results_list, Transmitter2)		  
		  
    print "listIndex:"	
    print listIndex	
    print "listpTransmitted1:"
    print listpTransmitted1	
    print "listpTransmitted2:"
    print listpTransmitted2	

    print Utility1
    print "Utility1: %.f" %(Utility1)		

    print Utility2
    print "Utility2: %.f" %(Utility2)

    print pTransmitted1
    print "pTransmitted1: %.3f dBm" %(10.00*math.log10(pTransmitted1/0.001))	

    print pTransmitted2
    print "pTransmitted2: %.3f dBm" %(10.00*math.log10(pTransmitted2/0.001))

    SINR1 = (pTransmitted1 * h11) / (pTransmitted2 * h21 + Noise1)
    SINR2 = (pTransmitted2 * h22) / (pTransmitted1 * h12 + Noise2)	

    print SINR1
    print "SINR1: %.3f dB" %(10.00*math.log10(SINR1))

    print SINR2
    print "SINR2: %.3f dB" %(10.00*math.log10(SINR2))	
	
    print "NrOfIterations: %.f" %(index)
	
    min_diferrence = float("inf")
    nearest_power = None	

    for i in range(0, len(available_generating_powers)):
        if (math.fabs(10.00*math.log10(pTransmitted1/0.001)-available_generating_powers[i]) < min_diferrence):
            min_diferrence = math.fabs(10.00*math.log10(pTransmitted1/0.001)-available_generating_powers[i])
            nearest_power = available_generating_powers[i]			
	
    pTransmitteddBm1=nearest_power
    print pTransmitteddBm1	
    print "pTransmitted1: %.3f dBm" %(pTransmitteddBm1)

    min_diferrence = float("inf")
    nearest_power = None	
	
    for i in range(0, len(available_generating_powers)):
        if (math.fabs(10.00*math.log10(pTransmitted2/0.001)-available_generating_powers[i]) < min_diferrence):
            min_diferrence = math.fabs(10.00*math.log10(pTransmitted2/0.001)-available_generating_powers[i])
            nearest_power = available_generating_powers[i]			
	
    pTransmitteddBm2=nearest_power
    print pTransmitteddBm2	
    print "pTransmitted2: %.3f dBm" %(pTransmitteddBm2)

    pTransmitted1=math.pow(10, pTransmitteddBm1/10.00) * 0.001
    pTransmitted2=math.pow(10, pTransmitteddBm2/10.00) * 0.001	

    SINR1 = (pTransmitted1 * h11) / (pTransmitted2 * h21 + Noise1)
    SINR2 = (pTransmitted2 * h22) / (pTransmitted1 * h12 + Noise2)

    print SINR1
    print "SINR1: %.3f dB" %(10.00*math.log10(SINR1))	

    print SINR2
    print "SINR2: %.3f dB" %(10.00*math.log10(SINR2))	

    # Plotting results of the game (attained through iterations)
	
    min_y_list = min(available_generating_powers)
    max_y_list = max(available_generating_powers)	
	
    plot.figure(1)		
    plot.grid()
    plot.title('Player 1')
    plot.plot(listIndex, listpTransmitted1)
    plot.axis([0, len(listpTransmitted1), min_y_list - 2, max_y_list +2])	
    plot.xlabel('Iteration')
    plot.ylabel('Transmission Power (dBm)')		
	
    plot.figure(2)	
    plot.grid()
    plot.title('Player 2')
    plot.plot(listIndex, listpTransmitted2)
    plot.axis([0, len(listpTransmitted2), min_y_list - 2, max_y_list +2])	
    plot.xlabel('Iteration')
    plot.ylabel('Transmission Power (dBm)')	

    plot.figure(3)
    plot.grid()
    plot.title('Player 1 and Player 2')
    plot.plot(listIndex, listpTransmitted1)	
    plot.plot(listIndex, listpTransmitted2)
    plot.axis([0, len(listpTransmitted2), min_y_list - 2, max_y_list +2])	
    plot.xlabel('Iteration')
    plot.ylabel('Transmission Power (dBm)')	
    plot.show()	

def printResultsInAFileSINR(results_list, tx_node_id):
     #appends results_list in a file.
     
     #check if the folder exits. If not then create it
     #try to make a folder
     try:
         os.mkdir("./SINR game")
     except OSError:
         pass
        
     #try to make a folder
     try:
         #os.mkdir("./gain measurements/coor_%d" %coordinator_id)
         os.mkdir("./SINR game/transmitter%d" %tx_node_id)		 
     except OSError:
         pass
            
     #open file
     #first see if the file exits
     path = "./SINR game/transmitter%d/results_%d.dat" %(tx_node_id,tx_node_id)
     if not os.path.isfile(path) or not os.path.exists(path):
         #if the file doesn't exits, then create it
         print "Writing a new file"
         f = open(path, "w")
         f.write("[transmission power] [direct gain] [cross gain] [Date]\n")		 
         f.close()
        
     #append new data to file
     f = open(path, "a")
        
     for element in results_list:
         f.write(str(element))
         f.write("        ")
     f.write("\n")
     f.close()

main()
