// Copyright (c) 2024, Build with DC Yadav and contributors
// For license information, please see license.txt

frappe.ui.form.on("Printrove Settings", {
	refresh(frm) {
        const btn = frm.add_custom_button("Sync Product Now", () => {
            frappe.call({
                method:"printrov_merch_store.tasks.sync_products_from_printrove", btn
            }), then (() => {
                frappe.show_alert({message:"Stored Product Synced Successfully!", indicator:"green"})

            })
        })

    },
});
