// Copyright (c) 2025, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("CTF Candidate", {
	refresh(frm) {
		if (!frm.doc.setup_completed) {
			frm.add_custom_button(__("Setup Stages"), () => {
				frm.call("setup_stages").then(() => {
					frm.refresh();
				});
			});
		} else {
			frm.add_custom_button(__("Cleanup Stages"), () => {
				frm.call("cleanup_stages").then(() => {
					frm.refresh();
				});
			});
		}
	},
});
