# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import json
import typing

import frappe
from frappe.model.document import Document


class CTFStage(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.MarkdownEditor
		points: DF.Int
		title: DF.Data
	# end: auto-generated types

	pass
