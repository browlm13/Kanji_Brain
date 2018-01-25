import pybrain
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import TanhLayer
from pybrain.tools.shortcuts import buildNetwork

#make sure size of array is correct
ds = SupervisedDataSet(100, 1)

#dictionary of kanji names and index (ie: sake:1 universe:2)
kanji = {'day':0, 'person':1, 'zzzTRAINING':-1}

#processing text document path/file
#data_file_path = "Documents/Processing/pixel_array_data_gen/pixel_array_data.txt"
data_file_path = "pixel_array_data.txt"

#create 2 arrays, one with all images pixel data, and one with associated kanji value
names_array = []
mass_pixel_data_arrays = []

#create test output arrays
training_names_array = []
training_mass_pixel_data_arrays = []
training_dict = {}

file = open(data_file_path, 'r')
images_data_strings = file.readlines()

#ugly for testing training data
#test_data_array_answers = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1]
test_data_array_answers = [1,1,1,1,1,1,1,0,0,0,0,0,0,0]

for image in images_data_strings:
    pixel_data_array = []
    data = image.split(' ')

    #get associated value from name key
    if(kanji.get(data[0]) != -1):
    	names_array.append(kanji.get(data[0]))

    #store pixel data
    for i in range(1,len(data)):
        if(data[i] == '0'):
            pixel_data_array.append(0)
        else:
            pixel_data_array.append(1)


    #get associated value from name key
    if(kanji.get(data[0]) != -1):
	   	#add image pixel data to mass array
	    mass_pixel_data_arrays.append(pixel_data_array)
	    #for pybrain:
	    ds.addSample( pixel_data_array, kanji.get(data[0]) )
    else:
    	training_mass_pixel_data_arrays.append(pixel_data_array)

    	
	"""
    #add image pixel data to mass array
    mass_pixel_data_arrays.append(pixel_data_array)

    #for pybrain:
    ds.addSample( pixel_data_array, kanji.get(data[0]) )
    """

#check dataset
#for inpt, target in ds:
#	print inpt, target

net = buildNetwork(100, 3, 1, bias=True, hiddenclass=TanhLayer)
trainer = BackpropTrainer(net, ds)
for i in range(0,1000000):
	if(i%10000==0):
		print trainer.train()


num_correct = 0.0
for i in range(0,len(test_data_array_answers)):
	net_output = net.activate(training_mass_pixel_data_arrays[i])

	if (test_data_array_answers[i] == 1) and (net_output > .5):
		print "CORRECT Expected {}, got {}".format(test_data_array_answers[i], net_output)
		num_correct += 1.0
	elif(test_data_array_answers[i] == 0) and (net_output < .5):
		print "CORRECT Expected {}, got {}".format(test_data_array_answers[i], net_output)
		num_correct += 1.0
	else:
		print "WRONG Expected {}, got {}".format(test_data_array_answers[i], net_output)

numerator = num_correct
denominator = len(test_data_array_answers)
ratio_correct = numerator/denominator * 100

print "neural net scored {} % correct on test data set".format(ratio_correct)

#trainer.trainUntilConvergence()