import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import json

# def get_instances(filename):
#     with open(filename) as file:
#         return json.load(file)

def intrinsic_value_function(qualities, multiplier):
    # intrinsic_value = qualities*multiplier
    return np.multiply(multiplier, qualities)


def time_cost(steps, multiplier):
    return np.exp(np.multiply(multiplier, steps))


def utility_function(instrinsic_values, time_costs):
    return instrinsic_values - time_costs

def non_stopping_point(comprehensive_values):
    # df = pd.Dataframe(comprehensive_values)
    # stopping_point = df['estmated_values'][comprehensive_values]
    return list(comprehensive_values).index(max(comprehensive_values))


def get_myopic_projected_stopping_point(qualities, steps, limit):
    intrinsic_value_groups = []
    stopping_point = limit - 1

    model = lambda x, a, b, c: a * np.arctan(x + b) + c

    for end in range(10, limit):
        try:
            start = 0
            params, _ = curve_fit(model, steps[start:end], qualities[start:end])
            projections = model(steps, params[0], params[1], params[2])

            intrinsic_values = intrinsic_value_function(projections, 100)
            time_costs = time_cost(steps, 0.075)
            comprehensive_values = utility_function(intrinsic_values, time_costs)

            intrinsic_value_groups.append(intrinsic_values)

            # current_comprehensive_value = intrinsic_value_function(qualities[end - 1], 100) - time_cost(end - 1, 0.075)
            current_intrinsic_value = intrinsic_value_function(qualities[end - 1], 100)
            current_time_cost = time_cost(end - 1, 0.075)
            current_comprehensive_value = utility_function(current_intrinsic_value, current_time_cost)



            next_intrinsic_value = intrinsic_value_function(projections[end], 100)
            next_time_cost = time_cost(end, 0.75)
            next_comprehensive_value = utility_function(next_intrinsic_value, next_time_cost)

            #checking if the condition for stopping is satified or not
            if next_comprehensive_value - current_comprehensive_value <= 0:

                return end - 1, comprehensive_values
        except Exception as e:
            pass
    return stopping_point


def get_nonmyopic_projected_stopping_point(qualities, steps, limit):
    stopping_point = 0

    model = lambda x, a, b, c: a * np.arctan(x + b) + c

    for end in range(10, limit):
        try:
            start = 0

            params, temp = curve_fit(model, steps[start:end], qualities[start:end])
            projections = model(steps, params[0], params[1], params[2])

            intrinsic_values = intrinsic_value_function(projections, 100)
            time_costs = time_cost(steps, 0.075)
            comprehensive_values = utility_function(intrinsic_values, time_costs)
            stopping_point = non_stopping_point(comprehensive_values)


            if stopping_point < end - 1:
                return end - 1
        except Exception as e:
            pass

    return stopping_point



if __name__ == "__main__":

    #loading data 
    with open('data/tsp.json') as file:
        instance = json.load(file)
    qualities_n= instance['instance-0']['estimated_qualities']
    time_limit = len(qualities_n)
    steps = range(time_limit)

    #myopic stopping condition
    myopic_p_stopping_point, comprehensive_values= get_myopic_projected_stopping_point(qualities_n, steps, time_limit)

    #plotting 
    plt.figure(figsize=(16, 12), dpi=80)
    file_path = 'plots/myopic' + '.png'
    plt.title('Performance Profile')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.plot(steps, comprehensive_values, color='k', label='Utility function')
    plt.scatter([myopic_p_stopping_point], comprehensive_values[myopic_p_stopping_point], color='m', label='Myopic Projected Stopping Point')
    plt.legend()
    plt.savefig(file_path)
    plt.close()

