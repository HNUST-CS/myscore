dynamicWebService = '.'
$(document).ready ->
	js = ''

	settleFile = (js)->
		console.log js.detail
		for semester,se of js.detail
			console.log semester
			for i,msg of se
				console.log msg.title
				console.log msg.score
				console.log msg.grade		

	$('#search-btn').click ->
		$('.jumbotron').slideUp();
		number = $('#input1').val();
		console.log number
		number = '1205030209.html'
		url = dynamicWebService + '/api/score/' + number
		$.get url,((result,status,xhr) ->
			console.log result+status
			settleFile result
		),'json'
		return false;

