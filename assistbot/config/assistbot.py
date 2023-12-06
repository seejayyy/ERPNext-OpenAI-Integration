from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
        {
            "label": _("AssistBot"),
            "icon": "fa fa-star",
            "items": [
                {
                "type": "doctype",
                "name": "AssistBot Chat",
                "description": _("Chat"),
                "onboard": 1,
                },
                {
                "type": "doctype",
                "name": "AssistBot Settings",
                "description": _("Settings"),
                "onboard": 1,
                },
            ]
        },
    ]