// https://datatables.net/download/index
// Datatable configurations
// Styling framework: Bootstrap 5
// Packages: jQuery 3, DataTables
// Extensions: DateTime, Responsive, SearchBuilder, SearchPanes, StateRestore
// Download method: Minify, Concetenate

var table = null;
let defaultJson = 'pokemon';

$(function () {
	fetchOptions();
});

function initDefaultSelectOption () {
	$("#typeDdl").val(`${defaultJson}.json`);
	typeChanged($("#typeDdl"));
}

function typeChanged (elem) {
	let selected = $(elem).val();
	if (selected.length == 0) {
		return;
	}

	generateTable(`https://raw.githubusercontent.com/sheppy9/pokemon-go/master/data/json/${selected}`);
}

function fetchOptions () {
	fetch('https://api.github.com/repos/sheppy9/pokemon-go/contents/data/json')
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok ' + response.statusText);
			}
			return response.json();
		})
		.then(data => {
			data.forEach((d, i) => {
				let name = d.name;
				let dname = name.split('.')[0].split('_').map(_ => _.replace(/^./, _[0].toUpperCase())).join(' ');
				$("#typeDdl").append(`<option value="${name}">${dname}</option>`);
			});

			initDefaultSelectOption();
		});
}

function generateTable (dataUrl, tableSelector = '#tableDefault') {
	fetch(dataUrl)
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok ' + response.statusText);
			}
			return response.text();
		})
		.then(data => {
			let jsond = JSON.parse(data);
			if (jsond == null || jsond.length == 0) {
				return;
			}

			let cols = [];
			Object.entries(jsond[0]).forEach(([k, v], i) => cols.push({ 'data': k, 'title': k }));

			let tableOptions = {
				data: jsond,
				destroy: true,
				columns: cols,
				pageLength: 10,
				stateSave: true,
				autoWidth: true,
				searching: true,
				processing: true,
				responsive: true,
				deferRender: true,
				layout: {
					topStart: 'search',
					topEnd: 'pageLength',
					bottomStart: 'paging',
					bottomEnd: 'info'
				}
			};

			table?.destroy();
			$(`${tableSelector} thead`).empty();
			$(`${tableSelector} tbody`).empty();
			table = $(tableSelector).DataTable(tableOptions);
// 			cols.forEach((col, i) => {
// 				let autofocus = i == 0 ? 'autofocus' : '';
// 				table.column(i).title(`<input type="text" class="col-12" placeholder="${col.title}" data-index="${i}" ${autofocus}/>`);
// 			});
// 
// 			$(table.table().container()).on('keyup', 'thead input', (e) => {
// 				let elem = e.currentTarget;
// 				table.column($(elem).data('index')).search(elem.value).draw();
// 			});
		});
}