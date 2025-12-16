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


def calculate_profit_percentage(doc, method=None):
    # Safety
    if not doc.customer:
        return

    customer_group = frappe.db.get_value(
        "Customer",
        doc.customer,
        "customer_group"
    )

    # ❌ Skip Individual customers
    if customer_group == "Individual":
        return

    for item in doc.items:
        selling_rate = item.rate or 0

        # ✅ Use incoming_rate as valuation
        valuation_rate = (
            item.incoming_rate
            or item.last_purchase_rate
            or 0
        )

        if valuation_rate == 0:
            item.custom_profit_percentage = 0
            continue

        item.custom_profit_percentage = (
            (selling_rate - valuation_rate) / valuation_rate
        ) * 100