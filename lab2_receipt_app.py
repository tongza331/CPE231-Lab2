from helper_functions import *
from Invoice import *
from Product import *
from Customer import *
from API import *
from payment_method import *
from receipt import *
######################################################################
#List of API function calls:
#def create_product(products, code, name, units):
#def read_product(products, code):
#def update_product(products, code, newName, newUnits):
#def delete_product(products, code):
#def report_list_products(products):

#def create_customer(customers, customerCode, customerName, address, creditLimit, country):
#def read_customer(customers, customerCode):
#def update_customer(customers, customerCode, newCustomerName, newAddress, newCreditLimit, newCountry):
#def delete_customer(customers, customerCode):
#def report_list_all_customers(customers):

#def create_invoice(invoices, invoiceNo, invoiceDate, customerCode, dueDate, invoiceLineTuplesList):
#def read_invoice(invoices, invoiceNo):
#def update_invoice(invoices, invoiceNo, newInvoiceDate, newCustomerCode, newDueDate, newInvoiceLineTuplesList):
#def delete_invoice(invoices, invoiceNo):
#def update_invoice_line(invoices, invoiceNo, itemNo, productCode, newQuantity, newUnitPrice):
#def delete_invoice_line(invoices, invoiceNo, itemNo):
#def report_list_all_invoices(invoices, customers, products):

#def report_products_sold(invoices, products, dateStart, dateEnd):
#def report_customer_products_sold_list(invoices, products, customers, dateStart, dateEnd):
#def report_customer_products_sold_total(invoices, products, customers, dateStart, dateEnd):
#######################################################################

def main():
#main function begins here
    try:
        
        products = Product() # create object products from class Product. Starts as blank dict.
        #'HD01': {'Name': 'Seagate HDD 80 GB', 'Units': 'PCS'},
        # 'HD02': {'Name': 'IBM HDD 60 GB', 'Units': 'PCS'},
        # 'INT01': {'Name': 'Intel Pentium IV 3.6 GHz', 'Units': 'PCS'}}

        create_product(products, "HD01", "Seagate HDD 80 GB", "PCS")
        create_product(products, "HD02", "IBM HDD 60 GB", "PCS")
        create_product(products, "INT01", "Intle Pentium IV 3.6 GHz", "PCS")
        create_product(products, "INT99", "Intle Pentium V 4.2 GHz", "PCS")
        report_list_products(products)
        waitKeyPress("Above are results for creating 4 products.")
        
        read_product(products, "HD01")
        read_product(products, "HD99") #error
        #correct the spelling error of "Intle":
        update_product(products, newName = "Intel Pentium IV 3.6 GHz", newUnits = "PCS",
                        code = "INT01")
        update_product(products, "INT99", "Intel Pentium V 4.2 GHz", "PCS")
        report_list_products (products)
        waitKeyPress("Results after 2 reads, 2 updates to correct Intle spelling.")

        delete_product(products, "INT33") #error
        delete_product(products, "INT99")
        report_list_products(products)
        waitKeyPress("Results after deleting INT33 (not exist error) and INT99.")

        # pretty print a dictionary (in helper functions):
        #printDictData(products.dict)
        #waitKeyPress("Above is dictionary printed in better format.")

        # pretty print in column format a dictionary (in helper functions):
        #printDictInCSVFormat(products.dict, ('Code',), ('Name', 'Units'))
        #waitKeyPress("Above is dictionary printed in csv format for copy/paste to excel.")

        """
        #shows in case of untrapped exception:
        result = products.dict["HDD5"]
        waitKeyPress("There will be error and exit before you see this.")
        """

        customers = Customer()
        create_customer(customers, "Sam", "Sam Co., Ltd.", "122 Bangkok", 500000, "Thailand")
        create_customer(customers, "CP", "Charoen Pokaphan", "14 Sukhumvit, Bangkok", 2000000, "Thailand")
        report_list_all_customers(customers)
        waitKeyPress("Above are results for creating 2 customers.")
        
        read_customer(customers, "IT City")#error
        read_customer(customers, "Sam")
        update_customer(customers, newCustomerName = "CPALL", newAddress = "123 Bangkok", newCreditLimit = 100000, newCountry = "Thailand", customerCode = "CP")
        delete_customer(customers, "CP1")#not found
        #delete_customer(customers, "CP")
        report_list_all_customers(customers)
        waitKeyPress("Results after 2 reads, and update and delete customer CP")

        
        invoices = Invoice()
        create_invoice(invoices, invoiceNo="INT100/20", invoiceDate="2020-01-02", customerCode="Sam", dueDate=None, invoiceLineTuplesList=[{"Item No": 1, "Product Code": "HD01", "Quantity": 2, "Unit Price": 3000}, {"Item No": 2, "Product Code": "HD02", "Quantity": 1, "Unit Price": 2000}])
        create_invoice(invoices, "INT101/20", "2020-01-04", "CP", None,
                       [{"Item No": 1, "Product Code": "HD02", "Quantity": 1, "Unit Price": 2000}])
        create_invoice(invoices, invoiceNo="INT100/21", invoiceDate="2021-01-03", customerCode="Sam", dueDate=None,
                       invoiceLineTuplesList=[{"Item No": 1, "Product Code": "HD01", "Quantity": 2, "Unit Price": 3000},
                                              {"Item No": 2, "Product Code": "HD02", "Quantity": 1, "Unit Price": 2000}])
        create_invoice(invoices, "INT101/21", "2021-01-04", "CP", None,
                       [{"Item No": 1, "Product Code": "HD02", "Quantity": 1, "Unit Price": 2000}])
        report_list_all_invoices(invoices, customers, products)
        waitKeyPress("Above are results for creating 2 invoices and line item.")
        
        read_invoice(invoices, "INT100/20")
        update_invoice(invoices, invoiceNo="INT100/20", newInvoiceDate="2020-01-03", newCustomerCode="Sam", newDueDate=None, newInvoiceLineTuplesList=[{"Item No": 1, "Product Code": "HD01", "Quantity": 2, "Unit Price": 3000}, {"Item No": 2, "Product Code": "HD02", "Quantity": 1, "Unit Price": 2000}])
        # delete_invoice(invoices, "INT101/19")
        read_invoice(invoices, "INT100/21")
        read_invoice(invoices, "INT101/21")
        update_invoice(invoices, invoiceNo="INT100/21", newInvoiceDate="2021-01-02", newCustomerCode="Sam", newDueDate=None,
                       newInvoiceLineTuplesList=[{"Item No": 1, "Product Code": "HD01", "Quantity": 2, "Unit Price": 3000},
                                                 {"Item No": 2, "Product Code": "HD02", "Quantity": 1, "Unit Price": 2000}])
        report_list_all_invoices(invoices, customers, products)
        waitKeyPress("Results after read, update and delete Invoice")

        
        update_invoice_line(invoices, "INT100/20",1, "HD02", 8, 1000)
        report_list_all_invoices(invoices, customers, products)
        waitKeyPress("Results after update Invoice Line Item")

        #delete_invoice_line(invoices, "INT101/20", "HD02")
        report_list_all_invoices(invoices, customers, products)
        waitKeyPress("Results after delete Invoice Line Item")


        update_invoice_line(invoices, "INT100/21", 1, "HD02", 8, 1000)
        report_list_all_invoices(invoices, customers, products)
        waitKeyPress("Results after update Invoice Line Item")

        #delete_invoice_line(invoices, "INT101/21", 1)
        report_list_all_invoices(invoices, customers, products)
        waitKeyPress("Results after delete Invoice Line Item")

        print("\n*** Print Report ***")
        report_products_sold(invoices, products, '2021-01-01', '2021-01-31')

        report_customer_products_sold_list(invoices, products, customers, '2021-01-01', '2021-01-31')

        report_customer_products_sold_total(invoices, products, customers, '2021-01-01', '2021-01-31')

        paymentMethods = payment_method()
        print('--------------------------------------------------------------------')
        create_payment_method(paymentMethods, "CC", "Credit")
        create_payment_method(paymentMethods, "DC", "Debit")
        create_payment_method(paymentMethods, "PP", "Prompt Pay")
        report_list_payment_method(paymentMethods)
        waitKeyPress("Above are results for creating")
        print('--------------------------------------------------------------------')

        read_payment_method(paymentMethods, "CC")
        read_payment_method(paymentMethods, "DD")  # error
        print('--------------------------------------------------------------------')
        #correct the spelling error of "Intle":
        update_payment_method(paymentMethods, newDescription="Debit Card",
                              paymentMethodCode="DC")
        update_payment_method(paymentMethods, "CC", "Credit Card")
        print('--------------------------------------------------------------------')
        report_list_payment_method(paymentMethods)
        waitKeyPress(
            "Results after 2 reads, 2 updates to correct Intle spelling.")
        print('--------------------------------------------------------------------')

        delete_payment_method(paymentMethods, "DD")  # error
        delete_payment_method(paymentMethods, "PP")
        report_list_payment_method(paymentMethods)
        waitKeyPress("Results after deleting CC (not exist error) and INT99.")
        print('--------------------------------------------------------------------')

        #Test receipt functions
        receipts = Receipt()
        #Create receipt
        create_receipt(receipts, 'RCT1001/20', '2020-02-04', 'CP', 'DC', 'Debit Card', 10000, 'Paid all invoices partially',
                       [{"Item No": 1, 'Invoice No': 'INT100/20', 'Amount Paid Here': 100}, {"Item No": 2, 'Invoice No': 'INT101/20', 'Amount Paid Here': 200}])
        create_receipt(receipts, 'RCT1002/20', '2020-02-05', 'Sam', 'CC', 'Master Card, Citibank', 15000,'Partially paid on INT101/20',
                       [{"Item No": 1, 'Invoice No': 'INT100/20', 'Amount Paid Here': 8560}, {"Item No": 2, 'Invoice No': 'INT101/20', 'Amount Paid Here': 1440}])
        create_receipt(receipts,'RCT1003/20','2020-02-06','CP','DC','Debit Card',20000,'This will later be deleted',
                       [{"Item No": 1, 'Invoice No': 'INT100/20', 'Amount Paid Here': 10}, {"Item No": 2, 'Invoice No': 'INT101/20', 'Amount Paid Here': 20}])
        create_receipt(receipts, "RCT1001/21", "2021-01-04", "CP", "DC", "KBTG card",
                       9000, "-", [{"Item No": 1, "Invoice No": "INT100/21", "Amount Paid Here": 600}])
        create_receipt(receipts, "RCT1002/21", "2021-01-05", "Sam", "CC", "pay ref", 10000, "rmark",
                       [{"Item No": 1, "Invoice No": "INT100/21", "Amount Paid Here": 8560},
                        {"Item No": 2, "Invoice No": "INT101/21", "Amount Paid Here": 900}])
        create_receipt(receipts, "RCT1003/21", "2021-01-06", "Sam", "CC", "Master Card,Citybank", 10000, "Partially paid on IN101/21",
                       [{"Item No": 1, "Invoice No": "INT100/21", "Amount Paid Here": 300}])
        print("")
        report_list_all_receipts()
        waitKeyPress("Results of creating 3 receipts: RCT1001/20, RCT1002/20, and RCT1003/20")
        
        #Read receipt
        read_receipt(receipts, "RCT1001/21")
        read_receipt(receipts, "RCT1002/21")
        read_receipt(receipts,'RCT1005/20') # cannot read RCT1005/20 
        report_list_all_receipts()
        waitKeyPress("Results of reading 3 receipts: RCT1001/21 (successfully), RCT1002/21 (successfully), and RCT1005/20 (unsuccessfully)")
        
        #Update receipt
        update_receipt(receipts, "RCT1002/20", "2020-02-06", "Sam", "CC", "Master Card,Citybank", 10000, "Partially paid on IN101/20",
                       [{"Item No": 1, "Invoice No": "INT100/20", "Amount Paid Here": 7000}, {"Item No": 2, "Invoice No": "INT101/20", "Amount Paid Here": 1500}])
        update_receipt(receipts, 'RCT1004/20', '1999-12-31', 'Sam', 'CC', 'Master Card, Citibank', 10000,'Partially paid on INT101/20',
                       [{"Item No": 1, 'Invoice No': 'INT100/20', 'Amount Paid Here': 8560}, {"Item No": 2, 'Invoice No': 'INT101/20', 'Amount Paid Here': 1440}])  # cannot update RCT1004/21
        report_list_all_receipts()
        waitKeyPress("Results of updating 2 receipts: RCT1002/20 (successfully) and RCT1004/20 (unsuccessfully)")

        # update receipt line item
        update_receipt_line (receipts, "RCT1002/21", 2, "INT101/21",1000)
        update_receipt_line(receipts, "RCT1004/21", 2, "INT101/21", 1500) #Cannot update line receipt 
        waitKeyPress("Results of updating 2 receipts line item: RCT1002/21 (successfully) and RCT1004/20 (unsuccessfully)")
        #Report unpaid invoice 1
        report_unpaid_invoices()
        waitKeyPress("Report unpaid invoice 1")

        # delete receipt line item
        delete_receipt_line(receipts, "RCT1001/20", 1)
        delete_receipt_line(receipts, "RCT1001/20", 2)
        delete_receipt_line(receipts, "RCT1003/20", 1)
        delete_receipt_line(receipts, "RCT1003/20", 2)
        # cannot delete INT1004/21 on item 2
        delete_receipt_line(receipts, "RCT1004/20", 2)
        delete_receipt_line(receipts, "RCT1001/21", 1)
        delete_receipt_line(receipts, "RCT1003/21", 1)
        # cannot delete INT1003/21 on item 2
        delete_receipt_line(receipts, "RCT1003/21", 2)
        waitKeyPress("Results of deleting 2 receipts line : RCT1003/20 (successfully) and RCT1004/20 (unsuccessfully)")

        #Delete receipt
        delete_receipt(receipts, 'RCT1001/20')
        delete_receipt(receipts, 'RCT1003/20')
        delete_receipt(receipts, 'RCT1005/20')  # cannot delete RCT1005/20
        # delete receipt
        delete_receipt(receipts, "RCT1001/21")
        delete_receipt(receipts, "RCT1003/21")
        report_list_all_receipts()
        waitKeyPress("Results of deleting 4 receipts: 3 receipts (successful) and RCT1005/20 (unsuccessfully)")

        

        #print ("\nTest Report")
        #report_products_sold(invoices, products, '2020-01-01', '2020-01-31')
        #report_customer_products_sold_list(invoices, products, customers, '2020-01-01', '2020-01-31')
        #report_customer_products_sold_total(invoices, products, customers, '2020-01-01', '2020-01-31')
        report_unpaid_invoices()
        
    except: #this traps for unexpected system errors
        print ("Unexpected error:", sys.exc_info()[0])
        raise # this line can be erased. It is here to raise another error so you can see which line to debug.
    else:
        print("Normal Termination.   Goodbye!")
#main function ends