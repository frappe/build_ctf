import os

import frappe


def generate_otp() -> str:
	return str(int.from_bytes(os.urandom(6), byteorder="big") % 900000 + 100000)


def generate_flag() -> str:
	return "FLAG{" + frappe.generate_hash(length=20) + "}"
