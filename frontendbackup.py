import Pyro4

#acts as a bridge between the client and the backend severs
ipaddress = "127.0.0.1"



#have a nested try and except to try and connect to a server
import Pyro4.errors

with Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + ':9090') as p:
	try:
		#try to connect to server number one
		p._pyroBind()
		print("RUNNING number 1")
	except Pyro4.errors.CommunicationError:
		#try to connect to server number two
		with Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + ':9092') as p:
				try:
					#try to connect to server number one
					p._pyroBind()
					print("RUNNING number 2")
				except Pyro4.errors.CommunicationError:
					with Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + ':9093') as p:
						try:
							#try to connect to server number one
							p._pyroBind()
							print("RUNNING number 3")
						except Pyro4.errors.CommunicationError:
							print("No backend servers are available")
							sys.exit()



# FoodMenu = Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + ':9090')
FoodMenu = p

#retrieve the menus from the backend

FoodDict = FoodMenu.foodmenureturn()

print(FoodDict)




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
	
		return listoforders

@Pyro4.behavior(instance_mode="single")
class UserOrderDetails(object):
	def __init__(self,userdict):
		self._userdict = userdict
	#	print("ok")

	@Pyro4.expose
	def getUserInfo(self):
		print("hello")
		print(self._userdict)
		return self._userdict
	@Pyro4.expose
	def setUserInfo(self,value):
		self._userdict = value


#instantiate the userorderdetails class
obj = UserOrderDetails({})
obj1 = FoodMenufrontend()


Pyro4.Daemon.serveSimple({
    obj1: 'FOOD2',
    #UserOrderDetails: 'UserOrders',
    obj: 'UserOrders'
}, host="127.0.0.1", port=9091, ns=False, verbose=True)



