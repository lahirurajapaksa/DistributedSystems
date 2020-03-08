import Pyro4

#acts as a bridge between the client and the backend severs
ipaddress = "127.0.0.1"

FoodMenu = Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + ':9090')


#retrieve the menus from the backend

FoodDict = FoodMenu.foodmenureturn()

print(FoodDict)



@Pyro4.expose
class FoodMenufrontend(object):
	def foodmenureturn(self):
		#send the food dict to the front end server
		return FoodDict

	def returnorderstring(self,listoforders):
		#send the list of orders from the client to the frontend
		print(listoforders)



Pyro4.Daemon.serveSimple({
    FoodMenufrontend: 'FOOD2',
}, host="127.0.0.1", port=9091, ns=False, verbose=True)



