function op(val){
	var httpReq = new XMLHttpRequest();
	url = "/control.py?op=" + val + '&time=' + new Date();
	httpReq.open("GET",url,false);
	httpReq.send(null);

	if(val == "photo" || val == "face"){
		document.getElementById("img").innerHTML =
		'<img src="/image.jpg?' + Math.random() + '" />';
	}
		
}
