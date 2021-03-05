from MLC import MetaLevelControl
import json
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

if __name__ == "__main__":

    #Data: Qualities of solution of anytime K-means algorithm in json format.
    with open('data/data.json') as file:
        data = json.load(file)

    #Initialization of self explanatory variables
    qualities= data['instance-0']['qualities']
    time_duration = len(qualities)
    num_of_steps = range(time_duration)

    intrinsic_value_multiplier = 100
    time_cost_multiplier = 0.075

    #Instantiating the MetaLevelControl class
    MLC = MetaLevelControl()
    MLC.setMultipliers(intrinsic_value_multiplier, time_cost_multiplier)
    MLC.setStepInfo(time_duration, num_of_steps)


    # Simulating online anytime kmeans where each time step will have solution qualities from 0 to t time.  
    for i in range(time_duration):
        qualities1 = qualities[0:i]

        #Myopic stopping condition
        model = lambda x, a, b, c: a * np.arctan(x + b) + c
        myopic_stopping_point, utility, condition = MLC.fit(qualities1, model)
        print(condition)
        if condition == True:
            print(myopic_stopping_point, utility)
            break
    
    #plotting
    filename = "Performance profile of anytime K-means algorithm."
    path = 'plots/'+ filename + '.png'
    MLC.plotting(path, myopic_stopping_point, utility)
