function back(){
    window.location.href="index3.html"
}
setInterval(refresh, 5000);
function refresh(){
    var xhttp = new XMLHttpRequest();
    var row_div=document.getElementById("datatable")
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           let data=this .response
            
    let a=JSON.parse(data);
    var dataHTMLformat='<thead><th class="text-center">#</th><th class="text-center">Date</th><th class="text-center">Time</th><th class="text-center">Data</th></thead>'
    a.forEach(function(item){
    
    dataHTMLformat+='<tr><td class="text-center"></td><td class="text-center">'+item['Date']+'</td><td class="text-center">'+item['Time']+'</td><td class="text-center">'+item['Output']+'</td></tr>'
    
    });
    row_div.innerHTML=dataHTMLformat;
        }
        };
    xhttp.open("GET","/refresh_table", true);
    
        xhttp.send();
    
}
