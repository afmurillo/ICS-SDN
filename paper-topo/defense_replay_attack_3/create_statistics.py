sensor_data=[]
ids_data=[]

sensor_normal_count = 0
sensor_attack_count = 0

ids_normal_count = 0
ids_attack_count = 0

true_positive = 0.0
false_positive = 0.0

false_negative = 0.0
true_negative = 0.0

accuracy = 0.0
precision = 0.0
sensibility = 0.0
specificity = 0.0

with open("replay_lit101.log") as f:
	for linea in f:
		a=linea.split(" ")
		sensor_data.append(a[3].split("\n")[0])
f.close()

for i in range(len(sensor_data)):
		if (sensor_data[i] == 'NORMAL'):
			sensor_normal_count = sensor_normal_count  +1 
		if (sensor_data[i] == 'ATTACK'):
			sensor_attack_count = sensor_attack_count  +1 

with open("ids101.log") as i:
	for linea in i:
		a=linea.split(" ")
		ids_data.append(a[4])

i.close()

for i in range(len(ids_data)):
		if (ids_data[i] == 'NORMAL'):
			ids_normal_count = ids_normal_count  +1 
		if (ids_data[i] == 'ATTACK'):
			ids_attack_count = ids_attack_count  +1 


print "Sensor normal ", sensor_normal_count
print "Sensor attack ", sensor_attack_count

print "IDS normal ", ids_normal_count
print "IDS attack ", ids_attack_count


print "\n"

sensor_count = sensor_normal_count + sensor_attack_count

data_len = 0
if (len(sensor_data) > len(ids_data)):
	data_len = ids_data
else:
	data_len = sensor_data

for i in range (len(data_len)):

	# True Positive
	if  (sensor_data[i] == 'ATTACK') and (ids_data[i]) == 'ATTACK':
		true_positive = true_positive + 1
	elif (sensor_data[i] == 'ATTACK') and (ids_data[i]) == 'NORMAL':
		false_negative =  false_negative + 1
	elif (sensor_data[i] == 'NORMAL') and (ids_data[i]) == 'ATTACK':
		false_positive = false_positive + 1 
	elif (sensor_data[i] == 'NORMAL') and (ids_data[i]) == 'NORMAL':
		true_negative = true_negative + 1 

accuracy = (true_negative + true_positive) / sensor_count
precision = true_positive / (true_positive + false_positive) 
sensibility = true_positive / (true_positive + false_negative)
specificity = true_negative / (false_positive + true_negative)

print "F+P", sensor_count

print "True Positives: ", true_positive
print "False Negatives: ", false_negative

print "False Positives: ", false_positive
print "True Negatives: ", true_negative

print "Accuracy: ", accuracy
print "p ", precision
print "r  ", sensibility
print "e ", specificity


