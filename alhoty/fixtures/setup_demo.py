"""
Setup script for AL HOTY NDT Demo
Run this via bench console:
    bench --site [your-site] console
    >>> exec(open('apps/alhoty/alhoty/fixtures/setup_demo.py').read())
"""

import frappe
from frappe import _


def enable_developer_mode():
	"""Temporarily enable developer mode for doctype updates"""
	print("Enabling developer mode...")
	try:
		frappe.conf.developer_mode = 1
		print("  ✓ Developer mode enabled")
	except Exception as e:
		print(f"  ⚠ Could not enable developer mode: {str(e)}")


def check_doctypes_installed():
	"""Check if required doctypes are installed"""
	print("Checking doctypes installation...")
	
	required_doctypes = [
		"Branch Master",
		"Client Master",
		"Project Master", 
		"Equipment Master",
		"Material Master",
		"Work Order",
		"MT Inspection",
		"MT Inspection Result"
	]
	
	missing = []
	for dt in required_doctypes:
		if not frappe.db.exists("DocType", dt):
			missing.append(dt)
	
	if missing:
		print("\n" + "!"*60)
		print("ERROR: Doctypes not installed in database!")
		print("!"*60)
		print("\nMissing doctypes:")
		for dt in missing:
			print(f"  - {dt}")
		print("\nPlease run this command first:")
		print("  bench --site [your-site] migrate")
		print("\nThen run this setup script again.")
		print("="*60 + "\n")
		raise Exception("Doctypes not installed. Run 'bench migrate' first.")
	
	print("  ✓ All doctypes installed\n")


def setup_demo():
	"""Main setup function"""
	print("\n" + "="*60)
	print("AL HOTY NDT Demo Setup")
	print("="*60 + "\n")
	
	frappe.flags.in_install = True
	
	try:
		# 0. Enable developer mode temporarily
		enable_developer_mode()
		
		# 1. Check if doctypes exist, if not prompt to migrate
		check_doctypes_installed()
		
		# 2. Create Roles
		create_roles()
		
		# 3. Create Custom Field for User signature
		create_user_signature_field()
		
		# 4. Create Test Users
		create_test_users()
		
		# 5. Load Branch Master data
		load_branch_master()
		
		# 6. Load Client Master data
		load_client_master()
		
		# 7. Load Project Master data
		load_project_master()
		
		# 8. Load Equipment Master data
		load_equipment_master()
		
		# 9. Create Workflow
		create_workflow()
		
		# 10. Create Print Format
		create_print_format()
		
		# 11. Setup naming series
		setup_naming_series()
		
		# 12. Update Select fields with empty options
		update_select_fields()
		
		frappe.db.commit()
		
		print("\n" + "="*60)
		print("✓ Setup Complete!")
		print("="*60)
		print("\nTest Users Created:")
		print("  Inspector: inspector@alhoty.com / password: Inspector@2024!")
		print("  Reviewer:  reviewer@alhoty.com / password: Reviewer@2024!")
		print("\nDemo Data Loaded:")
		print("  5 Branches (Riyadh, Dammam, Jeddah, Jubail, Yanbu)")
		print("  3 Clients (Saudi Aramco, SABIC, SEC)")
		print("  3 Projects")
		print("  7 Equipment records (5 in Dammam, 1 in Riyadh, 1 in Jeddah)")
		print("\nHierarchy:")
		print("  Branch → Equipment")
		print("  Branch → Work Order → MT Inspection")
		print("\nNext Steps:")
		print("  1. Run: bench migrate")
		print("  2. Login as inspector@alhoty.com")
		print("  3. Go to User Profile → Upload signature image")
		print("  4. Create Work Order (select Branch, Client, Project)")
		print("  5. Create MT Inspection from Work Order")
		print("="*60 + "\n")
		
	except Exception as e:
		frappe.db.rollback()
		print(f"\n✗ Error during setup: {str(e)}")
		import traceback
		traceback.print_exc()
	finally:
		frappe.flags.in_install = False


def create_roles():
	"""Create NDT Inspector and Reviewer roles"""
	print("Creating roles...")
	
	roles = [
		{
			"doctype": "Role",
			"role_name": "NDT Inspector",
			"desk_access": 1
		},
		{
			"doctype": "Role",
			"role_name": "NDT Reviewer",
			"desk_access": 1
		}
	]
	
	for role_data in roles:
		if not frappe.db.exists("Role", role_data["role_name"]):
			role = frappe.get_doc(role_data)
			role.insert(ignore_permissions=True)
			print(f"  ✓ Created role: {role_data['role_name']}")
		else:
			print(f"  - Role already exists: {role_data['role_name']}")


def create_user_signature_field():
	"""Add signature_image custom field to User doctype"""
	print("\nCreating User signature custom field...")
	
	if not frappe.db.exists("Custom Field", "User-signature_image"):
		custom_field = frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "User",
			"fieldname": "signature_image",
			"label": "Signature",
			"fieldtype": "Attach Image",
			"insert_after": "user_image",
			"description": "Upload your signature image here. Used on inspection report PDFs when electronic signature is enabled."
		})
		custom_field.insert(ignore_permissions=True)
		print("  ✓ Created User signature field")
	else:
		print("  - User signature field already exists")


def create_test_users():
	"""Create test inspector and reviewer users"""
	print("\nCreating test users...")
	
	users = [
		{
			"email": "inspector@alhoty.com",
			"first_name": "Test",
			"last_name": "Inspector",
			"roles": ["NDT Inspector"],
			"password": "Inspector@2024!"
		},
		{
			"email": "reviewer@alhoty.com",
			"first_name": "Test",
			"last_name": "Reviewer",
			"roles": ["NDT Reviewer"],
			"password": "Reviewer@2024!"
		}
	]
	
	for user_data in users:
		if not frappe.db.exists("User", user_data["email"]):
			user = frappe.get_doc({
				"doctype": "User",
				"email": user_data["email"],
				"first_name": user_data["first_name"],
				"last_name": user_data["last_name"],
				"send_welcome_email": 0,
				"new_password": user_data["password"]
			})
			user.insert(ignore_permissions=True)
			
			# Add roles
			for role in user_data["roles"]:
				user.add_roles(role)
			
			print(f"  ✓ Created user: {user_data['email']}")
		else:
			print(f"  - User already exists: {user_data['email']}")


def load_equipment_master():
	"""Load demo equipment data"""
	print("\nLoading Equipment Master data...")
	
	equipment_data = [
		{
			"branch": "Dammam Branch",
			"serial_no": "27418",
			"manufacturer": "PARKER",
			"equipment_type": "Yoke"
		},
		{
			"branch": "Dammam Branch",
			"serial_no": "1947904",
			"manufacturer": "SPECTROLINE",
			"equipment_type": "UV Light"
		},
		{
			"branch": "Dammam Branch",
			"serial_no": "1098116",
			"manufacturer": "SPECTRONICS CORP",
			"equipment_type": "Light Meter"
		},
		{
			"branch": "Dammam Branch",
			"serial_no": "2379",
			"manufacturer": "R.BANNIS Co",
			"equipment_type": "Gauss Meter"
		},
		{
			"branch": "Dammam Branch",
			"serial_no": "20120700",
			"manufacturer": "SMART SENSOR",
			"equipment_type": "Thermometer"
		},
		{
			"branch": "Riyadh Branch",
			"serial_no": "RYD-001",
			"manufacturer": "PARKER",
			"equipment_type": "Yoke"
		},
		{
			"branch": "Jeddah Branch",
			"serial_no": "JED-001",
			"manufacturer": "MAGNAFLUX",
			"equipment_type": "Yoke"
		}
	]
	
	for equip in equipment_data:
		if not frappe.db.exists("Equipment Master", equip["serial_no"]):
			doc = frappe.get_doc({
				"doctype": "Equipment Master",
				**equip
			})
			doc.insert(ignore_permissions=True)
			print(f"  ✓ Created equipment: {equip['serial_no']} - {equip['manufacturer']} ({equip['branch']})")
		else:
			print(f"  - Equipment already exists: {equip['serial_no']}")



def load_branch_master():
	"""Load demo branch data"""
	print("\nLoading Branch Master data...")
	
	branches = [
		{
			"branch_name": "Riyadh Branch",
			"branch_code": "RYD",
			"location": "Riyadh",
			"branch_manager": "Eng. Abdullah Al-Rashid",
			"contact_number": "+966-11-234-5678",
			"email": "riyadh@alhoty.com"
		},
		{
			"branch_name": "Dammam Branch",
			"branch_code": "DMM",
			"location": "Dammam",
			"branch_manager": "Eng. Mohammed Al-Qahtani",
			"contact_number": "+966-13-345-6789",
			"email": "dammam@alhoty.com"
		},
		{
			"branch_name": "Jeddah Branch",
			"branch_code": "JED",
			"location": "Jeddah",
			"branch_manager": "Eng. Khalid Al-Mutairi",
			"contact_number": "+966-12-456-7890",
			"email": "jeddah@alhoty.com"
		},
		{
			"branch_name": "Jubail Branch",
			"branch_code": "JUB",
			"location": "Jubail",
			"branch_manager": "Eng. Fahad Al-Dosari",
			"contact_number": "+966-13-567-8901",
			"email": "jubail@alhoty.com"
		},
		{
			"branch_name": "Yanbu Branch",
			"branch_code": "YNB",
			"location": "Yanbu",
			"branch_manager": "Eng. Omar Al-Zahrani",
			"contact_number": "+966-14-678-9012",
			"email": "yanbu@alhoty.com"
		}
	]
	
	for branch in branches:
		if not frappe.db.exists("Branch Master", branch["branch_name"]):
			doc = frappe.get_doc({
				"doctype": "Branch Master",
				**branch
			})
			doc.insert(ignore_permissions=True)
			print(f"  ✓ Created branch: {branch['branch_name']}")
		else:
			print(f"  - Branch already exists: {branch['branch_name']}")


def load_client_master():
	"""Load demo client data"""
	print("\nLoading Client Master data...")
	
	clients = [
		{
			"client_name": "Saudi Aramco",
			"client_code": "ARAMCO",
			"contact_person": "Ahmed Al-Rashid",
			"email": "contact@aramco.com",
			"phone": "+966-13-876-0000"
		},
		{
			"client_name": "SABIC",
			"client_code": "SABIC",
			"contact_person": "Mohammed Al-Qahtani",
			"email": "contact@sabic.com",
			"phone": "+966-13-359-0000"
		},
		{
			"client_name": "Saudi Electricity Company",
			"client_code": "SEC",
			"contact_person": "Khalid Al-Mutairi",
			"email": "contact@se.com.sa",
			"phone": "+966-11-253-5555"
		}
	]
	
	for client in clients:
		if not frappe.db.exists("Client Master", client["client_name"]):
			doc = frappe.get_doc({
				"doctype": "Client Master",
				**client
			})
			doc.insert(ignore_permissions=True)
			print(f"  ✓ Created client: {client['client_name']}")
		else:
			print(f"  - Client already exists: {client['client_name']}")


def load_project_master():
	"""Load demo project data"""
	print("\nLoading Project Master data...")
	
	projects = [
		{
			"project_name": "Ras Tanura Refinery Expansion",
			"project_code": "RT-EXP-2024",
			"client": "Saudi Aramco",
			"location": "Ras Tanura, Saudi Arabia",
			"project_manager": "Eng. Abdullah Hassan"
		},
		{
			"project_name": "Jubail Petrochemical Complex",
			"project_code": "JPC-2024",
			"client": "SABIC",
			"location": "Jubail Industrial City, Saudi Arabia",
			"project_manager": "Eng. Fahad Al-Dosari"
		},
		{
			"project_name": "Yanbu Power Plant Maintenance",
			"project_code": "YPP-MAINT-2024",
			"client": "Saudi Electricity Company",
			"location": "Yanbu, Saudi Arabia",
			"project_manager": "Eng. Omar Al-Zahrani"
		}
	]
	
	for project in projects:
		if not frappe.db.exists("Project Master", project["project_name"]):
			doc = frappe.get_doc({
				"doctype": "Project Master",
				**project
			})
			doc.insert(ignore_permissions=True)
			print(f"  ✓ Created project: {project['project_name']}")
		else:
			print(f"  - Project already exists: {project['project_name']}")


def create_workflow():
	"""Create MT Inspection approval workflow"""
	print("\nCreating workflow...")
	
	workflow_name = "MT Inspection Approval"
	
	if frappe.db.exists("Workflow", workflow_name):
		print(f"  - Workflow already exists: {workflow_name}")
		return
	
	try:
		workflow = frappe.get_doc({
			"doctype": "Workflow",
			"workflow_name": workflow_name,
			"document_type": "MT Inspection",
			"is_active": 1,
			"send_email_alert": 0,
			"workflow_state_field": "workflow_state"
		})
		
		# Add states
		workflow.append("states", {
			"state": "Draft",
			"doc_status": "0",
			"allow_edit": "NDT Inspector"
		})
		workflow.append("states", {
			"state": "Submitted for Review",
			"doc_status": "0",
			"allow_edit": "NDT Reviewer"
		})
		workflow.append("states", {
			"state": "Approved",
			"doc_status": "1",
			"allow_edit": ""
		})
		workflow.append("states", {
			"state": "Rejected",
			"doc_status": "0",
			"allow_edit": "NDT Inspector"
		})
		
		# Add transitions
		workflow.append("transitions", {
			"state": "Draft",
			"action": "Submit for Review",
			"next_state": "Submitted for Review",
			"allowed": "NDT Inspector",
			"allow_self_approval": 0
		})
		workflow.append("transitions", {
			"state": "Submitted for Review",
			"action": "Approve",
			"next_state": "Approved",
			"allowed": "NDT Reviewer",
			"allow_self_approval": 0
		})
		workflow.append("transitions", {
			"state": "Submitted for Review",
			"action": "Reject",
			"next_state": "Rejected",
			"allowed": "NDT Reviewer",
			"allow_self_approval": 0
		})
		workflow.append("transitions", {
			"state": "Rejected",
			"action": "Resubmit",
			"next_state": "Submitted for Review",
			"allowed": "NDT Inspector",
			"allow_self_approval": 0
		})
		
		workflow.insert(ignore_permissions=True)
		print(f"  ✓ Created workflow: {workflow_name}")
	except Exception as e:
		print(f"  ⚠ Workflow creation failed: {str(e)}")
		print(f"  → You can create the workflow manually via UI later")


def create_print_format():
	"""Create blank print format for MT Inspection"""
	print("\nCreating print format...")
	
	print_format_name = "MT Inspection Report"
	
	if frappe.db.exists("Print Format", print_format_name):
		print(f"  - Print format already exists: {print_format_name}")
		return
	
	print_format = frappe.get_doc({
		"doctype": "Print Format",
		"name": print_format_name,
		"doc_type": "MT Inspection",
		"standard": "No",
		"html": """
<div class="print-format">
	<h2>MT Inspection Report</h2>
	<p><strong>Report No:</strong> {{ doc.report_no }}</p>
	<p><strong>Work Order:</strong> {{ doc.work_order }}</p>
	<p><strong>Client:</strong> {{ doc.client }}</p>
	
	<!-- Add your custom Jinja2 template here -->
	
	{% if doc.include_signature %}
	<div class="signature-block">
		<img src="{{ doc.inspector_signature }}" style="max-width: 200px;" />
		<p><strong>Signed By:</strong> {{ doc.signed_by }}</p>
		<p><strong>Signed On:</strong> {{ doc.signed_on }}</p>
	</div>
	{% endif %}
</div>
"""
	})
	print_format.insert(ignore_permissions=True)
	print(f"  ✓ Created print format: {print_format_name}")


def setup_naming_series():
	"""Setup naming series for Work Order and MT Inspection"""
	print("\nSetting up naming series...")
	
	# Work Order naming series
	if not frappe.db.exists("Property Setter", "Work Order-naming_series-options"):
		frappe.get_doc({
			"doctype": "Property Setter",
			"doctype_or_field": "DocField",
			"doc_type": "Work Order",
			"field_name": "work_order_no",
			"property": "options",
			"value": "WO-.YYYY.-.####",
			"property_type": "Text"
		}).insert(ignore_permissions=True)
		print("  ✓ Set Work Order naming series")
	
	# MT Inspection naming series  
	if not frappe.db.exists("Property Setter", "MT Inspection-naming_series-options"):
		frappe.get_doc({
			"doctype": "Property Setter",
			"doctype_or_field": "DocField",
			"doc_type": "MT Inspection",
			"field_name": "naming_series",
			"property": "options",
			"value": "MTI-.YYYY.-.####",
			"property_type": "Text"
		}).insert(ignore_permissions=True)
		print("  ✓ Set MT Inspection naming series")


# Run setup
if __name__ == "__main__":
	setup_demo()
else:
	# When executed via exec()
	setup_demo()


def update_select_fields():
	"""Add empty first option to all Select fields in MT Inspection"""
	print("\nUpdating Select fields with empty options...")
	
	try:
		doc = frappe.get_doc("DocType", "MT Inspection")
		
		select_fields = [
			"mt_variant", "magnetizing_technique", "type", "examination_medium",
			"lifting_power", "particle_application", "calibrated_leg_space",
			"excess_particle_removal", "demagnetization", "acceptance_criteria",
			"examination_medium_manufacturer", "examination_medium_batch_no",
			"contrast_paint_manufacturer", "contrast_paint_batch_no",
			"solvent_cleaner_manufacturer", "solvent_cleaner_batch_no",
			"surface_condition", "type_of_weld", "lighting_equipment",
			"material_form", "magnetic_field_before", "magnetic_field_after",
			"post_cleaned"
		]
		
		updated_count = 0
		for field in doc.fields:
			if field.fieldname in select_fields and field.fieldtype == "Select":
				if field.options and not field.options.startswith("\n"):
					field.options = "\n" + field.options
					updated_count += 1
		
		doc.save()
		print(f"  ✓ Updated {updated_count} Select fields with empty option")
	except Exception as e:
		print(f"  ⚠ Could not update Select fields: {str(e)}")
