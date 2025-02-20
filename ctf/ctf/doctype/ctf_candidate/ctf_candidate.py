# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CTFCandidate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from ctf.ctf.doctype.ctf_candidate_stage.ctf_candidate_stage import CTFCandidateStage

		stages: DF.Table[CTFCandidateStage]
		status: DF.Literal[
			"Registration Pending", "Registration Completed", "Setting Up Stages", "Stages Setup Completed"
		]
		user: DF.Link
	# end: auto-generated types

	pass
