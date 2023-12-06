# -*- coding: utf-8 -*-
# Copyright (c) 2023, Chua Jun Jie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe import _

class AssistBotChat(Document):
	pass

@frappe.whitelist()
def execute_instruction(doc):
	doc = json.loads(doc)
	message = doc["assistbot_chatbox"]
	frappe.msgprint(_(message))
