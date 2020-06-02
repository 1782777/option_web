var volume_mean = new Array(244).fill(0);

function init(){
    $.ajax({
        type : "get",
        async : false,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
        url : "http://qiquan.pub/iv_mean/",    //请求发送到TestServlet处
        data : {},
        dataType : "json",        //返回数据形式为json
        success : function(data) {
            //请求成功时执行该函数内容，result即为服务器返回的json对象
            
            obj = JSON.parse(JSON.stringify(data));
            jsonTime = obj.time;
            console.log(jsonTime);
        },
        error : function(errorMsg) {
            console.log(" ");
        }
    })
    $.ajax({
        type : "get",
        async : false,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
        url : "http://qiquan.pub/etf/",    //请求发送到TestServlet处
        data : {},
        dataType : "json",        //返回数据形式为json
        success : function(data) {
            //请求成功时执行该函数内容，result即为服务器返回的json对象
            
            obj = JSON.parse(JSON.stringify(data));
            jsonTimel = obj.time;
            console.log(jsonTimel);
        },
        error : function(errorMsg) {
            console.log(" ");
        }
    })
}



var chart_north;
function Chart_north(id){
    chart_north = echarts.init(document.getElementById(id));
            
    // 指定图表的配置项和数据
    var option = {
    title: {
        text: '北向资金' ,  
        subtext:'北向资金数重要的严控大盘涨跌指标',
        textStyle:{
            fontSize:14
        }      
    },
    color:["red","blue","grey"],
    tooltip: {},
    legend: {},
    toolbox: {},      
    xAxis: [{         
        data: jsonTime
    }],
    yAxis:  [{         
        axisLabel:{formatter:'{value}亿'}
    }],
    series: [{
        name: '沪股通流入',
        type: 'line',
        data: []
        //areaStyle: {}       
    },
    {
        name: '深股通流入',
        type: 'line',
        data: []        
    },
    {
        name: '北向总体流入',
        type: 'line',
        data: []        
    }]
    };
    // 使用刚指定的配置项和数据显示图表。
    Load_north()
    setInterval(function(){Load_north()}, 10000); 
    chart_north.setOption(option);
}

function Load_north()
{
    $.ajax({
        type : "get",
        async : true,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
        url : "http://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1&fields2=f51,f52,f54,f56&ut=b2884a393a59ad64002292a3e90d46a5",    //请求发送到TestServlet处
        data : {},
        dataType : "json",        //返回数据形式为json
        success : function(data) {
            //请求成功时执行该函数内容，result即为服务器返回的json对象
            chart_north.hideLoading();
            obj = JSON.parse(JSON.stringify(data))
            var n1 = new Array();
            var n2 = new Array();
            var n3 = new Array();
            for (var i=0;i<obj.data.s2n.length;i++)
            { 
                var three = obj.data.s2n[i].split(',');
                //console.log(three);
                n1.push(three[1]/10000);
                n2.push(three[2]/10000);
                n3.push(three[3]/10000);
            }
            // console.log(n1);
            if (data) {
                chart_north.setOption({
                    
                    series: [{
                        //ame: 'hgt',
                        data: n1
                    },
                    {
                        //name: 'sgt',
                        data: n2
                    },
                    {
                        //name: 'north',
                        data: n3
                    }]
                });
            }
        },
        error : function(errorMsg) {
            //请求失败时执行该函数
            alert("图表请求数据失败!");
            chart_north.hideLoading();
        }
   })
}

var chart_volume;
function Chart_volume(id){
    chart_volume = echarts.init(document.getElementById(id));
            
    // 指定图表的配置项和数据
    var option = {
        title: {
            text: '上证50成交量对比',
            subtext:'成交量大于1.5绝对多大涨，此值越大涨幅越大',     
            textStyle:{
                fontSize:14
            }

        },
        color:["#61a0a8"],
        tooltip: {},
        legend: {},
        toolbox: {},      
        xAxis: [{         
            data: jsonTime
        }],
        yAxis:  [{         
            min:0,
            max:2.5,
        }],
        series: [{
            name: '成交量比例',
            type: 'line',
            data: [] ,
            areaStyle: {} 
            // smooth: true         
        }]
    };
    // 使用刚指定的配置项和数据显示图表。
    chart_volume.setOption(option);
    Load_volume()
    setInterval(function(){Load_volume()}, 10000); 
}

function Load_volume()
{
    $.ajax({
        type : "get",
        async : true,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
        url : "http://qiquan.pub/vol/",    //请求发送到TestServlet处
        data : {},
        dataType : "json",        //返回数据形式为json
        success : function(data) {
            // //请求成功时执行该函数内容，result即为服务器返回的json对象
            // chart_volume.hideLoading();
            // obj = JSON.parse(JSON.stringify(data))
            // var volume = new Array();
            // var diff = new Array();
            // console.log(obj.data.length);
            // for (var i=0;i<obj.data.length;i++)
            // { 
            //     // console.log(obj.data[i][3]);
            //     var v = obj.data[i][3];
            //     //console.log(three);
            //     volume.push(v);
                
            // }
            // console.log(volume);
            // for (var i=0;i<volume.length;i++)
            // {
            //     var d = volume[i]/volume_mean[i];
            //     diff.push(d);
            // }
            //console.log(data);
            if (data) {
                chart_volume.setOption({
                    series: [{
                        //name: 'today/5day',
                        data: data.vol
                    }]
                });
            }
        },
        error : function(errorMsg) {
            //请求失败时执行该函数
            // alert("图表请求数据失败!");
            chart_volume.hideLoading();
        }
   })
}


var CharETF ;
function Chart_etf(id){
    CharETF = echarts.init(document.getElementById(id));
    //var myChart = echarts.init(document.getElementById(id));
    var option ={
        title: {
            text: 'etf涨跌幅',
            subtext:'包含美股期货涨跌对比',
            textStyle:{
                fontSize:14
            }
        },
        tooltip: {},
        legend: {},
        xAxis: {
            data: jsonTimel
        },
        yAxis: {},
        series: [{
            name: '50etf',
            type: 'line',
            data: []
        },
        {
            name: '300etf',
            type: 'line',
            data: []
        },
        {
            name: '美股期货',
            type: 'line',
            data: []
        }]
    };
    CharETF.setOption(option);
    Load_etf()
    setInterval(function(){Load_etf()}, 10000); 
}


function Load_etf()
{
    $.ajax({
        type : "get",
        async : true,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
        url : "http://qiquan.pub/etf/",    //请求发送到TestServlet处
        data : {},
        dataType : "json",        //返回数据形式为json
        success : function(data) {
            //请求成功时执行该函数内容，result即为服务器返回的json对象
            CharETF.hideLoading();
            obj = JSON.parse(JSON.stringify(data))
            //console.log(obj.etf50);
            if (data) {
                CharETF.setOption({
                    series: [{
                        // 根据名字对应到相应的系列
                        //name: '50',
                        data: data.etf50
                    },
                    {
                        // 根据名字对应到相应的系列
                        //name: '300',
                        data: data.etf300
                    },
                    {
                        // 根据名字对应到相应的系列
                        //name: 'es',
                        data: data.es
                    },]
                });
            }
        },
        error : function(errorMsg) {
            //请求失败时执行该函数
            // alert("图表请求数据失败!");
            CharETF.hideLoading();
        }
   })
}


var CharIVMEAN ;
function Chart_iv_mean(id){
    CharIVMEAN = echarts.init(document.getElementById(id));
    //var myChart = echarts.init(document.getElementById(id));
    var option ={
        title: {
            text: '平均波动率',
            subtext:'50期权和300期权多波动率日变化',
            
            textStyle:{
                fontSize:14
            }
        },
        tooltip: {},
        legend: {},
        xAxis: {
            data: jsonTime,
            minInterval: 1
        },
        yAxis: {},
        series: [{
            name: 'IV50',
            type: 'line',
            data: []
        },
        {
            name: 'IV300',
            type: 'line',
            data: []
        }]
    };
    CharIVMEAN.setOption(option);
    Load_ivmean()
    setInterval(function(){Load_ivmean()}, 10000); 
}

function Load_ivmean()
{
    $.ajax({
        type : "get",
        async : true,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
        url : "http://qiquan.pub/iv_mean/",    //请求发送到TestServlet处
        data : {},
        dataType : "json",       //返回数据形式为json
        success : function(data) {
            //请求成功时执行该函数内容，result即为服务器返回的json对象
            CharIVMEAN.hideLoading();
            obj = JSON.parse(JSON.stringify(data))
            console.log(obj.iv_50);
            if (data) {
                CharIVMEAN.setOption({
                    // title: {
                    //     subtext:'测试一下副标题到底能写多长呢，会不会一下冲破列天际啊啊啊啊啊数数',
                    // },
                    series: [{
                        // 根据名字对应到相应的系列
                        //name: 'iv_50',
                        data: data.iv_50
                    },
                    {
                        // 根据名字对应到相应的系列
                        //name: 'iv_300',
                        data: data.iv_300
                    },
                    ]
                });
            }
        },
        error : function(errorMsg) {
            //请求失败时执行该函数
            // alert("图表请求数据失败!");
            CharIVMEAN.hideLoading();
        }
   })
}
