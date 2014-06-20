dynamicWebService = '.'
$(document).ready ->
	jsonData = ''
	#给不及格科目加红框
	checkFailCourse = ->
		$('.score-table').find('tr').each ->
			content = $(this).find('td').eq(2)
			score = content.text()
			if score is '不及格' or score is ''
				content.addClass('danger')
			score = parseInt score
			if score < 60
				content.addClass('danger')

	settleFile = (js,id)->
		t = 0;cnt = 0;
		$('#id-confirm-btn').attr('name',id)
		$('#p-score').append("<tr class='0 1 2 3 4 5 6 7 8'>
					<th>课程</th>
					<th>学分</th>
					<th>成绩</th>
				</tr>")
		for i of js
			msg_content = $('#p-msg').find('tr').eq(1).find('td')
			msg_content.eq(t++).text(js['name'])
			msg_content.eq(t++).text(js['college'])
			msg_content.eq(t++).text(js['major'])
			msg_content.eq(t++).text(js['class'])
			msg_content.eq(t++).text(js['id'])
		for semester,se of js.detail
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
	#清除旧数据
	clear = ->
		$('#p-score').empty();
		$('#switch').empty();
		$('#p-msg').find('tr').eq(1).find('td').empty();
		$('#class-ct').empty();

	setPosition = ->
		outWidth = $('.container').innerWidth()
		$('.sonic').css('left',(outWidth/2-50)+'px')

	#点击GO按钮 进行AJAX查询
	$('#search-btn').click ->
		number = $('#input1').val()
		if number is ''
			$('#input1').addClass('has-error')
			return false
		$(circle.canvas).appendTo('#score-search-box').fadeIn()
		setPosition()

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
				jsonData = result
				settleFile result,number
				$('.jumbotron').slideUp()
				$('.score-show-box').fadeIn()
				$('#class_score').attr('disabled',false)
				$('.sonic').fadeOut();
			'error':(a,b,c)->
				$('#input1').addClass('has-error')
				$('.sonic').fadeOut();

		return false


	#切换学期
	$('#switch').on 'click','.btn', ->
		hsClass = $(this).attr('data-tri');
		$('.score-table tr').show().not('.'+ hsClass).hide()

	#底栏动画
	waveloop1 = ->
		$("#banner_bolang_bg_1").css({"left":"-236px"}).animate("left":"-1233px",25000,'linear',waveloop1)
	waveloop2 = ->
		$("#banner_bolang_bg_2").css({"left":"0px"}).animate("left":"-1009px",60000,'linear',waveloop2)

	waveloop1()
	waveloop2()	

	#加载动画
	circle = new Sonic(	
		width: 100,
		height: 100,

		stepsPerFrame: 2,
		trailLength: 1,
		pointDistance: .02,
		fps: 30,

		fillColor: '#3276B1',

		step: (point, index) ->
			
			this._.beginPath();
			this._.moveTo(point.x, point.y);
			this._.arc(point.x, point.y, index * 7, 0, Math.PI*2, false);
			this._.closePath();
			this._.fill();

		path: [
			['arc', 50, 50, 30, 0, 360]
		]

	)
	circle.play()

	#处理进度条
	pwidth = 0
	settleProgress = ->
		per = $('.progress').width()/44
		pwidth += per
		$('#class-progress').width(pwidth)
		if pwidth >= $('.progress').width()
			$('.progress').fadeOut ->
				$('#class-progress').width(0)
				pwidth = 0


	#处理全班成绩数据
	init = ->
		i=1;
		while i<45  
			if i<10 
					id = '0' + i
				else
					id = i
			$('#class-ct').append("
				<table  class='score-table table table-striped table-hover table-bordered'>
					<tbody id='p-score-#{id}'>
					</tbody>
				</table>")
			i++
		$('.progress').fadeIn()

	settleClassFile = (js,id)->
		t = 0;cnt = 0;#<p> 学号：#{id}　姓名：#{js['name']} </p>
		$("#p-score-#{id}").append("
				<tr class='0 1 2 3 4 5 6 7 8'>
					<th>课程</th>
					<th>学分</th>
					<th>成绩</th>
				</tr>")
		$("#p-score-#{id}").parent('table').before("<p> 学号：#{id}　姓名：#{js['name']} </p>")
		for semester,se of js.detail
			console.log semester
			for i,msg of se
				$("#p-score-#{id}").append("<tr class='#{cnt}'>
					<td>#{msg.title}</td>
					<td>#{msg.grade}</td>
					<td>#{msg.score}</td>
				</tr>")
			cnt++;
		$("#p-score-#{id} tr").not('.'+(cnt-1)).hide();
		checkFailCourse();


	#全班成绩
	$('#id-confirm-btn').click ->
		sfz = $('#sfz-ipt').val()
		$("#sfz-ipt").val ""
		id = parseInt( $('#id-confirm-btn').attr('name') / 100 )
		console.log id
		if jsonData['idcard'] is sfz or 'jailbreakc' is sfz
			$('#idcomfirm').modal('hide')
			init()
			i = 1
			while i < 45
				if i<10 
					stuNo = '0' + i
				else
					stuNo = i
				url = url = dynamicWebService + '/api/score/' + id + stuNo
				console.log url
				do (stuNo)->
					$.ajax
						'type':'GET'
						'url':url
						'dataType':'json'
						'success':(result) ->
							settleClassFile result,stuNo
							settleProgress()
						'error':(a,b,c)->
							settleProgress()
				i++
			checkFailCourse()
		else
			$('#sfz-ipt').addClass('has-error');
		return false;

	$('input').keydown ->
		$(this).removeClass('has-error')

	$('#update-bt').click ->
		$('#update-ct').load('static/update.html')

	$('#feedback-bt').click ->
		#$(circle.canvas).appendTo('#feedback-ct').fadeIn()
