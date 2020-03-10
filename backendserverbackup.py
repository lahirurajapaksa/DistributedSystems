import Pyro4

@Pyro4.expose
class FoodMenu(object):
	def foodmenureturn(self):
		#send the food dict to the front end server
		return foodDict

@Pyro4.behavior(instance_mode="single")
class UserOrderfromfrontend(object):
	def __init__(self,userdict):
		self._userdict = userdict

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
	def sendDataToBackups(self):
	#this function will access all the data stored in the class by using a proxy of the same class
	#we point to the class with the proxy in order to access the variables
	#this function will connect to the other two backup servers and send the data there
		ipaddress = "127.0.0.1"
		portnumberforprimary = ":9090"
		print("ACCESSED SEND DATA TO BACKUPS")
		with Pyro4.core.Proxy('PYRO:UserOrdersBackend@'+ ipaddress + portnumberforprimary) as p:
			try:
				p._pyroBind()
			except Pyro4.errors.CommunicationError:
				print("connection error to backup class")

		print("BACKING UP THE FOLLOWING DATA")
		Backups = p
		print("BEfore Dictionary line")
		Dictionary = Backups.getUserInfoBackend()
		print('END OF BACKUP')
		#if u connect send it across

		#print(Dictionary)

		#connect to the remaining available servers and send over the information there

		# print("userdict is ", self._userinfo)

#the class that will store all the variables
# @Pyro4.behavior(instance_mode="single")
# class Backup(object):
# 	def __init__(self,userdict,):
# 		self.use
#class backup - point to this with the proxy
#class that has all variables that we need to store
#replicate function to send all the variables to the other two

#variable._self = pyroproxy ipaddress :9090

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

UserOrdersFrontEnd = UserOrderfromfrontend({})
def connecttofrontend():

	Pyro4.Daemon.serveSimple({
	    menuObject: 'FOOD',
	    UserOrdersFrontEnd : 'UserOrdersBackend'

	}, host="127.0.0.1", port=9090, ns=False, verbose=True)


connecttofrontend()