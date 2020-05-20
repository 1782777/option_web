
function myChart(id){
    var myChart = echarts.init(document.getElementById(id));
            
    // 指定图表的配置项和数据
    var option = {
    title: {
        text: '我的头发' ,  
        textStyle:{
            // //文字颜色
            // color:'#ccc',
            // //字体风格,'normal','italic','oblique'
            // fontStyle:'normal',
            // //字体粗细 'normal','bold','bolder','lighter',100 | 200 | 300 | 400...
            // fontWeight:'bold',
            // //字体系列
            // fontFamily:'sans-serif',
            // //字体大小
    　　　　 fontSize:14
        }      
    },
    color:["#61a0a8"],
    tooltip: {},
    legend: {},
    toolbox: {},      
    xAxis: [{         
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    }],
    yAxis: { },
    series: [{
        name: 'count',
        type: 'line',
        data: [11, 11, 15, 13, 12, 13, 10] , 
        areaStyle: {}       
    },
    {
        name: 'count',
        type: 'line',
        data: [1, -2, 2, 5, 3, 2, 0]        
    }]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function myChart2(id){
    var myChart = echarts.init(document.getElementById(id));
            
    // 指定图表的配置项和数据
    var option = {
    title: {
        text: '我的体重',     
        textStyle:{
            fontSize:14
        }

    },
    color:["#61a0a8"],
    tooltip: {},
    legend: {},
    toolbox: {},      
    xAxis: [{         
        data: ['1', '2', '3', '4', '5', '6', '7']
    }],
    yAxis: { },
    series: [{
        name: 'weight',
        type: 'line',
        data: [11, 17, 25, 23, 22, 23, 20] ,
        smooth: true         
    },
    {
        name: 'weight',
        type: 'line',
        data: [1, -2, 2, 5, 3, 2, 0]        
    }]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function Bar(id){
    var myChart = echarts.init(document.getElementById(id));
    var option = {
        title: {
            text: '我的钱包' ,
            textStyle:{
                fontSize:14
            }       
        },
        color:["#aaaaaa"],
        xAxis: {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: [120, 200, 150, 80, 70, 110, 130],
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
                color: 'rgba(220, 220, 220, 0.8)'
            }
        }]
    };
    myChart.setOption(option);
}