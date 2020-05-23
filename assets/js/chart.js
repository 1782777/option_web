
function myChart(id){
    var myChart = echarts.init(document.getElementById(id));
            
    // 指定图表的配置项和数据
    var option = {
    title: {
        text: '我的头发' ,  
        textStyle:{
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
        data: [11, 11, 15, 13, 12, 13, 100] , 
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
        data: [11, 17, 25, 23, 22, 523, 20] ,
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
    myChart.setOption({
        title: {
            text: '异步数据加载示例',
            textStyle:{
                fontSize:14
            }
        },
        tooltip: {},
        legend: {
            data:['销量']
        },
        xAxis: {
            data: []
        },
        yAxis: {},
        series: [{
            name: '销量',
            type: 'bar',
            data: [1,2,3,4,5,6,7]
        }]
    });
    myChart.showLoading();


    

    $.ajax({
        type : "get",
        async : true,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
        url : "http://127.0.0.1:8080/json/",    //请求发送到TestServlet处
        data : {},
        dataType : "json",        //返回数据形式为json
        success : function(data) {
            //请求成功时执行该函数内容，result即为服务器返回的json对象
            myChart.hideLoading();
            console.log(11111);
            if (data) {
                myChart.setOption({
                    xAxis: {
                        data: data.time
                        
                    },
                    series: [{
                        // 根据名字对应到相应的系列
                        name: '销量',
                        data: data.iv
                        
                    }]
                });
                   
            }
        
       },
        error : function(errorMsg) {
            //请求失败时执行该函数
            alert("图表请求数据失败!");
            myChart.hideLoading();
        }
   })

    
    // 异步加载json格式数据
    // $.getJSON('http://127.0.0.1:8080/json',function(data){
    //     console.log(data.iv);
    //     console.log("1111111111111111111");
    //     myChart.setOption({
    //         xAxis: {
    //             data: data.time
                
    //         },
    //         series: [{
    //             // 根据名字对应到相应的系列
    //             name: '销量',
    //             data: data.iv
                
    //         }]
    //     });
        
    // });
}
