from DBHelper import DBHelper
from helper_functions import *

class payment_method:
    def __init__(self):
        self.db = DBHelper()

    def create(self, payment_method, description):
        # Adds the new customer record to customers object (dictionary). 
        # Returns dictionary {"Is Error": ___, "Error Message": _____} 
        # Check customer code in products object

        data, columns = self.db.fetch ("SELECT * FROM payment_method WHERE payment_method = '{}' ".format(payment_method))
        if len(data) > 0:
            return {'Is Error': True, 'Error Message': "payment_method '{}' already exists. Cannot Create. ".format(payment_method)}
        else:
            self.db.execute ("INSERT INTO payment_method (payment_method,description) VALUES ('{}' ,'{}')".format(payment_method,description))
        return {'Is Error': False, 'Error Message': ""}

    def read(self, payment_method):
        # Finds the customer code in customers object and returns 1 record in dictionary form. 
        # To return error message + data a tuple returned:  of ({"Is Error": ___, "Error Message": _____}, {<customer data>}) 
        #  where the first one is error message related, and second one is the data.

        data, columns = self.db.fetch ("SELECT payment_method,description FROM payment_method WHERE payment_method = '{}' ".format(payment_method))
        if len(data) > 0:
            retpayment_method = row_as_dict(data, columns)
        else:
            return ({'Is Error': True, 'Error Message': "payment_method '{}' not found. Cannot Read.".format(payment_method)},{})

        return ({'Is Error': False, 'Error Message': ""},retpayment_method)

    def update(self, payment_method, newdescription):
        # Finds the customer code in customers object and then changes the values to the new ones. 
        # Returns dictionary {"Is Error": ___, "Error Message": _____}.

        data, columns = self.db.fetch ("SELECT * FROM payment_method WHERE payment_method = '{}' ".format(payment_method))
        if len(data) > 0:
            self.db.execute ("UPDATE payment_method SET description='{}' WHERE payment_method='{}' ".format(newdescription,payment_method))
        else:
            return {'Is Error': True, 'Error Message': "payment_method '{}' not found. Cannot Update.".format(payment_method)}

        return {'Is Error': False, 'Error Message': ""}

    def delete(self, payment_method):
        # Finds the customer code in customers object and removes it from the dictionary.
        # Returns dictionary {"Is Error": ___, "Error Message": _____}. 

        data, columns = self.db.fetch ("SELECT * FROM payment_method WHERE payment_method = '{}' ".format(payment_method))
        if len(data) > 0:
            self.db.execute ("DELETE FROM payment_method WHERE payment_method='{}' ".format(payment_method))
        else:
            return {'Is Error': True, 'Error Message': "payment_method '{}' not found. Cannot Delete".format(payment_method)}
        return {'Is Error': False, 'Error Message': ""}

    def dump(self):
        # Will dump all customers data and return 1 dictionary as output.

        data, columns = self.db.fetch ('SELECT payment_method as "Payment Method",description as "Description" FROM payment_method ')
        return row_as_dict(data, columns)