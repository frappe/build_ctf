# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CTFCandidateStage(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		correct: DF.Check
		correct_flag: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		points: DF.Int
		stage: DF.Link
		submitted_flag: DF.Data | None
		variables: DF.JSON | None
	# end: auto-generated types

	def submit_flag(self, flag: str):
		if self.correct:
			return

		self.submitted_flag = flag.strip()
		self.correct = self.correct_flag == flag
		points = 0
		if self.correct:
			points = frappe.db.get_value("CTF Stage", self.stage, "points")
			# First one to solve gets 100, 2nd one gets 99 and so on until 50.
			# Then everyone gets 50.
			rank = frappe.db.get_value(self.doctype, {"stage": self.stage, "correct": 1}, "count(*)", for_update=True) or 0
			rank = min(rank, 50)
			points -= rank

		self.points = points
		self.save(ignore_permissions=True)
