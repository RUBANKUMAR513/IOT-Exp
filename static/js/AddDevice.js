
document.getElementById("store_inputs").addEventListener("click", function(e){
    e.preventDefault();
});
function back(){
    window.location.href="index3.html"
}
function details(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        console.log(this.responseText);
    }
    };
    let storeform = document.getElementById("store_inputs");
    
    let model = storeform['cc-pament'];
    let hwversion = storeform['cc-name'];
    let swversion = storeform['cc-number'];
    let id = storeform['cc-exp'];
    let devicename = storeform['x_card_code'];
    xhttp.open("POST","/insertdata", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("Model="+model.value+"&HwVersion="+hwversion.value+"&SwVersion="+swversion.value+"&Id="+id.value+"&DeviceName="+devicename.value);
    
}
