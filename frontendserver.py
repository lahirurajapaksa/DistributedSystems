import Pyro4

#acts as a bridge between the client and the backend severs

#retrieve the menus from the backend
def getfoodmenusbackend():
	uri = input("what is the uri?").strip()
	FoodMenu = Pyro4.Proxy(uri)      # get a Pyro proxy to the FoodMenu object

	print("response is ",FoodMenu.foodmenureturn())
	#store the returned dictionary in FoodDict
	FoodDict = FoodMenu.foodmenureturn()

	return FoodDict

FoodDict = getfoodmenusbackend()

