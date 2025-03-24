import random
import json

import frappe

from ctf.utils import generate_otp, render_template

# This file contains only Stage Specific APIs


# Stage 04
@frappe.whitelist()
def is_correct_flag(submitted_flag: str):
	try:
		correct_flag = get_correct_flag("STAGE-04")
		if submitted_flag != correct_flag:
			frappe.throw("Invalid flag")
		else:
			return "Your flag is " + correct_flag
	except Exception as e:  # noqa: E722
		# Website users can't see exc by default
		frappe.local.response["http_status_code"] = 417
		tb =  frappe.get_traceback(with_context=True)
		frappe.response["exc"] = json.dumps([tb,])
		frappe.response.exception = tb.splitlines()[-1]
		frappe.response["exc_type"] = e.__name__


# Stage 06
@frappe.whitelist()
def send_verification_code(email: str):
	if email != "administrator@frappe.io":
		frappe.throw("Invalid email address. Only administrator@frappe.io is allowed")
	otp_key = "stage_06_verification_code||" + frappe.session.user
	otp = str(random.randint(1000, 9999))
	frappe.cache().set_value(otp_key, otp, expires_in_sec=1200)
	response = f"OTP Sent to {email} and valid for 20 minutes"
	frappe.msgprint(response)
	return response


@frappe.whitelist()
def validate_verification_code(code: str):
	code = str(code)
	otp_key = "stage_06_verification_code||" + frappe.session.user
	if len(code) != 4:
		frappe.throw("Verification code should be 4 digits")
		return
	if code != frappe.cache().get_value(otp_key, expires=True):
		frappe.throw("Invalid verification code")
		return
	response = "Your flag is " + get_correct_flag("STAGE-06")
	frappe.msgprint(response)
	return response


# Stage 09
@frappe.whitelist()
def retrieve_flag(template: str, answer: str):
	return render_template(
		template,
		{
			"flag": get_correct_flag("STAGE-09"),
			"super_secret": frappe.generate_hash(length=20),
			"answer": answer,
		},
	)


# Stage 10
@frappe.whitelist()
def check_flag(flag) -> str:
	candidate = current_ctf_candidate()
	flag = frappe.get_value(
		"CTF Candidate Stage",
		{"stage": "STAGE-10", "parent": candidate, "correct_flag": flag},
		"correct_flag",
	)
	if flag:
		return "Your flag is " + flag
	return "Invalid flag"


# Utility functions
def current_ctf_candidate() -> str:
	if frappe.session.user == "Guest":
		frappe.throw("You are not logged in")
	return frappe.get_cached_value("CTF Candidate", {"user": frappe.session.user}, "name")


def get_correct_flag(stage: str) -> str:
	return frappe.get_value(
		"CTF Candidate Stage",
		{
			"parent": current_ctf_candidate(),
			"stage": stage,
		},
		"correct_flag",
	)
