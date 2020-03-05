import Pyro4

#acts as a bridge between the client and the backend severs
def connecttobackendserver():
	ipaddress = "192.168.1.3"

	FoodMenu = Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + ':9090')

	return FoodMenu

#retrieve the menus from the backend
def getfoodmenusbackend(FoodMenu):

	FoodDict = FoodMenu.foodmenureturn()

	print(FoodDict)
	return FoodDict

classreturn = connecttobackendserver()

FoodDict = getfoodmenusbackend(classreturn)

def connecttoclient():

	@Pyro4.expose
	class FoodMenufrontend(object):
		def foodmenureturn(self):
			#send the food dict to the front end server
			return FoodDict


	Pyro4.Daemon.serveSimple({
	    FoodMenufrontend: 'FOOD',
	}, host="192.168.1.3", port=9091, ns=False, verbose=True)

connecttoclient()