# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from ctf.utils import generate_otp


class AccountRequest(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		completed: DF.Check
		email: DF.Data
		first_name: DF.Data
		last_name: DF.Data
		verification_code: DF.Data | None
	# end: auto-generated types

	def validate(self):
		# validate no user exists with this email
		if self.is_new() and frappe.db.exists("User", self.email):
			frappe.throw("You already have an account with this email. Please login.")
		# validate name
		if not self.first_name or not self.last_name:
			frappe.throw("Please provide your first and last name.")

	def after_insert(self):
		self.send_otp()

	def send_otp(self):
		self.verification_code = generate_otp()

		self.save()
		send_verification_mail(self.email, self.verification_code)

	def verify_code_and_login(self, code: str):
		if self.completed or frappe.db.exists("User", self.email):
			frappe.throw("You already completed sign up. Please login.")

		if not self.verification_code or self.verification_code != code:
			frappe.throw("Invalid verification code")

		session_user = frappe.session.user
		try:
			frappe.set_user("Administrator")
			# create the user
			user = frappe.get_doc(
				{
					"doctype": "User",
					"email": self.email,
					"first_name": self.first_name,
					"last_name": self.last_name,
					"send_welcome_email": 0,
				}
			).insert()
			# create ctf candidate
			frappe.get_doc(
				{
					"doctype": "CTF Candidate",
					"user": user.name,
				}
			).insert()
			# mark ar as completed
			self.completed = 1
			self.save()
			# login the user
			frappe.local.login_manager.login_as(user.name)
		except Exception:
			frappe.set_user(session_user)
			raise

	@staticmethod
	def register(email: str, first_name: str, last_name: str) -> "AccountRequest":
		if not frappe.get_value("CTF Settings", None, "registration_enabled"):
			frappe.throw("Registration is not yet open. Stay tuned!")
		return frappe.get_doc(
			{
				"doctype": "Account Request",
				"email": email,
				"first_name": first_name,
				"last_name": last_name,
			}
		).insert(ignore_permissions=True)


def send_verification_mail(email: str, code: str):
	if frappe.conf.developer_mode and frappe.local.dev_server:
		print("Sending verification mail to", email)
		print("Verification code:", code)
		return
	# TODO send verification mail
