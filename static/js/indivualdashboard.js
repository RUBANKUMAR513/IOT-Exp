function back(user_id){
    window.location.href = "/dashboard/" + user_id;
}
setInterval(refresh, 5000);
function refresh(){
    var xhttp = new XMLHttpRequest();
    var row_div=document.getElementById("datatable")
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           let data=this .response
            
    let a=JSON.parse(data);
    Convert_binary(a[0].Output)
    //display_relay()
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
function Convert_binary(decimal){
    decimal=Number(decimal)
    let binary=decimal.toString(2);

    while (binary.length< 8) {
           binary = "0" + binary;
        } 
   for(let i=0;i<binary.length;i++){
    let a="radio"
    a+=(i+1)
    
    if(binary[i]==1){
        document.getElementById(a).checked = true;
    }
    else if(binary[i]==0){
        document.getElementById(a).checked = false;
    }
   }
}
let b=[];
function check(){
    let s1=document.getElementById("s1").checked;
    let s2=document.getElementById("s2").checked;
    let s3=document.getElementById("s3").checked;
    let s4=document.getElementById("s4").checked;
    let s5=document.getElementById("s5").checked;
    let s6=document.getElementById("s6").checked;
    let s7=document.getElementById("s7").checked;
    let s8=document.getElementById("s8").checked;
    b=[s1,s2,s3,s4,s5,s6,s7,s8]
    
    var binary=""
    for(let i=0;i<8;i++){
       if(b[i]){
          binary+=1;
       }
       else{
          binary+=0;
       }
    }
    let decimal=parseInt(binary,2);
    console.log(decimal)
    let data={
        value:decimal
    };
    fetch('/decimal',{
    method:'POST',
    headers :{
        'content-Type':'application/json'
    },
        body:JSON.stringify(data)
}).then(response =>{
    console.log("success")
    console.log(response);
}).catch(error=>{
    console.log(error);
});

}
outputbox();
function outputbox(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let decimal= this.responseText;
        console.log("decimal---->"+decimal)
        decimal=Number(decimal)
        console.log("decimal---->"+decimal)
        let binary=decimal.toString(2);
    while (binary.length< 8) {
           binary = "0" + binary;
        } 
   console.log("binary----->"+binary)
   for(let i=0;i<binary.length;i++){
    let a="s"
    a+=(i+1)
    if(binary[i]==1){
        document.getElementById(a).click();
    }
    else if(binary[i]==0){
        continue;
    }
   }
       
    }
    };
    xhttp.open("POST","/show_output", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("hii");
}
