frappe.ui.form.on("Report", {
	refresh: function (frm) {
        let doc = frm.doc;
		if (!doc.__islocal && doc.report_type == "Query Report") {
            frm.add_custom_button(__("Text2SQL"), function(){
                let d = new frappe.ui.Dialog({
                    title: 'Enter you query',
                    fields: [
                        {
                            label: 'Text',
                            fieldname: 'question',
                            fieldtype: 'Small Text'
                        }
                    ],
                    size: 'small',
                    primary_action_label: 'Submit',
                    primary_action(values) {
                        frappe.call({
                            method: "texttosql.text_to_sql.report.get_gemini_response",
                            args: {
                                question: values.question,
                            },
                            freeze: true,
			                freeze_message: __("Converting Your Text to SQL..."),
                            callback: function (r) {
                                frm.set_value('query', r.message);
                                frm.save()
                            },
                        });
                        d.hide();
                    }
                });
                
                d.show();				
            });
        }
    }
})