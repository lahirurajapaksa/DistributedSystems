import Pyro4

@Pyro4.expose
class FoodMenu(object):
	def foodmenureturn(self):
		#send the food dict to the front end server
		return foodDict

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

def connecttofrontend():

	Pyro4.Daemon.serveSimple({
	    menuObject: 'FOOD',
	}, host="127.0.0.1", port=9090, ns=False, verbose=True)


connecttofrontend()