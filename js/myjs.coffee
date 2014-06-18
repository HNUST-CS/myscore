dynamicWebService = '.'
$(document).ready ->
	js = ''
	fail = ->
		$('#p-msg').find('tr')

	settleFile = (js)->
		t = 0;cnt = 0;
		$('#p-score').append("<tr class='0 1 2 3 4 5 6 7 8'>
					<th>课程</th>
					<th>学分</th>
					<th>成绩</th>
				</tr>")
		for i,j of js
			console.log i,j
			$('#p-msg').find('tr').eq(1).find('td').eq(t++).text(j)
		for semester,se of js.detail
			console.log semester
			$('.btn-group').prepend("<button data-tri='#{cnt}' class='btn btn-primary'>#{semester}</button>")
			for i,msg of se
				console.log msg.title
				console.log msg.score
				console.log msg.grade
				$('#p-score').append("<tr class='#{cnt}'>
					<td>#{msg.title}</td>
					<td>#{msg.grade}</td>
					<td>#{msg.score}</td>
				</tr>")
			cnt++;
		$('#p-score tr').not('.'+(cnt-1)).hide();

	$('#search-btn').click ->
		$('.jumbotron').slideUp()
		number = $('#input1').val()
		console.log number
		number = '1205030209.html'
		url = dynamicWebService + '/api/score/' + number
		$.get url,((result,status,xhr) ->
			$('#p-score').empty();
			settleFile result
			$('.score-show-box').fadeIn()
		),'json'
		return false
	$('.btn-group').on 'click','.btn', ->
		hsClass = $(this).attr('data-tri');
		$('#p-score tr').show().not('.'+ hsClass).hide()

