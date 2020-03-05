import Pyro4

#display questions to the user to get the user's basic info to facilitate delivery
def getuserinfo():

	name = input("Full Name: ").strip()
	deliveryAddress = input("Delivery address: ").strip()
	postcode = input("Postcode: ").strip()
	restaurantname = input("Which restaurant would you like to place your order at?")
	ordernumbers = input("Enter the 'numbers' corresponding to your order. If you would like more than one order of the same portion, please repeat this number the desired amount. Example:'1,2,2,4' :")
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