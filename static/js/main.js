/*APPLICATION FOR RECEIPT*/

let input = document.getElementById('amount');
if(input){
	input.onfocus = function(){
		let tooltip = document.createElement('div');
		tooltip.classList.add('tooltip1');
		tooltip.innerHTML = "Enter value more then 0";
		document.body.append(tooltip);
		let coords = input.getBoundingClientRect();
		tooltip.style.left = coords.left +'px';
		if(coords.top - tooltip.offsetHeight - 10 < 0) tooltip.style.top = coords.bottom + 10 + 'px';
		else tooltip.style.top = coords.top - tooltip.offsetHeight - 10 + 'px';
	}
	input.oninput = function(){	
		let tooltip = document.querySelector('.tooltip1');
		if(input.value > 0) {
			tooltip.innerHTML = "Price:" + (input.value * 5) + ' UAH'; //мінять ціну тут			
		}
		else {			
			tooltip.innerHTML = "Uncorrect value";
		}
	}
	input.onblur = function() {
		let tooltip = document.querySelector('.tooltip1');
		tooltip.remove();	
	}
}

// MAIN PAGE

let currentApp = document.getElementById('currentApp');
let filledInApp = document.getElementById('filledInApp');
let mainTable = document.getElementsByClassName('mainTable')[0];

if(currentApp && filledInApp){

currentApp.onclick = function(){
	
	mainTable.tHead.rows[0].innerHTML = `
		<th data-type="string">Category</th>
		<th data-type="string">Type (Fason)</th>
		<th data-type="string">Manufacturer (Brand)</th>
		<th data-type="number">Model number</th>
        <th data-type="number">Quantity</th>
        <th data-type="number">Date adoption</th>
        <th data-type="number">Date issue</th>
        <th data-type="number">Price</th>`;
	mainTable.tBodies[0].innerHTML = `
	{% for sklad in NNNN_table_result %}
        <tr>
		    <td>{{ sklad.category }}</td>
			<td>{{ sklad.fason }}</td>
			<td>{{ sklad.brand }}</td>
			<td>{{ sklad.model }}</td>
		    <td>{{ sklad.quantity }}</td>
		    <td>{{ sklad.date_adoption }}</td>
		    <td>{{ sklad.date_issue }}</td>
		    <td>{{ sklad.price }}</td>
		</tr>
    {% endfor %}`
}
filledInApp.onclick = function(){
	
	mainTable.tHead.rows[0].innerHTML = `
		<th data-type="string">Category</th>
		<th data-type="string">Type (Fason)</th>
		<th data-type="string">Manufacturer (Brand)</th>
		<th data-type="number">Model number</th>
        <th data-type="number">Quantity</th>
        <th data-type="number">Date adoption</th>
        <th data-type="number">Date issue</th>`;
	mainTable.tBodies[0].innerHTML = `
	    {% for product in first_table_result %}
                        <tr>
                            <td>{{ product[1].category}}</td>
							<td>{{ product[1].fason }}</td>
							<td>{{ product[1].brand }}</td>
							<td>{{ product[1].model }}</td>
                            <td>{{ product[0].quantity }}</td>
                            <td>{{ product[0].date_adoption }}</td>
                            <td>{{ product[0].date_issue }}</td>
						</tr>
                    {% endfor %}
	}
}
if(mainTable){
mainTable.onclick = function(event){
		if(event.target.tagName != 'TH') return;
		let columnType = event.target.getAttribute('data-type');
		let columnIndex = event.target.cellIndex;
		sortColumn(columnType, columnIndex);
	}

	function sortColumn(type, index){
		let rowArray = [].slice.call(mainTable.getElementsByTagName('tbody')[0].rows);
		
		var compare;
		switch (type) {
			case 'number':
				compare = function(rowA, rowB){
					return rowA.cells[index].innerHTML - rowB.cells[index].innerHTML;
				}
				break;				
			case 'string':
				compare = function(rowA, rowB) {
		          return rowA.cells[index].innerHTML > rowB.cells[index].innerHTML;
		        };
				break;
		}

		rowArray.sort(compare);
		for (let i = 0; i < rowArray.length; i++) {
			mainTable.getElementsByTagName('tbody')[0].append(rowArray[i]);
		}
	}
}