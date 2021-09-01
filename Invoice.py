from DBHelper import DBHelper
from helper_functions import *
from Product import *
from Customer import *

class Invoice:
    def __init__(self):
        self.db = DBHelper()
    
    def __updateInvoiceTotal (self, invoiceNo):
        sql = ("UPDATE invoice SET "
              "  total = line_item.new_total "
              " , vat = line_item.new_total*7 /100 "
              " , amount_due = line_item.new_total + (line_item.new_total * 7 / 100) "
              " FROM (SELECT invoice_no, SUM(quantity * unit_price) as new_total FROM invoice_line_item GROUP BY invoice_no) line_item "
              " WHERE invoice.invoice_no = line_item.invoice_no "
              " AND invoice.invoice_no = '{}' ".format(invoiceNo))
        self.db.execute (sql)

    def __updateLineItem (self, invoiceNo, invoiceLineTuplesList):
        self.db.execute ("DELETE FROM invoice_line_item WHERE invoice_no = '{}' ".format(invoiceNo))
        for lineItem in invoiceLineTuplesList:
            self.db.execute ("INSERT INTO invoice_line_item (invoice_no, item_no, product_code, quantity, unit_price, product_total) VALUES ('{}',{},'{}','{}','{}',{}*{})".format(invoiceNo,lineItem["Item No"],lineItem["Product Code"],lineItem["Quantity"],lineItem["Unit Price"],lineItem["Quantity"],lineItem["Unit Price"]))
        self.__updateInvoiceTotal(invoiceNo)

    def create(self, invoiceNo, invoiceDate, customerCode, dueDate, invoiceLineTuplesList):
        # Adds the new invoice record to invoices object (dictionary).
        # Note that the function will calculate Total, VAT, and Amount Due
        #  from the data in the invoiceLineDictList parameter.  
        # The invoiceLineDictList data will be a list of dictionary,
        #  where each dictionary item of the list is in this example
        #  format: {'Product Code': 'HD01',  'Quantity': 2,  'Unit Price': 3000.00}.  
        # Note that for each line item the Price Total will be calculated by the function using Quantity * Unit Price. 
        # Returns dictionary {‘Is Error’: ___, ‘Error Message’: _____}.

        data, columns = self.db.fetch ("SELECT * FROM invoice WHERE invoice_no = '{}' ".format(invoiceNo))
        if len(data) > 0:
            return {'Is Error': True, 'Error Message': "Invoice No '{}' already exists. Cannot Create. ".format(invoiceNo)}
        else:
            self.db.execute ("INSERT INTO invoice (invoice_no, date, customer_code, due_date) VALUES ('{}' ,{},'{}',{})".format(invoiceNo,invoiceDate,customerCode,dueDate))
            self.__updateLineItem(invoiceNo, invoiceLineTuplesList)

        return {'Is Error': False, 'Error Message': ""}

    def read(self, invoiceNo):
        # Finds the invoice number in invoices object and returns 1invoice  record in dictionary form. 
        # Returns tuple dictionary, one for error, one for the data.
          
        data, columns = self.db.fetch ("SELECT invoice_no, date, customer_code, due_date, total, vat, amount_due FROM invoice WHERE invoice_no = '{}' ".format(invoiceNo))
        if len(data) > 0:
            retInvoice = row_as_dict(data, columns)
        else:
            return ({'Is Error': True, 'Error Message': "Invoice No '{}' not found. Cannot Read.".format(invoiceNo)},{})

        return ({'Is Error': False, 'Error Message': ""},retInvoice)

    def update(self, invoiceNo, newInvoiceDate, newCustomerCode, newDueDate, newInvoiceLineTuplesList):
        # Finds the invoice number in invoices object and then changes the values to the new ones. 
        # Returns dictionary {‘Is Error’: ___, ‘Error Message’: _____}.
        data, columns = self.db.fetch ("SELECT * FROM invoice WHERE invoice_no = '{}' ".format(invoiceNo))
        if len(data) > 0:
            self.db.execute ("UPDATE invoice SET date = {}, customer_code = '{}', due_date={} WHERE invoice_no = '{}' ".format(newInvoiceDate,newCustomerCode,newDueDate,invoiceNo))
            self.__updateLineItem(invoiceNo, newInvoiceLineTuplesList)
        else:
            return {'Is Error': True, 'Error Message': "Invoice No '{}' not found. Cannot Update.".format(invoiceNo)}

        return {'Is Error': False, 'Error Message': ""}

    def delete(self, invoiceNo):
        # Finds the invoice number invoices object and removes it from the dictionary. 
        # Returns dictionary {‘Is Error’: ___, ‘Error Message’: _____}.
        data, columns = self.db.fetch ("SELECT * FROM invoice WHERE invoice_no = '{}' ".format(invoiceNo))
        if len(data) > 0:
            self.db.execute ("DELETE FROM invoice WHERE invoice_no = '{}' ".format(invoiceNo))
            self.db.execute ("DELETE FROM invoice_line_item WHERE invoice_no = '{}' ".format(invoiceNo))
        else:
            return {'Is Error': True, 'Error Message': "Invoice No '{}' not found. Cannot Delete".format(invoiceNo)}
        return {'Is Error': False, 'Error Message': ""}

    def dump(self):
        # Will dump all invoice data by returning 1 dictionary as output.
        
        data, columns = self.db.fetch ('SELECT i.invoice_no as "Invoice No", i.date as "Date" '
                              ' , i.customer_code as "Customer Code", c.name as "Customer Name" '
                              ' , i.due_date as "Due Date", i.total as "Total", i.vat as "VAT", i.amount_due as "Amount Due" '
                              ' , ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , ili.quantity as "Quantity", ili.unit_price as "Unit Price", ili.product_total as "Extended Price" '
                              ' FROM invoice i JOIN customer c ON i.customer_code = c.customer_code '
                              '  JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '  JOIN product p ON ili.product_code = p.code '
                              ' ')
        return row_as_dict(data, columns)

    def update_invoice_line(self, invoiceNo, itenNo, productCode, newQuantity, newUnitPrice):
        # The line item of this invoice number is updated for this product code.  
        # Note that the Product Total must also be recalculated, 
        #  after which all the related data in the invoice must be updated such as Total, VAT, and Amount Due. 
        # Returns dictionary {‘Is Error’: ___, ‘Error Message’: _____}. 
        data, columns = self.db.fetch ("SELECT * FROM invoice_line_item WHERE invoice_no = '{}' AND item_no = '{}' ".format(invoiceNo, itenNo))
        if len(data) > 0:
            self.db.execute ("UPDATE invoice_line_item SET quantity = {}, unit_price = '{}', product_total={}*{} WHERE invoice_no = '{}' AND product_code = '{}' ".format(newQuantity, newUnitPrice,newQuantity, newUnitPrice, invoiceNo, itenNo))
            self.__updateInvoiceTotal(invoiceNo)
        else:
            return {'Is Error': True, 'Error Message': "Item No '{}' not found in Invoice No '{}'. Cannot Update.".format(itenNo, invoiceNo)}

        return {'Is Error': False, 'Error Message': ""}

    def delete_invoice_line(self, invoiceNo, itemNo):
        # The line item of this invoice number is updated to delete this Item No.  
        # Note that all the related data in the invoice must be updated such as Total, VAT, and Amount Due. 
        # Returns dictionary {‘Is Error’: ___, ‘Error Message’: _____}
        data, columns = self.db.fetch ("SELECT * FROM invoice_line_item WHERE invoice_no = '{}' AND item_no = '{}' ".format(invoiceNo, itemNo))
        if len(data) > 0:
            self.db.execute ("DELETE FROM invoice_line_item WHERE invoice_no = '{}' AND item_no = '{}' ".format(invoiceNo, itemNo))
            self.__updateInvoiceTotal(invoiceNo)

        else:
            return {'Is Error': True, 'Error Message': "Item No '{}' not found in Invoice No '{}'. Cannot Delete.".format(itemNo, invoiceNo)}

        return {'Is Error': False, 'Error Message': ""}

