
function Stock_vol()
{
    console.log("Stock_vol");
    Load_stock_vol();
    setInterval(function(){Load_stock_vol()}, 10000); 
}

window.onload = function () {
    console.log("onload");
    Load_stock_vol();
    setInterval(function(){Load_stock_vol()}, 10000); 
}

function Load_stock_vol()
{
    $.ajax({
        type : "get",
        async : true,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
        url : "http://qiquan.pub/stock/vol/",    //请求发送到TestServlet处
        data : {},
        dataType : "json",        //返回数据形式为json
        success : function(data) {
            //请求成功时执行该函数内容，result即为服务器返回的json对象
            
            obj = JSON.parse(JSON.stringify(data))
            
            var str = "<tr>"
            for(var i=0;i < obj.code.length;i++){
                str += "</tr>"
                //var x=document.getElementById('tb').insertRow();
                console.log(obj.code[i])
                code = obj.code[i]
                name = obj.name[i]
                vol =  obj.vol[i]
                c = obj.c[i]
                str += "<td>"+code+"</td>" + "<td>"+name+"</td>" + "<td>"+vol+"</td>" +"<td>"+c+"</td>"
                str += "</tr>"
            }
            
            console.log(str)
            var body=document.getElementById('body')
            console.log(body)
            body.innerHTML=str
        },
        error : function(errorMsg) {
            console.log(errorMsg)
            //请求失败时执行该函数
            // alert("图表请求数据失败!");
            // chart_north.hideLoading();
        }
   })
}
