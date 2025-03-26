import os

import frappe
from frappe.rate_limiter import rate_limit
from frappe.utils.caching import site_cache


def generate_otp() -> str:
	if frappe.conf.developer_mode and frappe.local.dev_server:
		return "999999"
	return str(int.from_bytes(os.urandom(6), byteorder="big") % 900000 + 100000)


def generate_flag() -> str:
	return "FLAG{" + frappe.generate_hash(length=20) + "}"


def render_template(template: str, context=None):
	if not context:
		context = {}
	jenv = get_jenv()
	template = jenv.from_string(template)
	template.globals = {}
	jenv.globals = {}
	jenv.filters = {}
	try:
		return template.render(**context)
	except Exception as e:
		return "Error: " + str(e)


def get_jenv():
	if jenv := getattr(frappe.local, "jenv", None):
		return jenv
	frappe.local.jenv = _get_jenv()
	return frappe.local.jenv


@site_cache(ttl=10 * 60, maxsize=4)
def _get_jenv():
	from frappe.utils.safe_exec import UNSAFE_ATTRIBUTES
	from jinja2 import DebugUndefined
	from jinja2.sandbox import SandboxedEnvironment

	UNSAFE_ATTRIBUTES = UNSAFE_ATTRIBUTES - {"format", "format_map"}

	class FrappeSandboxedEnvironment(SandboxedEnvironment):
		def is_safe_attribute(self, obj, attr, *args, **kwargs):
			if attr in UNSAFE_ATTRIBUTES:
				return False

			return super().is_safe_attribute(obj, attr, *args, **kwargs)

	return FrappeSandboxedEnvironment(undefined=DebugUndefined)


def apply_global_rate_limit():
	"""Apply a global rate limit of ~1000 req/minute.

	This is just added to
	- avoid DDOS
	- slow down OTP cracking stage (which requires enumerating ~9000 values)
	"""
	frappe.form_dict._user = frappe.session.user
	limiter(frappe.session.user)
	frappe.form_dict.pop("_user", None)




@rate_limit(key="_user", ip_based=False, limit=300, seconds=60)
def limiter(_user: str):
	# This function doesn't need to do anything.
	pass
