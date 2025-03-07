import json
from typing import Literal

import frappe
import frappe.utils

from ctf.api.stage import current_ctf_candidate


@frappe.whitelist()
def status():
	return {"setup_completed": is_setup_completed(), "ctf_status": get_ctf_status()}


@frappe.whitelist(allow_guest=True)
def stages():
	if frappe.session.user == "Guest":
		return [
			{
				"stage": "STAGE-0",
				"title": "Register to CTF",
				"description": """This is the first step towards the CTF.

You will find a unique link somewhere in the page to register to this contest.
""",
				"points": 0,
				"variables": {},
				"submitted": False,
				"submitted_flag": "",
				"correct": False,
				"status": "Not Registered",
				"show_input": False,
			}
		]

	if not is_setup_completed():
		return []

	"""
	{
		"stage": "STAGE-01",
		"title" : "Title of the stage",
		"description": "Description of the stage",
		"points": 100,
		"variables": {
			"FLAG_PAGE_ROUTE": "route to the flag page",
			"FLAG_CHARACTERS": "characters to be replaced in the flag page",
		},
		"submitted": false,
		"correct": false,
	}
	"""

	ctf_active = is_ctf_active()
	stages = frappe.get_all("CTF Stage", fields=["title", "description", "points", "name"], order_by="name")
	candidate_stages = frappe.get_all(
		"CTF Candidate Stage",
		fields=["stage", "variables", "submitted_flag", "correct"],
		filters={"parent": current_ctf_candidate()},
	)
	for stage in stages:
		candidate_stage = None
		for s in candidate_stages:
			if s.stage == stage.name:
				candidate_stage = s
				break
		if not candidate_stage:
			frappe.throw("Something is wrong. Please contact CTF admin.")

		stage["submitted"] = bool(candidate_stage.submitted_flag and len(candidate_stage.submitted_flag) > 0)
		stage["correct"] = bool(candidate_stage.correct)
		stage["status"] = (
			"Not Submitted" if not stage["submitted"] else "Correct" if stage["correct"] else "Incorrect"
		)
		stage["variables"] = json.loads(candidate_stage.variables)
		stage["show_input"] = ctf_active

	return stages


@frappe.whitelist(methods=["POST"])
def submit_flag(stage: str, flag: str):
	ctf_status = get_ctf_status()
	if ctf_status != "Started":
		frappe.throw("CTF is " + ctf_status)

	candidate_stage_name = frappe.get_cached_value(
		"CTF Candidate Stage", {"stage": stage, "parent": current_ctf_candidate()}, "name"
	)
	if not candidate_stage_name:
		frappe.throw("Invalid stage")
		return
	candidate_stage = frappe.get_doc("CTF Candidate Stage", candidate_stage_name)
	candidate_stage.submit_flag(flag)


def is_setup_completed() -> bool:
	return frappe.get_value("CTF Candidate", current_ctf_candidate(), "setup_completed")


def get_ctf_status() -> Literal["Not Started", "Started", "Ended"]:
	return frappe.get_value("CTF Settings", "CTF Settings", "status")


def is_ctf_active() -> bool:
	return get_ctf_status() == "Started"
