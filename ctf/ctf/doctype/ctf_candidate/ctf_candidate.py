# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import json

import frappe
from frappe.model.document import Document

from ctf.ctf.doctype.ctf_stage.ctf_stage_impl import setup_stage


class CTFCandidate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from ctf.ctf.doctype.ctf_candidate_stage.ctf_candidate_stage import CTFCandidateStage

		setup_completed: DF.Check
		stages: DF.Table[CTFCandidateStage]
		user: DF.Link
	# end: auto-generated types

	def after_insert(self):
		self.setup_stages()

	@frappe.whitelist()
	def setup_stages(self):
		frappe.enqueue_doc("CTF Candidate", self.name, "_setup_stages", enqueue_after_commit=True)

	def _setup_stages(self):
		stages = frappe.get_all("CTF Stage", pluck="name", order_by="name")

		for stage in stages:
			flag, variables = setup_stage(stage, self)
			self.append(
				"stages",
				{
					"stage": stage,
					"correct_flag": flag,
					"variables": json.dumps(variables),
				},
			)

		self.setup_completed = 1
		self.save()

	@frappe.whitelist()
	def cleanup_stages(self):
		# server script cleanup
		frappe.delete_doc(
			"Server Script", f"stage-01-{self.name}", delete_permanently=True, ignore_missing=True
		)
		# delete all stages
		self.stages = []
		self.setup_completed = 0
		self.save()


def has_file_permission(doc, ptype, user):
	if frappe.session.data.user_type == "System User":
		return True
	if ptype != "read":
		return False
	return doc.owner == user
