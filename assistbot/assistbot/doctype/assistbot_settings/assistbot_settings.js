// Copyright (c) 2023, Chua Jun Jie and contributors
// For license information, please see license.txt

frappe.ui.form.on('AssistBot Settings', {
	openai_verify_key(frm){
		frm.call({
			method:"verify_key",
			args:{
				doc: frm.doc
			},
			callback:function(r){
				console.log(r.message)
			},
		})
	},
	function(){
		window.close();
	}
});
