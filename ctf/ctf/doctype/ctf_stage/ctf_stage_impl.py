# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

from __future__ import annotations

from typing import TYPE_CHECKING

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
			"name": f"STAGE-01-{candidate.name}",
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

	return {"FLAG_PAGE_URL": f"/stage-01/{api_method}"}


# Abstraction + Utility functions

STAGE_IMPLEMENTATIONS = {
	"STAGE-01": setup_stage_01,
}


def setup_stage(stage: str, candidate: CTFCandidate) -> tuple[str, dict[str, str]]:
	if stage not in STAGE_IMPLEMENTATIONS:
		frappe.throw(f"Stage {stage} not implemented")
	flag = generate_flag()
	variables = STAGE_IMPLEMENTATIONS[stage](candidate, flag)
	return flag, variables
