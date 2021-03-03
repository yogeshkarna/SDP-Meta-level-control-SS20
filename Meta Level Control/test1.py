from mlc import MetaLevelControl
import json
import matplotlib.pyplot as plt
import matplotlib

if __name__ == "__main__":

    # with open('data/tsp.json') as file:
    with open('C:/Users/alex0/Desktop/HBRS/Semester 2/SDP/Git/SDP-Meta-level-control-SS20/Meta Level Control/data/data.json') as file:
        data = json.load(file)


    ###################

    # qualities= data['instance-0']['estimated_qualities']
    qualities= data['instance-0']['qualities']
    # data = [1 - x for x in qualities]
    # print(data[0:100])
    # qualities= [float(i) for i in data]
    print(type(qualities))
    # print(qualities)
    time_duration = len(qualities)
    num_of_steps = range(time_duration)

    ##################


    intrinsic_value_multiplier = 100
    # time_cost_multiplier = 0.01
    time_cost_multiplier = 0.075
    # time_cost_multiplier = 0.08
    MLC = MetaLevelControl(time_duration, num_of_steps, intrinsic_value_multiplier, time_cost_multiplier)


    # kmeans 
    for i in range(time_duration):
        # break
        # qualities = #
        # qualities1 = data['instance-0']['estimated_qualities'][0:i]
        # qualities1 = data['instance-0']['qualities'][0:i]
        qualities1 = qualities[0:i]
        # print(qualities1)

        #myopic stopping condition
        myopic_stopping_point, utility, condition = MLC.fit(qualities1)
        print(condition)
        if condition == True:
            print(myopic_stopping_point, utility)
            break


    #plotting 
    plt.figure(figsize=(16, 12), dpi=80)
    font = {
        # 'family' : 'normal',
        'weight' : 'bold',
        'size'   : 23}

    matplotlib.rc('font', **font)

    path = 'C:/Users/alex0/Desktop/HBRS/Semester 2/SDP/Git/SDP-Meta-level-control-SS20/Meta Level Control/plots/myopic_kmeans_final1' + '.png'
    plt.title('Performance Profile of the solution')
    plt.xlabel('Time taken')
    plt.ylabel('Value incurred')
    plt.plot(num_of_steps, utility, color='k', label='Utility function')
    plt.scatter([myopic_stopping_point], utility[myopic_stopping_point], color='m', label='Projected Stopping Point for Myopic')
    plt.legend()
    plt.savefig(path)
    plt.close()