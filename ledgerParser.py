import csv
from dataStructures import generateTransactions, Entity
from datetime import datetime

class Ledger:
    """
    A class representation of the ledger.

    Attributes
    ----------
    entities : list
        a list of Entity types that are allowed to make payments.
    ledgerFile : str
        the name of the entity.

    Methods
    ----------
    getEntityByName(name)
        retrieves an entity from the entities list of this object by its name.
        
    parseRandomLedger(entitiesFile, ledgerFile, number, startDate)
        creates a new ledger of randomized transactions in csv format and parses it.
    
    parseLedger(ledgerFile)
        parses a ledger of transactions in csv format.
    
    getBalanceAtDate(date,format)
        gets the balance for all entities at the specified date in JSON format.
    
    printBalanceAtDate(date,format)
        prints the balance for all entities at the specified date.
    """
    def __init__(self):
        """
        Initializes the ledger object.
        """
        self.entities = None
        self.ledgerFile = None
        
    def getEntityByName(self,name):
        """
        Retrieves an entity from the entities list of this object by its name.

        Parameters
        ----------
        name : str
            The name to look for in the entities list.
        
        Returns
        ----------
        Entity or None
            The entity located in the entities array or None if no entity was found.
        """
        for entity in self.entities:
            if entity.name.lower() == name.lower():
                return entity
        return None
        
    def parseRandomLedger(self,entitiesFile = 'entities.csv', ledgerFile = 'transactions.csv', number = 5000, startDate='2021-04-01'):
        """
        Creates a new ledger of randomized transactions in csv format and parses it.

        Parameters
        ----------
        entitiesFile : str
            The entities csv filename to parse and create the entities list for the random generation of transactions.
        ledgerFile : str
            The ledger csv filename to be created.
        number : int
            The number of transactions to be generated.
        startdate : str
            The date of the first transaction.
        """
        generateTransactions(entitiesFile, ledgerFile, number, startDate)
        self.ledgerFile = ledgerFile
        self.entities = Entity.parseEntities(entitiesFile)
        
    def parseLedger(self,ledgerFile = 'transactions.csv'):
        """
        Parses a ledger of transactions in csv format.

        Parameters
        ----------
        ledgerFile : str
            The ledger csv filename to be parsed.
        """
        self.ledgerFile = ledgerFile
        self.entities = Entity.parseEntities(None,ledgerFile)
        
    def getBalanceAtDate(self,date,format='%Y-%m-%d'):
        """
        Gets the balance for all entities at the specified date in JSON format.

        Parameters
        ----------
        date : str
            The date to search for in string format.
        format : str
            The format of the date provided, default format is '%Y-%m-%d'. 
        
        Returns
        ----------
        json
            The list of balances for all entities in JSON format.
            
        Raises
        ----------
        Exception
            If the date is not provided or sender, receiver, date and/or amount is not present in the ledger csv.
        ValueError 
            If the format specified does not match the date's format.
        IOError
            If a file specified could not be found or opened.
        """
        if date is None:
            raise Exception('No date was provided.')
        try:
            date = datetime.strptime(date,format)
        except:
            raise
        try:
            with open(self.ledgerFile) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for rowIndex,row in enumerate(csv_reader):
                    if rowIndex == 0:
                        headers = row
                        if 'sender' not in headers or 'receiver' not in headers or 'date' not in headers or 'amount' not in headers :
                            raise Exception('sender, receiver, date and amount must be contained as headers in the ledger CSV.')
                    else:
                        sender = self.getEntityByName(row[headers.index('sender')])
                        receiver = self.getEntityByName(row[headers.index('receiver')])
                        currentDate = datetime.strptime(row[headers.index('date')],'%Y-%m-%d')
                        amount = float(row[headers.index('amount')])
                        if currentDate <= date:
                            sender.pay(receiver,amount)
                        else:
                            return {date.strftime(format):[{'name':entity.name,'balance':entity.balance} for entity in self.entities]}
        except:
            raise
    
    def printBalanceAtDate(self,date,format='%Y-%m-%d'):
        """
        Prints the balance for all entities at the specified date.

        Parameters
        ----------
        date : str
            The date to search for in string format.
        format : str
            The format of the date provided, default format is '%Y-%m-%d'. 
            
        Raises
        ----------
        Exception
            If the date is not provided.
        ValueError 
            If the format specified does not match the date's format.
        IOError
            If a file specified could not be found or opened.
        """
        try:
            balance = self.getBalanceAtDate(date,format)
            print('Balances on '+str(list(balance.keys())[0])+':')
            for entity in balance[list(balance.keys())[0]]:
                print(entity['name'].capitalize()+' has a balance of §'+"{:.2f}".format(entity['balance'])+'.')
        except:
            raise