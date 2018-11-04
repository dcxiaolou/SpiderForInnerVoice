
http://m.xinli001.com/lesson/tagList?tag_name=free&page=1&size=20&lesson_type=normal 可直接使用，可获得课程引导信息，返回josn文件
提取内容： id：课程编号  title：标题  cover：封面  joinnum：加入课程的人数  teacherName：老师名称

http://m.xinli001.com//lesson/272  -> id 	
获取课程页面详细介绍  

https://m.xinli001.com/lesson/rate-list?lesson_id=194&page=1&size=10 可直接获取课程评论，返回json数据

https://m.xinli001.com/lesson/getPeriodList?lesson_id=194&__from__=detail  可直接获取课程各个目录的标题
title：各个目录的标题  duration：课程时长  video_id：视频id  is_video: 1为MP4  0为MP3

video_id分解 605ea32beeff8e75d23d0b170f9fa071_6 --> 605ea32bee  1_6 : 1 --> 1   1_6:   61-->1 

https://plvod01.videocc.net/605ea32bee/1/605ea32beeff8e75d23d0b170f9fa071_1.mp3

introduce 下的 1.josn 表示课程1的简介
introduce: 视频简介

detail 下的 1_1.json
	1表示课程的编号
	_1表示该课程下的第几个

编号为194的课程太多，只取前100个

medio: 视频连接