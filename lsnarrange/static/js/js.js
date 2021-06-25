
$(function () {
	echarts_1();
	function echarts_1() {
 		// 基于准备好的dom，初始化echarts实例
 		var myChart = echarts.init(document.getElementById('echart1'));
 option = {
	    tooltip: {
        trigger: 'axis',
        axisPointer: {
            lineStyle: {
                color: '#dddc6b'
            }
        }
    },
    grid: {
        left: '0',
		top: '10',
        right: '0',
        bottom: '0',
        containLabel: true
    },

    xAxis: [{
        type: 'category',
        boundaryGap: false,
		axisLabel:  {show:false},
        axisLine: {show:false},

   data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

    }, {

        axisPointer: {show: false},
        axisLine: {  show: false},

    }],

    yAxis: [{
        type: 'value',
        axisTick: {show: false},
        axisLine: {show:false},
       axisLabel:  {show:false},
        splitLine: {show:false}
    }],
    series: [
		{
        name: '治疗方案浏览量',
        type: 'line',
        smooth: true,
         symbol: 'none',
        symbolSize: 1,
        showSymbol: false,

        areaStyle: {
            normal: { color:'#ad29ec',opacity:1}
        },
			itemStyle: {
			normal: {
				color: '#ad29ec',
				borderColor: '#ad29ec',
				borderWidth: 12
			}
		},
        data: [2, 1, 3, 3, 6, 2, 3, 2, 4, 1, 2, 4]

    }, 

		 ]

};  
 		// 使用刚指定的配置项和数据显示图表。
 		myChart.setOption(option);
 		window.addEventListener("resize", function () {
 			myChart.resize();
 		});
 	}
})
$(function () {
	echarts_2();
	function echarts_2() {
 		// 基于准备好的dom，初始化echarts实例
 		var myChart = echarts.init(document.getElementById('echart2'));
option = {
  //  backgroundColor: '#00265f',
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },

    grid: {
        left: '0',
		top:'0',
        right: '0',
        bottom: '0',
       containLabel: true
    },
    xAxis: [{
        type: 'category',
      		data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        axisLine: {show: false,},
        axisTick: {show: false,},
		axisLabel:  {show: false,},
    }],
    yAxis: [{
        type: 'value',
        axisLabel: {show: false,},
        axisTick: {show: false,},
        axisLine: {show: false,},
        splitLine: {show: false,}
    }],
    series: [{
        name: '家庭作业完成数',
        type: 'bar',
        data: [2, 3, 3, 9, 15, 12, 6, 4, 6, 7, 4, 10],
        barWidth:'50%', //柱子宽度
       // barGap: 1, //柱子之间间距
        itemStyle: {
            normal: {color:'#1890ff'}
        }
    }
	]
};
      
 		// 使用刚指定的配置项和数据显示图表。
 		myChart.setOption(option);
 		window.addEventListener("resize", function () {
 			myChart.resize();
 		});
 	}
})
$(function () {
	echarts_3();
	function echarts_3() {
 		// 基于准备好的dom，初始化echarts实例
 		var myChart = echarts.init(document.getElementById('echart3'));
//百分比数值的位置

var data = 57;
var position = '';
if (data >= 50) {
    position = 'top';

} else if (data < 50) {
    position = 'right';

}



var option = {
    animationDuration: 3000,
    grid: {
        top: '70%',
        left: '0%',
        right: '0%',
        height: '26%',
        containLabel: false
    },
    xAxis: {
        type: 'value',
        axisLabel:  {show: false, },
        max: 100,
        axisTick: {show: false, },
        axisLine: {show: false, },
        splitLine: {show: false, },
    },
    yAxis: [{
        type: 'category',
        data: [],
        axisLabel:  {show: false, },
        axisTick: {show: false, },
        axisLine: {show: false, },
        splitLine: {show: false},
        z: 10
    }, {
        type: 'category',
        axisLabel: {show: false, },
        axisTick:  {show: false, },
        axisLine:  {show: false, },
        splitLine:  {show: false, },
        data: [],

    }],

    series: [{
        name: '',
        type: 'bar',
        barWidth: '100%',
        // barMaxWidth: '100%',
        label: {
            normal: {
                show: true,
                position:position,
                formatter: '{c} %',
                textStyle: {
                    color: '#888',
                   // fontSize: 14
                }
            }
        },
        itemStyle: {
            normal: {
                barBorderRadius:55,
                color: '#e55957'
            }
        },

        data: [data],
        z: 10
    }, {

        type: 'bar',
        barWidth: '100%',
        yAxisIndex: 1,
        silent: true,
        // barMaxWidth: '100%',
        itemStyle: {
            normal: {
                barBorderRadius: 55,
                color: '#eee'
            }

        },

        data: [100],

    }]

};  
 		// 使用刚指定的配置项和数据显示图表。
 		myChart.setOption(option);
 		window.addEventListener("resize", function () {
 			myChart.resize();
 		});
 	}
})
$(function () {
	echarts_4();
	function echarts_4() {
 		// 基于准备好的dom，初始化echarts实例
 		var myChart = echarts.init(document.getElementById('echart4'));
   option1 = {

    title : {
      text: '总用户数',
      subtext: '123,224',
		width:'20%',
      subtextStyle: {
    	fontSize : 20,
    	
    	color: '#84aef5'
     },
        x: '99px',
        y: '40%',
		//center: ['80%', '50%'],
        textStyle: {
            fontWeight: 'normal',
            fontSize: 16
        }
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
		"icon": "circle",
        orient: 'vertical',
        left: 'right',
		top:'25%',
		formatter: function(name) {
            var oa = option1.series[0].data;
            var num = oa[0].value + oa[1].value + oa[2].value + oa[3].value;
            for (var i = 0; i < option1.series[0].data.length; i++) {
                if (name == oa[i].name) {
                    return name + '     ' + (oa[i].value / num * 100).toFixed(2) + '%';
                }
            }
        }
        //data: ['轻度患者','中度患者','重度患者','阳性']
    },
    color : ['#3296ff','#2fc4c4','#44c468','#f9cd31','#f05870','#8c55e0','#D671F5','#F430E8','#8A31FB'],
    series : [
        {
            name: '抑郁类别占比',
            type: 'pie',
            radius : ['50%','70%'],
            center: ['140px', '50%'],
            data:[
                {value:335, name:'轻度患者'},
                {value:310, name:'中度患者'},
                {value:234, name:'重度患者'},
                {value:135, name:'阳性'},
   
            ],
			labelLine: { show:false},
			 label: { show:false,},
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

 		// 使用刚指定的配置项和数据显示图表。
 		myChart.setOption(option1);
 		window.addEventListener("resize", function () {
 			myChart.resize();
 		});
 	} 
})
$(function () {
	echarts_5();
	function echarts_5() {
 		// 基于准备好的dom，初始化echarts实例
 		var myChart = echarts.init(document.getElementById('echart5'));
   option = {
  //  backgroundColor: '#00265f',
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
   
    grid: {
       left: '5',
		top:'40px',
        right: '0%',
        bottom: '2%',
       containLabel: true
    },
    xAxis: [{
        type: 'category',
      		data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        axisLine: {
            show: true,
         lineStyle: {
                color: "rgba(0,0,0,.1)",
                width: 1,
                type: "solid"
            },
        },
		splitLine: {
			 show: false,
		},
        axisTick: {
            show: false,
        },
		axisLabel:  {
                interval: 0,
               // rotate:50,
                show: true,
                splitNumber: 15,
                textStyle: {
 					color: "rgba(0,0,0,.6)",
                    fontSize: '14',
                },
            },
    }],
    yAxis: [{
		name: '自杀提醒',
		"nameTextStyle": {color: 'rgba(0,0,0,.6)',fontSize:'14'},
        type: 'value',
		max: 80,
        axisLabel: {
           //formatter: '{value} %'
			show:true,
			 textStyle: {
 					color: "rgba(0,0,0,.6)",
                    fontSize: '14',
                },
        },
        axisTick: {
            show: false,
        },
        axisLine: {
            show: true,
            lineStyle: {
				
                color: "rgba(0,0,0,.1	)",
                width: 1,
				
                type: "solid"
            },
        },
        splitLine: {
            lineStyle: {
               color: "rgba(0,0,0,.1)",
				 type: "dotted"
            }
        }
    }],
    series: [
		{
        name: '提醒次数',
        type: 'bar',
        data: [28, 44, 12, 39, 14, 4, 23, 30, 25, 48, 27, 22],
        barWidth:'35%', //柱子宽度
			label: {
                        normal: {
                            show: true,
                            position: 'top',
							formatter: '{c}',
							textStyle: {
 					color: "rgba(0,0,0,.4)",
                  
                },
                        }

                    },
       // barGap: 1, //柱子之间间距
        itemStyle: {
            normal: {
				 color:'#1890ff',
				
                opacity: 1,
				barBorderRadius: 3,
            }
        }
    },]
		
};
     

 		// 使用刚指定的配置项和数据显示图表。
 		myChart.setOption(option);
 		window.addEventListener("resize", function () {
 			myChart.resize();
 		});
 	}
})


