// navbar_override.js — Custom profile dropdown for AL HOTY
// Loaded globally via app_include_js in hooks.py.
// Extends frappe.ui.toolbar.Toolbar (defined in Frappe's bundle before this runs)
// to replace settings_dropdown with 4 custom items, then styles Logout after render.

frappe.provide("alhoty.toolbar");

// Alias: some cached navbar HTML may call alhoy (without 't') — keep both working
frappe.provide("alhoy.toolbar");
Object.defineProperty(window, "alhoy", { get: function(){ return alhoty; }, configurable: true });

// ── 1. Extend Toolbar — runs BEFORE instantiation, modifies boot data ──
(function () {
	const _OriginalToolbar = frappe.ui.toolbar.Toolbar;

	frappe.ui.toolbar.Toolbar = class AlhotyToolbar extends _OriginalToolbar {
		constructor() {
			// Inject our 4 items before the navbar template is rendered
			if (frappe.boot && frappe.boot.navbar_settings) {
				frappe.boot.navbar_settings.settings_dropdown = alhoty.toolbar._dropdown_items();
			}
			super();
		}
	};
})();

// ── 2. After toolbar renders: enforce not-full-width default + style logout ──
$(document).on("toolbar_setup", function () {
	// Default is NEVER full-width. Only apply full-width if the user explicitly
	// clicked "Toggle Width" during this browser session (sessionStorage marker).
	if (!sessionStorage.getItem("ndt_fw_on")) {
		localStorage.setItem("container_fullwidth", "false");
		document.body.classList.remove("full-width");
	}
	alhoty.toolbar._apply_logout_style();
});

// ── 3. Dropdown item definitions ──
alhoty.toolbar._dropdown_items = function () {
	return [
		{
			item_label: "My Settings",
			action: "frappe.set_route('Form', 'User', frappe.session.user); return false;",
		},
		{
			item_label: "Toggle Width",
			action: "frappe.ui.toolbar.toggle_full_width(); var fw=localStorage.getItem('container_fullwidth')==='true'; if(fw){sessionStorage.setItem('ndt_fw_on','1');}else{sessionStorage.removeItem('ndt_fw_on');} return false;",
		},
		{
			item_label: "Logout",
			action: "frappe.app.logout(); return false;",
		},
	];
};

// ── 4. Mark logout button so SCSS can style it ──
alhoty.toolbar._apply_logout_style = function () {
	$("#toolbar-user .dropdown-item, #toolbar-user button.dropdown-item").each(function () {
		if ($(this).text().trim() === __("Logout")) {
			$(this).addClass("alhoty-logout-btn");
		}
	});
};

// ── 5. Theme toggle — live switch, no page reload needed ──
alhoty.toolbar.toggle_theme = function () {
	const root = document.documentElement;
	const current = root.getAttribute("data-theme-mode") || "light";
	const next = current === "dark" ? "light" : "dark";

	// Update DOM immediately for instant feedback
	root.setAttribute("data-theme-mode", next);
	root.setAttribute("data-theme", next);

	frappe.show_alert({ message: __("Theme changed to {0}", [__(next.charAt(0).toUpperCase() + next.slice(1))]), indicator: "blue" }, 2);

	// Persist to user profile
	frappe.xcall("frappe.core.doctype.user.user.switch_theme", {
		theme: next.charAt(0).toUpperCase() + next.slice(1),
	});
};
