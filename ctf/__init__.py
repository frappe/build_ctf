__version__ = "0.0.1"

import frappe
from frappe.utils import response

# Need to patch exception checker


def _allow_website_users():
	# from frappe.permissions import is_system_user

	return (
		frappe.db
		# and frappe.get_system_settings("allow_error_traceback")
		and (not frappe.local.flags.disable_traceback or frappe._dev_server)
		# and is_system_user()
	)


response.is_traceback_allowed = _allow_website_users
