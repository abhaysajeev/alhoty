import frappe
from frappe.utils import getdate, add_days, add_months, get_first_day, get_last_day
from datetime import timedelta


@frappe.whitelist()
def get_dashboard_data(from_date=None, to_date=None, period="monthly"):
    """
    Single endpoint for the NDT Analytics Dashboard.
    Returns KPIs, chart data, recent inspections, etc.
    """
    today = getdate()
    if not from_date:
        from_date = get_first_day(today)
    if not to_date:
        to_date = today

    from_date = getdate(from_date)
    to_date = getdate(to_date)

    return {
        "kpis": _get_kpis(from_date, to_date),
        "inspections_by_branch": _get_inspections_by_branch(from_date, to_date),
        "inspection_trend": _get_inspection_trend(from_date, to_date, period),
        "work_order_status": _get_work_order_status(),
        "equipment_by_type": _get_equipment_by_type(),
        "acceptance_rate": _get_acceptance_rate(from_date, to_date),
        "recent_inspections": _get_recent_inspections(),
    }


def _get_kpis(from_date, to_date):
    total_inspections = frappe.db.count("MT Inspection", filters={
        "date_of_test": ["between", [from_date, to_date]]
    })
    total_work_orders = frappe.db.count("Work Order")
    pending_approval = frappe.db.count("MT Inspection", filters={"docstatus": 0})
    accepted = frappe.db.count("MT Inspection", filters={
        "docstatus": 1,
        "date_of_test": ["between", [from_date, to_date]]
    })
    equipment_count = frappe.db.count("Equipment Master")

    return {
        "total_inspections": total_inspections or 0,
        "total_work_orders": total_work_orders or 0,
        "pending_approval": pending_approval or 0,
        "accepted": accepted or 0,
        "equipment_count": equipment_count or 0,
    }


def _get_inspections_by_branch(from_date, to_date):
    data = frappe.db.sql("""
        SELECT b.name AS branch,
               COALESCE(SUM(CASE WHEN m.name IS NOT NULL THEN 1 ELSE 0 END), 0) AS count
        FROM `tabBranch Master` b
        LEFT JOIN `tabMT Inspection` m
            ON m.branch = b.name
            AND m.date_of_test BETWEEN %s AND %s
        GROUP BY b.name
        ORDER BY count DESC, b.name ASC
    """, (from_date, to_date), as_dict=True)
    return data


def _get_inspection_trend(from_date, to_date, period="monthly"):
    if period == "daily":
        group_expr = "DATE(date_of_test)"
        date_fmt = "%Y-%m-%d"
    elif period == "weekly":
        group_expr = "DATE(date_of_test - INTERVAL WEEKDAY(date_of_test) DAY)"
        date_fmt = "%Y-%m-%d"
    else:  # monthly
        group_expr = "DATE_FORMAT(date_of_test, '%%Y-%%m-01')"
        date_fmt = "%Y-%m"

    query = """
        SELECT """ + group_expr + """ AS period_start,
               COUNT(*) AS count
        FROM `tabMT Inspection`
        WHERE date_of_test BETWEEN %s AND %s
        GROUP BY period_start
        ORDER BY period_start ASC
    """
    data = frappe.db.sql(query, (from_date, to_date), as_dict=True)

    # Format labels
    for row in data:
        if row.period_start:
            d = getdate(str(row.period_start))
            if period == "daily":
                row["label"] = d.strftime("%d %b")
            elif period == "weekly":
                row["label"] = "W/" + d.strftime("%d %b")
            else:
                row["label"] = d.strftime("%b %Y")
        else:
            row["label"] = "—"

    return data


def _get_work_order_status():
    data = frappe.db.sql("""
        SELECT status, COUNT(*) AS count
        FROM `tabWork Order`
        GROUP BY status
        ORDER BY FIELD(status, 'Open', 'In Progress', 'Completed', 'Cancelled')
    """, as_dict=True)
    return data


def _get_equipment_by_type():
    data = frappe.db.sql("""
        SELECT equipment_type AS type, COUNT(*) AS count
        FROM `tabEquipment Master`
        WHERE equipment_type IS NOT NULL AND equipment_type != ''
        GROUP BY equipment_type
        ORDER BY count DESC
    """, as_dict=True)
    return data


def _get_acceptance_rate(from_date, to_date):
    data = frappe.db.sql("""
        SELECT r.result, COUNT(*) AS count
        FROM `tabMT Inspection Result` r
        INNER JOIN `tabMT Inspection` m ON m.name = r.parent
        WHERE m.date_of_test BETWEEN %s AND %s
            AND r.result IN ('Acceptable', 'Rejectable')
        GROUP BY r.result
    """, (from_date, to_date), as_dict=True)
    return data


def _get_recent_inspections():
    inspections = frappe.db.sql("""
        SELECT name, date_of_test, branch, mt_variant, docstatus, client
        FROM `tabMT Inspection`
        ORDER BY creation DESC
        LIMIT 8
    """, as_dict=True)
    return inspections
