import Pyro4

#acts as a bridge between the client and the backend severs
ipaddress = "127.0.0.1"

FoodMenu = Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + ':9090')


#retrieve the menus from the backend

FoodDict = FoodMenu.foodmenureturn()

print(FoodDict)

listoforders1 ="hey !!!!!!!!"


@Pyro4.expose
class FoodMenufrontend(object):

	def foodmenureturn(self):
		#send the food dict to the front end server
		return FoodDict

	# def returnuserdict(self,userdict):
	# 	#send the restaurant name

	# 	ThisDict = userdict
	# 	return userdict

	# print(ThisDict)

	def returnorderstring(self,listoforders):
		#send the list of orders from the client to the frontend
		global listoforders1
		listoforders1 = listoforders
		return listoforders
	print(listoforders1)

Pyro4.Daemon.serveSimple({
    FoodMenufrontend: 'FOOD2',
}, host="127.0.0.1", port=9091, ns=False, verbose=True)



