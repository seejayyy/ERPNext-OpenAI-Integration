# -*- coding: utf-8 -*-
# Copyright (c) 2023, Chua Jun Jie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe import _
from frappe.integrations.utils import make_post_request
import re

class AssistBotChat(Document):
	pass

@frappe.whitelist()
def execute_instruction(doc):
	doc = json.loads(doc)
	message = doc["assistbot_chatbox"]
	frappe.msgprint(_(message))
	context, operation, info = extract_context(message)
	if operation == "Create":
		# create 
		create_entry(context, info)
	elif operation == "Delete":
		# delete 
		delete_entry(context, info)
	elif operation == "Update":
		# update 
		update_entry(context, info)
	else:
		# get
		list_entry(context, info)

def create_entry(context, info):
	return

def delete_entry(context, info):
	return

def update_entry(context, info):
	return

def list_entry(context, info):
	db_data = get_data_from_doctype(context, info)
	# add a check to see if item exists
	if db_data == []:
		frappe.msgprint(_("Item does not exst"))
	else:
		output = json.dumps(db_data[0])
		frappe.msgprint(_(output))
	return

def get_data_from_doctype(context, info):	
	# most operations do things towards items
	info_data = frappe.db.get_list(context.title(), fields=["item_name"], filters={"item_name": info[0]})
	return info_data
	

def extract_context(instruction):
	# operation and the doctype 
	operation = ""
	context = ""

	# # find keywords in instruction
	keywords = "Create, Delete, Update, List"
	output_format = "Context: example, \nOperation: example, \nInformation: example"
	
	# use chatgpt to find context and operation
	prompt = "With the keywords provided here: " + keywords + ", \n The instruction here: " + instruction + ", \n The output format here: " + output_format + "\n Please tell me the context of the instruction in two word, the operation in one word using the keyword provided, and list the information provided. The output should follow the output format provided above"
	response = execute(prompt)
	splitted = re.split(': |, |\n', response)

	context = splitted[1]
	operation = splitted[3]
	information = splitted[5:]

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