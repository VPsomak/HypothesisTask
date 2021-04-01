import csv, random
from datetime import datetime, timedelta

class Entity:
    """
    An Entity holding currency.

    Attributes
    ----------
    allowedToPay : list
        a list of Entity types that are allowed to make payments.
    name : str
        the name of the entity.
    type : str
        the type of this entity which is either person or company.
    balance : float
        the amount of money this entity holds. 

    Methods
    -------
    pay(receiver,amount)
        sends the specified amount of currency to the receiver, updating both balances.
        
    getBalance()
        retrieves the current balance of this entity.
    
    print()
        prints the details for this entity.
    
    printBalance()
        prints the balance for this entity.
    
    parseEntities()
        parses the entities to be used from an entities or transactions csv file.
    """
    allowedToPay = ['person',None]
    
    def __init__(self, name, type, balance):
        """
        Initialises the entity object.

        Parameters
        ----------
        name : str
            The name of the entity.
        type : str
            The type of this entity which is either person or company.
        balance : float
            The amount of money this entity holds. 
        """
        self.balance = balance
        self.name = name
        self.type = type
    
    def pay(self, receiver, amount):
        """
        Sends the specified amount of currency to the receiver, updating both balances.

        Parameters
        ----------
        receiver : Entity
            The entity that will receive the currency.
        amount : float
            The amount of currency that will be sent to the receiving entity. 
        
        Returns
        ----------
        float
            The amount that was transfered.
            
        Raises
        ------
        Exception
            If the type of the entity is not allowed to make payments or the receiver is None.
        """
        if self.type in self.allowedToPay:
            try:
                uncommitedBalance = self.balance
                uncommitedBalance -= amount
                receiver.balance += amount
                self.balance = uncommitedBalance
                return amount
            except:
                raise
        else:
            raise Exception('Transaction not allowed. Trying to sent currency from a '+self.type+' entity.')
    
    def getBalance(self):
        """
        Retrieves the current balance of this entity.
        
        Returns
        ----------
        float
            The current balance of currency for this entity.
        """
        return self.balance
    
    def print(self):
        """
        Prints the details for this entity.
        """
        print('Entity of type '+str(self.type)+ ' and name '+str(self.name)+' has a balance of '+str(self.balance)+'.')
        
    def printBalance(self):
        """
        Prints the balance for this entity.
        """
        print(self.name.capitalize()+' has a balance of '+str(self.balance)+'.')

    def parseEntities(entitiesFile='entities.csv', transactionsFile=None):
        """
        Parses the entities to be used from an entities or transactions csv file.

        Parameters
        ----------
        entitiesFile : str
            The filename of the csv to be parsed.
        transactionsFile : str
            The transactions filename to be parsed if an entities file is not available.
        
        Returns
        ----------
        list
            A list of the Entities parsed as ledgerParser.Entity objects.
            
        Raises
        ------
        IOError
            If a file specified could not be found or opened.
        """
        entities = []
        if entitiesFile is not None:
            try:
                with open(entitiesFile) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for rowIndex,row in enumerate(csv_reader):
                        if rowIndex == 0:
                            headers = row
                        else:
                            entities.append(Entity(row[headers.index('name')],row[headers.index('type')],float(row[headers.index('startingBalance')])))
            except:
                raise
        elif transactionsFile is not None:
            try:
                with open(transactionsFile) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for rowIndex,row in enumerate(csv_reader):
                        if rowIndex == 0:
                            headers = row
                        else:
                            entities.append(Entity(row[headers.index('sender')],None,0.0))
                            entities.append(Entity(row[headers.index('receiver')],None,0.0))
            except:
                raise
        return entities
    
def generateTransactions(entitiesFile='entities.csv', outfile='transactions.csv',number=50,startdate='2015-01-16'):
    """
    Generates randomized transactions using a list of Entities.

    Parameters
    ----------
    outfile : str
        The filename of the csv to be generated.
    number : int
        The number of transactions to be generated.
    startdate : str
        The date of the first transaction.
    
    Raises
    ----------
        IOError
            If a file specified could not be found or opened.
    """
    entities = Entity.parseEntities(entitiesFile)
    date = datetime.strptime(startdate, '%Y-%m-%d')
    try:
        with open(outfile,'w') as csv_out_file:
            csv_writer = csv.writer(csv_out_file, delimiter=',')
            csv_writer.writerow(['date','sender','receiver','amount'])
            n=0
            while n < number:
                if random.random() < 0.90:
                    sender,receiver = random.sample(entities,2)
                    if sender.type not in Entity.allowedToPay: # fix illegal sender choices.
                        maxTries = 1000
                        tries = 0
                        while tries < maxTries and (sender.type not in Entity.allowedToPay and receiver.type not in Entity.allowedToPay):
                            sender,receiver = random.sample(entities,2)
                            tries += 1
                        if sender.type not in Entity.allowedToPay and receiver.type in Entity.allowedToPay:
                            sender, receiver = receiver, sender
                    csv_writer.writerow([date.strftime("%Y-%m-%d"),sender.name,receiver.name,"{:.2f}".format(random.random()*500)])
                    if random.random() < 0.10:
                        date += timedelta(days=1)
                    n+=1
                else:
                    date += timedelta(days=1)
    except:
        raise