import frappe

def handle_customer_creation(doc, method=None):
    # ❌ Skip Individual customers
    if doc.customer_group == "Individual":
        return

    # 🔒 Prevent duplicate Sales Partner
    if frappe.db.exists("Sales Partner", {"customer": doc.name}):
        return

    create_sales_partner(doc)


def create_sales_partner(customer):
    sales_partner = frappe.get_doc({
        "doctype": "Sales Partner",
        "partner_name": customer.customer_name,
        "customer": customer.name,

        # ✅ Mandatory fields
        "commission_rate": 0,
        "territory": "All Territories"
    })

    sales_partner.insert(ignore_permissions=True)
