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
		self.submitted_flag = flag.strip()
		self.correct = self.correct_flag == flag
		self.points = frappe.get_value("CTF Stage", self.stage, "points") if self.correct else 0
		self.save()
