#This program makes the assumption (google suggested so) that the name of the user that is typing is stored under the variable "turn_context.activity.name"
#In the bot builder, this variable also returns "none" when converted to a string because there is no user in the bot emulator
#When deployed to teams, if this variable turns out to not to store the name of the user typing, then every reference to the variable in the WelcomeUserBot::on_message_activity function needs to be changed

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    UserState,
)
from botbuilder.schema import (
    ChannelAccount,
)

import mysql.connector

from data_models import WelcomeUserState

class DataList:

    def __init__(self):
        self.users = []
    
    def _append(self, type, name, nominations = 0):
        if(type == "User"):
            temp = User(name, nominations)
            if not self.users:
                self.users.append(temp)
            
            else:
                for i in self.users:
                    if(i._name == name):
                        return False
                
                self.users.append(temp)
                return True
        if(type == "Nominator"):
            temp = Nominator(name, nominations)
            if not self.users:
                self.users.append(temp)
            
            else:
                for i in self.users:
                    if(i._name == name):
                        return False
                
                self.users.append(temp)
                return True

    def _find(self, name):
        for i in self.users:
            if(i._name == name):
                return i
            
        return -1    

    def _remove(self, name):
        x = self._find(name)
        if(x == -1):
            return False
        else:
            self.users.remove(x)
            return True
        
    def _list(self):
        nameslist = []
        for i in self.users:
            nameslist.append(i._name)
        return nameslist
    
    def _isEmpty(self):
        if not self.users:
            return True
        else:
            return False
        
    def _empty(self):
        self.users = []

UserList = DataList()

NominatorsList = DataList()
        
class User:

    def __init__(self, name, nominations = 0):

        self._name = name

        self._nominations = nominations

class Nominator:

    def __init__(self, name, nominations = 0):

        self._name = name

        self._timesnominated = nominations

#This class intracts with the database and stores the data in lists within python
class Database:

    def __init__(self):
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="password",
            database="tableplustest"
        )

        self.cursor = self.db.cursor()

    def _checkNominator(self, userName):
        if(NominatorsList._find(userName) == -1):
            return False
        else:
            return True

    def _buildDatabase(self):
        self._buildUsers()
        self._buildNominators()

    def _buildUsers(self):
        self.cursor.execute("SELECT name, nominations FROM users")
        result = self.cursor.fetchall()
        for name, nominations in result:
            UserList._append("User", str(name), int(nominations))

    def _buildNominators(self):
        self.cursor.execute("SELECT name, times_nominated FROM nominators")
        result = self.cursor.fetchall()
        for name, times_nominated in result:
            NominatorsList._append("Nominator", str(name), int(times_nominated))

    def _getCurrent(self):
        UserList._empty()
        NominatorsList._empty()
        self._buildDatabase()

    def _addUser(self, name, nominations = 0):
        try:
            sql = "INSERT INTO users (name, nominations) VALUES (%s, %s)"
            val = (name, nominations)
            self.cursor.execute(sql, val)
            self.db.commit()
            return True
        except:
            return False
        
    def _addNominator(self, userName, nominations = 0):
        try:
            sql = "INSERT INTO nominators (name, times_nominated) VALUES (%s, %s)"
            val = (userName, nominations)
            self.cursor.execute(sql, val)
            self.db.commit()
            return True
        except:
            return False
        
    def _getNominations(self, name):
        temp = UserList._find(name)
        if(temp == -1):
            return -1
        else:
            return temp._nominations
        
    def _getTimesNominated(self, name):
        temp = NominatorsList._find(name)
        if(temp == -1):
            return -1
        else:
            return temp._timesnominated
        
    def _updateUsers(self, name, noms):
        sql = "UPDATE users SET nominations = {} WHERE name = '{}'".format(noms, str(name))
        self.cursor.execute(sql)
        self.db.commit()
        
    def _updateNominators(self, name, times_nominated):
        sql = "UPDATE nominators SET times_nominated = {} WHERE name = '{}'".format(times_nominated, str(name))
        self.cursor.execute(sql)
        self.db.commit()

    def _incrementNominations(self, name, userName):
        noms = self._getNominations(name)
        times_nominated = self._getTimesNominated(userName)
        if(noms == -1):
            return False
        else:
            noms+=1
            times_nominated+=1
            self._updateUsers(name, noms)
            self._updateNominators(userName, times_nominated)
            return True

    def _removeUser(self, name):
        sql = "DELETE FROM users WHERE name = '{}'".format(name)
        self.cursor.execute(sql)
        self.db.commit()

database = Database()

class WelcomeUserBot(ActivityHandler):
    def __init__(self, user_state: UserState):
        if user_state is None:
            raise TypeError(
                "[WelcomeUserBot]: Missing parameter. user_state is required but None was given"
            )

        self._user_state = user_state

        self._nominationProcess = False

        self._checkNominations = False

        self._add = False

        self._remove = False

        self._loadData = False

        self.user_state_accessor = self._user_state.create_property("WelcomeUserState")
        
        self.OPTIONS_MESSAGE = """These are the following options: List (lists users) \n Add (adds a user) \n Remove (removes a user) \n nominate (nominates a user) \n listnominations (lists the nomination count for a user) \n"""

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # save changes to WelcomeUserState after each turn
        await self._user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Hi there { member.name }. "
                )
                
                await turn_context.send_activity(self.OPTIONS_MESSAGE)

    # This function is called each time it is the bot's "turn"
    async def on_message_activity(self, turn_context: TurnContext):
        if(self._loadData == False):
            self._loadData = True
            database._buildDatabase()

        database._getCurrent()

        if(database._checkNominator(str(turn_context.activity.name)) == False):
            database._addNominator(str(turn_context.activity.name))

        text = turn_context.activity.text.lower()
        if(self._add == True): 
            name = turn_context.activity.text
            truth = UserList._append("User", name)
            if(truth == False):
                await turn_context.activity.text("That name is already in the list!")
            else:
                database._addUser(name)
                await turn_context.send_activity("You have added " + name + " to the list")
            self._add = False

        elif(self._remove == True): 
            name = turn_context.activity.text
            i = UserList._remove(name)
            if(i == True):
                await turn_context.send_activity("You have removed " + name + " from the list")
                database._removeUser(name)

            elif(i == False):
                await turn_context.send_activity("Failed to remove " + name)

            self._remove = False    

        elif(self._nominationProcess == True):
            name = turn_context.activity.text
            x = UserList._find(name)
            if(x == -1):
                await turn_context.send_activity("Unable to find that person!")
                self._nominationProcess = False
            else:
                await turn_context.send_activity("Nominated " + x._name)
                self._nominated = True
                self._nominationProcess = False
                database._incrementNominations(name, str(turn_context.activity.name))

        elif(self._checkNominations == True):
            name = turn_context.activity.text
            x = UserList._find(name)
            if(x == -1):
                await turn_context.send_activity("This user does not exist!")
                self._checkNominations = False
            else:
                await turn_context.send_activity("This user has " + str(x._nominations) + " nominations")
                self._checkNominations = False

        elif text in ("list"):
            if(UserList._isEmpty() == True):
                await turn_context.send_activity("There are no items in the list!")
            else:
                returnedList = UserList._list()
                for i in returnedList:
                    await turn_context.send_activity(i)

        elif text in ("add"):
            await turn_context.send_activity("Type the name that you want to enter:")
            self._add = True

        elif text in ("nominate"):
            if(UserList._isEmpty()):
                await turn_context.send_activity("The list is empty!")
            else:
                await turn_context.send_activity("Type the name that you want to nominate!")
                self._nominationProcess = True

        elif text in ("remove"):
            if(UserList._isEmpty()):
                await turn_context.send_activity("You cannot remove anyone, the list is empty")
            else:
                await turn_context.send_activity("Type the name you want to remove: ")
                self._remove = True

        elif text in ("listnominations"):
            if(UserList._isEmpty()):
                await turn_context.send_activity("You cannot list any nominations, there are no users!")
            else: 
                await turn_context.send_activity("Type the name you want to see nominations for: ")
                self._checkNominations = True

        else:
            await turn_context.send_activity(self.OPTIONS_MESSAGE)