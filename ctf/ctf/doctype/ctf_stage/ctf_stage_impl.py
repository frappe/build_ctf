# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

from __future__ import annotations

from typing import TYPE_CHECKING

from ctf.ctf.doctype.ctf_stage.ctf_stage_assets import STAGE_02_JS
import frappe

from ctf.utils import generate_flag

if TYPE_CHECKING:
	from ctf.ctf.doctype.ctf_candidate.ctf_candidate import CTFCandidate

"""
Stage Implementation Function Signature -
def (candidate: CTFCandidate, flag:str) -> dict[str, str]

Return dictionary of variables, which will be stored in the candidate stage
"""


# Implementations
def setup_stage_01(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	# Create a server script
	api_method = f"stage-01-{candidate.name}"
	frappe.get_doc(
		{
			"doctype": "Server Script",
			"name": api_method,
			"api_method": api_method,
			"script_type": "API",
			"disabled": 0,
			"allow_guest": 1,
			"script": f"""
print("{flag}")
frappe.response['message'] = "Hi, you got close to your flag"
""",
		}
	).insert()

	return {"FLAG_PAGE_ROUTE": f"/stage-01/{api_method}"}


def setup_stage_02(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	flag_characters = flag.replace("FLAG{", "").replace("}", "")
	file_doc = frappe.get_doc(
		{
			"doctype": "File",
			"file_name": f"stage-02-{candidate.name}.js",
			"attached_to_doctype": None,
			"attached_to_name": None,
			"content": STAGE_02_JS.replace("{{FLAG_CHARACTERS}}", flag_characters),
			"is_private": 1,
			"owner": candidate.user,
		}
	).insert()
	file_name_without_ext = file_doc.file_name.split(".")[0]
	return {
		"FLAG_PAGE_ROUTE": f"/stage-02/{file_name_without_ext}",
	}


def setup_stage_03(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_04(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_05(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_06(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_07(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_08(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_09(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_10(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


# Abstraction + Utility functions

STAGE_IMPLEMENTATIONS = {
	"STAGE-01": setup_stage_01,
	"STAGE-02": setup_stage_02,
	"STAGE-03": setup_stage_03,
	"STAGE-04": setup_stage_04,
	"STAGE-05": setup_stage_05,
	"STAGE-06": setup_stage_06,
	"STAGE-07": setup_stage_07,
	"STAGE-08": setup_stage_08,
	"STAGE-09": setup_stage_09,
	"STAGE-10": setup_stage_10,
}


def setup_stage(stage: str, candidate: CTFCandidate) -> tuple[str, dict[str, str]]:
	if stage not in STAGE_IMPLEMENTATIONS:
		frappe.throw(f"Stage {stage} not implemented")
	flag = generate_flag()
	variables = STAGE_IMPLEMENTATIONS[stage](candidate, flag)
	return flag, variables
