from node import Node
from datetime import datetime as DateTime
from myQueue import MyQueue
import time
import math
import os
import datetime

class GainCalculations:
    #contains several static methods which can be used for channel gain measurements between the VESNA nodes
    #you can either use the measured channel gains saved in .dat files or perform new measurements
    
    @staticmethod
    def calculateInstantGainForSINR(coordinator_id,tx_node_id, rx_node_id, trans_power, measuring_freq = 2420e6, saveresults = True , transmitting_duration = 10):
        #this method measures the instant channel gain between tx_node_id and rx_node_id within the coordinator_id
        #calculate gain as the following: Gain_between_i_and_j = (Power received by j - Power noise)/(Power transmitted by i)
        #you can specify the frequency at which you want to measure the gain
        #you can save the results ( append ) in a file or you can just get instant gain without saving the results
        #you can specify transmitting_duration of the generated signal. Taking into account the programming times I recommend using at least 6 seconds
        
        #define two Node objects
        tx_node = Node(coordinator_id, tx_node_id)
        rx_node = Node(coordinator_id, rx_node_id)
        
        #a few measurement parameters
        #transmitting power [dBm]
        p_tx_dBm = trans_power
        
        #transmitting duration [s]. For how long will the generator generate a signal. This parameter is given in the method parameters
        
        #sensing duration [s] . For how much time will the node sense the spectrum.
        sensing_duration = 2
        
        #specify when to start the sensing (after 1-2 seconds). Note: the packet which I send to the node, includes a time (when to transmit), but, there takes some time until packet arrives at node.
        time_after = 1.5
        
        #First we want to measure the noise power, for that it is really important that no signal is generated
        attempts = 0
        while True:
            try:
                #configure rx_node
                rx_node.setSenseConfiguration(measuring_freq, measuring_freq, 400e3)
                #start sensing
                rx_node.senseStart(time.time()+time_after, sensing_duration, 5)
                #Observation: Computer clock is not synchronized with the node clock. This is a reason why we choose to start the sensing only after a few seconds, otherwise the are cases when node report that "Start time cannot be in the past"
                
                #if everything is fine, break this loop
                break
            except:
                if attempts<3:
                    attempts+=1
                    print "Calculate gain between %d and %d: Noise measurement error, retry %d" %(tx_node_id, rx_node_id, attempts) 
                    continue
                else:
                    print "Calculate gain between %d and %d: Noise measurement error, return nothing" %(tx_node_id, rx_node_id) 
                    return
                    
        #now we have the measured results in a file, we have to read the file and do the average.
        #data returned has the following structure: [[frequency], [average power in W for that frequency]]. Normally there is only one frequency because we've set the nodes to sense and generate signal only on a single channel
        noise_power = GainCalculations.getAverageDataMeasurementsFromFile(coordinator_id ,rx_node.node_id)[1][0]
        
        #now we have to generate a signal and measure the received power
        #configure and start the signal generation
        try:
            tx_node.setGeneratorConfiguration(measuring_freq, p_tx_dBm)
            tx_node.generatorStart(time.time(), transmitting_duration)
        except:
            print "Calculate gain between %d and %d :  Error at generator. Return" %(tx_node_id, rx_node_id) 
            return
        
        #get current time. I want to know when I started the signal generation
        start_gen_time = time.time()
        #wait a second just to be sure that receiver senses the signal generated. (With this we take into account other delays that can appear in testbed)
        time.sleep(0.5)
        #sense the spectrum
        attempts =0
        while True:
            try:
                #start sense after time_after seconds from now
                rx_node.senseStart(time.time()+time_after, sensing_duration, 5)
               
                #if everything is fine, break this loop               
                break
            except Exception:
                #try a few more times if something went wrong
                if attempts < 2:
                    attempts += 1
                    print "Calculate gain between %d and %d : Receive power measurement error, retry %d" %(tx_node_id, rx_node_id, attempts) 
                    continue
                else:
                    print "Calculate gain between %d and %d : Receive power measurement error, return nothing" %(tx_node_id, rx_node_id)
                    #anyway, at this point there is a signal generated, so I don't want to affect other measurements, so we have to wait until signal generation stops
                    GainCalculations.sleepUntilSignalGenerationStops(start_gen_time, transmitting_duration)
                    return
        
        #now we have in file data with the measurements. Average data from the file: [[frequencies], [average power in W for a specific frequency]]
        received_power = GainCalculations.getAverageDataMeasurementsFromFile(coordinator_id,rx_node.node_id)[1][0]
        
        print "Gain calculation between tx_%d and rx_%d : Noise power: %.6fE-12      Received power: %.6fE-12" %(tx_node_id, rx_node_id,noise_power*1e12, received_power*1e12)
        
        #calculate gain
        gain = (received_power - noise_power) / (math.pow(10.00, p_tx_dBm/10.00) * 0.001)
        if gain<0:
            #in this case, something wrong happened, no signal was generated
            print "Calculate gain between %d and %d : Bad measurement, noise power is bigger than received_power, omit this measurement" %(tx_node_id, rx_node_id) 
            #wait for the signal generation stops
            GainCalculations.sleepUntilSignalGenerationStops(start_gen_time, transmitting_duration)
            return None
        
        print "Gain between node %d and node %d: %.9fE-6  ( %.6f dB)" %(tx_node.node_id, rx_node.node_id, gain *1e6, 10.00*math.log10(gain))
        
        #write this gain in a file if this is what we want
        results_list = [gain, received_power, noise_power, math.pow(10, p_tx_dBm/10.00) * 0.001, datetime.datetime.now()]
        
        #save results
        if(saveresults):
            GainCalculations.printResultsInAFile(results_list, coordinator_id ,tx_node.node_id, rx_node.node_id)
        
        #wait until signal generation stops
        GainCalculations.sleepUntilSignalGenerationStops(start_gen_time, transmitting_duration)
        
        #return gain
        return gain
		
    @staticmethod 
    def sleepUntilSignalGenerationStops(start_gen_time, transmitting_duration):
        #use this just when you generated a signal and you want to wait until generated signal is over.
        #generally this method is used by other methods inside this class
        #print "Time passed: %f" %(time.time() - start_gen_time)
        if ( (time.time() - start_gen_time) < transmitting_duration):
            #that means we have to wait
            print "Sleep for %f until signal generation stops" %(math.ceil(transmitting_duration - (time.time() - start_gen_time)))
            time.sleep(math.ceil(transmitting_duration - (time.time() - start_gen_time)))
        return
    
    @staticmethod    
    def convertListElementsToFloat(list_to_be_converted):
        #use this when you have a list with string numbers and you want to convert the list elements to float numbers.
        #return list_to_be_converted with float elements
        #conversion can generate exceptions
        try:
            for i in range(0, len(list_to_be_converted)):
                list_to_be_converted[i] = float(list_to_be_converted[i])
            #return converted_list
            return list_to_be_converted
        except Exception:
            print Exception.message
            return None
    
    @staticmethod
    def getAverageDataMeasurementsFromFile(coordinator_id ,node_id):
        #when we do the sensing, all data is saved in a .dat file. For the same frequency, we can have multiple samples of RSSI. We want the average of the measured powers from that file
        #reads the data from file, average power at every frequency
        #returns a list with the following structure: [[frequency] , [average_power for one specific frequency]]
        #average power returned is linear [ W ]
        
        #open the file for reading
        f = open("./data/coor_%d/node_%d.dat" %(coordinator_id ,node_id) , "r")
        
        #read first line, it's a header
        f.readline()
        
        #I want to make a data_list with the following structure: [ [frequency]  ,[ [ list of all powers for that frequency] ] ]
        #An example of data_list:  [[freq1, freq2] , [[RSSI1, RSSI2, RSSI3], [RSSI1, RSSI2] ]]
        data_list = [[], []]
        
        #read the entire file
        while True:
            #read current line. It's a string at this step
            line = f.readline()
            if not line:
                break
            
            #line structure: "time   frequency_hz   power_dbm"
            #split line string (contains several numbers)
            line_list = line.split()
            #at this step, line_split is something like that: ['123',  '2340e6' , '-90']
            
            #convert data_list elements to float
            line_list = GainCalculations.convertListElementsToFloat(line_list)
            #now , line_List : [123,  2340e6, -90]
            
            try:
                #check if this frequency was added in data_list
                if line_list[1] not in data_list[0]:
                    #then, we have a new frequency which has to be added in data_list
                    data_list[0].append(float(line_list[1]))
                    data_list[1].append([ math.pow(10.00, float(line_list[2])/10.00)*1e-3 ])
                else:
                    #this frequency was added in data_list
                    #get index for that that frequency
                    index = data_list[0].index(float(line_list[1]))
                    data_list[1][index].append(math.pow(10.00, float(line_list[2])/10.00)*1e-3)
            except:
                continue
                
        #close the file
        f.close()
        #I want a list average_data: [[frequency], [average_power for that frequency]]. It will contain average power for several certain frequencies
        average_data = [[],[]]
        for i in range(0, len(data_list[0])):
            average_data[0].append(data_list[0][i])
            average_data[1].append( math.fsum(data_list[1][i])/len(data_list[1][i]))
            
        return average_data
    
    @staticmethod
    def printResultsInAFile(results_list, coordinator_id, tx_node_id, rx_node_id):
        #appends results_list in a file. The results_list contains : [gain , received_power[w] , noise_power[w], transmitted_power[w], date ]
        
        #check if the folder exits. If not then create it
        #try to make a folder
        try:
            os.mkdir("./gain measurements")
        except OSError:
            pass
        
        #try to make a folder
        try:
            os.mkdir("./gain measurements/coor_%d" %coordinator_id)
        except OSError:
            pass
            
        #open file
        #first see if the file exits
        path = "./gain measurements/coor_%d/gain_between_tx_%d_and_rx_%d.dat" %(coordinator_id ,tx_node_id,  rx_node_id)
        if not os.path.isfile(path) or not os.path.exists(path):
            #if the file doesn't exits, then create it
            print "Writing a new file"
            f = open(path, "w")
            f.write("[Gain]                [Received power ]           [Noise power]            [Transmitted power]            [Date]     - all power units in W\n")
            f.close()
        
        #append new data to file
        f = open(path, "a")
        
        for element in results_list:
            f.write(str(element))
            f.write("        ")
        f.write("\n")
        f.close()