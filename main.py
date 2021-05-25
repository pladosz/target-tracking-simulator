import matplotlib.pyplot as plt
import numpy as np


def create_noisy_data(positions,sensor_standard_deviation,size,rng,config):

    #initialize per object markers
    readings_per_object_list=[]
    for object_id in range(0,positions.shape[1]):
        #decide random number of readings from 20 to 50
        readings_number = rng.randint(config.min_observation_objects,config.max_observation_objects)
        readings_per_object_shape=(*positions[:,object_id].shape,readings_number)
        readings_per_object_x=rng.normal(positions[0,object_id],sensor_standard_deviation,readings_number)
        readings_per_object_y=rng.normal(positions[1,object_id],sensor_standard_deviation,readings_number)
        #combine the x-y
        readings_per_object=np.row_stack((readings_per_object_x,readings_per_object_y))
        #combine all points together
        readings_per_object_list.append(readings_per_object)
    #combine readings around objects
    readings_per_object_final=np.hstack(readings_per_object_list)
    ## add random readings
    #decide number of imaginery objects of this type
    imaginary_object_number = rng.randint(config.min_number_imaginary_object,config.max_number_imaginary_object)
    imaginary_objects_positions=rng.rand(2,imaginary_object_number)*size
    print(imaginary_object_number)
    print(imaginary_objects_positions)
    for fake_object_id in range(0,imaginary_object_number):
        readings_number = rng.randint(config.min_observation_imaginary_object,config.max_observation_imaginary_object)
        readings_per_object_x=rng.normal(imaginary_objects_positions[0,fake_object_id],sensor_standard_deviation,readings_number)
        readings_per_object_y=rng.normal(imaginary_objects_positions[1,fake_object_id],sensor_standard_deviation,readings_number)
        #combine the x-y
        readings_per_object=np.row_stack((readings_per_object_x,readings_per_object_y)) 
        readings_per_object_final=np.hstack((readings_per_object_final,readings_per_object))               
    #add couple of random readings
    readings_number=rng.randint(config.min_random_observation,config.max_random_observation)
    false_false_readings= rng.rand(2,readings_number)*size
    readings_per_object_final=np.hstack((readings_per_object_final,false_false_readings))
    return readings_per_object_final

class observations_config:
    #observations parameters
    min_observation_objects = 20
    max_observation_objects = 50
    #false readings parameters
    min_number_imaginary_object = 1
    max_number_imaginary_object = 5
    min_observation_imaginary_object = 5
    max_observation_imaginary_object = 12
    min_random_observation = 2
    max_random_observation = 10


if __name__=='__main__':

    #define env properties
    size = 25
    no_dogs = 5
    no_soldier = 3
    no_civilian = 2
    dog_marker = "o"
    soldier_marker = "s"
    civilian_marker = "*"
    sensor_standard_deviation = 1 #m
    probability_of_false_false = 0.1
    fig, ax = plt.subplots()
    rng = np.random.RandomState(22154)
    config = observations_config()
    #initialize random objects positions
    dogs_positions=rng.rand(2,no_dogs)*size
    soldier_positions=rng.rand(2,no_soldier)*size
    civilian_positions=rng.rand(2,no_civilian)*size
    #combine in lists
    true_object_positions_list=[dogs_positions, soldier_positions, civilian_positions]
    marker_list=[dog_marker,soldier_marker,civilian_marker]
    names_list=["dog","soldier","civilian"]

    measured_object_positions_list=[]
    for true_object_positions in true_object_positions_list:
        measured_object_positions=create_noisy_data(true_object_positions,sensor_standard_deviation,size,rng,config)
        measured_object_positions_list.append(measured_object_positions)

    #plot true and measured positions
    for object_index in range(0,len(true_object_positions_list)):
        ax.scatter(measured_object_positions_list[object_index][0,:],measured_object_positions_list[object_index][1,:], marker=marker_list[object_index], color = 'r')
        ax.scatter(true_object_positions_list[object_index][0,:],true_object_positions_list[object_index][1,:], marker=marker_list[object_index],label = names_list[object_index])


plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.legend()
plt.show()