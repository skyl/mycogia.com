jQuery.fn.nginxUploadProgress = function(settings) {
	return this.each(function(){
		$(this).submit(function() {
			settings = jQuery.extend({
				interval: 2000,
				progress_bar_id: "progressbar",
				nginx_progress_url: "/progress"
			}, settings);
		
			/* generate random progress-id */
			var uuid = "";
			for (i = 0; i < 32; i++) { uuid += Math.floor(Math.random() * 16).toString(16); }
			/* patch the form-action tag to include the progress-id */
			$(this).attr("action", $(this).attr("action") + "?X-Progress-ID=" + uuid);
		
			this.timer = window.setInterval(function() { jQuery.nginxUploadProgress(this, settings['nginx_progress_url'], settings['progress_bar_id'], uuid) }, settings['interval']);
		});
	});
};

jQuery.nginxUploadProgress = function(e, nginx_progress_url, progress_bar_id, uuid) {
	$.ajax({
		type: "GET",
		url: nginx_progress_url,
		dataType: "json",
		beforeSend: function(xhr) {
			xhr.setRequestHeader("X-Progress-ID", uuid);
		},
		success: function(upload) {
			/* change the width if the inner progress-bar */
			if (upload.state == 'uploading') {
				bar = $('#'+progress_bar_id);
				w = Math.floor((upload.received / upload.size)*100);
				bar.width(w + '%');
			}
			/* we are done, stop the interval */
			if (upload.state == 'done') {
				window.clearTimeout(e.timer);
			}
		}
	});
};