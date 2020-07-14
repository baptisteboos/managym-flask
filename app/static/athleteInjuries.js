function Add(){
	var url =  window.location.pathname + '/_add_injury';
	$.post(url, {
    }).done(function(response) {
		$('#tblInjuriesData >tbody').prepend(
			"<tr data-info-id='"+response['id']+"'>"+
			"<td class='col-sm-10'>"+
			"<p><b>"+
			response['author_first_name']+" "+response['author_last_name']+" - "+
			moment().format('LL')+":"+
			"</b></p>"+
			// "<p contenteditable='true'></p>"+
			"<div><textarea class='form-control' rows='3' placeholder='Write something...'></textarea></div>"+
			"</td>"+
			"<td class='col-sm-1'>"+
			"<ul class='list-inline'>"+
			"<li>"+
			"<button class='btn btn-success btn-sm rounded-0 btn-save' type='button' data-toggle='tooltip' data-placement='top' title='Save'><i class='glyphicon glyphicon-save'></i></button>"+
			"</li>"+
			"<li>"+
			"<button class='btn btn-danger btn-sm rounded-0 btn-delete' type='button' data-toggle='tooltip' data-placement='top' title='Delete'><i class='glyphicon glyphicon-trash'></i></button>"+
			"</li>"+
			"</ul>"+
			"</tr>"
		)
		$(".btn-save").bind("click", Save);		
		$(".btn-delete").bind("click", Delete);
    }).fail(function() {
            alert('problem with the server...');
    });

};	

function Save(){
	var url =  window.location.pathname + '/_update_injury';
	var par = $(this).closest('tr'); //tr
	var tdDataContent = par.children("td:nth-child(1)").children('div');
	var tdDataAuhor = par.children("td:nth-child(1)").children('p');
	var tdButtons = par.children("td:nth-child(2)");
	$.post(url, {
		info_id: $(par).attr('data-info-id'),
		// info_body: $(tdDataContent).text()
		info_body: $(tdDataContent).children('textarea').val()
    }).done(function(response) {
		// tdDataContent.attr('contenteditable', 'false');
		tdDataContent.text(tdDataContent.children('textarea').val());
		tdButtons.find('li').first().html("<button class='btn btn-success btn-sm rounded-0 btn-edit' type='button' data-toggle='tooltip' data-placement='top' title='Edit'><i class='glyphicon glyphicon-edit'></i></button>");

		$(".btn-edit").bind("click", Edit);
	}).fail(function() {
		alert('problem with the server...');
	})
}; 	

function Edit(){
	var par = $(this).closest('tr'); //tr
	var tdDataAuhor = par.children("td:nth-child(1)").children('p');
	var tdDataContent = par.children("td:nth-child(1)").children('div');
	var tdButtons = par.children("td:nth-child(2)");

	// tdDataContent.attr('contenteditable', 'true');
	tdDataContent.html("<textarea class='form-control' rows='3'>"+tdDataContent.text().trim()+"</textarea>");
	tdButtons.find('li').first().html("<button class='btn btn-success btn-sm rounded-0 btn-save' type='button' data-toggle='tooltip' data-placement='top' title='Save'><i class='glyphicon glyphicon-save'></i></button>");
	$(".btn-save").bind("click", Save);
};

function Delete(){
	var url =  window.location.pathname + '/_delete_injury';
	var par = $(this).closest('tr'); //tr
	$.post(url, {
		info_id: $(par).attr('data-info-id')
    }).done(function(response) {
		par.remove();
	}).fail(function() {
		alert('problem with the server...');
	})
}; 

$(document).ready(function(){
	$(function () {
	    $('[data-toggle="tooltip"]').tooltip()

	 //Add, Save, Edit and Delete functions code
	$(".btn-edit").bind("click", Edit);
	$(".btn-delete").bind("click", Delete);
	$("#btn-add").bind("click", Add);
	 });
})