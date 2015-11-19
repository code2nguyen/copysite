$(window).resize(function(){
    $(".vaadin-grid-style").height($(window).height() - 180);    
});

$(document).ready(function(){
         $(".vaadin-grid-style").height($(window).height() - 180);
});

function clearInput() {
	 document.getElementById('site').value = '';
};