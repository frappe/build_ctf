import frappe


@frappe.whitelist(allow_guest=True)
def ping():
	return "pong"


@frappe.whitelist()
def status():
	return "hi"


@frappe.whitelist()
def stages():
	pass


@frappe.whitelist(methods=["POST"])
def submit_flag(stage_id: str, flag: str):
	pass
