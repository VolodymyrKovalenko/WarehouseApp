/*APPLICATION FOR RECEIPT*/

let input = document.getElementById('amount');

input.onfocus = function(){
	let tooltip = document.createElement('div');
	tooltip.classList.add('tooltip1');
	tooltip.innerHTML = "Price: 0";
	document.body.append(tooltip);
	let coords = input.getBoundingClientRect();
	tooltip.style.left = coords.left +'px';
	if(coords.top - tooltip.offsetHeight - 10 < 0) tooltip.style.top = coords.bottom + 10 + 'px';
	else tooltip.style.top = coords.top - tooltip.offsetHeight - 10 + 'px';
}
input.oninput = function(){	
	let tooltip = document.querySelector('.tooltip1');
	tooltip.innerHTML = "Price:" + (input.value * 5) + ' UAH'; //мінять ціну тут
}
input.onblur = function() {
	let tooltip = document.querySelector('.tooltip1');
	tooltip.remove();	
}
