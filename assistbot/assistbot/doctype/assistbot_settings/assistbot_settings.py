# -*- coding: utf-8 -*-
# Copyright (c) 2023, Chua Jun Jie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe,json
from frappe.model.document import Document
from frappe import _

class AssistBotSettings(Document):
	pass

@frappe.whitelist()
def verify_key(doc):
	doc = json.loads(doc)
	key = doc["openai_api_key"]

	# try:
	# 	response = openai.Completion.create(
	# 		engine="davinci",
    #         prompt="This is a test.",
    #         max_tokens=5
	# 	)
	# except:
	# 	return False
	# else:
	# 	return True

	frappe.msgprint(_("API key is valid."))
 
 
	# try:
	# 	response = openai.Completion.create(
	# 		engine="davinci",
	# 		prompt="This is a test.",
	# 		max_tokens=5
	# 	)
	# except:
	# 	frappe.msgprint(_("Invalid API key."))
	# else:
	# 	frappe.msgprint(_("API key is valid."))
 	

	#return delete