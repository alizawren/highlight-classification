import subprocess
import cv2
from os import listdir

if __name__ == '__main__':

	all_labels = []
	all_results = []
	test_image_names = []
	test_images = []

	for test_image in listdir('../highlight_tests'):
		image_name = '../highlight_tests/' + test_image
		test_image_names.append(test_image)
		test_images.append(cv2.imread(image_name))
		print(test_image)
		command = "python label_image.py --graph=../highlight/output_graph.pb --labels=../highlight/output_labels.txt --input_layer=Placeholder --output_layer=final_result --image="
		command = command + '../highlight_tests/' + test_image
		
		#os.system(command)
		#print(label_image.main("--graph=../highlight/output_graph.pb", "--labels=../highlight/output_labels.txt", "--input_layer=Placeholder", "--output_layer=final_result", last_arg))

		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		output = proc.communicate()[0]
		output_parts = output.split()
		size = len(output_parts)
		labels = []
		results = []
		for i in range(5, 0, -1):
			labels.append(output_parts[size - i * 2].decode('UTF-8'))
			results.append(output_parts[size - (i * 2 - 1)].decode('UTF-8'))

		all_labels.append(labels)
		all_results.append(results)

  # Do some matlab plotting

	import matplotlib.pyplot as plt

	fig = plt.figure(figsize=(8, 3 * len(test_image_names)))
	for i in range(len(test_image_names)):
		label_list = all_labels[i]
		result_list = all_results[i]
		plt.subplot(len(test_image_names),2,i*2 + 1)
		plt.xticks([])
		plt.yticks([])
		plt.grid('off')
		plt.imshow(cv2.cvtColor(test_images[i], cv2.COLOR_BGR2RGB))

		plt.subplot(len(test_image_names),2,i*2 + 2)
		plt.xticks([])
		plt.yticks([])
		plt.grid('off')
		#plt.box('off')
		predicted_label = label_list[1]
		true_label = test_image_names[i]
		if predicted_label == true_label:
			color = 'green'
		else:
			color = 'red'
		description = "Image was: " + true_label + "\n\n"
		description = description + "Prediction was: " + label_list[0] + "\n\n"
		description = description + "Prediction | Confidence \n"
		#description = description + "Prediction was: " + label_list[0] + "\n    with a confidence of: " + result_list[0] + "\n"
		#description = description + "Other top guesses: \n"
		for i in range(0,5):
			formatted = "%-10s | %-10s\n" % (label_list[i], result_list[i])
			description = description + formatted
			#description = description + label_list[i] + ": " + result_list[i] + "\n"
		plt.text(0.1,0.07,description)
      #plt.xlabel("{} ({})".format(class_names[predicted_label], 
      #                              class_names[true_label]),
      #                              color=color)
		plt.savefig('../highlight_results.png')
		#plt.savefig('results.png')
