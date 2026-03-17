import base64
import os

import frappe


def get_file_base64(file_url):
	"""Return a base64 data-URL for a file so wkhtmltopdf can embed it.

	Works for both public (/files/...) and private (/private/files/...) files.
	Called from the MT Inspection Report Jinja print template via the
	jinja_methods() hook registered in hooks.py.
	"""
	if not file_url:
		return ""

	try:
		site_path = frappe.get_site_path()

		if file_url.startswith("/private/files/"):
			file_path = os.path.join(site_path, "private", "files", os.path.basename(file_url))
		elif file_url.startswith("/files/"):
			file_path = os.path.join(site_path, "public", "files", os.path.basename(file_url))
		else:
			# External URL or data-URL — return as-is
			return file_url

		if not os.path.exists(file_path):
			return ""

		with open(file_path, "rb") as f:
			data = base64.b64encode(f.read()).decode("utf-8")

		ext = file_url.rsplit(".", 1)[-1].lower() if "." in file_url else "png"
		mime_map = {
			"png": "image/png",
			"jpg": "image/jpeg",
			"jpeg": "image/jpeg",
			"gif": "image/gif",
			"webp": "image/webp",
			"bmp": "image/bmp",
		}
		mime = mime_map.get(ext, "image/png")
		return f"data:{mime};base64,{data}"

	except Exception:
		return ""


def jinja_methods():
	"""Expose custom functions to all Frappe Jinja templates (print formats, etc.)."""
	return {"get_file_base64": get_file_base64}
