// user.js — User form customizations for alhoty app
// Forces private upload and adds crop guidance for signature/seal fields.

frappe.ui.form.on('User', {
	refresh: function(frm) {
		['signature_image', 'seal_image'].forEach(function(fieldname) {
			var control = frm.fields_dict[fieldname];
			if (!control || control._alhoty_patched) return;

			// Patch set_upload_options so every upload for these fields
			// defaults to private — override happens after Frappe's own logic
			// so it wins regardless of system-level make_attachments_public setting.
			var orig = control.set_upload_options.bind(control);
			control.set_upload_options = function() {
				orig();
				this.upload_options.make_attachments_public = 0;
			};

			control._alhoty_patched = true;
		});
	}
});
