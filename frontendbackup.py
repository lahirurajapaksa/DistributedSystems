import Pyro4
import sys
#acts as a bridge between the client and the backend severs
ipaddress = "127.0.0.1"



#have a nested try and except to try and connect to a server
import Pyro4.errors
portnumberforprimary = ':9090'
with Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + portnumberforprimary) as p:
	try:
		#try to connect to server number one
		p._pyroBind()
		print("RUNNING number 1")
	except Pyro4.errors.CommunicationError:
		#try to connect to server number two
		portnumberforprimary = ':9092'
		with Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + portnumberforprimary) as p:
				try:
					#try to connect to server number one
					p._pyroBind()
					print("RUNNING number 2")
				except Pyro4.errors.CommunicationError:
					#try to connect to server number three
					portnumberforprimary = ':9093'
					with Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + portnumberforprimary) as p:
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


@Pyro4.behavior(instance_mode="single")
class UserOrderDetails(object):
	def __init__(self,userdict,ipaddress,portnumberforprimary):
		self._userdict = userdict
		self._ipaddress = ipaddress
		self._portnumberforprimary = portnumberforprimary

	#	print("ok")

	@Pyro4.expose
	def getUserInfo(self):
		print("hello")
		print(self._userdict)
		return self._userdict
	@Pyro4.expose
	def setUserInfo(self,value):
		self._userdict = value

	@Pyro4.expose
	def sendUserInfotoBackend(self,value):
		self._userdict = value
		print('received')
		print(self._ipaddress)
		print(self._portnumberforprimary)

		#connect to the backend and send over userinfo
		print('START!!!')
		with Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforprimary) as p:
			try:
				#try to connect to server number one
				p._pyroBind()
				print("WE ARE CONNECTED")
			except Pyro4.errors.CommunicationError:
				print('Could not connect to main server')
		print('END!!')

		UserOrderBackend = p

		UserOrderBackend.setUserInfoBackend(value)

		neworder = UserOrderBackend.getUserInfoBackend()




	# #create instance of the order class
	# UserOrderBackend = Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforprimary)


	# UserOrderBackend.setUserInfoBackend(selfuserinfo)

	# neworder = UserOrderBackend.getUserInfoBackend()

#instantiate the userorderdetails class
obj = UserOrderDetails({},"127.0.0.1",portnumberforprimary)
obj1 = FoodMenufrontend()


Pyro4.Daemon.serveSimple({
    obj1: 'FOOD2',
    #UserOrderDetails: 'UserOrders',
    obj: 'UserOrders'
}, host="127.0.0.1", port=9091, ns=False, verbose=True)



