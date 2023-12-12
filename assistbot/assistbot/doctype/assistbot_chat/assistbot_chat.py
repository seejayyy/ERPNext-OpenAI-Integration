# -*- coding: utf-8 -*-
# Copyright (c) 2023, Chua Jun Jie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe import _
from frappe.integrations.utils import make_post_request
import re
import datetime

class AssistBotChat(Document):
	pass

@frappe.whitelist()
def execute_instruction(doc):
	doc = json.loads(doc)
	message = doc["assistbot_chatbox"]
	frappe.msgprint(_(message))
	context, operation, info = extract_context(message)
	if "Create" in operation[0]:
		# create 
		create_entry(context, info)
		frappe.msgprint(_("{0} is created").format(context[0]))
	elif "Delete" in operation[0]:
		# delete 
		delete_entry(context, info)
	elif "Update" in operation[0]:
		# update 
		update_entry(context, info)
	else:
		# get
		list_entry(context, info)

def create_entry(context, info):
	# get necessary information 
	# customer, company, item, quantity (defaulted by the item), source warehouse
	info = re.split('\s', info)
	info = list(filter(None,info))
	# print(info)
	# check if instruction specify customer
	try:
		customer_index = info.index("Customer")
	except:
		frappe.throw(_("Please specify customer for the sales order"))
	try:
		company_index = info.index("Company")
	except:
		frappe.throw(_("Please specify company for the sales order"))
	try:
		item_index = info.index("Item")
	except:
		frappe.throw(_("Please specify item for the sales order"))
	try:
		warehouse_index = info.index("Warehouse")
	except:
		frappe.throw(_("Please specify source warehosue for the sales order"))

	# check if info is valid
	try:
		customer_info = info[customer_index+1:company_index]
		customer_info = ' '.join(customer_info)
		customer_data = get_data_from_doctype("Customer","customer_name", customer_info)
		print(customer_data)
		if len(customer_data) == 0:
			frappe.throw(_("Invalid customer"))
		if len(customer_data) > 1:
			frappe.throw(_("Multiple records detected. Please specify the correct customer."))
		customer_queried = customer_data[0].name
	except:
		frappe.throw(_("Invalid customer"))
	try:
		company_info = info[company_index+1:item_index]
		company_info = ' '.join(company_info)
		company_data = get_data_from_doctype("Company","company_name", company_info)
		print(company_data)
		if len(company_data) == 0:
			frappe.throw(_("Invalid company"))
		if len(company_data) > 1:
			frappe.throw(_("Multiple records detected. Please specify the correct company."))
		company_queried = company_data[0].name
	except:
		frappe.throw(_("Invalid company"))
	
	try:
		print("get item")
		item_info = info[item_index+1:warehouse_index]
		item_info = ' '.join(item_info)
		item_data = get_data_from_doctype("Item","item_name", item_info)
		print(item_data)
		if len(item_data) == 0:
			frappe.throw(_("Invalid item"))
		if len(item_data) > 1:
			frappe.throw(_("Multiple records detected. Please specify the correct item."))
		item_queried = item_data[0].name
		item_valuation_rate = item_data[0].valuation_rate
	except:
		frappe.throw(_("Invalid item"))
	
	try:
		warehouse = info[warehouse_index+1:]
		warehouse = ' '.join(warehouse)
		warehouse_data = get_data_from_doctype("Warehouse","warehouse_name", warehouse)
		print(warehouse_data)
		if len(warehouse_data) == 0:
			frappe.throw(_("Invalid warehouse"))
		if len(warehouse_data) > 1:
			frappe.throw(_("Multiple records detected. Please specify the correct warehouse."))
		warehouse_queried = warehouse_data[0].name
	except:
		frappe.throw(_("Invalid warehouse"))

	# param = json.dumps({
	# 	"doctype": context[0].title(),
	# 	"customer": customer_queried,
	# 	"company": company_queried,
	# 	"item": item_queried,
	# 	"warehouse": warehouse_queried
	# })
	sales_order_doc = frappe.get_doc({
		"doctype": "Sales Order",
		"company": company_queried,
		"customer": customer_queried,
		"set_warehouse": warehouse_queried,
		"delivery_date": datetime.date.today(),
		"items": [
			{
				"item_code": item_queried,
				"qty": 1.0,
				"rate": item_valuation_rate,
				"warehouse": warehouse_queried
			}
		]
	})
	sales_order_doc.insert()
	# webhook_post(param)
	return 

def delete_entry(context, info):
	return

def update_entry(context, info):
	return

def list_entry(context, info):
	# db_data = get_data_from_doctype(context, info)
	# # add a check to see if item exists
	# if len(db_data) == 0:
	# 	frappe.msgprint(_("Item does not exst"))
	# else:
	# 	output = json.dumps(db_data[0])
	# 	frappe.msgprint(_(output))
	return

def get_data_from_doctype(doctype, field, info):

	# print(doctype)
	# print(field)
	# print(info)
	
	# most operations do things towards items
	# frappe.db.get_list(doctype.title(), fields="*", filters={field: info[0]}) 
	return frappe.db.get_list(doctype.title(), fields="*", filters={field: info}) 
	

def extract_context(instruction):
	# # find keywords in instruction
	keywords = "Create, Delete, Update, List"
	output_format = "Context:example,Operation:example,Information:info1,example1"
	
	# use chatgpt to find context and operation
	prompt = "With the keywords provided here: " + keywords + ", \n The instruction here: " + instruction + ", \n The output format here: " + output_format + "\n Please tell me the context of the instruction in two word, the operation in one word using the keyword provided, and list the information provided. The output should strictly follow the output format provided above"
	response = execute(prompt)

	splitted = re.split(':\s|,|=|-\s|[\n]', response)
	# print(splitted)
	context_index = splitted.index("Context")	
	operation_index = splitted.index("Operation")
	information_index = splitted.index("Information")

	context = splitted[context_index+1:operation_index]
	operation = splitted[operation_index+1:information_index]
	information_list = splitted[information_index+1:]

	information = ' '.join(information_list)

	# print(context)
	# print(operation)
	# print(information)
	return context, operation, information

def execute(instruction):
	# obtain API key
	openai_settings = frappe.get_doc("AssistBot Settings")
	openai_api_key = openai_settings.openai_api_key

	url = 'https://api.openai.com/v1/chat/completions'
	headers = {
		'Content-type': 'application/json;',
		'Authorization': 'Bearer ' + openai_api_key,
	}
	data = json.dumps({
		"model": "gpt-3.5-turbo",
		"messages": [{"role": "user", "content": instruction}],
		"temperature": 0.7
	})

	response = make_post_request(url, headers=headers, data=data)
	frappe.msgprint(_(response["choices"][0]["message"]["content"]))
	return response["choices"][0]["message"]["content"]

def webhook_post(param):
	url = 'http://192.168.4.223:5678/webhook-test/erpnextchatbot'
	headers = {
		'Content-type': 'application/json;'
	}
	response = make_post_request(url, headers=headers, data=param)