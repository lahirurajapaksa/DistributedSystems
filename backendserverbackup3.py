import Pyro4

@Pyro4.expose
class FoodMenu(object):
	def foodmenureturn(self):
		#send the food dict to the front end server
		return foodDict

@Pyro4.behavior(instance_mode="single")
class UserOrderfromfrontend(object):
	BIGorderlist = []
	def __init__(self,userdict,OrderList):
		self._userdict = userdict
		self._OrderList = OrderList

	@Pyro4.expose
	def getUserInfoBackend(self):
		print("getting user info")
		print(self._userdict)
		return self._userdict
	@Pyro4.expose
	def setUserInfoBackend(self,value):
		print("setting user info")
		self._userdict = value
		print('received', value)

	@Pyro4.expose
	def setOrderList(self,value):
		print("Setting the list of orders")

		self._OrderList = value
		print("Order List is ",self._OrderList)

	@Pyro4.expose
	def getOrderList(self):

		print("Getting list of orders")
		print(self._OrderList)
		return self._OrderList

	#will be appending a dictionary to the list of dictionaries
	@Pyro4.expose
	def appendtoOrderList(self,dictionary):
		print("APPEND to order list")

		# self.BIGorderlist.append(dictionary)
		# print('list is ',self.BIGorderlist)

		#create instance of the class
		ipaddress = "127.0.0.1"
		portnumberforprimary = ":9093"
		with Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforprimary) as p:
			try:
				p._pyroBind()
			except Pyro4.errors.CommunicationError:
				print("connection error to OG class")

		OGclass = p
		#get the list
		ReturnedOrderlist = OGclass.getOrderList()
		#append the new dictionary to it
		ReturnedOrderlist.append(dictionary)
		print('list is ',ReturnedOrderlist)
		#Set the updated list
		OGclass.setOrderList(ReturnedOrderlist)
		




	@Pyro4.expose
	def sendDataToBackups(self):
	#this function will access all the data stored in the class by using a proxy of the same class
	#we point to the class with the proxy in order to access the variables
	#this function will connect to the other two backup servers and send the data there
		ipaddress = "127.0.0.1"
		portnumberforprimary = ":9093"
		print("ACCESSED SEND DATA TO BACKUPS")
		with Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforprimary) as p:
			try:
				p._pyroBind()
			except Pyro4.errors.CommunicationError:
				print("connection error to backup class")

		print("BACKING UP THE FOLLOWING DATA")
		Backups = p
		# print("BEfore Dictionary line")
		# Dictionary = Backups.getUserInfoBackend()
		
		#Get the list of orders
		BigList = Backups.getOrderList()

		print('LIST TO BACKUP IS ',BigList)

		print('END OF BACKUP')
		#if u connect send it across to the backups
		
		backupserver1exists = False
		backupserver2exists = False
		#create the objects for backups with try and except
		ipaddress = "127.0.0.1"
		portnumberforbackup1 = ":9092"
		with Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforbackup1) as p:
			try:
				p._pyroBind()
				print('connected to backup server 1')
				backupserver1exists = True
			except Pyro4.errors.CommunicationError:
				print("connection error to backup server 1")

		Backupserver1 = p
		print("Backupserver1",Backupserver1)

		ipaddress = "127.0.0.1"
		portnumberforbackup2 = ":9090"
		with Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforbackup2) as p:
			try:
				p._pyroBind()
				print('connected to backup server 2')
				backupserver2exists = True
			except Pyro4.errors.CommunicationError:
				print("connection error to backup server 2")

		Backupserver2 = p
		print("Backupserver2", Backupserver2)
		#store BigList in the backups by setting that as the OrderList in their respective classes
		print('BIG LIST IS')
		print(BigList)


		if backupserver1exists==True:
			Backupserver1.setOrderList(BigList)
			print("Successfully backed up backup server 1")
		if backupserver2exists==True:
			Backupserver2.setOrderList(BigList)
			print("Successfully backed up backup server 2")




def storemenus():
	#store the food menus
	foodDict={}
	#define menu for Chinese Dragon
	chinesedragonmenu =['1. Hot Butter Cuttlefish','2. Sweet and Sour Fish','3. Garlic Prawns','4. Cajun Chicken', '5. Roasted Duck']
	foodDict['Chinese Dragon'] = chinesedragonmenu
	#define menu for Mc Donalds
	MCmenu = ['1. Cheesburger','2. Filet -o- fish','3. Mc Spicy','4. Traditional Burger','5. Mc Special']
	foodDict['Mc Donalds']=MCmenu
	#define menu for Pizza Hut
	pizzamenu = ['1. Margerita','2. Chicken Supreme','3. Chicken Hawaiian','4. Pepperoni','5. Jalopeno and Pork']
	foodDict['Pizza Hut'] = pizzamenu
	#define menu for exotic dishes
	exoticmenu = ['1. Chicken Feet','2. Snail', '3. Bear Droppings', '4. Dog Ice Cream', '5. Shark Uterus']
	foodDict['Exotic Dishes'] = exoticmenu

	return foodDict

foodDict = storemenus()

menuObject = FoodMenu()

UserOrdersFrontEnd = UserOrderfromfrontend({},[])
def connecttofrontend():

	Pyro4.Daemon.serveSimple({
	    menuObject: 'FOOD',
	    UserOrdersFrontEnd : 'UserOrdersBackend'

	}, host="127.0.0.1", port=9093, ns=False, verbose=True)


connecttofrontend()