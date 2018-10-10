import cv2
import os
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import glob
import math
import shutil
from PIL import Image, ImageTk

#Simple class for front-end realisation of the end of setup
class Setup(object):
        complete = False
        
class Door(object):
	PIN = "" #To be generated upon setup
	unlocked = False #Turns into true when person is recognised
	recognised = ""
	
class Person(object):
	this_name = ""
	folder = ""
	num_instances = 0
	people = {}

	# The class "constructor" - It's actually an initializer 
	def __init__(self, name, folder):
		Person.num_instances = Person.num_instances + 1
		self.name = name
		self.folder = folder

#These methods are for terminal use instead of FAIC with a GUI
		
#def unlock_screen():
#	print "                                                                 "
#	print "                                                                 "
#	print "                                                                 "
#	print "                                                                 "
#	print "                         ***FAIC Inc.***                         "
#	print "                                                                 "
#	print "                                                                 "
#	print "                                                                 "
#	print "                                                                 "
#	ans = raw_input("              Press -u- to unlock door with your face            ")
#	print "                                                                 "
#	print "                                                                 "
#
#	if ans == "u":
#		recognise_user()
#		if Door.unlocked == True:
#			menu_screen()
#		elif Door.unlocked == False:
#			ans2 = raw_input("1.Try again / 2.Use PIN? ")
#			if ans2 == "1":
#				recognise_user()
#			elif ans2 == "2":
#				enter_pin = raw_input("Enter PIN: ")
#				if int(enter_pin) == Door.PIN:
#					print "PIN Override successful, door unlocked"#
#					Door.unlocked = True
#					menu_screen()
#					
#def menu_screen():
#	print " ____________________________MENU__________________________ "
#	print "|                                                          |"
#	print "|  1. Re-lock Door                                         |"
#	print "|  2. Settings                                             |"
#	print "|__________________________________________________________| "
#	menu_choice = raw_input("...")
#	if menu_choice == "1":
#		Door.unlocked = False
#		print "Door has been locked."
#	elif menu_choice == "2":
#		settings_screen()
#
#def settings_screen():
#	print " __________________________SETTINGS________________________ "
#	print "|                                                          |"
#	print "|  1. Edit Users                                           |"
#	print "|  2. Register New User                                    |"
#	print "|  3. Change PIN                                           |"
#	print "|__________________________________________________________|"
#	settings_choice = raw_input("...")
#	if settings_choice == "1":
#		edit_users_screen()
#	elif settings_choice == "2":
#		username = raw_input("What is your name?: ")
#		register_user(username, Person.people)
#	elif settings_choice == "3":
#		pin_change = raw_input("Are you sure you want to generate a new pin? Y/N")
#		if pin_change == "Y":
#			Door.PIN = generate_PIN()
#			print "Your new PIN is: ", Door.PIN
#
#def edit_users_screen():
#	print " ____________________________USERS_________________________ "
#	print "|                                                          |"
#	for i in range(Person.num_instances):
#		print "|  " + str(i+1) + ". " + str(Person.people.keys()[i])
#	print "|__________________________________________________________|"
#	user_choice = raw_input("First select a user (by number)...")
#	print str(Person.people.keys()[int(user_choice)-1]) + " - A. Edit Name / B. Retake Pictures / C. Delete"
#	option_choice = raw_input("Now select an action (by letter)...")
#
#	if option_choice == "A":
#		new_name = raw_input("Enter new name: ")
#		os.rename(str(Person.people[Person.people.keys()[int(user_choice)-1]].folder), "training/" + new_name)
#		Person.people[new_name] = Person.people.pop(Person.people.keys()[int(user_choice)-1])
#		Person.people[new_name].folder = "training/" + new_name
#		
#	elif option_choice == "C":
#		#del Person.people.keys()[int(user_choice-1)]
#		
#		#os.remove("training/" + Person.people.keys()[int(user_choice)-1])
#		path = "training/" + Person.people.keys()[int(user_choice)-1]
#		shutil.rmtree(path, ignore_errors=False, onerror=None)
#		del Person.people[Person.people.keys()[int(user_choice)-1]]
#		Person.num_instances = Person.num_instances - 1
#		if Person.num_instances == 0:
#			setup()
#		
#def home_screen():
#	print "You currently have " + str(Person.num_instances) + " homeowner(s)..."
#	
#	if Person.num_instances == 0:
#		setup()
#	#print "You currently have " + str(Person.num_instances) + " homeowner(s)"
#	answer = raw_input("Do you want to create another user? Y/N")
#	if answer == "Y":
#		username = raw_input("What is your name?: ")
#		register_user(username, Person.people)
#
#	unlock_screen()
#
#def setup():
#	
#	time.sleep(1)
#	print "Please set up a homeowner..."
#	print "                                                                 "
#	time.sleep(1)
#	print "                        ~SETUP~                                  "
#	print "                                                                 "
#	username = raw_input("What is your name?: ")
#	register_user(username, Person.people)
#
#	Door.PIN = generate_PIN()
#	print "Your back-up PIN is: ", Door.PIN
#def take_picture_for_comparison():
#	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#	cap = cv2.VideoCapture(0)
#	while(True):
#		ret, frame = cap.read()
#		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#		#feedback
#		for (x, y, w, h) in faces:
#			cv2.rectangle(frame, (x,y),(w+w, y+h), (255,0,0),2)
#			roi_gray = gray[y:y+h, x:x+w]
#		cv2.imshow('image', frame)
#		if cv2.waitKey(1) & 0xFF == ord('1'):
#			crop_img = frame[y: y + h, x: x + w] # Crop from x, y, w, h -> 100, 200, 300, 400
#			cv2.imwrite("testing/videotest.jpg", crop_img)
#			break
#def take_images(username, people):
#	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#	cap = cv2.VideoCapture(0)
#
#	images_taken = 0
#	print "You will need to take 5 photos of yourself, when you have aligned your face to the correct position, press -space-"
#	time.sleep(3)
#	print "Whilst looking directly into the camera:"
#	time.sleep(1)
#	print "1. Position your face infront of the camera, with half a metre's distance"
#	
#	while(images_taken != 5):
#	      
#		ret, frame = cap.read()
#		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#		#feedback
#		for (x, y, w, h) in faces:
#		      cv2.rectangle(frame, (x,y),(w+w, y+h), (255,0,0),2)
#		      roi_gray = gray[y:y+h, x:x+w]
#		cv2.imshow('image', frame)
#	      
#		if cv2.waitKey(1) & 0xFF == ord(" "):
#			if images_taken == 0:
#				images_taken = crop_and_save(images_taken, frame[y: y + h, x: x + w], "1.jpg", people[username])
#				print "2. Turn your head 5 degrees to the left of centre..."
#			elif images_taken == 1:
#				images_taken = crop_and_save(images_taken, frame[y: y + h, x: x + w], "2.jpg", people[username])
#				print "3. 5 degrees to the right of centre..."
#			elif images_taken == 2:
#				images_taken = crop_and_save(images_taken, frame[y: y + h, x: x + w], "3.jpg", people[username])
#				print "4. 5 degrees up from centre..."
#			elif images_taken == 3:
#				images_taken = crop_and_save(images_taken, frame[y: y + h, x: x + w], "4.jpg", people[username])
#				print "5. and finally 5 degrees down from centre..."
#			elif images_taken == 4:
#				images_taken = crop_and_save(images_taken, frame[y: y + h, x: x + w], "5.jpg", people[username])

def recognise_user():
        #This is used when the door lock is prompted
	M, N, avg_img, num_of_eig, eigenfaces, wi, xci, X = training_PCA()
	testing_PCA(M, N, avg_img, num_of_eig, eigenfaces, wi, xci, X)
	
def make_person(name, folder):
	person = Person(name, folder)
	os.mkdir(folder)
	return person

def register_user(name, people):
	people[name] = make_person(name, "training/" + name + "/")
	take_images(name, people)

def crop_and_save(images_taken, framecrop, picture_number, person):
	crop_img = framecrop # Crop from x, y, w, h -> 100, 200, 300, 400
	cv2.imwrite(person.folder + picture_number, crop_img)
	return images_taken + 1
    
def generate_PIN():
	pin = random.randint(100000,999999)
	return pin

def create_base():
        #Creates the Base face to allow for more than 1 user
        Person.people["base"] = Person("base", "training/base")
        
def matmult(a,b):
	zip_b = zip(*b)
	#uncomment next line if python 3 : 
	#zip_b = list(zip_b)
	return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) for col_b in zip_b] for row_a in a]

def training_PCA():
        #Size of the image dimensions
	N = 50
	#Array of all of the images
	train_imgs = []
	for key, value in Person.people.iteritems():
		files = glob.glob ("training" + "/" + key + "/" + "*.jpg")
		for myFile in files:
			#Read image into greyscale
			image = cv2.imread (myFile, cv2.IMREAD_GRAYSCALE)
			#Resize to 50x50
			image = cv2.resize(image, (N,N))                 
			train_imgs.append (image) 


	#M is the amount of facial images
	M = len(train_imgs)
	#N*N = 50*50, X is matrix of 2D-vectorised faces
	X = np.reshape(train_imgs, (M, N*N))
	#Calculate mean image
	avg_img = np.mean(X, axis=0)
	#This is purely just to view the average image, is not used within the software as of now
	#avg_img_rshp = np.reshape(avg_img, (N,N))
	#avg_img_rshp = Image.fromarray(avg_img_rshp)

	#Normalise (remove mean)
	A = []
	for i in range(M):
		A.append(X[i] - avg_img)

	#Calculate covariance matrix
	C = np.cov(A)

	#Determine eigenvalues
	eigenvalues, eigenvectors = np.linalg.eig(C) #only 4 diagonal values

	#Eigenface in large dimension, A*eigenvectors is eigenvector of Clarge
	v_large = matmult(eigenvectors, A)

	#Reshape to construct eigenfaces
	eigenfaces = []
	for k in range(M):
		c = v_large[k]
		eigenfaces.append(np.reshape(c,(N,N)))

	print "eigenfaces: ", np.array(eigenfaces).shape
	xci = np.argsort(eigenvalues)[::-1]
	#print "xci :", xci

	#Calculate weights
	num_of_eig = M
	wi = [[0 for y in range(M)] for x in range(num_of_eig)]
	for mi in range(M): #mi iterates through number of faces
		for k in range(num_of_eig):
			k_eigenface_1D = np.reshape(eigenfaces[xci[k]], (1,N*N)) #Create vectorised eigenface for k
			mi_face_1D = np.reshape(A[mi], (1,N*N)) 
			wi[mi][k] = (mi_face_1D*k_eigenface_1D).sum() #Create the weights
        
	return M, N, avg_img, num_of_eig, eigenfaces, wi, xci, X

def testing_PCA(M, N, avg_img, num_of_eig, eigenfaces, wi, xci, X):
	
	#For terminal use: take_picture_for_comparison()
        #Read image into greyscale
	test = cv2.imread ("testing/recognise_me.jpg", cv2.IMREAD_GRAYSCALE)
	test = cv2.resize(test, (N,N))
	test = np.reshape(test, (1, N*N))
	test_normalised = test - avg_img

        #loop through number of eigenfaces
	wtest = [0 for x in range(num_of_eig)]
	for tt in range(num_of_eig):
                #mutiply normalised face by eigenfaces to proudce projection of the eigenfaces from test face
		wtest[tt] = (test_normalised * np.reshape(eigenfaces[xci[tt]],(1, N*N))).sum()

        #Find the difference of weights for each training face from the test face using euclidean distance
	diff_weights = [0 for x in range(M)]
	#Loop through number of faces
	for mi in range(M):
		fsumcur=0
		#Loop through number of eigenfaces
		for tt in range(num_of_eig):
                        #Calculate euclidean distance 
			fsumcur = fsumcur + ((wtest[tt] - wi[mi][tt])**2)
                #square root it
		d_temp = math.trunc(math.sqrt(fsumcur))
		#and again to minimize complex value
		diff_weights[mi] = math.trunc(math.sqrt(d_temp))
	print "Difference in weights:", diff_weights

	#This takes into consideration the five faces used to generate an overall average weight per person
	new_diff = [0 for x in range(Person.num_instances)]
	temp = 0
	for i in range(Person.num_instances):
		new_diff[i] = (diff_weights[temp] + diff_weights[temp+1] + diff_weights[temp+2] + diff_weights[temp+3] + diff_weights[temp+4])/5
		temp = temp + 5

	for i in range(Person.num_instances):
		print str(Person.people.keys()[i]) + " chance = " + str(new_diff[i])

        #!This threshold does not function with one person, however with >=2 people it is efficient
	# at identifying the correct people for recognition and discriminating against non-users to
	# be unrecognised
	#threshold = 0.5*np.amax(diff_weights)
	#print "threshold is: ", threshold

	#!This threshold works with the BASE CLASS & >=1 person(s)
	# and is a set limit which I have dervied throughout a series of tests
	threshold = 1800

	#Find closest match through finding person with minimum value 
	closest_match = np.argmin(new_diff)
	
	Door.recognised = Person.people.keys()[closest_match]
	if new_diff[closest_match] <= threshold:
		print " --------------------- Welcome home: " + Person.people.keys()[closest_match] + "! ---------------------"
		print " "
		Door.unlocked = True
	elif diff_weights[closest_match] > threshold:
		print("Round 1: You are unrecognised")
		Door.unlocked = False
		
#For terminal use: home_screen()
