// https://datatables.net/download/index
// Datatable configurations
// Styling framework: Bootstrap 5
// Packages: jQuery 3, DataTables
// Extensions: DateTime, Responsive, SearchBuilder, SearchPanes, StateRestore
// Download method: Minify, Concetenate

$(function () {
	generate_table('https://raw.githubusercontent.com/kaiying1991/pokemon-go/master/data/json/pvp_moves.json');
});

function generate_table (dataUrl, tableSelector = '#tableDefault') {
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
			$(`${tableSelector} thead`).append('<tr></tr>');
			Object.entries(jsond[0]).forEach(([k, v], i) => cols.push({ data: k, title: k }));

			let tableOptions = {
				data: jsond,
				columns: cols,
				pageLength: 10,
				stateSave: true
			};

			let table = $(tableSelector).DataTable(tableOptions);
			cols.forEach((col, i) => {
				let autofocus = i == 0 ? 'autofocus' : '';
				table.column(i).title(`<input type="text" class="col-12" placeholder="${col.title}" data-index="${i}" ${autofocus}/>`)
			});

			$(table.table().container()).on('keyup', 'thead input', (e) => {
				let elem = e.currentTarget;
				table.column($(elem).data('index')).search(elem.value).draw();
			});
		});
}