dynamicWebService = '.'
$(document).ready ->
	js = ''
	fail = ->
		$('#p-score').find('tr').each ->
			content = $(this).find('td').eq(2)
			score = parseInt $(this).find('td').eq(2).text()
			if score < 60
				content.addClass('danger')

	settleFile = (js,id)->
		t = 0;cnt = 0;
		$('#id-confirm-btn').attr('data-id',id)
		$('#p-score').append("<tr class='0 1 2 3 4 5 6 7 8'>
					<th>课程</th>
					<th>学分</th>
					<th>成绩</th>
				</tr>")
		for i of js
			console.log i
			msg_content = $('#p-msg').find('tr').eq(1).find('td')
			msg_content.eq(t++).text(js['name'])
			msg_content.eq(t++).text(js['college'])
			msg_content.eq(t++).text(js['major'])
			msg_content.eq(t++).text(js['class'])
			msg_content.eq(t++).text(js['id'])
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
		fail()

	clear = ->
		$('#p-score').empty();
		$('.btn-group').empty();
		$('#p-msg').find('tr').eq(1).find('td').empty();

	$('#search-btn').click ->
		$('.jumbotron').slideUp()
		number = $('#input1').val()
		clear()
		console.log number
		url = dynamicWebService + '/api/score/' + number
		$.get url,((result,status,xhr) ->
			settleFile result,number
			$('.score-show-box').fadeIn()
		),'json'
		return false
	$('#id-confirm-btn').click ->




	$('.btn-group').on 'click','.btn', ->
		hsClass = $(this).attr('data-tri');
		$('#p-score tr').show().not('.'+ hsClass).hide()

