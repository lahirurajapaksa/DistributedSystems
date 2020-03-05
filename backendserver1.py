import Pyro4
def storemenus():
	#store the food menus
	foodDict={}
	#define menu for Chinese Dragon
	chinesedragonmenu =['1. Hot Butter Cuttlefish','2. Sweet and Sour Fish','3. Garlic Prawns','4. Cajun Chicken', '5. Roasted Duck']
	foodDict['ChineseDragon'] = chinesedragonmenu
	#define menu for Mc Donalds
	MCmenu = ['1. Cheesburger','2. Filet -o- fish','3. Mc Spicy','4 Traditional Burger','5. Mc Special']
	foodDict['MC']=MCmenu
	#define menu for Pizza Hut
	pizzamenu = ['1. Margerita','2. Chicken Supreme','3. Chicken Hawaiian','4. Pepperoni','5. Jalopeno and Pork']
	foodDict['PizzaHut'] = pizzamenu
	#define menu for exotic dishes
	exoticmenu = ['1. Chicken Feet','2. Snail', '3. Bear Droppings', '4. Dog Ice Cream', '5. Shark Uterus']
	foodDict['ExoticDishes'] = exoticmenu

	return foodDict

foodDict = storemenus()

@Pyro4.expose
class FoodMenu(object):
	def foodmenureturn(self):
		#send the food dict to the front end server
		return foodDict

daemon = Pyro4.Daemon()        # make a Pyro daemon
uri = daemon.register(FoodMenu)   # register the Hello as a Pyro object

print("Server Ready: Object uri =", uri)      # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls



