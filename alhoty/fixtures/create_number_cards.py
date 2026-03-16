#!/usr/bin/env python3

import frappe

def create_number_cards():
    """Create Number Card doctypes for the NDT Portal workspace"""
    
    cards = [
        {
            "name": "Active Work Orders",
            "label": "Active Work Orders", 
            "document_type": "Work Order",
            "function": "Count",
            "filters_json": '{"docstatus": ["!=", 2]}',
            "color": "#2490ef"
        },
        {
            "name": "Pending Inspections",
            "label": "Pending Inspections",
            "document_type": "MT Inspection", 
            "function": "Count",
            "filters_json": '{"docstatus": ["=", 0]}',
            "color": "#f39c12"
        },
        {
            "name": "Equipment Due Calibration",
            "label": "Equipment Due Calibration",
            "document_type": "Equipment Master",
            "function": "Count", 
            "filters_json": '{}',
            "color": "#e74c3c"
        },
        {
            "name": "Total Branches",
            "label": "Total Branches",
            "document_type": "Branch Master",
            "function": "Count",
            "filters_json": '{}', 
            "color": "#27ae60"
        }
    ]
    
    for card_data in cards:
        if not frappe.db.exists("Number Card", card_data["name"]):
            card = frappe.new_doc("Number Card")
            card.update(card_data)
            card.insert(ignore_permissions=True)
            print(f"Created Number Card: {card_data['name']}")
        else:
            print(f"Number Card already exists: {card_data['name']}")
    
    frappe.db.commit()
    print("All Number Cards created successfully!")

if __name__ == "__main__":
    frappe.init(site="alhoty.local")
    frappe.connect()
    frappe.set_user("Administrator")
    create_number_cards()