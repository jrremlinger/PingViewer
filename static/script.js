let max = 0;
let dataArr = [];

let socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {});

function writeData(data) {
	dataArr[max] = data;
	$('#dataLog').html(`<tr id='data_${max}'><td>${data.ip}</td><td>${data.type}</td><td>${data.id}</td><td>${data.seq}</td><td>${data.len}</td></tr>` + $('#dataLog').html());
	max++;
}

socket.on('send data', function(data) { writeData(JSON.parse(data)); });