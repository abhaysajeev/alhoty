app_name = "alhoty"
app_title = "AL HOTY"
app_publisher = "abhay"
app_description = "NDT Web app"
app_email = "abhaysajeev32@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "alhoty",
# 		"logo": "/assets/alhoty/logo.png",
# 		"title": "AL HOTY",
# 		"route": "/alhoty",
# 		"has_permission": "alhoty.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "alhoty.bundle.css",
    "/assets/alhoty/css/alhoty_theme.css",
]
app_include_js = "/assets/alhoty/js/navbar_override.js"

# include js, css files in header of web template
# web_include_css = "/assets/alhoty/css/alhoty.css"
# web_include_js = "/assets/alhoty/js/alhoty.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "alhoty/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "User": "public/js/user.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "alhoty/public/icons.svg"

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

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": "alhoty.utils.jinja_methods",
}

# Installation
# ------------

# before_install = "alhoty.install.before_install"
# after_install = "alhoty.install.after_install"

# Fixtures
# --------
# Export fixtures for automatic installation
fixtures = [
    # Roles required for doctype permissions
    {"dt": "Role", "filters": [["role_name", "in", ["NDT Inspector", "NDT Reviewer"]]]},
    # Custom fields on User for inspector e-signature and seal on PDFs
    {"dt": "Custom Field", "filters": [["dt", "=", "User"], ["fieldname", "in", ["signature_image", "seal_image"]]]},
    # MT Inspection PDF output template
    {"dt": "Print Format", "filters": [["doc_type", "=", "MT Inspection"]]},
    # Naming series: WO-.YYYY.- and MTI-.YYYY.-
    {"dt": "Property Setter", "filters": [["doc_type", "in", ["Work Order", "MT Inspection"]]]},
    # KPI cards shown on the NDT Portal workspace
    {"dt": "Number Card", "filters": [["name", "in", [
        "Active Work Orders", "Completed This Month", "Equipment Due Calibration",
        "Pending Approvals", "Pending Inspections", "Rejected Joints",
        "Total Branches", "Total MT Reports",
    ]]]},
    # Dashboard widgets — workspaces are blank without these
    {"dt": "Custom HTML Block", "filters": [["name", "in", ["MT Branch Inspection", "NDT Analytics Dashboard"]]]},
]

# Uninstallation
# ------------

# before_uninstall = "alhoty.uninstall.before_uninstall"
# after_uninstall = "alhoty.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "alhoty.utils.before_app_install"
# after_app_install = "alhoty.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "alhoty.utils.before_app_uninstall"
# after_app_uninstall = "alhoty.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "alhoty.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

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
# 		"alhoty.tasks.all"
# 	],
# 	"daily": [
# 		"alhoty.tasks.daily"
# 	],
# 	"hourly": [
# 		"alhoty.tasks.hourly"
# 	],
# 	"weekly": [
# 		"alhoty.tasks.weekly"
# 	],
# 	"monthly": [
# 		"alhoty.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "alhoty.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "alhoty.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "alhoty.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["alhoty.utils.before_request"]
# after_request = ["alhoty.utils.after_request"]

# Job Events
# ----------
# before_job = ["alhoty.utils.before_job"]
# after_job = ["alhoty.utils.after_job"]

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
# 	"alhoty.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

