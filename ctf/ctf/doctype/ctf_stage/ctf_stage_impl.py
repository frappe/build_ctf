# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

from __future__ import annotations

import codecs
import contextlib
import os
import subprocess
from typing import TYPE_CHECKING

import frappe

from ctf.ctf.doctype.ctf_stage.ctf_stage_assets import (
	get_stage_02_js,
	get_stage_03_js_minified,
	get_stage_08_c_source,
)
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
frappe.response['message'] = "You are on the right path, but a crucial detail escapes you - examine again, and you may yet arrive at the truth."
""",
		}
	).insert()

	return {"FLAG_PAGE_ROUTE": f"/stage-01/{api_method}"}


def setup_stage_02(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	current_user = frappe.session.user
	frappe.set_user(candidate.user)
	try:
		flag_characters = flag.replace("FLAG{", "").replace("}", "")
		file_doc = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": f"stage-02-{candidate.name}.js",
				"content": get_stage_02_js().replace("{{FLAG_CHARACTERS}}", flag_characters),
				"is_private": 1,
			}
		).insert(ignore_permissions=True)
		file_name_without_ext = file_doc.file_name.split(".")[0]
		return {
			"FLAG_PAGE_ROUTE": f"/stage-02/{file_name_without_ext}",
		}
	finally:
		frappe.set_user(current_user)


def setup_stage_03(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	current_user = frappe.session.user
	try:
		frappe.set_user(candidate.user)
		flag_characters = flag.replace("FLAG{", "").replace("}", "")
		hash = frappe.generate_hash(length=10)
		base_file_name = f"stage-03-{candidate.name}-{hash}"
		min_js_file_name = f"{base_file_name}.min.js"
		min_js_content = get_stage_03_js_minified()

		frappe.set_user(candidate.user)

		frappe.get_doc(
			{
				"doctype": "File",
				"file_name": min_js_file_name,
				"content": min_js_content.replace("FLAG_CHARACTERS", flag_characters),
				"is_private": 1,
			}
		).insert(ignore_permissions=True)

		return {
			"FLAG_PAGE_ROUTE": f"/stage-03/{base_file_name}",
		}
	finally:
		frappe.set_user(current_user)


def setup_stage_04(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_05(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	current_user = frappe.session.user
	try:
		frappe.set_user(candidate.user)
		frappe.get_doc(
			{
				"doctype": "File",
				"file_name": "memento.txt",
				"content": f"Remember this: {flag}",
				"is_private": 1,
			}
		).insert(ignore_permissions=True)
	finally:
		frappe.set_user(current_user)
	return {}


def setup_stage_06(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_07(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	return {}


def setup_stage_08(candidate: CTFCandidate, flag: str) -> dict[str, str]:
	flag_characters = flag.replace("FLAG{", "").replace("}", "")
	flag_characters = codecs.encode(flag_characters, "rot13")
	tmp_source_file_name = "/tmp/stage-08-" + frappe.generate_hash(length=30) + ".c"
	with open(tmp_source_file_name, "w") as f:
		f.write(get_stage_08_c_source().replace("FLAG_CHARACTERS", flag_characters))

	tmp_dest_file_name = "/tmp/stage-08-" + frappe.generate_hash(length=30) + ".out"
	subprocess.run(["gcc", tmp_source_file_name, "-o", tmp_dest_file_name], check=True)

	# read and store in file
	with open(tmp_dest_file_name, "rb") as f:
		filecontent = f.read()

	current_user = frappe.session.user

	try:
		frappe.set_user(candidate.user)

		file = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": tmp_dest_file_name.split("/")[-1],
				"content": filecontent,
				"is_private": 1,
			}
		).insert(ignore_permissions=True)
	finally:
		frappe.set_user(current_user)

	with contextlib.suppress(Exception):
		os.remove(tmp_source_file_name)
		os.remove(tmp_dest_file_name)

	return {
		"BINARY_FILE_URL": file.file_url,
	}


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
