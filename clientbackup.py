import Pyro4
import sys
#display questions to the user to get the user's basic info to facilitate delivery
def getuserinfo():
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


		valid = False
		while valid == False:
			lastname = input("Last Name: ").strip()
			if lastname.isalpha()==False:
				print("Do not use any non-alphabetic characters")
			else:
				valid = True

		if lastname.lower() == "restart":
			continue

		deliveryAddress = input("Delivery address: ").strip()

		if deliveryAddress.lower() == "restart":
			continue

		postcode = input("Postcode: ").strip()

		if postcode.lower() == "restart":
			continue

		valid = False
		validrestnames = ["chinesedragon","mcdonalds","pizzahut","exoticdishes","restart"]
		while valid==False:
			restaurantname = input("Which restaurant would you like to place your order at?").strip()
			#remove any whitespaces from the string
			restaurantname="".join(restaurantname.split())
			if restaurantname.isalpha()==False:
				print("Do not use any non-alphabetic characters")
				continue
			elif restaurantname.lower() not in validrestnames:
				print("Please enter a valid restaurantname")
				continue
			else:
				valid = True

		if restaurantname.lower() == "restart":
			continue

		valid = False
		while valid == False:
			ordernumbers = input("Enter the 'numbers' corresponding to your order. If you would like more than one order of the same portion, please repeat this number the desired amount. Example:'1,2,2,4' :").strip()
			ordernumbers="".join(ordernumbers.split())
			if ordernumbers.lower() == "restart":
				break
			for i in range(0,len(ordernumbers),2):
			    if ordernumbers[i].isdigit()==False:
			        print("only use numerals")
			    else:
			    	valid = True
		if ordernumbers.lower()=="restart":
			continue
		else:
			print("ordernumbers ",ordernumbers)
			return ordernumbers
			break

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
FoodMenu.returnorderstring(listoforders)


# @Pyro4.expose
# class Sendorders(object):
# 	def orderreturn(self):
# 		return ordernumbers

# Pyro4.Daemon.serveSimple({
#     Sendorders: 'ORDERS',
# }, host="192.168.1.3", port=9092, ns=False, verbose=True)
