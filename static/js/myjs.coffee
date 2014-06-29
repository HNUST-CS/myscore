dynamicWebService = '.'

$('#input1').click ->
	$('.verif').slideDown('fast')

$('#update-bt').click ->
	$('#update-ct').load('static/update.html')


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

	#处理成绩数据
	settleFile = (js,id)->
		t = 0;cnt = 0;
		#$('#id-confirm-btn').attr('name',id)
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

		sor = []; i =0
		for semester,se of js.detail
			sor[i++] = semester
		sor = sor.sort (a,b) ->
			if a > b 
				return -1
			if a < b
				return 1
			else
				return 0
		i--
		j = 0
		while j < sor.length
			semester = sor[j]
			se = js.detail[ semester ]
			$('#switch').append("<button id='"+"#{cnt}"+"' data-tri='"+"#{cnt}"+"' class='col-xs-6 col-sm-2 btn btn-primary'>#{semester}</button>")
			for i,msg of se
				$('#p-score').append("<tr class='#{cnt}'>
					<td>#{msg.title}</td>
					<td>#{msg.grade}</td>
					<td>#{msg.score}</td>
				</tr>")
			cnt++;
			j++
		$('#0').mousedown()
		$('#p-score tr').not('.'+ 0).hide()
		checkFailCourse()
	#清除旧数据
	clear = ->
		$('#p-score').empty();
		$('#switch').empty();
		$('#p-msg').find('tr').eq(1).find('td').empty();
		$('#class-ct').empty();
		$('#input1,#sfz-4').removeClass('has-error')
		$('#ver-error').fadeOut('fast')

	#设定加载动画位置
	setPosition = ->
		outWidth = $('.container').innerWidth()
		$('.sonic').css('left',(outWidth/2-50)+'px')

	#点击GO按钮 进行查询
	$('#search-btn').click ->
		number = $('#input1').val()
		sfz = $('#sfz-4').val().toUpperCase()
		if number is '' or sfz is ''
			$("#input1,#sfz-4").addClass('has-error')
			return false
		$(circle.canvas).appendTo('#score-search-box').fadeIn()
		setPosition()

		#$('#class_score').attr('disabled','disabled')
		clear()
		stat = 0
		url = dynamicWebService + '/api/score/' + number + '/' + sfz
		$.ajax
			'type':'GET'
			'url':url
			'dataType':'json'
			'success':(result) ->
				console.log result
				if result.error
					$('#ver-error').show().text(result.msg)
					$('#input1,#sfz-4').addClass('has-error')
					$('.sonic').fadeOut();
				else		
					jsonData = result
					settleFile result,number
					$('.jumbotron').slideUp()
					$('.verif').slideUp()
					$('.score-show-box').fadeIn()
					$('#class_score').attr('disabled',false)
					$('.sonic').fadeOut();
			'error':(a,b,c)->
				$('#ver-error').show().text("与服务器连接错误")
				$('#input1,#sfz-4').addClass('has-error')
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
	###
	pwidth = 0
	settleProgress = ->
		pwidth += 0.02272727273
		$('#class-progress').width(pwidth + '%')
		if pwidth >= 1.0
			$('.progress').fadeOut ->
				$('#class-progress').width(0)
				pwidth = 0
	###

	#处理全班成绩数据
	###
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
		$('#0').click()
	###
	###
	settleClassFile = (js,id)->
		t = 0;cnt = 0;
		$("#p-score-#{id}").append("
				<tr class='0 1 2 3 4 5 6 7 8'>
					<th>课程</th>
					<th>学分</th>
					<th>成绩</th>
				</tr>")
		$("#p-score-#{id}").parent('table').before("<button class='btn btn-success btn-xs no-radius'> 学号：#{id}　姓名：#{js['name']} </button> </p>")
		for semester,se of js.detail
			console.log semester
			for i,msg of se
				$("#p-score-#{id}").append("<tr class='#{cnt}'>
					<td>#{msg.title}</td>
					<td>#{msg.grade}</td>
					<td>#{msg.score}</td>
				</tr>")
			cnt++;
		$("#p-score-#{id} tr").not('.'+ 0).hide();
		checkFailCourse();
	###

	#全班成绩
	###
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
							settleProgress()
							settleClassFile result,stuNo
						'error':(a,b,c)->
							settleProgress()
				i++
			checkFailCourse()
		else
			$('#sfz-ipt').addClass('has-error');
		return false;
	###

	$('input').keydown ->
		$('#ver-error').fadeOut('fast')
		$(this).removeClass('has-error')



	$('#feedback-bt').click ->
		#$(circle.canvas).appendTo('#feedback-ct').fadeIn()
	$('#share-btn').click ->
		$(this).fadeOut 'fast', ->
			$('#ckepop').fadeIn 'fast'
	addcolors = [
    '#0c84b0',
    '#5ab39d',
    '#fdc32b',
    '#272822',
    '#3f4564',
    '#f69448',
    '#336699'
  ]
	doc = [
	  	'本站本来是我们突发奇想一个通宵做出来的小玩具',
	  	'没想到上线之后得到了这么多同学的支持',
	  	'很高兴本站能够带给同学们一点点的便捷',
	  	'看到同学们相继转发，评论，支持，我们真的非常感动',
	  	'所以尽管在期末到处是考试的情况下我们还是尽全力去维护',
	  	'每天1W,2W上涨的访问量更是给与我们了无限的动力',
	  	'由于撸主是大二学生，顶不住学校给"恐吓"和压力',
	  	'迫于无奈之举，今天正式关闭本网站',
	  	'不过，结束就是下一个开始',
	  	'未来我们肯定努力去做出更多更好玩的东西带给大家来分享。',
	  	'不管怎样最后还是要说一句',
	  	'-----谢谢！-----',
	  	'PS：不过我们还是迫使教务处封堵了一个很严重的漏洞，也算是做了一件好事',
	  	'PS-2：其实他们这样从技术上还是挡不住我们的，不过。。。',
	  	'-----END-----',
	  ]
	cnt=-1#用来计数m
	max=doc.length
	change = ->#切换背景颜色和主页文字
		cnt++;
		$('#sor-text').fadeOut('fast',->
			$(this).text(doc[cnt%max]);
		).fadeIn('slow');#文字切换
		
		$('.sorry').animate({backgroundColor: addcolors[cnt%7]});#背景颜色切换
		
	setInterval change,4000

	if $.cookie('no-record') isnt 'true'
		$('#record').modal('show')

	$('#record-bt').click ->
		if document.getElementsByClassName('no-record')[0].checked is true
			$.cookie('no-record','true')