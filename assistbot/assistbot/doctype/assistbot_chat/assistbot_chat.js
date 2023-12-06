// Copyright (c) 2023, Chua Jun Jie and contributors
// For license information, please see license.txt

frappe.ui.form.on('AssistBot Chat', {
	assistbot_execute(frm){
		frm.call({
			method:"execute_instruction",
			args:{
				doc:frm.doc
			},
			callback:function(r){
				console.log(r.message)
			},
		})
	}
});
