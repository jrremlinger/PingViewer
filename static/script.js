let max = 0;
let dataArr = [];

let socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {});

function writeData(data) {
	dataArr[max] = data;
	$('#dataLog').html(`<tr id='data_${max}'><td>${data.ip}</td><td>${data.type}</td><td>${data.id}</td><td>${data.seq}</td><td>${data.len}</td></tr>` + $('#dataLog').html());
	max++;
	updateFilter();
}

function updateFilter() {
	if ($('#ipFilterCheck').prop('checked')) {
		for (i in dataArr) {
			if (!dataArr[i].ip.includes(($('#ipFilter').val()))) {
				$('#data_' + i).hide();
			} else {
				filterProtocol(i);
			}
		}
	} else {
		for (i in dataArr) {
			filterProtocol(i);
		}
	}
}

function filterProtocol(index) {
	if (dataArr[index].type == 'ICMP' && $('#ipv4Check').prop('checked')) {
		filterLength(index);
	} else if (dataArr[index].type == 'ICMP' && !$('#ipv4Check').prop('checked')) {
		$('#data_' + index).hide();
	} else if (dataArr[index].type == 'ICMP6' && $('#ipv6Check').prop('checked')) {
		filterLength(index);
	} else if (dataArr[index].type == 'ICMP6' && !$('#ipv6Check').prop('checked')) {
		$('#data_' + index).hide();
	}
}

function filterLength(index) {
	if ($('#lengthFilterCheck').prop('checked')) {
		if ($('#filterOperator').val() == "equals") {
			if (dataArr[index].len == $('#lengthFilter').val()) {
				$('#data_' + index).show();
			} else {
				$('#data_' + index).hide();
			}
		} else if ($('#filterOperator').val() == "greater") {
			if (dataArr[index].len > $('#lengthFilter').val()) {
				$('#data_' + index).show();
			} else {
				$('#data_' + index).hide();
			}
		} else if ($('#filterOperator').val() == "less") {
			if (dataArr[index].len < $('#lengthFilter').val()) {
				$('#data_' + index).show();
			} else {
				$('#data_' + index).hide();
			}
		}
	} else {
		$('#data_' + index).show();
	}
}


socket.on('send data', function(data) { writeData(JSON.parse(data)); });