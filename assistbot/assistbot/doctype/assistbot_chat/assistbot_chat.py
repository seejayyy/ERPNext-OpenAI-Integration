# -*- coding: utf-8 -*-
# Copyright (c) 2023, Chua Jun Jie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AssistBotChat(Document):
	pass

@frappe.whitelist()
def submit_message(doc):
	DocName = "AssistBot Chat"
