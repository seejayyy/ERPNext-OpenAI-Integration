// Copyright (c) 2023, Chua Jun Jie and contributors
// For license information, please see license.txt

frappe.ui.form.on('AssistBot Chat', {
	submit_message: function(frm){
		frm.call({
			method:"submit_message",
			args:{
				doc:frm.doc
			},
			callback:function(r){
				console.log(r.message)
			},
		})
	}
});
