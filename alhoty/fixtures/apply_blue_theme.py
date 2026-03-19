"""
Blue Theme Dashboard Update
Run via: bench --site alhoty.local console
Then:    exec(open('apps/alhoty/alhoty/fixtures/apply_blue_theme.py').read())
"""
import json, os, frappe

HTML = """<div class="ndt-dash">
  <div class="ndt-dash-header">
    <div style="flex:1;">
      <p class="ndt-dash-greeting" id="ndt-greeting">Good morning</p>
      <p class="ndt-dash-sub">NDT Inspection Portal</p>
      <div class="ndt-kpi-row" style="margin-top:14px;margin-bottom:0;">
        <a class="ndt-kpi-card" id="kpi-link-month" style="--kpi-color:#2563eb;">
          <div class="ndt-kpi-top">
            <p class="ndt-kpi-lbl">Inspections this month</p>
            <div class="ndt-kpi-icon" style="background:rgba(37,99,235,0.1);">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/></svg>
            </div>
          </div>
          <p class="ndt-kpi-val ndt-kpi-loading-val" id="kpi-month">&#8212;</p>
        </a>
        <a class="ndt-kpi-card" id="kpi-link-wo" style="--kpi-color:#7c3aed;">
          <div class="ndt-kpi-top">
            <p class="ndt-kpi-lbl">Work orders</p>
            <div class="ndt-kpi-icon" style="background:rgba(124,58,237,0.1);">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            </div>
          </div>
          <p class="ndt-kpi-val ndt-kpi-loading-val" id="kpi-wo">&#8212;</p>
        </a>
        <a class="ndt-kpi-card" id="kpi-link-pending" style="--kpi-color:#d97706;">
          <div class="ndt-kpi-top">
            <p class="ndt-kpi-lbl">Pending approval</p>
            <div class="ndt-kpi-icon" style="background:rgba(217,119,6,0.1);">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            </div>
          </div>
          <p class="ndt-kpi-val ndt-kpi-loading-val" id="kpi-pending">&#8212;</p>
        </a>
        <a class="ndt-kpi-card" id="kpi-link-accepted" style="--kpi-color:#10b981;">
          <div class="ndt-kpi-top">
            <p class="ndt-kpi-lbl">Accepted this month</p>
            <div class="ndt-kpi-icon" style="background:rgba(16,185,129,0.1);">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            </div>
          </div>
          <p class="ndt-kpi-val ndt-kpi-loading-val" id="kpi-accepted">&#8212;</p>
        </a>
        <a class="ndt-kpi-card" id="kpi-link-equipment" style="--kpi-color:#0891b2;">
          <div class="ndt-kpi-top">
            <p class="ndt-kpi-lbl">Equipment registered</p>
            <div class="ndt-kpi-icon" style="background:rgba(8,145,178,0.1);">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0891b2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            </div>
          </div>
          <p class="ndt-kpi-val ndt-kpi-loading-val" id="kpi-equipment">&#8212;</p>
        </a>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:10px;">
      <div class="ndt-cal-widget" id="ndt-cal-widget-trigger" style="cursor:pointer;">
        <div class="ndt-cal-month" id="ndt-cal-month">March</div>
        <div class="ndt-cal-day" id="ndt-cal-day">15</div>
        <div class="ndt-cal-weekday" id="ndt-cal-weekday">Sunday</div>
      </div>
      <div class="ndt-time-widget">
        <div class="ndt-time-display" id="ndt-cal-time">00:00:00 AM</div>
      </div>
    </div>
  </div>

  <div class="ndt-dash-body">
    <div style="display:flex;flex-direction:column;gap:12px;">
      <div class="ndt-glass-card">
        <p class="ndt-card-title">MT Inspections by Branch</p>
        <div id="ndt-branch-grid"></div>
      </div>
      <div class="ndt-glass-card">
        <p class="ndt-card-title">Recent Inspections</p>
        <table class="ndt-recent-table">
          <thead>
            <tr>
              <th>Report No</th>
              <th>Date</th>
              <th>Technique</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody id="ndt-recent-body">
            <tr><td colspan="4" style="color:#60a5fa;font-size:12px;padding:12px 0;">Loading...</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="ndt-right-col">
      <div class="ndt-alert-glass" id="ndt-alert">
        <p class="ndt-alert-glass-title">Pending Review</p>
        <p class="ndt-alert-glass-text" id="ndt-alert-text">&#8212;</p>
        <button class="ndt-alert-glass-btn" id="ndt-alert-btn">Review Now &rarr;</button>
      </div>
      <div class="ndt-shortcuts-card">
        <p class="ndt-card-title">Quick Actions</p>
        <div class="ndt-shortcut-item" id="sc-new-wo">
          <p class="ndt-shortcut-label">Work Order</p>
          <span><span class="ndt-shortcut-tag tag-new">New</span><span class="ndt-shortcut-arrow">&rarr;</span></span>
        </div>
        <div class="ndt-shortcut-item" id="sc-new-mt">
          <p class="ndt-shortcut-label">MT Inspection</p>
          <span><span class="ndt-shortcut-tag tag-new">New</span><span class="ndt-shortcut-arrow">&rarr;</span></span>
        </div>
        <div class="ndt-shortcut-item" id="sc-all-mt">
          <p class="ndt-shortcut-label">All Inspections</p>
          <span><span class="ndt-shortcut-tag tag-all">View</span><span class="ndt-shortcut-arrow">&rarr;</span></span>
        </div>
        <div class="ndt-shortcut-item" id="sc-equipment">
          <p class="ndt-shortcut-label">Equipment Master</p>
          <span><span class="ndt-shortcut-tag tag-master">Master</span><span class="ndt-shortcut-arrow">&rarr;</span></span>
        </div>
        <div class="ndt-shortcut-item" id="sc-client">
          <p class="ndt-shortcut-label">Client Master</p>
          <span><span class="ndt-shortcut-tag tag-master">Master</span><span class="ndt-shortcut-arrow">&rarr;</span></span>
        </div>
        <div class="ndt-shortcut-item" id="sc-project">
          <p class="ndt-shortcut-label">Project Master</p>
          <span><span class="ndt-shortcut-tag tag-master">Master</span><span class="ndt-shortcut-arrow">&rarr;</span></span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Calendar Modal -->
<div class="ndt-calendar-modal" id="ndt-calendar-modal">
  <div class="ndt-calendar-overlay" id="ndt-calendar-overlay"></div>
  <div class="ndt-calendar-popup">
    <div class="ndt-calendar-header">
      <button class="ndt-calendar-nav" id="ndt-cal-prev">&larr;</button>
      <div class="ndt-calendar-title" id="ndt-calendar-title">March 2026</div>
      <button class="ndt-calendar-nav" id="ndt-cal-next">&rarr;</button>
    </div>
    <div class="ndt-calendar-weekdays">
      <div>S</div><div>M</div><div>T</div><div>W</div><div>T</div><div>F</div><div>S</div>
    </div>
    <div class="ndt-calendar-days" id="ndt-calendar-days"></div>
  </div>
</div>"""

STYLE = """.ndt-dash {
  background: linear-gradient(135deg, #e8f0fe 0%, #dbeafe 45%, #eff6ff 100%);
  border-radius: 16px;
  padding: clamp(20px, 2.2vw, 28px);
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.ndt-dash-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: clamp(16px, 1.8vw, 22px);
  margin-bottom: clamp(14px, 1.6vw, 18px);
}

.ndt-dash-greeting {
  font-size: clamp(22px, 2.2vw, 26px);
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 4px;
  letter-spacing: -0.4px;
}

.ndt-dash-sub {
  font-size: clamp(13px, 1.3vw, 15px);
  color: #64748b;
  margin: 0;
  font-weight: 500;
}

/* Calendar widget */
.ndt-cal-widget {
  background: rgba(255,255,255,0.92);
  border: 1px solid rgba(191,219,254,0.8);
  border-radius: 14px;
  overflow: hidden;
  min-width: 96px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(37,99,235,0.10);
  flex-shrink: 0;
  transition: transform 0.2s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.2s ease;
}

.ndt-cal-widget:hover {
  transform: scale(1.04) translateZ(0);
  box-shadow: 0 6px 24px rgba(37,99,235,0.20);
}

.ndt-cal-month {
  background: linear-gradient(135deg, #1d4ed8, #3b82f6);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 7px 16px 6px;
}

.ndt-cal-day {
  font-size: 36px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
  padding: 10px 16px 4px;
  letter-spacing: -1px;
}

.ndt-cal-weekday {
  font-size: clamp(10px, 1vw, 12px);
  font-weight: 600;
  color: #2563eb;
  padding: 0 16px 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* KPI row */
.ndt-kpi-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(clamp(140px, 15vw, 170px), 1fr));
  gap: clamp(8px, 1vw, 12px);
  margin-bottom: clamp(14px, 1.8vw, 18px);
}

.ndt-kpi-card {
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(191,219,254,0.6);
  border-radius: 12px;
  padding: clamp(12px, 1.4vw, 16px);
  cursor: pointer;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.2s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.2s ease;
  min-height: clamp(82px, 8.5vw, 96px);
  position: relative;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(37,99,235,0.07);
}

.ndt-kpi-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--kpi-color, #2563eb);
  opacity: 0.7;
  border-radius: 0 0 12px 12px;
}

.ndt-kpi-card:hover {
  transform: scale(1.04) translateZ(0);
  -webkit-transform: scale(1.04) translateZ(0);
  background: #fff;
  box-shadow: 0 6px 24px rgba(37,99,235,0.16);
  text-decoration: none;
}

.ndt-kpi-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 6px;
  margin-bottom: 8px;
}

.ndt-kpi-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ndt-kpi-val {
  font-size: clamp(22px, 2.5vw, 28px);
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.8px;
  margin: 0;
  line-height: 1;
}

.ndt-kpi-lbl {
  font-size: clamp(9px, 0.9vw, 10px);
  color: #64748b;
  margin: 0;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  line-height: 1.3;
  flex: 1;
}

.ndt-kpi-loading-val { color: #bfdbfe; }

/* Body grid */
.ndt-dash-body {
  display: grid;
  grid-template-columns: 1fr clamp(260px, 24vw, 300px);
  gap: clamp(12px, 1.4vw, 16px);
}

@media (max-width: 1200px) {
  .ndt-dash-body { grid-template-columns: 1fr; }
}

/* Glass cards */
.ndt-glass-card {
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(191,219,254,0.6);
  border-radius: 14px;
  padding: clamp(16px, 1.8vw, 22px) clamp(18px, 2vw, 24px);
  box-shadow: 0 2px 8px rgba(37,99,235,0.06);
}

.ndt-card-title {
  font-size: clamp(10px, 1vw, 11px);
  font-weight: 700;
  color: #94a3b8;
  margin: 0 0 clamp(14px, 1.6vw, 18px);
  text-transform: uppercase;
  letter-spacing: 0.9px;
}

/* Right column */
.ndt-right-col {
  display: flex;
  flex-direction: column;
  gap: clamp(10px, 1.2vw, 14px);
}

/* Alert */
.ndt-alert-glass {
  display: none;
  background: rgba(219,234,254,0.7);
  border: 1px solid rgba(147,197,253,0.5);
  border-left: 3px solid #2563eb;
  border-radius: 12px;
  padding: clamp(12px, 1.4vw, 16px) clamp(14px, 1.6vw, 18px);
}

.ndt-alert-glass.visible { display: block; }

.ndt-alert-glass-title {
  font-size: clamp(10px, 1vw, 11px);
  font-weight: 700;
  color: #1e40af;
  margin: 0 0 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ndt-alert-glass-text {
  font-size: clamp(12px, 1.2vw, 13px);
  color: #1d4ed8;
  margin: 0 0 10px;
}

.ndt-alert-glass-btn {
  font-size: clamp(11px, 1.1vw, 12px);
  font-weight: 600;
  color: #1e40af;
  background: rgba(255,255,255,0.75);
  border: 1px solid rgba(37,99,235,0.3);
  border-radius: 6px;
  padding: clamp(5px, 0.6vw, 7px) clamp(12px, 1.4vw, 14px);
  cursor: pointer;
  width: 100%;
  transition: all 0.2s ease;
}

.ndt-alert-glass-btn:hover {
  background: #fff;
  box-shadow: 0 4px 16px rgba(37,99,235,0.18);
  transform: scale(1.02);
}

/* Shortcuts */
.ndt-shortcuts-card {
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(191,219,254,0.6);
  border-radius: 14px;
  padding: clamp(14px, 1.6vw, 18px) clamp(16px, 1.8vw, 20px);
  box-shadow: 0 2px 8px rgba(37,99,235,0.06);
}

.ndt-shortcut-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: clamp(8px, 1vw, 10px) clamp(8px, 1vw, 10px);
  margin: 0 clamp(-8px, -1vw, -10px);
  border-bottom: 1px solid rgba(219,234,254,0.5);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s ease, box-shadow 0.15s ease;
}

.ndt-shortcut-item:last-child { border-bottom: none; }

.ndt-shortcut-item:hover {
  background: rgba(239,246,255,0.9);
  box-shadow: 0 2px 10px rgba(37,99,235,0.10);
}

.ndt-shortcut-label {
  font-size: clamp(12px, 1.2vw, 13px);
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.ndt-shortcut-tag {
  font-size: clamp(9px, 0.9vw, 10px);
  font-weight: 700;
  padding: clamp(2px, 0.3vw, 3px) clamp(7px, 0.8vw, 9px);
  border-radius: 10px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.tag-new    { background: rgba(37,99,235,0.10);  color: #1d4ed8; }
.tag-all    { background: rgba(16,185,129,0.10);  color: #065f46; }
.tag-master { background: rgba(249,115,22,0.10);  color: #c2410c; }

.ndt-shortcut-arrow {
  font-size: clamp(12px, 1.1vw, 14px);
  color: #60a5fa;
  margin-left: clamp(6px, 0.7vw, 8px);
}

/* Recent table */
.ndt-recent-table { width: 100%; border-collapse: collapse; }

.ndt-recent-table th {
  font-size: clamp(9px, 0.95vw, 11px);
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  text-align: left;
  padding: 0 0 clamp(10px, 1.2vw, 12px);
  border-bottom: 1px solid rgba(191,219,254,0.6);
}

.ndt-recent-table td {
  font-size: clamp(12px, 1.2vw, 13px);
  color: #1e293b;
  padding: clamp(9px, 1vw, 11px) 0;
  border-bottom: 1px solid rgba(219,234,254,0.4);
}

.ndt-recent-table tr:last-child td { border-bottom: none; }
.ndt-recent-table tbody tr { cursor: pointer; transition: background 0.12s; }
.ndt-recent-table tbody tr:hover td { background: rgba(239,246,255,0.6); }

.ndt-badge {
  font-size: clamp(10px, 1vw, 11px);
  font-weight: 600;
  padding: clamp(2px, 0.3vw, 3px) clamp(8px, 0.9vw, 10px);
  border-radius: 10px;
}

.badge-draft     { background: rgba(148,163,184,0.14); color: #475569; }
.badge-submitted { background: rgba(16,185,129,0.12);  color: #065f46; }
.badge-pending   { background: rgba(249,115,22,0.12);  color: #c2410c; }

/* Branch rings */
#ndt-branch-grid {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(2px, 0.4vw, 4px);
  align-items: flex-start;
  justify-content: flex-start;
}

.ndt-ring-wrap {
  width: clamp(125px, 14vw, 145px);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: clamp(8px, 1vw, 11px) clamp(6px, 0.8vw, 9px);
  border-radius: 12px;
  box-sizing: border-box;
  transition: transform 0.2s cubic-bezier(0.34,1.56,0.64,1), background 0.2s ease, box-shadow 0.2s ease;
  background: rgba(255,255,255,0.5);
  border: 1px solid transparent;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
}

.ndt-ring-wrap:hover {
  transform: scale(1.05) translateZ(0);
  -webkit-transform: scale(1.05) translateZ(0);
  background: rgba(255,255,255,0.98);
  box-shadow: 0 4px 20px rgba(37,99,235,0.14);
  border-color: rgba(191,219,254,0.8);
}

.ndt-ring-name {
  font-size: clamp(11px, 1.1vw, 12px);
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 clamp(6px, 0.8vw, 8px);
  text-align: center;
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ndt-ring-sub {
  font-size: clamp(10px, 1vw, 11px);
  color: #64748b;
  text-align: center;
  margin: clamp(4px, 0.6vw, 6px) 0 0;
  white-space: nowrap;
}

/* Time widget */
.ndt-time-widget {
  background: rgba(255,255,255,0.92);
  border: 1px solid rgba(191,219,254,0.8);
  border-radius: 14px;
  overflow: hidden;
  min-width: 96px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(37,99,235,0.10);
  flex-shrink: 0;
}

.ndt-time-display {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.3;
  padding: 10px 14px;
  letter-spacing: 0.5px;
  font-variant-numeric: tabular-nums;
}

/* Mobile */
@media (max-width: 768px) {
  .ndt-cal-widget, .ndt-time-widget { display: none !important; }
  .ndt-dash-header { flex-direction: column; }
  .ndt-kpi-row { grid-template-columns: repeat(2, 1fr) !important; }
  .ndt-dash-body { grid-template-columns: 1fr !important; }
}

/* Calendar modal */
.ndt-calendar-modal {
  display: none;
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 9999;
  animation: ndtFadeIn 0.2s ease-out;
}

.ndt-calendar-modal.active { display: block; }

.ndt-calendar-overlay {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(15,23,42,0.5);
  backdrop-filter: blur(4px);
}

.ndt-calendar-popup {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 50%, #e0f2fe 100%);
  border: 1px solid rgba(255,255,255,0.9);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 20px 60px rgba(37,99,235,0.22);
  width: 90%;
  max-width: 380px;
  animation: ndtSlideUp 0.3s cubic-bezier(0.34,1.56,0.64,1);
}

@keyframes ndtFadeIn { from { opacity: 0; } to { opacity: 1; } }

@keyframes ndtSlideUp {
  from { transform: translate(-50%, -45%); opacity: 0; }
  to   { transform: translate(-50%, -50%); opacity: 1; }
}

.ndt-calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.ndt-calendar-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.3px;
}

.ndt-calendar-nav {
  background: rgba(255,255,255,0.7);
  border: 1px solid rgba(37,99,235,0.2);
  border-radius: 8px;
  width: 36px; height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #2563eb;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 600;
}

.ndt-calendar-nav:hover {
  background: #fff;
  border-color: #2563eb;
  transform: scale(1.08);
  box-shadow: 0 2px 8px rgba(37,99,235,0.2);
}

.ndt-calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-bottom: 8px;
}

.ndt-calendar-weekdays div {
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  text-align: center;
  padding: 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ndt-calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.ndt-calendar-day {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  text-align: center;
  padding: 9px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.18s ease;
  background: rgba(255,255,255,0.45);
}

.ndt-calendar-day:hover {
  background: rgba(255,255,255,0.9);
  transform: scale(1.06);
  box-shadow: 0 2px 8px rgba(37,99,235,0.12);
}

.ndt-calendar-day.other-month { color: #93c5fd; opacity: 0.55; }

.ndt-calendar-day.today {
  background: linear-gradient(135deg, #1d4ed8, #3b82f6);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 2px 12px rgba(37,99,235,0.38);
}

.ndt-calendar-day.today:hover {
  background: linear-gradient(135deg, #1e40af, #2563eb);
  transform: scale(1.08);
}

.ndt-calendar-day.selected {
  background: rgba(37,99,235,0.15);
  border: 2px solid #2563eb;
  font-weight: 700;
}"""

SCRIPT = """// Saudi time via Intl
function getSaudiParts() {
  const now   = new Date();
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Asia/Riyadh",
    weekday: "long", month: "long", day: "numeric",
    hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: true
  }).formatToParts(now);
  const get = (type) => (parts.find(p => p.type === type) || {}).value || "";
  return {
    day:     get("day"),
    month:   get("month"),
    weekday: get("weekday"),
    hour:    parseInt(get("hour")),
  };
}

function updateClock() {
  const p         = getSaudiParts();
  const greetWord = p.hour < 12 ? "Good morning" : p.hour < 17 ? "Good afternoon" : "Good evening";
  const userName  = (frappe.session.user_fullname || frappe.session.user || "").split(" ")[0];
  const greetEl   = root_element.querySelector("#ndt-greeting");
  const monthEl   = root_element.querySelector("#ndt-cal-month");
  const dayEl     = root_element.querySelector("#ndt-cal-day");
  const weekdayEl = root_element.querySelector("#ndt-cal-weekday");
  const timeEl    = root_element.querySelector("#ndt-cal-time");

  if (greetEl)   greetEl.textContent   = greetWord + (userName ? ", " + userName : "");
  if (monthEl)   monthEl.textContent   = p.month;
  if (dayEl)     dayEl.textContent     = p.day;
  if (weekdayEl) weekdayEl.textContent = p.weekday;

  if (timeEl) {
    const timeParts = new Intl.DateTimeFormat("en-US", {
      timeZone: "Asia/Riyadh",
      hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: true
    }).formatToParts(new Date());
    const hour   = timeParts.find(p => p.type === "hour")?.value   || "00";
    const minute = timeParts.find(p => p.type === "minute")?.value || "00";
    const second = timeParts.find(p => p.type === "second")?.value || "00";
    const period = timeParts.find(p => p.type === "dayPeriod")?.value || "AM";
    timeEl.textContent = hour + ":" + minute + ":" + second + " " + period.toUpperCase();
  }
}

updateClock();
setInterval(updateClock, 1000);

// KPI card links
const now = new Date();
const firstOfMonth = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split("T")[0];
const lastOfMonth  = new Date(now.getFullYear(), now.getMonth() + 1, 0).toISOString().split("T")[0];

const kpiCardEl1 = root_element.querySelector("#kpi-link-month");
if (kpiCardEl1) kpiCardEl1.addEventListener("click", (e) => { e.preventDefault(); frappe.set_route("List", "MT Inspection", { "date_of_test": ["between", [firstOfMonth, lastOfMonth]] }); });

const kpiCardEl2 = root_element.querySelector("#kpi-link-wo");
if (kpiCardEl2) kpiCardEl2.addEventListener("click", (e) => { e.preventDefault(); frappe.set_route("List", "Work Order"); });

const kpiCardEl3 = root_element.querySelector("#kpi-link-pending");
if (kpiCardEl3) kpiCardEl3.addEventListener("click", (e) => { e.preventDefault(); frappe.set_route("List", "MT Inspection", { "docstatus": 0 }); });

const kpiCardEl4 = root_element.querySelector("#kpi-link-accepted");
if (kpiCardEl4) kpiCardEl4.addEventListener("click", (e) => { e.preventDefault(); frappe.set_route("List", "MT Inspection", { "docstatus": 1, "date_of_test": ["between", [firstOfMonth, lastOfMonth]] }); });

const kpiCardEl5 = root_element.querySelector("#kpi-link-equipment");
if (kpiCardEl5) kpiCardEl5.addEventListener("click", (e) => { e.preventDefault(); frappe.set_route("List", "Equipment Master"); });

// Shortcuts
const shortcuts = {
  "sc-new-wo":    "/app/work-order/new-work-order-1",
  "sc-new-mt":    "/app/mt-inspection/new-mt-inspection-1",
  "sc-all-mt":    "/app/mt-inspection",
  "sc-equipment": "/app/equipment-master",
  "sc-client":    "/app/client-master",
  "sc-project":   "/app/project-master"
};
Object.entries(shortcuts).forEach(([id, route]) => {
  const el = root_element.querySelector("#" + id);
  if (el) el.addEventListener("click", () => frappe.set_route(route));
});

// KPI counts
function setKPI(id, value, color) {
  const el = root_element.querySelector(id);
  if (!el) return;
  el.textContent = value;
  el.classList.remove("ndt-kpi-loading-val");
  if (color) el.style.color = color;
}

frappe.call({ method: "frappe.client.get_count", args: { doctype: "MT Inspection", filters: [["date_of_test", ">=", firstOfMonth]] }, callback: (r) => setKPI("#kpi-month", r.message ?? 0, "#2563eb") });
frappe.call({ method: "frappe.client.get_count", args: { doctype: "Work Order", filters: [] }, callback: (r) => setKPI("#kpi-wo", r.message ?? 0, "#7c3aed") });
frappe.call({
  method: "frappe.client.get_count",
  args: { doctype: "MT Inspection", filters: [["docstatus", "=", 0]] },
  callback: (r) => {
    const count = r.message ?? 0;
    setKPI("#kpi-pending", count, count > 0 ? "#d97706" : "#1e293b");
    const alertBox  = root_element.querySelector("#ndt-alert");
    const alertText = root_element.querySelector("#ndt-alert-text");
    if (count > 0 && alertBox && alertText) {
      alertText.textContent = count + " inspection" + (count > 1 ? "s" : "") + " awaiting your review.";
      alertBox.classList.add("visible");
    }
  }
});
frappe.call({ method: "frappe.client.get_count", args: { doctype: "MT Inspection", filters: [["docstatus", "=", 1], ["date_of_test", ">=", firstOfMonth]] }, callback: (r) => setKPI("#kpi-accepted", r.message ?? 0, "#10b981") });
frappe.call({ method: "frappe.client.get_count", args: { doctype: "Equipment Master" }, callback: (r) => setKPI("#kpi-equipment", r.message ?? 0, "#0891b2") });

const alertBtn = root_element.querySelector("#ndt-alert-btn");
if (alertBtn) alertBtn.addEventListener("click", () => frappe.set_route("/app/mt-inspection"));

// Recent inspections
frappe.call({
  method: "frappe.client.get_list",
  args: { doctype: "MT Inspection", fields: ["name", "date_of_test", "mt_variant", "docstatus"], order_by: "creation desc", limit: 5 },
  callback: (r) => {
    const tbody = root_element.querySelector("#ndt-recent-body");
    if (!tbody) return;
    const rows = r.message || [];
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="4" style="color:#60a5fa;font-size:12px;padding:12px 0;">No inspections yet</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(row => {
      const statusMap = { 0: ["Draft", "badge-draft"], 1: ["Submitted", "badge-submitted"] };
      const [label, cls] = statusMap[row.docstatus] || ["Pending", "badge-pending"];
      const date = row.date_of_test ? new Date(row.date_of_test).toLocaleDateString("en-GB") : "—";
      return `<tr onclick="frappe.set_route('/app/mt-inspection/${row.name}')">
        <td style="font-weight:600;">${row.name || "—"}</td>
        <td style="color:#64748b;">${date}</td>
        <td>${row.mt_variant || "MT"}</td>
        <td><span class="ndt-badge ${cls}">${label}</span></td>
      </tr>`;
    }).join("");
  }
});

// Branch rings
const BRANCH_COLORS = ["#2563eb","#0891b2","#7c3aed","#10b981","#f59e0b","#ef4444","#3b82f6","#06b6d4"];

function makeSVG(count, pct, color) {
  const R=48, stroke=11, W=125, cx=W/2, cy=54, circ=Math.PI*R;
  const dash = ((pct/100)*circ).toFixed(2);
  return `<svg width="${W}" height="62" viewBox="0 0 ${W} 62" style="display:block;overflow:visible;">
    <path d="M ${cx-R} ${cy} A ${R} ${R} 0 0 1 ${cx+R} ${cy}" fill="none" stroke="#dbeafe" stroke-width="${stroke}" stroke-linecap="round"/>
    <path d="M ${cx-R} ${cy} A ${R} ${R} 0 0 1 ${cx+R} ${cy}" fill="none" stroke="${color}" stroke-width="${stroke}" stroke-linecap="round"
          stroke-dasharray="0 ${circ}" style="transition:stroke-dasharray 1s cubic-bezier(0.4,0,0.2,1);"
          data-dash="${dash}" data-circ="${circ}"/>
    <text x="${cx}" y="${cy-10}" text-anchor="middle" font-family="Helvetica Neue,Arial,sans-serif" font-size="20" font-weight="700" fill="${color}">${count}</text>
    <text x="${cx}" y="${cy+6}" text-anchor="middle" font-family="Helvetica Neue,Arial,sans-serif" font-size="9" fill="#64748b">${pct}% of total</text>
  </svg>`;
}

const grid = root_element.querySelector("#ndt-branch-grid");
if (grid) {
  frappe.call({
    method: "frappe.client.get_list",
    args: { doctype: "Branch Master", fields: ["name"], limit: 50, order_by: "name asc" },
    callback: (branchRes) => {
      const branches = (branchRes.message || []).map(b => b.name);
      if (!branches.length) { grid.innerHTML = '<p style="font-size:12px;color:#64748b;margin:0;">No branches found.</p>'; return; }
      const slots = {};
      branches.forEach((name, i) => {
        const color = BRANCH_COLORS[i % BRANCH_COLORS.length];
        const wrap  = document.createElement("div");
        wrap.className = "ndt-ring-wrap";
        wrap.innerHTML = `<p class="ndt-ring-name" title="${name}">${name}</p>
          <svg width="125" height="62" viewBox="0 0 125 62" style="display:block;overflow:visible;">
            <path d="M 14 54 A 48 48 0 0 1 111 54" fill="none" stroke="#dbeafe" stroke-width="11" stroke-linecap="round"/>
          </svg>
          <p class="ndt-ring-sub">Loading...</p>`;
        wrap.addEventListener("click", () => frappe.set_route("List", "MT Inspection", { branch: name }));
        grid.appendChild(wrap);
        slots[name] = { wrap, color };
      });
      frappe.call({
        method: "frappe.client.get_count",
        args: { doctype: "MT Inspection", filters: [] },
        callback: (totalRes) => {
          const total = totalRes.message || 1;
          branches.forEach(name => {
            const { wrap, color } = slots[name];
            frappe.call({
              method: "frappe.client.get_count",
              args: { doctype: "MT Inspection", filters: [["branch", "=", name]] },
              callback: (r) => {
                const count = r.message ?? 0;
                const pct   = Math.round((count / total) * 100);
                const tmp   = document.createElement("div");
                tmp.innerHTML = makeSVG(count, pct, color);
                const newSvg = tmp.querySelector("svg");
                const oldSvg = wrap.querySelector("svg");
                if (oldSvg && newSvg) wrap.replaceChild(newSvg, oldSvg);
                const sub = wrap.querySelector(".ndt-ring-sub");
                if (sub) sub.textContent = "Total inspections";
                setTimeout(() => {
                  const arc = newSvg.querySelector("path[data-dash]");
                  if (arc) arc.setAttribute("stroke-dasharray", arc.getAttribute("data-dash") + " " + arc.getAttribute("data-circ"));
                }, 150);
              }
            });
          });
        }
      });
    }
  });
}

// Calendar Modal
let currentCalendarDate = new Date();

function renderCalendar(date) {
  const year = date.getFullYear(), month = date.getMonth();
  const monthNames = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  const titleEl = root_element.querySelector("#ndt-calendar-title");
  if (titleEl) titleEl.textContent = monthNames[month] + " " + year;
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const daysInPrevMonth = new Date(year, month, 0).getDate();
  const today = new Date();
  const isCurrentMonth = today.getFullYear() === year && today.getMonth() === month;
  const daysContainer = root_element.querySelector("#ndt-calendar-days");
  if (!daysContainer) return;
  daysContainer.innerHTML = "";
  for (let i = firstDay - 1; i >= 0; i--) {
    const d = document.createElement("div");
    d.className = "ndt-calendar-day other-month";
    d.textContent = daysInPrevMonth - i;
    daysContainer.appendChild(d);
  }
  for (let day = 1; day <= daysInMonth; day++) {
    const d = document.createElement("div");
    d.className = "ndt-calendar-day";
    d.textContent = day;
    if (isCurrentMonth && day === today.getDate()) d.classList.add("today");
    d.addEventListener("click", function() {
      daysContainer.querySelectorAll(".ndt-calendar-day.selected").forEach(el => el.classList.remove("selected"));
      if (!d.classList.contains("today")) d.classList.add("selected");
    });
    daysContainer.appendChild(d);
  }
  const remaining = 42 - daysContainer.children.length;
  for (let day = 1; day <= remaining; day++) {
    const d = document.createElement("div");
    d.className = "ndt-calendar-day other-month";
    d.textContent = day;
    daysContainer.appendChild(d);
  }
}

const calTrigger = root_element.querySelector("#ndt-cal-widget-trigger");
const calModal   = root_element.querySelector("#ndt-calendar-modal");
const calOverlay = root_element.querySelector("#ndt-calendar-overlay");

if (calTrigger && calModal) {
  calTrigger.addEventListener("click", function() {
    currentCalendarDate = new Date();
    renderCalendar(currentCalendarDate);
    calModal.classList.add("active");
  });
}
if (calOverlay && calModal) calOverlay.addEventListener("click", () => calModal.classList.remove("active"));

const prevBtn = root_element.querySelector("#ndt-cal-prev");
const nextBtn = root_element.querySelector("#ndt-cal-next");
if (prevBtn) prevBtn.addEventListener("click", () => { currentCalendarDate.setMonth(currentCalendarDate.getMonth()-1); renderCalendar(currentCalendarDate); });
if (nextBtn) nextBtn.addEventListener("click", () => { currentCalendarDate.setMonth(currentCalendarDate.getMonth()+1); renderCalendar(currentCalendarDate); });

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && calModal && calModal.classList.contains("active")) calModal.classList.remove("active");
});"""

# Apply to database
doc = frappe.get_doc("Custom HTML Block", "MT Branch Inspection")
doc.html   = HTML
doc.style  = STYLE
doc.script = SCRIPT
doc.save(ignore_permissions=True)
frappe.db.commit()

# Write back to fixture JSON
fixture_path = os.path.join(frappe.get_app_path("alhoty"), "fixtures", "custom_html_block.json")
data = [{
    "docstatus": 0,
    "doctype":   "Custom HTML Block",
    "html":      HTML,
    "modified":  str(doc.modified),
    "name":      "MT Branch Inspection",
    "private":   0,
    "roles":     [],
    "script":    SCRIPT,
    "style":     STYLE,
}]
with open(fixture_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)

print("Blue theme applied to DB and fixture updated!")
