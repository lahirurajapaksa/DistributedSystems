import Pyro4
import sys
import Pyro4.errors
import requests
#acts as a bridge between the client and the backend severs
ipaddress = "127.0.0.1"


portnumberforprimary = ':9090'

#have a nested try and except to try and connect to a server
def connecttoprimary():
	global portnumberforprimary
	with Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforprimary) as p:
		try:
			#try to connect to server number one
			#call function in the main server that sends data to the other two
			
			p._pyroBind()

			#print("RUNNING number 1")
			return p
			
		except Pyro4.errors.CommunicationError:
			#try to connect to server number two
			portnumberforprimary = ':9092'
			with Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforprimary) as p:
					try:
						#try to connect to server number one
						p._pyroBind()
						#print("RUNNING number 2")
						return p
					except Pyro4.errors.CommunicationError:
						#try to connect to server number three
						portnumberforprimary = ':9093'
						with Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforprimary) as p:
							try:
								#try to connect to server number one
								p._pyroBind()
								#print("RUNNING number 3")
								return p
							except Pyro4.errors.CommunicationError:
								print("No backend servers are available")
								sys.exit()

UserOrderBackend =connecttoprimary()

#connect to the food class
with Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + portnumberforprimary) as p2:
	try:
		p2._pyroBind()
		#print("Created food object")

	except Pyro4.errors.CommunicationError:
		print("Could not connect to food object")




# FoodMenu = Pyro4.core.Proxy('PYRO:FOOD@'+ ipaddress + ':9090')
FoodMenu = p2

#retrieve the menus from the backend

FoodDict = FoodMenu.foodmenureturn()

#print(FoodDict)




@Pyro4.expose
class FoodMenufrontend(object):



	def foodmenureturn(self):
		#send the food dict to the front end server
		return FoodDict


@Pyro4.behavior(instance_mode="single")
class UserOrderDetails(object):
	def __init__(self,userdict,ipaddress,portnumberforprimary,fulluserorder,usermessage,postcoderesult):
		self._userdict = userdict
		self._ipaddress = ipaddress
		self._portnumberforprimary = portnumberforprimary
		self._fulluserorder = fulluserorder
		self._usermessage = usermessage
		self._postcoderesult = postcoderesult
		

	#	print("ok")

	@Pyro4.expose
	def getUserInfo(self):
		#print("hello")
		print(self._userdict)
		return self._userdict
	@Pyro4.expose
	def setUserInfo(self,value):
		self._userdict = value

	@Pyro4.expose
	def setFullUserOrder(self,value):
		#print("Setting full user order")
		self._fulluserorder = value

	@Pyro4.expose
	def getFullUserOrder(self):
		#print("Getting full user order")
		return self._fulluserorder

	@Pyro4.expose
	def SetUserMessage(self,value):
		#print("Setting user message")
		self._usermessage = value

	@Pyro4.expose
	def GetUserMessage(self):
		#print("Getting user message")
		return self._usermessage

	@Pyro4.expose
	def setpostcoderesult(self,value):
		#print("Setting the postcode result")
		self._postcoderesult = value

	@Pyro4.expose
	def Getpostcoderesult(self):
		#print("Getting the postcode result")
		return self._postcoderesult

	@Pyro4.expose
	def validatepostcode(self,value):
		#create instance of the class here
		ipaddress = "127.0.0.1"
		portnumberforprimary = ":9091"
		with Pyro4.core.Proxy('PYRO:UserOrders@'+ ipaddress + portnumberforprimary) as p:
			try:
				p._pyroBind()
			except Pyro4.errors.CommunicationError:
				print("connection error to Frontend class")

		Frontendclass = p


		#the given postcode is the value
		#before sending any of the order data to the backend,
		#we need to validate the postcode
		postcodetoexamine =  str(value)

		#print("this is the postcode",postcodetoexamine)

		try:
			response = requests.get("https://api.postcodes.io/postcodes/"+postcodetoexamine+"/validate")
			jsondata = response.json()
			postcodevalid = str(jsondata['result'])

			#set the postcode result using the set function
			Frontendclass.setpostcoderesult(postcodevalid)

			postcodestatus = response.status_code #can be sth like 200 or 404

		except:
			#print("Postcode API non-functional, user must try again later")
			#set the postcode result as unavailable
			Frontendclass.setpostcoderesult("N/A")






	@Pyro4.expose
	def sendUserInfotoBackend(self,value):
		self._userdict = value
		#print('received')
		#print(self._ipaddress)
		#print(self._portnumberforprimary)

		#create instance of this class on the frontend 
		ipaddress = "127.0.0.1"
		portnumberforprimary = ":9091"
		with Pyro4.core.Proxy('PYRO:UserOrders@'+ ipaddress + portnumberforprimary) as p:
			try:
				p._pyroBind()
			except Pyro4.errors.CommunicationError:
				print("connection error to OG class")

		Frontendclass = p



		UserOrderBackend =connecttoprimary()

		#check if the value is of type string, if so then use different function that sets string variable
		result = isinstance(value, str)

		if result == False:
			#print("Placing Normal Order")





			#we have a dictionary and placing order as normal with dict
			UserOrderBackend.setUserInfoBackend(value)
			
			UserOrderBackend =connecttoprimary()

			#append the overall list of orders with the current order
			UserOrderBackend.appendtoOrderList(value)

			#UserOrderBackend =connecttoprimary()
			UserOrderBackend =connecttoprimary()

			#get the confirmation message to send back
			confirmation = UserOrderBackend.sendendmessage()

			UserOrderBackend =connecttoprimary()


			#set this as a message on the frontend 
			Frontendclass.SetUserMessage(confirmation)

			UserOrderBackend =connecttoprimary()


			#print('Confimation of order placed',confirmation)

		else:
			#we are retrieving an order, using Order ID - string
			#print("Received a User ID ",value)
			#set the order ID
			UserOrderBackend.setUserInfoOrderID(value)

			UserOrderBackend =connecttoprimary()

			#retrieve the OrderID
			result = UserOrderBackend.retrieveOrder()

			UserOrderBackend =connecttoprimary()

	


			#this means that the order ID has been found so we get the order Dict
			if result ==1:
				RetrievedOrder = UserOrderBackend.getorderdictforReturn()
				UserOrderBackend =connecttoprimary()
				#print("we found the order, it is",RetrievedOrder)
				#we set the message as this so the client knows to call getFullUserOrder
				Frontendclass.SetUserMessage("OrderFound")
				Frontendclass.setFullUserOrder(RetrievedOrder)

			else:
				InvalidOrder = UserOrderBackend.sendendmessage()
				UserOrderBackend =connecttoprimary()
				#print("We did not find the order", InvalidOrder)
				Frontendclass.SetUserMessage(InvalidOrder)





		#backup the new list, sending across to the backup servers
		UserOrderBackend.sendDataToBackups()

		UserOrderBackend =connecttoprimary()


		#UserOrderBackend =connecttoprimary()

		#neworder = self._UserOrderBackend.getUserInfoBackend()

#instantiate the userorderdetails class
obj = UserOrderDetails({},"127.0.0.1",portnumberforprimary,{},"","")
obj1 = FoodMenufrontend()


Pyro4.Daemon.serveSimple({
    obj1: 'FOOD2',
    #UserOrderDetails: 'UserOrders',
    obj: 'UserOrders'
}, host="127.0.0.1", port=9091, ns=False, verbose=True)



