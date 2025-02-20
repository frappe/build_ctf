# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

from __future__ import annotations

from typing import TYPE_CHECKING

import frappe

if TYPE_CHECKING:
	from ctf.ctf.doctype.ctf_candidate.ctf_candidate import CTFCandidate


def setup_stage_01(candidate: CTFCandidate) -> tuple[str, dict[str, str]]:
	pass


"""
Stage Implementation Function Signature -
def (candidate: CTFCandidate) -> tuple[str, dict[str, str]]

Return Values:
 - First element -> Generated flag
 - Second element -> Variables dict to insert in description of the stage
"""

STAGE_IMPLEMENTATIONS = {
	"STAGE-01": setup_stage_01,
}
