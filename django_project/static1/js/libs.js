function doRateLD( rate, id ) {
	ShowLoading('');
	$.get(dle_root + "engine/ajax/controller.php?mod=rating", { go_rate: rate, news_id: id, skin: dle_skin, user_hash: dle_login_hash }, function(data){
		HideLoading('');
		if ( data.success ) {
			var rating = data.rating;
			rating = rating.replace(/&lt;/g, "<");
			rating = rating.replace(/&gt;/g, ">");
			rating = rating.replace(/&amp;/g, "&");
			$("#ratig-layer-" + id).html(rating);
			$("#vote-num-id-" + id).html(data.votenum);
			var rt = parseInt($(rating).text());
			var ms = (data.votenum - rt)/2;
			var ps = data.votenum - ms;
			var cr = (Math.round((data.votenum - (data.votenum - rt)/2)/data.votenum*100))/10;
			$("#ps-" + id).children('.psc').text(ps);
			$("#ms-" + id).children('.msc').text(ms);
			$('.slide-circle > div').html(cr+'<div>рейтинг</div>');
			$('.slide-circle').circleProgress({value: cr/10});
		} else if (data.error) {DLEalert ( data.errorinfo, dle_info );}
	}, "json");
};