"""
Script to add empty option to all Select fields in MT Inspection
Run via: bench execute alhoty.fixtures.update_select_fields.add_empty_options
"""

import frappe


def add_empty_options():
	"""Add empty first option to all Select fields"""
	print("\nUpdating MT Inspection Select fields...")
	
	# Get the doctype
	doc = frappe.get_doc("DocType", "MT Inspection")
	
	# List of Select fields to update
	select_fields = [
		"mt_variant",
		"magnetizing_technique",
		"type",
		"examination_medium",
		"lifting_power",
		"particle_application",
		"calibrated_leg_space",
		"excess_particle_removal",
		"demagnetization",
		"acceptance_criteria",
		"examination_medium_manufacturer",
		"examination_medium_batch_no",
		"contrast_paint_manufacturer",
		"contrast_paint_batch_no",
		"solvent_cleaner_manufacturer",
		"solvent_cleaner_batch_no",
		"surface_condition",
		"type_of_weld",
		"lighting_equipment",
		"material_form",
		"magnetic_field_before",
		"magnetic_field_after",
		"post_cleaned"
	]
	
	updated_count = 0
	
	for field in doc.fields:
		if field.fieldname in select_fields and field.fieldtype == "Select":
			# Check if options already start with empty line
			if field.options and not field.options.startswith("\n"):
				# Add empty option at the beginning
				field.options = "\n" + field.options
				updated_count += 1
				print(f"  ✓ Updated {field.fieldname}")
	
	# Save the doctype
	doc.save()
	frappe.db.commit()
	
	print(f"\n✓ Updated {updated_count} Select fields")
	print("All Select fields now have empty first option\n")


if __name__ == "__main__":
	add_empty_options()
