from DBHelper import DBHelper
from helper_functions import *
from Product import *
from Customer import *
from Invoice import *

class Receipt:
    def __init__(self):
        self.db = DBHelper()
    
    def __updateReceiptTotal (self, receiptNo):
        sql = ("UPDATE receipt SET "
              "  total_receipt = line_item.new_total "
              " FROM (SELECT receipt_no, SUM(amount_paid_here) as new_total FROM receipt_line_item GROUP BY receipt_no) line_item "
              " WHERE receipt.receipt_no = line_item.receipt_no "
              " AND receipt.receipt_no = '{}' ".format(receiptNo))
        self.db.execute (sql)

    def __updateLineItem (self, receiptNo, receiptLineTuplesList):
        self.db.execute ("DELETE FROM receipt_line_item WHERE receipt_no = '{}' ".format(receiptNo))
        for lineItem in receiptLineTuplesList:
            self.db.execute ("INSERT INTO receipt_line_item (receipt_no, item_no, invoice_no, amount_paid_here) VALUES ('{}',{},'{}','{}')".format(receiptNo, lineItem['Item No'], lineItem['Invoice No'], lineItem['Amount Paid Here']))
        self.__updateReceiptTotal(receiptNo)

    def create(self, receiptNo, receiptDate, customerCode, paymentMethod, paymentReference, totalReceived ,remarks, receiptLineTuplesList):
        # Adds the new invoice record to invoices object (dictionary).
        # Note that the function will calculate Total, VAT, and Amount Due
        #  from the data in the invoiceLineDictList parameter.  
        # The invoiceLineDictList data will be a list of dictionary,
        #  where each dictionary item of the list is in this example
        #  format: {'Product Code': 'HD01',  'Quantity': 2,  'Unit Price': 3000.00}.  
        # Note that for each line item the Extended Price will be calculated by the function using Quantity * Unit Price. 
        # Returns dictionary {‘Is Error’: ___, ‘Error Message’: _____}.

        data, columns = self.db.fetch ("SELECT * FROM receipt WHERE receipt_no = '{}' ".format(receiptNo))
        if len(data) > 0:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' already exists. Cannot Create. ".format(receiptNo)}
        else:
            self.db.execute ("INSERT INTO receipt (receipt_no, date, customer_code, payment_method, payment_reference, total_receipt, remarks) VALUES ('{}' ,'{}','{}','{}','{}','{}','{}')".format(receiptNo, receiptDate, customerCode, paymentMethod, paymentReference, totalReceived ,remarks))
            self.__updateLineItem(receiptNo, receiptLineTuplesList)

        return {'Is Error': False, 'Error Message': ""}




    def read(self, receiptNo):
        # Finds the invoice number in invoices object and returns 1invoice  record in dictionary form. 
        # Returns tuple dictionary, one for error, one for the data.
          
        data, columns = self.db.fetch ("SELECT * FROM receipt WHERE receipt_no = '{}' ".format(receiptNo))
        if len(data) > 0:
            retReceipt = row_as_dict(data, columns)
        else:
            return ({'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Read.".format(receiptNo)},{})

        return ({'Is Error': False, 'Error Message': ""},retReceipt)

    def update(self, receiptNo, newReceiptDate, newCustomerCode, newPaymentMethod, newPaymentReference, newTotalReceived, newRemarks, newReceiptlineTuplelist):
        # Finds the invoice number in invoices object and then changes the values to the new ones. 
        # Returns dictionary {‘Is Error’: ___, ‘Error Message’: _____}.
        data, columns = self.db.fetch ("SELECT * FROM receipt WHERE receipt_no = '{}' ".format(receiptNo))
        if len(data) > 0:
            self.db.execute ("UPDATE receipt SET date = '{}', customer_code = '{}', payment_method='{}',payment_reference = '{}', total_receipt = '{}', remarks = '{}'  WHERE receipt_no = '{}' ".format(newReceiptDate, newCustomerCode, newPaymentMethod, newPaymentReference, newTotalReceived, newRemarks,receiptNo))
            self.__updateLineItem(receiptNo, newReceiptlineTuplelist)
        else:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Update.".format(receiptNo)}

        return {'Is Error': False, 'Error Message': ""}

    def delete(self, receiptNo):
        # Finds the invoice number invoices object and removes it from the dictionary. 
        # Returns dictionary {‘Is Error’: ___, ‘Error Message’: _____}.
        data, columns = self.db.fetch ("SELECT * FROM receipt WHERE receipt_no = '{}' ".format(receiptNo))
        if len(data) > 0:
            self.db.execute ("DELETE FROM receipt WHERE receipt_no = '{}' ".format(receiptNo))
            self.db.execute ("DELETE FROM receipt_line_item WHERE receipt_no = '{}' ".format(receiptNo))
        else:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Delete".format(receiptNo)}
        return {'Is Error': False, 'Error Message': ""}

    def dump(self):
        # Will dump all invoice data by returning 1 dictionary as output.
        
        data, columns = self.db.fetch ('SELECT r.receipt_no as "Receipt No", r.date as "Date", c.name as "Customer Name '
                              ' , r.customer_code as "Customer Code", r.payment_method as "Payment Method" '
                              ' , r.payment_reference as "Payment Reference" ,r.total_receipt as "Total receipt"'
                              ' , r.remarks as "Remarks", rli.receipt_no as "Receipt No",rli.item_no as "Item No" '
                              ' , rli.invoice_no as "Invoice No", i.invoice_date as "Invoice Date", i.amount_due as "Invoice Full Amount" '
                              ' , rli.invoice_amount_remain as "Invoice Amount Remain", rli.amount_paid_here as "Amount piad here" '
                              ' , ili.invoice_no as "Invoice No", rli.invoice_date as "Invoice Date" '
                              '  FROM receipt r JOIN customer c ON r.customer_code = c.customer_code '
                              '  JOIN receipt_line_item rli ON r.receipt_no = rli.receipt_no '
                              '  JOIN invoice i ON rli.invoice_no = i.invoice_no '
                              ' ')
        return row_as_dict(data, columns)

    def update_receipt_line(self, receiptNo,itemNo, newInvocie, newPaidHere):
        # The line item of this invoice number is updated for this product code.  
        # Note that the Product Total must also be recalculated, 
        #  after which all the related data in the invoice must be updated such as Total, VAT, and Amount Due. 
        # Returns dictionary {‘Is Error’: ___, ‘Error Message’: _____}. 
        data, columns = self.db.fetch ("SELECT * FROM receipt_line_item WHERE receipt_no = '{}' AND item_no = '{}' ".format(receiptNo, itemNo))
        if len(data) > 0:
            self.db.execute ("UPDATE receipt_line_item SET invoice_no = '{}', amount_paid_here = '{}' WHERE receipt_no = '{}' AND item_no = '{}' ".format(newInvocie, newPaidHere,receiptNo, itemNo))
            self.__updateReceiptTotal(receiptNo)
        else:
            return {'Is Error': True, 'Error Message': "Item No '{}' not found in Invoice No '{}'. Cannot Update.".format(itemNo, receiptNo)}

        return {'Is Error': False, 'Error Message': ""}

    def delete_receipt_line(self, receiptNo, itemNo):
            data, columns = self.db.fetch ("SELECT * FROM receipt_line_item WHERE receipt_no = '{}' AND item_no = '{}' ".format(receiptNo, itemNo))
            if len(data) > 0:
                self.db.execute ("DELETE FROM receipt_line_item WHERE receipt_no = '{}' AND item_no = '{}' ".format(receiptNo, itemNo))
                self.__updateReceiptTotal(receiptNo)

            else:
                return {'Is Error': True, 'Error Message': "Item No '{}' not found in Invoice No '{}'. Cannot Delete.".format(itemNo, receiptNo)}

            return {'Is Error': False, 'Error Message': ""}