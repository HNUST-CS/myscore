dynamicWebService = '.'
$(document).ready ->
	js = ''
	checkFailCourse = ->
		$('#p-score').find('tr').each ->
			content = $(this).find('td').eq(2)
			score = content.text()
			if score is '不及格' or score is ''
				content.addClass('danger')
			score = parseInt score
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
			$('#switch').prepend("<button data-tri='#{cnt}' class='col-xs-6 col-sm-2 btn btn-primary'>#{semester}</button>")
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
		checkFailCourse()

	clear = ->
		$('#p-score').empty();
		$('#switch').empty();
		$('#p-msg').find('tr').eq(1).find('td').empty();

	$('#search-btn').click ->
		number = $('#input1').val()
		if number is ''
			$('#input1').addClass('has-error')
			return false
		$('#input1').removeClass('has-error')
		$('#class_score').attr('disabled','disabled')
		clear()
		stat = 0
		url = dynamicWebService + '/api/score/' + number
		$.ajax
			'type':'GET'
			'url':url
			'dataType':'json'
			'success':(result) ->
				settleFile result,number
				$('.jumbotron').slideUp()
				$('.score-show-box').fadeIn()
				$('#class_score').attr('disabled',false)
			'error':(a,b,c)->
				$('#input1').addClass('has-error')

		return false
	$('#id-confirm-btn').click ->




	$('#switch').on 'click','.btn', ->
		hsClass = $(this).attr('data-tri');
		$('#p-score tr').show().not('.'+ hsClass).hide()

	waveloop1 = ->
		$("#banner_bolang_bg_1").css({"left":"-236px"}).animate("left":"-1233px",25000,'linear',waveloop1)
	waveloop2 = ->
		$("#banner_bolang_bg_2").css({"left":"0px"}).animate("left":"-1009px",60000,'linear',waveloop2)

	waveloop1()
	waveloop2()	
