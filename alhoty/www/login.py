# login.py — Custom login page controller for alhoty app
#
# Frappe loads this automatically when a browser visits /login.
# It must NOT import from ndt (NDT is transparent middleware).
# All NDT gating is enforced via hooks — this file only controls
# what the login page template renders.

import frappe


def get_context(context):
	"""
	Populate Jinja context for login.html.

	Frappe calls this before rendering www/login.html.
	If the user is already logged in, redirect straight to /app.
	"""
	# If already authenticated, skip login
	if frappe.session and frappe.session.user and frappe.session.user != "Guest":
		frappe.local.flags.redirect_location = "/app"
		raise frappe.Redirect

	# Pass site-level context
	context.no_header = True          # suppress default Frappe navbar/header
	context.no_footer = True          # suppress default Frappe footer
	context.no_sidebar = True         # suppress any sidebar injection
	context.csrf_token = frappe.sessions.get_csrf_token()
	context.title = "Login — AlHoty Stanger NDT Portal"
