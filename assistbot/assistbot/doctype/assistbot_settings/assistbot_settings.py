# -*- coding: utf-8 -*-
# Copyright (c) 2023, Chua Jun Jie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe,json
from frappe.model.document import Document
from frappe import _
from frappe.integrations.utils import make_post_request

class AssistBotSettings(Document):
	pass

@frappe.whitelist()
def verify_key(doc):
	# turn str into json object
	doc = json.loads(doc)
	# obtain key
	key = doc["openai_api_key"]
	url = 'https://api.openai.com/v1/chat/completions'
	headers = {
		'Content-type': 'application/json;',
		'Authorization': 'Bearer ' + key,
	}
	data = json.dumps({
		"model": "gpt-3.5-turbo",
		"messages": [{"role": "user", "content": "Say this is a test!"}],
		"temperature": 0.7
	})
	try:
		output = make_post_request(url, headers=headers, data=data)
	except:
		frappe.msgprint(_("Invalid Key"))
	else:
		frappe.msgprint(_("Key is valid"))