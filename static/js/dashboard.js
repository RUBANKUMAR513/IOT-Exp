function back(){
    window.location.href="login.html"
}
function addDevice(){
    window.location.href="formEdited.html"
}
function del(id){
    let name="ruban"
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           console.log(this.responseText);
           refresh();
        }
    };

    xhttp.open("POST", "/deletedata", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhttp.send("ID="+id+"&Name="+name);
}

function refresh(){
    var xhttp = new XMLHttpRequest();
    var row_div=document.getElementById("row")
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           let data=this .response
            
    let a=JSON.parse(data);
    var dataHTMLformat=''
    a.forEach(function(item){
    
    dataHTMLformat+='<div class="col-md-6 col-lg-3"><div class="statistic__item statistic__item--green"><h2 class="number">'+item['DeviceName']+'</h2><div><a class="clicking" href="/individualdashboard.html?id='+item['_Id']+'"></a></div><div style="text-align: end;"><button id="'+item['_Id']+'" onclick="del(this.id)"><i class="fa-solid fa-trash fa-lg" style="color: lightcyan;"></i></button></div></div></div>'
    
   // '<div class="col-md-6 col-lg-3"><div class="statistic__item statistic__item--green"><h2 class="number">'+item['DeviceName']+'</h2><div><a href="/individualdashboard.html?id='+item['_Id']+'" style="margin-top: 30px;"><span class="desc">Click</span></a></div><div><button id="'+item['_Id']+'" onclick="del(this.id)"><span class="desc">delete</span></button></div></div></div>'
    
    });
    row_div.innerHTML=dataHTMLformat;
        }
        };
    xhttp.open("GET","/refresh", true);
    
        xhttp.send();
    
    }



