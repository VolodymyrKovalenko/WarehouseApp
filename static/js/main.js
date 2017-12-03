/*APPLICATION FOR RECEIPT*/

let input = document.getElementById('amount');
if(input){
	if(category.value != parseInt(category.value)) var priceForUnit = 1
	else priceForUnit = category.value;

	var priceForCategory = 12 + priceForUnit;

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
			tooltip.innerHTML = "Shoes - 13 UAH; Outerwere - 14 UAH; Pants - 15 UAH; per unit"; //мінять ціну тут
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

let acceptedApp = document.getElementById('acceptedApp');
let filledInApp = document.getElementById('filledInApp');
let mainTable = document.getElementsByClassName('mainTable')[0];

if(acceptedApp && filledInApp){

	acceptedApp.onclick = function(){
		for (let i = 0; i < mainTable.tBodies[0].rows.length; i++) {
			if(mainTable.tBodies[0].rows[i].cells[8].innerHTML == 'False')
				mainTable.tBodies[0].rows[i].hidden = true;
			if(mainTable.tBodies[0].rows[i].cells[8].innerHTML == 'True')
				mainTable.tBodies[0].rows[i].hidden = false;
			mainTable.tBodies[0].rows[i].cells[10].hidden = true;
			mainTable.tHead.rows[0].cells[10].hidden = true;
		}
	}

	filledInApp.onclick = function(){
		for (let i = 0; i < mainTable.tBodies[0].rows.length; i++) {
			if(mainTable.tBodies[0].rows[i].cells[8].innerHTML == 'False')
				mainTable.tBodies[0].rows[i].hidden = false;
			if(mainTable.tBodies[0].rows[i].cells[8].innerHTML == 'True')
				mainTable.tBodies[0].rows[i].hidden = true;
			mainTable.tBodies[0].rows[i].cells[10].hidden = true;
			mainTable.tHead.rows[0].cells[10].hidden = true;
		}
	}

	allApp.onclick = function(){
		for (let i = 0; i < mainTable.tBodies[0].rows.length; i++) {
			mainTable.tBodies[0].rows[i].hidden = false;
		}
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