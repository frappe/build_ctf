app_name = "ctf"
app_title = "Ctf"
app_publisher = "Frappe"
app_description = "Frappe Build CTF"
app_email = "support@frappe.io"
app_license = "apache-2.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ctf",
# 		"logo": "/assets/ctf/logo.png",
# 		"title": "Ctf",
# 		"route": "/ctf",
# 		"has_permission": "ctf.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ctf/css/ctf.css"
# app_include_js = "/assets/ctf/js/ctf.js"

# include js, css files in header of web template
# web_include_css = "/assets/ctf/css/ctf.css"
# web_include_js = "/assets/ctf/js/ctf.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ctf/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ctf/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ctf.utils.jinja_methods",
# 	"filters": "ctf.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ctf.install.before_install"
# after_install = "ctf.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ctf.uninstall.before_uninstall"
# after_uninstall = "ctf.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ctf.utils.before_app_install"
# after_app_install = "ctf.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ctf.utils.before_app_uninstall"
# after_app_uninstall = "ctf.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ctf.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"User": "ctf.ctf.doctype.ctf_candidate.ctf_candidate.user_query",
}

has_permission = {
	"File": "ctf.ctf.doctype.ctf_candidate.ctf_candidate.has_file_permission",
}

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ctf.tasks.all"
# 	],
# 	"daily": [
# 		"ctf.tasks.daily"
# 	],
# 	"hourly": [
# 		"ctf.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ctf.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ctf.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ctf.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ctf.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ctf.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
before_request = ["ctf.utils.apply_global_rate_limit"]
# after_request = ["ctf.utils.after_request"]

# Job Events
# ----------
# before_job = ["ctf.utils.before_job"]
# after_job = ["ctf.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ctf.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = ["Web Page", "CTF Stage", "Stat Counter"]

persistent_cache_keys = [
	"stage_06_verification_code*",
]

website_route_rules = [{"from_route": "/frontend/<path:app_path>", "to_route": "frontend"}]

website_redirects = [
	{
		"source": "/",
		"target": "/frontend",
	}
]
