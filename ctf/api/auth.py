import frappe
from frappe.rate_limiter import rate_limit
from frappe.utils import validate_email_address

from ctf.ctf.doctype.account_request.account_request import AccountRequest, send_verification_mail
from ctf.utils import generate_otp

VERIFICATION_CODE_KEY_FORMAT = "user_verification_code||{}"


@frappe.whitelist(allow_guest=True, methods=["POST"])
def login(email: str):
	if not email:
		frappe.throw("Email is required")
	if not validate_email_address(email, throw=False):
		frappe.throw("Invalid email address")
	# check if there is any CTF candidate with this email
	if not frappe.db.exists("CTF Candidate", {"user": email}):
		return {
			"account_exists": False,
		}

	verification_code = generate_otp()
	frappe.cache().set_value(
		VERIFICATION_CODE_KEY_FORMAT.format(email), verification_code, expires_in_sec=600
	)
	send_verification_mail(email, verification_code)
	return {
		"account_exists": True,
	}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def register(email: str, first_name: str, last_name: str):
	if not email:
		frappe.throw("Email is required")
	if not validate_email_address(email, throw=False):
		frappe.throw("Invalid email address")
	if not first_name or not last_name:
		frappe.throw("First name and last name are required")
	ar = AccountRequest.register(email, first_name, last_name)
	return ar.name


@frappe.whitelist(allow_guest=True, methods=["POST"])
def resend_verification_code(ar: str):
	if not frappe.db.exists("Account Request", ar):
		frappe.throw("Invalid account request")
		return
	frappe.get_doc("Account Request", ar).send_otp()


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=5, seconds=60)
def verify_code(
	code: str,
	email: str | None = None,
	ar: str | None = None,
):
	if email:
		if code == frappe.cache().get_value(VERIFICATION_CODE_KEY_FORMAT.format(email), expires=True):
			frappe.cache().delete_value(VERIFICATION_CODE_KEY_FORMAT.format(email))
			frappe.local.login_manager.login_as(email)
		else:
			frappe.throw("Invalid verification code")
			return
	elif ar:
		if not frappe.db.exists("Account Request", ar):
			frappe.throw("Invalid account request")
			return

		ar_doc: AccountRequest = frappe.get_doc("Account Request", ar)
		ar_doc.verify_code_and_login(code)
	else:
		frappe.throw("Invalid request")
