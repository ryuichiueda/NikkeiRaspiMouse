function op(val){
	var httpReq = new XMLHttpRequest();
	url = "/control.py?op=" + val;
	httpReq.open("GET",url,false);
	httpReq.send(null);
}
