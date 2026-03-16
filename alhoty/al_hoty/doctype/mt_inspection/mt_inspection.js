frappe.ui.form.on('MT Inspection', {
	// Electronic signature handling
	include_signature: function(frm) {
		if (frm.doc.include_signature) {
			// Fetch signature from User profile
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'User',
					filters: { name: frappe.session.user },
					fieldname: ['signature_image', 'full_name']
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('inspector_signature', r.message.signature_image);
						frm.set_value('signed_by', r.message.full_name);
						frm.set_value('signed_on', frappe.datetime.now_datetime());
					} else {
						frappe.msgprint(__('Please upload your signature in your User Profile first.'));
						frm.set_value('include_signature', 0);
					}
				}
			});
		} else {
			// Clear signature fields
			frm.set_value('inspector_signature', '');
			frm.set_value('signed_by', '');
			frm.set_value('signed_on', '');
		}
	}
});
