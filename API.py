from DBHelper import DBHelper
from helper_functions import *
#This file will contain all API functions calls exposed to outside world for users to use

# function about Product
def create_product(products, code, name, units):
    result = products.create(code, name, units)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Create Success.')
    return result #send result for caller program to use

def read_product(products, code):
    result = products.read(code) #returns tuple of (error dict, data dict)
    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_product(products, code, newName, newUnits):
    result = products.update(code, newName, newUnits) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Update Success.')
    return result #send result for caller program to use

def delete_product(products, code):
    result = products.delete(code)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Delete Success.')
    return result #send result for caller program to use

def report_list_products(products):
    result = products.dump()
    #printDictInCSVFormat(result, ('Code',), ('Name', 'Units'))
    print (result)
    return result #send result for caller program to use


# function about Customer 
def create_customer(customers, customerCode, customerName, address, creditLimit, country):
    result = customers.create(customerCode, customerName, address, creditLimit, country)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Customer Create Success.')
    return result #send result for caller program to use

def read_customer(customers, customerCode):
    result = customers.read(customerCode) #returns tuple of (error dict, data dict)
    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_customer(customers, customerCode, newCustomerName, newAddress, newCreditLimit, newCountry):
    result = customers.update(customerCode, newCustomerName, newAddress, newCreditLimit, newCountry) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Customer Update Success.')
    return result #send result for caller program to use

def delete_customer(customers, customerCode):
    result = customers.delete(customerCode)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Customer Delete Success.')
    return result #send result for caller program to use

def report_list_all_customers(customers):
    result = customers.dump()
    printDictInCSVFormat(result, ('Customer Code',), ('Name', 'Address','Credit Limit', 'Country'))
    return result #send result for caller program to use

# function about Invoice 
def create_invoice(invoices, invoiceNo, invoiceDate, customerCode, dueDate, invoiceLineTuplesList):
    if invoiceDate == None:
        invoiceDate = 'null'
    else:
        invoiceDate = "'" + invoiceDate + "'"
    if dueDate == None:
        dueDate = 'null'
    else:
        dueDate = "'" + dueDate + "'"
    result = invoices.create(invoiceNo, invoiceDate, customerCode, dueDate, invoiceLineTuplesList)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Create Success.')
    return result #send result for caller program to use

def read_invoice(invoices, invoiceNo):
    result = invoices.read(invoiceNo) #returns tuple of (error dict, data dict)
    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_invoice(invoices, invoiceNo, newInvoiceDate, newCustomerCode, newDueDate, newInvoiceLineTuplesList):
    if newInvoiceDate == None:
        newInvoiceDate = 'null'
    else:
        newInvoiceDate = "'" + newInvoiceDate + "'"
    if newDueDate == None:
        newDueDate = 'null'
    else:
        newDueDate = "'" + newDueDate + "'"
    result = invoices.update(invoiceNo, newInvoiceDate, newCustomerCode, newDueDate, newInvoiceLineTuplesList) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Update Success.')
    return result #send result for caller program to use

def delete_invoice(invoices, invoiceNo):
    result = invoices.delete(invoiceNo)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Delete Success.')
    return result #send result for caller program to use

def update_invoice_line(invoices, invoiceNo, itemNo, productCode, newQuantity, newUnitPrice):
    result = invoices.update_invoice_line(invoiceNo, itemNo, productCode, newQuantity, newUnitPrice) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Line Item Update Success.')
    return result #send result for caller program to use

def delete_invoice_line(invoices, invoiceNo, itemNo):
    result = invoices.delete_invoice_line(invoiceNo, itemNo) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Line Item Delete Success.')
    return result #send result for caller program to use

def report_list_all_invoices(invoices, customers, products):
    # Will dump all invoices data and return 1 dictionary as a result (with header and line item joined).  
    # Please show the customer name and product name also. 
    # A helper function such as def print_tabular_dictionary(tabularDictionary) can then be called to print this in a tabular (table-like) form with column headings and data. 

    db = DBHelper()
    data, columns = db.fetch ('SELECT i.invoice_no as "Invoice No", i.date as "Date" '
                              ' , i.customer_code as "Customer Code", c.name as "Customer Name" '
                              ' , i.due_date as "Due Date", i.total as "Total", i.vat as "VAT", i.amount_due as "Amount Due" '
                              ' , ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , ili.quantity as "Quantity", ili.unit_price as "Unit Price", ili.product_total as "Extended Price" '
                              ' FROM invoice i JOIN customer c ON i.customer_code = c.customer_code '
                              '  JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '  JOIN product p ON ili.product_code = p.code '
                              ' ')
    #print (result)
    result = row_as_dict(data, columns)
    printDictInCSVFormat(result, ('Invoice No',), ('Date', 'Customer Code', 'Customer Name','Due Date','Total','VAT','Amount Due'
                                                , 'Product Code', 'Product Name', 'Quantity', 'Unit Price', 'Extended Price'))
    return result #send result for caller program to use

def report_products_sold(invoices, products, dateStart, dateEnd):
    # Will return 2 dictionaries: 
    # 1) a dictionary as list of in products sold in the given date range in tabular format of: Product Code, Product Name, Total Quantity Sold, Total Value Sold. Here, (product code) will be unique. 
    # And 2) a second dictionary of the footer will also be returned containing: t the end also show the sum of Total Value Sold.  
    db = DBHelper()
    data, columns = db.fetch ('SELECT p.code as "Code", ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.product_total) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' GROUP BY p.code, ili.product_code, p.name ')
    result = row_as_dict(data, columns)
    data, columns = db.fetch ('SELECT 0 as "Footer", SUM(ili.product_total) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' ')
    result2 = row_as_dict(data, columns)

    printDictInCSVFormat(result, (None), ('Product Code','Product Name', 'Total Quantity Sold', 'Total Value Sold'))
    printDictInCSVFormat(result2, (None), ('Total Value Sold',))
    return result, result2

def report_customer_products_sold_list(invoices, products, customers, dateStart, dateEnd):
    # Will return 2 dictionaries: 
    # 1) a dictionary as list of customers and list the products sold to them in the given date range in this format:  Customer Code, Customer Name, Product Code,  Product Name, Invoice No, Invoice Date, Quantity Sold, Value Sold. Here, (customer code, product code, invoice no) will be unique.  
    # And 2) a second footer dictionary showing:  At the end also show the sum of Quantity Sold and sum of Value Sold.
    db = DBHelper()
    data, columns = db.fetch ('SELECT i.customer_code, c.customer_code as "Customer Code", c.name as "Customer Name" '
                              ' , ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , i.invoice_no as "Invoice No" '
                              ' , SUM(ili.quantity) as "Quantity Sold", SUM(ili.product_total) as "Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN customer c ON i.customer_code = c.customer_code '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' GROUP BY i.customer_code, c.customer_code, c.name, i.invoice_no, ili.product_code, p.name ')
    result = row_as_dict(data, columns)
    data, columns = db.fetch ('SELECT 0 as "Footer", SUM(ili.quantity) as "Quantity Sold", SUM(ili.product_total) as "Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN customer c ON i.customer_code = c.customer_code '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' ')
    result2 = row_as_dict(data, columns)

    printDictInCSVFormat(result, (None), ('Customer Code','Customer Name', 'Product Code', 'Product Name', 'Invoice No', 'Quantity Sold', 'Value Sold'))
    printDictInCSVFormat(result2, (None), ('Quantity Sold','Value Sold'))
    return result.values(), result2

def report_customer_products_sold_total(invoices, products, customers, dateStart, dateEnd):
    # Will return 2 dictionaries: 
    # 1) a dictionary as list customers and the total number and value of products sold to them in the given date range in this format:  Customer Code, Customer Name, Product Code,  Product Name, Total Quantity Sold, Total Value Sold. Here (customer code, product code) will be unique.
    # And 2) a second footer dictionary showing: t the end also show the sum of Total Quantity Sold, sum of Total Value Sold.
    db = DBHelper()
    data, columns = db.fetch ('SELECT i.customer_code, c.customer_code as "Customer Code", c.name as "Customer Name" '
                              ' , ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.product_total) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN customer c ON i.customer_code = c.customer_code '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' GROUP BY i.customer_code, c.customer_code, c.name, i.invoice_no, ili.product_code, p.name ')
    result = row_as_dict(data, columns)
    data, columns = db.fetch ('SELECT 0 as "Footer", SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.product_total) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN customer c ON i.customer_code = c.customer_code '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' ')
    result2 = row_as_dict(data, columns)

    printDictInCSVFormat(result, (None), ('Customer Code','Customer Name', 'Product Code', 'Product Name', 'Total Quantity Sold', 'Total Value Sold'))
    printDictInCSVFormat(result2, (None), ('Total Quantity Sold','Total Value Sold'))
    return result.values(), result2

#function about Payment
def create_payment_method(payments, payment_method, description):
    result = payments.create(payment_method, description)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('payment_method Create Success.')
    return result #send result for caller program to use

def read_payment_method(payments, payment_method):
    result = payments.read(payment_method) #returns tuple of (error dict, data dict)
    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_payment_method(payments, newPayment,newdescription):
    result = payments.update(newPayment,newdescription) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Update Success.')
    return result #send result for caller program to use

def delete_payment_method(payments, payment_method):
    result = payments.delete(payment_method)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Delete Success.')
    return result #send result for caller program to use

def report_list_payment_method(payments):
    result = payments.dump()
    #printDictInCSVFormat(result, ('Code',), ('Name', 'Units'))
    print (result)
    return result #send result for caller program to use


# function about Receipt
def create_receipt(receipts, receiptNo, receiptDate, customerCode, paymentMethod, paymentReference, totalReceived, remarks, receiptLineTuplesList):
    result = receipts.create(receiptNo, receiptDate, customerCode, paymentMethod, paymentReference,totalReceived, remarks, receiptLineTuplesList)  # returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Create Success.')
    return result #send result for caller program to use



def read_receipt(receipts, receiptNo):
    result = receipts.read(receiptNo) #returns tuple of (error dict, data dict)
    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_receipt(receipts, receiptNo, newReceiptDate, newCustomerCode,newPayment, newPaymentRef, newTotal_receipt, newRemarks, ReceiptLineTuplesList):
    if newReceiptDate == None:
        newReceiptDate = 'null'
    else:
        newReceiptDate = "'" + newReceiptDate + "'"
    if newReceiptDate == None:
        newReceiptDate = 'null'
    else:
        newReceiptDate = "'" + newReceiptDate + "'"
    result = receipts.update(receiptNo, newReceiptDate, newCustomerCode, newPayment, newPaymentRef, newTotal_receipt,newRemarks,ReceiptLineTuplesList) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Update Success.')
    return result #send result for caller program to use

def delete_receipt(receipts, receiptNo):
    result = receipts.delete(receiptNo)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Delete Success.')
    return result #send result for caller program to use

def update_receipt_line(receipts, receiptNo,itemNo, newInvocie, newPaidHere):
    result = receipts.update_receipt_line(receiptNo, itemNo, newInvocie, newPaidHere) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Line Item Update Success.')
    return result #send result for caller program to use

def delete_receipt_line(receipts, receiptNo, itemNo):
    result = receipts.delete_receipt_line(receiptNo, itemNo) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Line Item Delete Success.')
    return result #send result for caller program to use

def report_list_all_receipts():
    # Will dump all invoices data and return 1 dictionary as a result (with header and line item joined).  
    # Please show the customer name and product name also. 
    # A helper function such as def print_tabular_dictionary(tabularDictionary) can then be called to print this in a tabular (table-like) form with column headings and data. 

    db = DBHelper()
    data, columns = db.fetch ('SELECT 0 as "Footer", r.receipt_no as "Receipt No" '
                                ', i.date as "Date" '
                                ', c.customer_code as "Customer Code"'
                                ', c.name as "Customer Name"'
                                ', p.description as "Payment Name"'
                                ', r.total_receipt as "Total Receipt" '
                                ', r.payment_reference as "Payment Reference"'
                                ', r.remarks as "Remarks"'
                                ', rli.invoice_no as "Invoice No"'
                                ', rli.amount_paid_here as "Amount Paid Here"'
                                ' FROM receipt r JOIN receipt_line_item rli ON r.receipt_no =  rli.receipt_no '
                                ' JOIN customer c ON r.customer_code = c.customer_code'
                                ' JOIN payment_method p ON r.payment_method = p.payment_method' 
                                ' JOIN invoice i ON i.invoice_no = rli.invoice_no ' )
    result = row_as_dict(data, columns)    
    data2, columns2 = db.fetch ('SELECT 0 as "Footer", rli.invoice_no as "Invoice No" '
                                ', i.date as "Invoice Date" '
                                ', i.amount_due as "Invoice Full Amount" '
                                ', rli.amount_paid_here as "Amount Paid Here"'
                                ' FROM receipt r JOIN receipt_line_item rli ON r.receipt_no =  rli.receipt_no '
                                ' JOIN invoice i ON i.invoice_no = rli.invoice_no ')                 
    result2 = row_as_dict(data2, columns2)

    printDictInCSVFormat(result, (None), ('Receipt No','Date', 'Customer Code', 'Customer Name', 'Payment Name', 'Total Receipt', 'Payment Reference', 'Remarks'))
    printDictInCSVFormat(result2, (None), ('Invoice No','Invoice Date', 'Invoice Full Amount', 'Amount Paid Here'))
    return result, result2 #send result for caller program to use 
  

def report_unpaid_invoices():
    db = DBHelper()
    data, columns = db.fetch('SELECT i.invoice_no as "Inoivce No" ,'
                             ' i.date as "Date" ,'
                             '   r.customer_code as "Customer Code" ,'
                             '   c.name as "Customer Name" ,'
                             '   i.amount_due as "Amount Due", '
                             '   i.amount_due - SUM(rli.amount_paid_here) as "Amount Unpaid",'
                             '   rli.amount_paid_here as "Amount Paid Here"  '
                             '   FROM invoice i JOIN receipt_line_item rli ON i.invoice_no = rli.invoice_no '
                             '   JOIN receipt r ON r.receipt_no = rli.receipt_no '
                             '   JOIN customer c ON c.customer_code = r.customer_code '
                             '   GROUP BY i.invoice_no,r.customer_code,c.name,rli.amount_paid_here ' )
    result = row_as_dict(data, columns)
    data, columns = db.fetch('SELECT 0 as "Footer",SUM(unpaid) as "Total Invoice Amount Not Paid" , SUM("Amount Paid Here") as "Total Invoice Amount Received"'
                            ' FROM (SELECT rli.invoice_no as "Invoice No", i.date as "Invoice Date", c.name as "Customer Name" ,'
                            ' i.amount_due as "Amount Received", SUM(rli.amount_paid_here) as "Amount Paid Here", '
                            ' (i.amount_due - sum(rli.amount_paid_here)) as "unpaid" '
                            ' FROM receipt r JOIN receipt_line_item rli ON r.receipt_no = rli.receipt_no'
                            ' JOIN invoice i ON i.invoice_no = rli.invoice_no '
                            ' JOIN customer c ON c.customer_code = i.customer_code '
                            ' GROUP BY rli.invoice_no ,i.date, c.name,i.amount_due) as total_un_re;')
    result2 = row_as_dict(data, columns)
    printDictInCSVFormat(result, ('Invoice No',), ('Date', 'Customer Code', 'Customer Name', 'Amount Due', 'Amount Unpaid', 'Amount Paid Here'))
    printDictInCSVFormat(result2, (None), ('Total Invoice Amount Not Paid', 'Total Invoice Amount Received'))
    return result