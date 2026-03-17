frappe.ui.form.on('MT Inspection', {

	refresh: function(frm) {
		render_sig_seal_preview(frm);

		if (!frm.is_new()) {
			frm.add_custom_button(__('Export Report'), function() {
				window.open(
					'/api/method/alhoty.report_api.download_mt_report?docname=' +
					encodeURIComponent(frm.docname)
				);
			});
		}
	},

	// ── Contrast Paint toggle ─────────────────────────────────────────
	use_contrast_paint: function(frm) {
		if (!frm.doc.use_contrast_paint) {
			frm.set_value('contrast_paint_manufacturer', '');
			frm.set_value('contrast_paint_batch_no', '');
		}
	},

	// ── Electronic Signature ──────────────────────────────────────────
	include_signature: function(frm) {
		if (frm.doc.include_signature) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'User',
					filters: { name: frappe.session.user },
					fieldname: ['signature_image', 'full_name']
				},
				callback: function(r) {
					if (r.message && r.message.signature_image) {
						frm.set_value('inspector_signature', r.message.signature_image);
						frm.set_value('signed_by', r.message.full_name);
						frm.set_value('signed_on', frappe.datetime.now_datetime());
						render_sig_seal_preview(frm);
					} else {
						frappe.msgprint(__('Please upload your signature in your User Profile first.'));
						frm.set_value('include_signature', 0);
					}
				}
			});
		} else {
			frm.set_value('inspector_signature', '');
			frm.set_value('signed_by', '');
			frm.set_value('signed_on', '');
			render_sig_seal_preview(frm);
		}
	},

	// ── Seal ─────────────────────────────────────────────────────────
	include_seal: function(frm) {
		if (frm.doc.include_seal) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'User',
					filters: { name: frappe.session.user },
					fieldname: ['seal_image']
				},
				callback: function(r) {
					if (r.message && r.message.seal_image) {
						frm.set_value('inspector_seal', r.message.seal_image);
						render_sig_seal_preview(frm);
					} else {
						frappe.msgprint(__('Please upload your seal image in your User Profile first.'));
						frm.set_value('include_seal', 0);
					}
				}
			});
		} else {
			frm.set_value('inspector_seal', '');
			render_sig_seal_preview(frm);
		}
	}
});

// ── Signature & Seal Preview Card ────────────────────────────────────
function render_sig_seal_preview(frm) {
	if (!frm.fields_dict.signature_seal_preview) return;

	const $wrapper = frm.fields_dict.signature_seal_preview.$wrapper;
	$wrapper.empty();

	const has_sig  = frm.doc.include_signature && frm.doc.inspector_signature;
	const has_seal = frm.doc.include_seal && frm.doc.inspector_seal;

	if (!has_sig && !has_seal) return;

	const sig_html = has_sig ? `
		<div class="ndt-preview-item">
			<img src="${frm.doc.inspector_signature}" alt="Signature" class="ndt-preview-img">
			<div class="ndt-preview-label">Inspector Signature</div>
			<div class="ndt-preview-name">${frm.doc.signed_by || ''}</div>
		</div>` : '';

	const seal_html = has_seal ? `
		<div class="ndt-preview-item">
			<img src="${frm.doc.inspector_seal}" alt="Seal" class="ndt-preview-img ndt-preview-img--seal">
			<div class="ndt-preview-label">Inspector Seal</div>
		</div>` : '';

	$wrapper.html(`
		<div class="ndt-sig-seal-card">
			<div class="ndt-sig-seal-header">
				<svg class="icon icon-xs" style="margin-right:6px"><use href="#icon-printer"></use></svg>
				Print Preview — will appear on exported report
			</div>
			<div class="ndt-sig-seal-body">
				${sig_html}
				${seal_html}
			</div>
		</div>
	`);
}
