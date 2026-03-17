import base64
import os

import frappe
from jinja2 import Environment
from frappe.utils.pdf import get_pdf


@frappe.whitelist(allow_guest=True)
def download_mt_report(docname):
	doc = frappe.get_doc("MT Inspection", docname)
	doc.check_permission("read")

	html = _render_html(doc)
	pdf = get_pdf(html, {
		"page-size": "A4",
		"margin-top": "0",
		"margin-bottom": "0",
		"margin-left": "0",
		"margin-right": "0",
		"disable-smart-shrinking": "",
	})

	frappe.response.filename = f"{docname}.pdf"
	frappe.response.filecontent = pdf
	frappe.response.type = "download"


def _file_base64(file_url):
	if not file_url:
		return ""
	try:
		site_path = frappe.get_site_path()
		if file_url.startswith("/private/files/"):
			path = os.path.join(site_path, "private", "files", os.path.basename(file_url))
		elif file_url.startswith("/files/"):
			path = os.path.join(site_path, "public", "files", os.path.basename(file_url))
		else:
			return file_url
		if not os.path.exists(path):
			return ""
		with open(path, "rb") as f:
			data = base64.b64encode(f.read()).decode("utf-8")
		ext = file_url.rsplit(".", 1)[-1].lower() if "." in file_url else "png"
		mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
				"gif": "image/gif", "webp": "image/webp", "bmp": "image/bmp"}.get(ext, "image/png")
		return f"data:{mime};base64,{data}"
	except Exception:
		return ""


def _fmt_date(d):
	if not d:
		return ""
	from frappe.utils import formatdate
	return formatdate(d)


_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Magnetic Particle Examination Report</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: Arial, Helvetica, sans-serif; font-size: 9pt; color: #000; }
  .page {
    width: 100%;
    background: #fff;
    padding: 14mm 16mm 12mm;
  }
  table { width: 100%; border-collapse: collapse; }
  td, th { border: 1px solid #000; padding: 3px 6px; font-size: 8.5pt; vertical-align: middle; }
  .no-border td, .no-border th { border: none; }
  .sec-hdr { font-weight: bold; text-align: center; font-size: 9pt; padding: 4px 6px; background: #e0e0e0; }
  .lbl { font-weight: bold; }
  .val-line { border-bottom: 1px solid #000 !important; border-top: none !important; border-left: none !important; border-right: none !important; }
  .mb { margin-bottom: 7px; }
  @media print {
    body { background: white; }
    .page { margin: 0; page-break-after: always; box-shadow: none; }
  }
</style>
</head>
<body>

<!-- ===================== PAGE 1 ===================== -->
<div class="page">

  <div style="text-align:right; margin-bottom:4px;">
    <table class="no-border" style="width:auto; margin-left:auto;">
      <tr>
        <td style="text-align:right; padding:1px 2px;">Date of Rpt :</td>
        <td style="border-bottom:1px solid #000; min-width:100px; padding:1px 4px;">{{ fmt_date(doc.date_of_report) }}</td>
      </tr>
      <tr>
        <td style="text-align:right; padding:1px 2px;">Date of Test :</td>
        <td style="border-bottom:1px solid #000; padding:1px 4px;">{{ fmt_date(doc.date_of_test) }}</td>
      </tr>
      <tr>
        <td style="text-align:right; padding:1px 2px;">Report No. :</td>
        <td style="border-bottom:1px solid #000; padding:1px 4px;">{{ doc.name }}</td>
      </tr>
      <tr>
        <td style="text-align:right; padding:1px 2px;">Page</td>
        <td style="padding:1px 4px;">1 of 2</td>
      </tr>
    </table>
  </div>

  <div style="text-align:center; font-weight:bold; font-size:12pt; margin: 4px 0 10px;">
    MAGNETIC PARTICLE EXAMINATION REPORT
  </div>

  <table class="no-border mb" style="width:100%;">
    <tr>
      <td style="width:22%; padding:2px 4px;">Client</td>
      <td style="width:2%; padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; padding:2px 6px;">{{ doc.client }}</td>
    </tr>
    <tr>
      <td style="padding:2px 4px;">Project</td>
      <td style="padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; padding:2px 6px;">{{ doc.project_name }}</td>
    </tr>
    <tr>
      <td style="padding:2px 4px;">Location</td>
      <td style="padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; padding:2px 6px;">{{ doc.location }}</td>
    </tr>
    <tr>
      <td style="padding:2px 4px;">Client's Reference</td>
      <td style="padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; padding:2px 6px;">{{ doc.client_reference }}</td>
    </tr>
  </table>

  <table class="mb">
    <tr><td colspan="4" class="sec-hdr">Examination Technique</td></tr>
    <tr>
      <td class="lbl" style="width:26%;">Magnetizing Technique</td>
      <td style="width:24%;">{{ doc.magnetizing_technique }}</td>
      <td class="lbl" style="width:26%;">Procedure No</td>
      <td style="width:24%;">{{ doc.procedure_no }}</td>
    </tr>
    <tr>
      <td class="lbl">Type</td>
      <td>{{ doc.type }}</td>
      <td class="lbl">Examination Medium</td>
      <td>{{ doc.examination_medium }}</td>
    </tr>
    <tr>
      <td class="lbl">Lifting Power</td>
      <td>{{ doc.lifting_power }}</td>
      <td class="lbl">Particle Application</td>
      <td>{{ doc.particle_application }}</td>
    </tr>
    <tr>
      <td class="lbl">Calibrated leg space</td>
      <td>{{ doc.calibrated_leg_space }}</td>
      <td class="lbl">Excess Particle Removal</td>
      <td>{{ doc.excess_particle_removal }}</td>
    </tr>
    <tr>
      <td class="lbl">Demagnetization</td>
      <td>{{ doc.demagnetization }}</td>
      <td class="lbl">Acceptance Criteria</td>
      <td>{{ doc.acceptance_criteria }}</td>
    </tr>
  </table>

  <table class="mb">
    <tr><td colspan="4" class="sec-hdr">Equipment</td></tr>
    <tr>
      <td class="lbl" style="width:26%;">Yoke Manufacturer</td>
      <td style="width:24%;">{{ doc.yoke_manufacturer }}</td>
      <td class="lbl" style="width:26%;">Yoke Serial No</td>
      <td style="width:24%;">{{ doc.yoke_serial_no }}</td>
    </tr>
    <tr>
      <td class="lbl">UV Light Manufacturer</td>
      <td>{{ doc.uv_light_manufacturer }}</td>
      <td class="lbl">UV Light Serial No</td>
      <td>{{ doc.uv_light_serial_no }}</td>
    </tr>
    <tr>
      <td class="lbl">Light Meter Manufacturer</td>
      <td>{{ doc.light_meter_manufacturer }}</td>
      <td class="lbl">Light Meter Serial No</td>
      <td>{{ doc.light_meter_serial_no }}</td>
    </tr>
    <tr>
      <td class="lbl">Gauss Meter Manufacturer</td>
      <td>{{ doc.gauss_meter_manufacturer }}</td>
      <td class="lbl">Gauss Meter Serial No</td>
      <td>{{ doc.gauss_meter_serial_no }}</td>
    </tr>
    <tr>
      <td class="lbl">Thermometer Manufacturer</td>
      <td>{{ doc.thermometer_manufacturer }}</td>
      <td class="lbl">Thermometer Serial No</td>
      <td>{{ doc.thermometer_serial_no }}</td>
    </tr>
  </table>

  <table class="mb">
    <tr><td colspan="4" class="sec-hdr">Magnetic Particle Testing Material</td></tr>
    <tr>
      <th style="text-align:left; width:40%;">Manufacture</th>
      <th style="width:20%;">Magna flux</th>
      <th style="width:20%;">Ardrox</th>
      <th style="width:20%;">Batch No</th>
    </tr>
    <tr>
      <td class="lbl">Examination Medium (Batch No)</td>
      <td style="text-align:center;">{% if doc.examination_medium_manufacturer == 'Magnaflux' %}&#10003;{% endif %}</td>
      <td style="text-align:center;">{% if doc.examination_medium_manufacturer == 'Ardrox' %}&#10003;{% endif %}</td>
      <td>{{ doc.examination_medium_batch_no }}</td>
    </tr>
    <tr>
      <td class="lbl">Contrast Paint (Batch No)</td>
      <td style="text-align:center;">{% if doc.contrast_paint_manufacturer == 'Magnaflux' %}&#10003;{% endif %}</td>
      <td style="text-align:center;">{% if doc.contrast_paint_manufacturer == 'Ardrox' %}&#10003;{% endif %}</td>
      <td>{{ doc.contrast_paint_batch_no }}</td>
    </tr>
    <tr>
      <td class="lbl">Solvent Cleaner (Batch No)</td>
      <td style="text-align:center;">{% if doc.solvent_cleaner_manufacturer == 'Magnaflux' %}&#10003;{% endif %}</td>
      <td style="text-align:center;">{% if doc.solvent_cleaner_manufacturer == 'Ardrox' %}&#10003;{% endif %}</td>
      <td>{{ doc.solvent_cleaner_batch_no }}</td>
    </tr>
  </table>

  <table>
    <tr><td colspan="4" class="sec-hdr">Examination Part Surface</td></tr>
    <tr>
      <td class="lbl" style="width:26%;">Component Description</td>
      <td colspan="3">{{ doc.component_description }}</td>
    </tr>
    <tr>
      <td class="lbl">Material &amp; Thickness</td>
      <td style="width:24%;">{{ doc.material }}{% if doc.thickness %} / {{ doc.thickness }}{% endif %}</td>
      <td class="lbl" style="width:26%;">White Light Intensity</td>
      <td style="width:24%;">{{ doc.white_light_intensity }}</td>
    </tr>
    <tr>
      <td class="lbl">Surface Condition</td>
      <td>{{ doc.surface_condition }}</td>
      <td class="lbl">UV Light Intensity</td>
      <td>{{ doc.uv_light_intensity }}</td>
    </tr>
    <tr>
      <td class="lbl">Type of Weld</td>
      <td>{{ doc.type_of_weld }}</td>
      <td class="lbl">Magnetic Field Measurement Before Magnetization (G)</td>
      <td>{{ doc.magnetic_field_before }}</td>
    </tr>
    <tr>
      <td class="lbl">Material form</td>
      <td>{{ doc.material_form }}</td>
      <td class="lbl">Magnetic Field Measurement After Magnetization (G)</td>
      <td>{{ doc.magnetic_field_after }}</td>
    </tr>
    <tr>
      <td class="lbl">Surface Temperature</td>
      <td>{{ doc.surface_temperature }}</td>
      <td class="lbl">Magnetic Field strength and Direction</td>
      <td>{{ doc.magnetic_field_strength_direction }}</td>
    </tr>
    <tr>
      <td class="lbl">Lighting Equipment</td>
      <td>{{ doc.lighting_equipment }}</td>
      <td class="lbl">Post Cleaned</td>
      <td>{{ doc.post_cleaned }}</td>
    </tr>
  </table>

</div>

<!-- ===================== PAGE 2 ===================== -->
<div class="page">

  <div style="border:1px solid #000; text-align:center; padding:8px; margin-bottom:10px;">
    <span style="font-weight:bold; font-size:11.5pt; text-decoration:underline;">MAGNETIC PARTICLE EXAMINATION REPORT</span>
  </div>

  <table class="no-border mb">
    <tr>
      <td style="width:18%; padding:2px 4px;">Client Name</td>
      <td style="width:2%; padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; width:30%; padding:2px 6px;">{{ doc.client }}</td>
      <td style="width:18%; text-align:right; padding:2px 4px;">Date of Test</td>
      <td style="width:2%; padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; width:30%; padding:2px 6px;">{{ fmt_date(doc.date_of_test) }}</td>
    </tr>
    <tr>
      <td style="padding:2px 4px;">Project Name</td>
      <td style="padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; padding:2px 6px;">{{ doc.project_name }}</td>
      <td style="text-align:right; padding:2px 4px;">Date of Report</td>
      <td style="padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; padding:2px 6px;">{{ fmt_date(doc.date_of_report) }}</td>
    </tr>
    <tr>
      <td style="padding:2px 4px;"></td>
      <td></td>
      <td></td>
      <td style="text-align:right; padding:2px 4px;">Report No</td>
      <td style="padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; padding:2px 6px;">{{ doc.name }}</td>
    </tr>
    <tr>
      <td style="padding:2px 4px;"></td>
      <td></td>
      <td></td>
      <td style="text-align:right; padding:2px 4px;">Page No</td>
      <td style="padding:2px 0;">:</td>
      <td style="border-bottom:1px solid #000; padding:2px 6px;">2 of 2</td>
    </tr>
  </table>

  <table style="width:100%; margin-bottom:8px;">
    <thead>
      <tr>
        <th rowspan="2" style="width:5%;">SL#</th>
        <th rowspan="2" style="width:16%;">Component<br>Reference</th>
        <th rowspan="2" style="width:11%;">Weld<br>Ref. No.</th>
        <th rowspan="2" style="width:10%;">Welder<br>Symbol</th>
        <th colspan="4" style="text-align:center;">Discontinuity</th>
        <th rowspan="2" style="width:11%;">Results<br>(Acc / Rej)</th>
        <th rowspan="2" style="width:10%;">Remarks</th>
      </tr>
      <tr>
        <th style="width:9%;">Location</th>
        <th style="width:7%;">Type</th>
        <th style="width:7%;">Size</th>
        <th style="width:14%;">Flaw Type</th>
      </tr>
    </thead>
    <tbody>
      {% for row in doc.results %}
      <tr>
        <td style="height:23px; text-align:center;">{{ loop.index }}</td>
        <td>{{ row.component_reference }}</td>
        <td>{{ row.weld_ref_no }}</td>
        <td>{{ row.welder_symbol }}</td>
        <td>{{ row.discontinuity_location }}</td>
        <td>{{ row.discontinuity_type }}</td>
        <td>{{ row.discontinuity_size }}</td>
        <td>{{ row.flaw_type }}</td>
        <td>{{ row.result }}</td>
        <td>{{ row.remarks }}</td>
      </tr>
      {% endfor %}
      {% for i in range(14) %}{% if i >= doc.results | length %}
      <tr><td style="height:23px;"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      {% endif %}{% endfor %}
    </tbody>
  </table>

  <p style="font-size:7.5pt; font-style:italic; text-align:center; margin-bottom:14px;">
    This report relates only to the sample tested and shall only be reproduced in full with the written approval of the AHS testing laboratory.
  </p>

  <table class="no-border" style="width:100%; margin-top:24px;">
    <tr>
      <td style="width:50%; vertical-align:top; padding-right:16px;">
        <div style="font-weight:bold; margin-bottom:6px; font-size:9.5pt;">Examined by:</div>
        <table class="no-border" style="width:100%;">
          <tr>
            <td style="width:30%; padding:3px 4px;">Name</td>
            <td style="width:4%; padding:3px 0;">:</td>
            <td style="border-bottom:1px solid #000; padding:3px 6px;">{% if doc.include_signature %}{{ doc.signed_by }}{% endif %}</td>
          </tr>
          <tr>
            <td style="padding:3px 4px;">Designation</td>
            <td style="padding:3px 0;">:</td>
            <td style="border-bottom:1px solid #000; padding:3px 6px;">NDT Inspector</td>
          </tr>
          <tr>
            <td style="padding:3px 4px; vertical-align:top;">Signature</td>
            <td style="padding:3px 0; vertical-align:top;">:</td>
            <td style="border-bottom:1px solid #000; padding:3px 6px; height:60px;">
              {% if doc.include_signature and doc.inspector_signature %}
              <img src="{{ file_b64(doc.inspector_signature) }}" style="max-height:50px; max-width:150px; vertical-align:middle;">
              {% endif %}
              {% if doc.include_seal and doc.inspector_seal %}
              <img src="{{ file_b64(doc.inspector_seal) }}" style="max-height:50px; max-width:50px; vertical-align:middle; margin-left:10px;">
              {% endif %}
            </td>
          </tr>
        </table>
      </td>
      <td style="width:50%; vertical-align:top; padding-left:16px;">
        <div style="font-weight:bold; margin-bottom:6px; font-size:9.5pt;">Noted by:</div>
        <table class="no-border" style="width:100%;">
          <tr>
            <td style="width:30%; padding:3px 4px;">Name</td>
            <td style="width:4%; padding:3px 0;">:</td>
            <td style="border-bottom:1px solid #000; padding:3px 6px;"></td>
          </tr>
          <tr>
            <td style="padding:3px 4px;">Designation</td>
            <td style="padding:3px 0;">:</td>
            <td style="border-bottom:1px solid #000; padding:3px 6px;"></td>
          </tr>
          <tr>
            <td style="padding:3px 4px; vertical-align:top;">Signature</td>
            <td style="padding:3px 0; vertical-align:top;">:</td>
            <td style="border-bottom:1px solid #000; padding:3px 6px; height:60px;"></td>
          </tr>
        </table>
      </td>
    </tr>
  </table>

</div>

</body>
</html>"""


def _render_html(doc):
	env = Environment(autoescape=False)
	template = env.from_string(_TEMPLATE)
	return template.render(
		doc=doc,
		fmt_date=_fmt_date,
		file_b64=_file_base64,
	)
