import Pyro4
import sys
#display questions to the user to get the user's basic info to facilitate delivery
def getuserinfo():
	valid = False
	while valid==False:
		firstname = input("First Name: ").strip()
		if firstname.isalpha()==False:
			print("Do not use any non-alphabetic characters")
		else:
			valid = True

	valid = False
	while valid == False:
		lastname = input("Last Name: ").strip()
		if lastname.isalpha()==False:
			print("Do not use any non-alphabetic characters")
		else:
			valid = True
	
	deliveryAddress = input("Delivery address: ").strip()

	postcode = input("Postcode: ").strip()

	valid = False
	while valid==False:
		restaurantname = input("Which restaurant would you like to place your order at?").strip()
		if restaurantname.isalpha()==False:
			print("Do not use any non-alphabetic characters")
		else:
			valid = True

	valid = False
	while valid == False:
		ordernumbers = input("Enter the 'numbers' corresponding to your order. If you would like more than one order of the same portion, please repeat this number the desired amount. Example:'1,2,2,4' :").strip()
		for i in range(0,len(ordernumbers),2):
		    if ordernumbers[i].isdigit()==False:
		        print("only use numerals")
		    else:
		    	valid = True
	        

def connecttofrontend():
	ipaddress = "192.168.1.3"

	FoodMenu = Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + ':9091')

	return FoodMenu

def getfoodmenusfrontend(FoodMenu):
	FoodDict = FoodMenu.foodmenureturn()

	return FoodDict	

classreturn = connecttofrontend()
FoodDict = getfoodmenusfrontend(classreturn)



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

getuserinfo()