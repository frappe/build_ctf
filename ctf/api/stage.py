import frappe

# This file contains only Stage Specific APIs

# Stage 04
@frappe.whitelist(methods=["GET"])
def is_correct_flag(submitted_flag: str):
	try:
		correct_flag = frappe.get_value(
			"CTF Candidate Stage",
			{
				"parent": current_ctf_candidate(),
				"stage": "STAGE-04",
			},
			"correct_flag",
		)
		if submitted_flag != correct_flag:
			return 1 / 0
		else:
			return correct_flag
	except:
		frappe.local.response["http_status_code"] = 500
		return frappe.get_traceback(with_context=True)


def current_ctf_candidate() -> str:
	if frappe.session.user == "Guest":
		frappe.throw("You are not logged in")
	return frappe.get_value("CTF Candidate", {"user": frappe.session.user}, "name")
