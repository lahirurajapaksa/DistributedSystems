import Pyro4
import sys
import math
import random
#display questions to the user to get the user's basic info to facilitate delivery
userinfo={}
retrieveorder = False

def getuserinfo():
	global retrieveorder
	#will be adding to this id as we go along, need to make it somewhat unique
	customerid = ""

	#check if the user wants to enter a Customer ID?
	valid1 = False
	retrieveorder = False
	while valid1==False:
		IDresponse = input("Do you want to retrieve an existing order? (Yes/No)").strip()
		if (IDresponse.lower() =="yes"):
			retrieveorder = True
			valid1 = True
		elif (IDresponse.lower() == 'no'):
			valid1 = True
		else:
			print("Please enter Yes or No")
			continue


	if (retrieveorder == False):
		while True:
			valid = False
			while valid==False:
				firstname = input("First Name: ").strip()
				if firstname.isalpha()==False:
					print("Do not use any non-alphabetic characters")
				else:
					valid = True
			if firstname.lower() == "restart":
				continue
			else:
				userinfo['firstname'] = firstname
				#first char of customer id
				customerid = customerid + firstname[0]

			valid = False
			while valid == False:
				print('\n')
				lastname = input("Last Name: ").strip()
				if lastname.isalpha()==False:
					print("Do not use any non-alphabetic characters")
				else:
					valid = True

			if lastname.lower() == "restart":
				continue
			else:
				userinfo['lastname'] = lastname
				#second char of customer id
				customerid = customerid + lastname[0]


			print('\n')
			valid = False
			while valid == False:

				deliveryAddress = input("Delivery address: ").strip()

				if len(deliveryAddress.split())<=0:
					print('Cannot leave this field blank')
				else:
					valid = True


			if deliveryAddress.lower() == "restart":
				continue
			else:
				userinfo['deliveryaddress'] = deliveryAddress
				#third char of customer id
				customerid = customerid + deliveryAddress[0]

			print('\n')
			valid = False
			while valid == False:

				postcode = input("Postcode: ").strip()

				if len(postcode.split())<=0:
					print("Cannot leave this field blank")
				else:
					valid = True

			if postcode.lower() == "restart":
				continue
			else:
				userinfo['postcode'] = postcode
				#fourth char of customer id
				customerid = customerid + postcode[0]

			valid = False
			validrestnames = ["chinesedragon","mcdonalds","pizzahut","exoticdishes","restart"]
			while valid==False:
				print('\n')
				restaurantname = input("Which restaurant would you like to place your order at?").strip()
				#remove any whitespaces from the string
				restaurantname="".join(restaurantname.split())
				if restaurantname.isalpha()==False:
					print("Please enter a valid restaurant name")
					continue
				elif restaurantname.lower() not in validrestnames:
					print("Please enter a valid restaurant name")
					continue
				else:
					valid = True

			if restaurantname.lower() == "restart":
				continue
			else:
				userinfo['restaurantname'] = restaurantname
				#fifth char of customer id
				customerid = customerid + restaurantname[0]

				#add two random numbers to the end of it
				num1 = random.randint(1,9)
				num2 = random.randint(1,9)

				customerid = customerid + str(num1) + str(num2)
				#add the customerid to the dictionary
				print("Customer id is ",customerid)
				userinfo['customerid'] = customerid

			valid = False
			while valid == False:
				print('\n')
				ordernumbers = input("Enter the 'numbers' corresponding to your order. If you would like more than one order of the same portion, please repeat this number the desired amount. Example: 1,2,2,4  or 1,2,3  :").strip()
				ordernumbers="".join(ordernumbers.split())
				if ordernumbers.lower() == "restart":
					break
				#check that the length is an even number - this is an incorrect format
				if len(ordernumbers)%2==0:
					print('\n')
					print("Incorrect format, please refer to example")
					continue

				commacount = 0
				intcount = 0
				wrongformat = False
				#check that the number of commas and integers is valid
				for j in range(len(ordernumbers)):
					if ordernumbers[j]==",":
						commacount += 1
					elif ordernumbers[j].isdigit()==True:
						intcount += 1
					else:
						wrongformat = True

				requiredcommacount = math.floor(len(ordernumbers)/2)
				requiredintcount = math.ceil(len(ordernumbers)/2)

				if wrongformat==True:
					print("use only numerals and commas")
				elif commacount != requiredcommacount:
					print("Incorrect commas used, please refer to example")
				elif intcount != requiredintcount:
					print("Incorrect numerals used, please refer to example")
				else:
					valid = True
				# nointcount = 0
				# for i in range(0,len(ordernumbers),2):
				#     if ordernumbers[i].isdigit()==False:
				#         nointcount+=1
				# if nointcount == 0:
				# 	valid = True
				# else:
				# 	print("Use only numerals")

			if ordernumbers.lower()=="restart":
				continue
			else:
				userinfo['ordernumbers'] = ordernumbers


				return ordernumbers
				break
	else:
		#get their customer id
		valid1=False
		while valid1==False:
			OrderID = input("Please provide your Order ID to continue: ").strip()
			#this is the valid length for order ID
			if len(OrderID)==7:
				valid1=True
			else:
				print("Please enter an Order ID of valid length : 7")
				continue
		return OrderID




ipaddress = "127.0.0.1"

FoodMenu = Pyro4.core.Proxy('PYRO:FOOD2@'+ ipaddress + ':9091')

FoodDict = FoodMenu.foodmenureturn()



def displayfoodmenu():
	#get the food menus from the backend servers
	print("-----MENU-----")
	print('\n')
	for key, value in FoodDict.items():
		print(key)
		menu = FoodDict[key]
		for i in range(len(menu)):
			print(menu[i])
		print('\n')
	print('--------------')


print("Welcome to Just Hungry, strap in for some finger licking food 👅\n")
print('The menu is as follows\n')

displayfoodmenu()

listoforders = getuserinfo()

print("list of orders ",listoforders)

#create instance of the order class
OrderInstance = Pyro4.core.Proxy('PYRO:UserOrders@'+ ipaddress + ':9091')

if retrieveorder == False:
	OrderInstance.sendUserInfotoBackend(userinfo)
	#we expect to retrieve a confirmation message that the order was placed
	confirmation = OrderInstance.GetUserMessage()
	print(confirmation)
else:
	OrderInstance.sendUserInfotoBackend(listoforders)

	check = OrderInstance.GetUserMessage()
	if check == "OrderFound":
		RetrievedOrder = OrderInstance.getFullUserOrder()
		print("Retrieved Order is ")
		print(RetrievedOrder)
	else:
		print(check)

#now get the messages back from the frontend

#check whether what you sent was an OrderID or dictionary




