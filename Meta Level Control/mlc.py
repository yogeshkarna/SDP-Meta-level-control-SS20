import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib

class MetaLevelControl():
    ''' Meta Level Control Class'''
    def __init__(self):
        self.utility = 0
        self.next_utility = 0
        self.current_utility = 0


    '''----Separate Query for Modifier-----'''
    '''----Setters for changing the class variables.----'''
    def setMultipliers(self, intrinsic_value_multiplier, time_cost_multiplier):
        ''' Setter function for intrinsic value and time cost multiplier'''
        self.intrinsic_value_multiplier = intrinsic_value_multiplier
        self.time_cost_multiplier = time_cost_multiplier

    def setStepInfo(self, time_duration, num_of_steps):
        ''' Setter function for time duration and number of steps'''
        self.time_duration = time_duration
        self.num_of_steps = num_of_steps

    def intrinsic_value_function(self, qualities, cost):
        ''' Finding the intrinsic values of the qualities. '''
        return np.multiply(cost, qualities)


    def cost_of_time(self, number_of_steps, cost):
        ''' Computing the cost of time. '''
        return np.exp(np.multiply(cost, number_of_steps))


    def utility_function(self, instrinsic_value, cost_of_time):
        ''' Computing the Utility function as difference between intrinsic value and cost of time. '''
        return instrinsic_value - cost_of_time


    def fit(self, qualities, model):
        ''' Fit and predict the myopic stopping point '''
        
        self.qualities = qualities
        self.stop_point = self.time_duration - 1

        ''' Example model for reference'''
        # performance_model = lambda x, a, b, c: a * np.arctan(x + b) + c
        performance_model = model

        try:
            if len(qualities) < 10:
                return self.stop_point, 0, False

            start = 0
            end = len(qualities)
            
            parameters, _ = curve_fit(performance_model, self.num_of_steps[start:end], self.qualities[start:end])
            performance_projections = performance_model(self.num_of_steps, parameters[0], parameters[1], parameters[2])

            '''----Replace Temp with Query-----'''
            '''----Instead of using 2 variables to store the intermediate temp variables, we provide a query----'''
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


    '''----Extract Method---- '''
    '''----Code fragments that goes together are grouped together into a function.----'''
    def plotting(self, path, myopic_stopping_point, utility):
        ''' Plotting the accepted solution's performance profile. '''
        plt.figure(figsize=(18, 12), dpi=80)
        font = {
            'weight' : 'bold',
            'size'   : 25}

        matplotlib.rc('font', **font)
        plt.xlabel('Time incurred')
        plt.ylabel('Value incurred')
        plt.title('Performance Profile of the solution')
        plt.plot(self.num_of_steps, utility, color='k', label='Utility function')
        plt.scatter([myopic_stopping_point], utility[myopic_stopping_point], color='m', label='Projected Stopping Point for Myopic')
        plt.legend()
        plt.savefig(path)
        plt.close()