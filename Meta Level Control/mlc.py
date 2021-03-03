import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib
import json

class MetaLevelControl():
    ''' Meta Level Control Class'''
    def __init__(self, time_duration, num_of_steps, intrinsic_value_multiplier, time_cost_multiplier):
        
        self.time_duration = time_duration
        self.num_of_steps = num_of_steps
        self.intrinsic_value_multiplier = intrinsic_value_multiplier
        self.time_cost_multiplier = time_cost_multiplier

        self.utility = 0
        self.next_utility = 0
        self.current_utility = 0

    def intrinsic_value_function(self, qualities, cost):
        ''' Finding the intrinsic values of the qualities. '''
        return np.multiply(cost, qualities)


    def cost_of_time(self, number_of_steps, cost):
        ''' Computing the cost of time. '''
        return np.exp(np.multiply(cost, number_of_steps))


    def utility_function(self, instrinsic_value, cost_of_time):
        ''' Computing the Utility function as difference between intrinsic value and cost of time. '''
        return instrinsic_value - cost_of_time


    def fit(self, qualities):
        ''' Fit and predict the myopic stopping point '''
        
        self.qualities = qualities
        self.stop_point = self.time_duration - 1

        # 
        performance_model = lambda x, a, b, c: a * np.arctan(x + b) + c

        try:
            if len(qualities) < 10:
                return self.stop_point, 0, False

            
            start = 0
            end = len(qualities)
            
            parameters, _ = curve_fit(performance_model, self.num_of_steps[start:end], self.qualities[start:end])
            performance_projections = performance_model(self.num_of_steps, parameters[0], parameters[1], parameters[2])

            ''' Replace Temp with Query 
            Instead of using 2 variables to store the intermediate temp variables, we provide a query'''
            # intrinsic_values = self.intrinsic_value_function(performance_projections, self.intrinsic_value_multiplier)
            # time_costs = self.cost_of_time(self.num_of_steps, self.time_cost_multiplier)
            # utility = self.utility_function(intrinsic_values, time_costs)
            self.utility = self.utility_function(self.intrinsic_value_function(performance_projections, self.intrinsic_value_multiplier), self.cost_of_time(self.num_of_steps, self.time_cost_multiplier))

            # current_intrinsic_value = self.intrinsic_value_function(self.qualities[end - 1], self.intrinsic_value_multiplier)
            # current_time_cost = self.cost_of_time(end - 1, self.time_cost_multiplier)
            # current_utility = self.utility_function(current_intrinsic_value, current_time_cost)
            self.current_utility = self.utility_function(self.intrinsic_value_function(self.qualities[end - 1], self.intrinsic_value_multiplier), self.cost_of_time(end - 1, self.time_cost_multiplier))


            # next_intrinsic_value = self.intrinsic_value_function(performance_projections[end], self.intrinsic_value_multiplier)
            # next_time_cost = self.cost_of_time(end, self.time_cost_multiplier)
            # next_utility = self.utility_function(next_intrinsic_value, next_time_cost)
            self.next_utility = self.utility_function(self.intrinsic_value_function(performance_projections[end], self.intrinsic_value_multiplier), self.cost_of_time(end, self.time_cost_multiplier))

            #checking if the condition for stopping is satified or not
            if self.next_utility - self.current_utility <= 0:
                return end - 1, self.utility, True
        except Exception as e:
            pass
        return self.stop_point, 0, False


    def plotting(self, path, myopic_stopping_point, utility):
        ''' Plotting the '''
        plt.figure(figsize=(16, 12), dpi=80)
        font = {
            # 'family' : 'normal',
            'weight' : 'bold',
            'size'   : 23}

        matplotlib.rc('font', **font)
        plt.title('Performance Profile of the solution')
        plt.xlabel('Time taken')
        plt.ylabel('Value incurred')
        plt.plot(self.num_of_steps, utility, color='k', label='Utility function')
        plt.scatter([myopic_stopping_point], utility[myopic_stopping_point], color='m', label='Projected Stopping Point for Myopic')
        plt.legend()
        plt.savefig(path)
        plt.close()


# if __name__ == "__main__":

#     # with open('data/tsp.json') as file:
#     with open('C:/Users/alex0/Desktop/HBRS/Semester 2/SDP/Git/SDP-Meta-level-control-SS20/Meta Level Control/data/data.json') as file:
#         data = json.load(file)

#     qualities= data['instance-0']['qualities']
#     time_duration = len(qualities)
#     num_of_steps = range(time_duration)

#     ##################


#     intrinsic_value_multiplier = 100
#     # time_cost_multiplier = 0.01
#     time_cost_multiplier = 0.075
#     # time_cost_multiplier = 0.08
#     MLC = MetaLevelControl(time_duration, num_of_steps, intrinsic_value_multiplier, time_cost_multiplier)


#     # kmeans 
#     for i in range(time_duration):
#         qualities1 = qualities[0:i]
#         #myopic stopping condition
#         myopic_stopping_point, utility, condition = MLC.fit(qualities1)
#         if condition == True:
#             print(myopic_stopping_point, utility)
#             break
    
#     path = 'C:/Users/alex0/Desktop/HBRS/Semester 2/SDP/Git/SDP-Meta-level-control-SS20/Meta Level Control/plots/myopic_kmeans_final2' + '.png'
#     MLC.plotting(path, myopic_stopping_point, utility)

