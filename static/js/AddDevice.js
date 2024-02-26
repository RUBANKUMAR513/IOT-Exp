
document.getElementById("store_inputs").addEventListener("click", function(e){
    e.preventDefault();
});
function back(){
    window.location.href="index3.html"
}
function clr_form(){
    document.getElementById("store_inputs").reset();
}
function details(model,hwversion,swversion,id,devicename){
    console.log(model,hwversion,swversion,id,devicename)
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        console.log(this.responseText);
        const newdiv=document.createElement("div");
        newdiv.className="alert alert-success";
        newdiv.role="alert";
        newdiv.style.textAlign="center";
        newdiv.textContent="Device Successfully Added! If you want to redirect dashboard ";
        const a_tag=document.createElement("a");
        a_tag.href="/index3.html";
        a_tag.className="alert-link";

        a_tag.textContent="CLICK HERE";
        newdiv.appendChild(a_tag);
        const parent=document.getElementById("Alerts");
        parent.appendChild(newdiv);
    }
    };
    xhttp.open("POST","/insertdata", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("Model="+model+"&HwVersion="+hwversion+"&SwVersion="+swversion+"&Id="+id+"&DeviceName="+devicename);
    
}
function checkvalidation(){
    let storeform = document.getElementById("store_inputs");
    let model = storeform['cc-pament'].value;
    let hwversion = storeform['cc-name'].value;
    let swversion = storeform['cc-number'].value;
    let id = storeform['cc-exp'].value;
    let devicename = storeform['x_card_code'].value;
    const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,<>\/?~]/
    if(model=="" || hwversion=="" || swversion=="" || id=="" || devicename=="") {
    	const newdiv=document.createElement("div");
        newdiv.className="alert alert-danger";
        newdiv.role="alert";
        newdiv.style.textAlign="center";
        newdiv.textContent="Please Fill form!";
        const parent=document.getElementById("Alerts");
        parent.appendChild(newdiv);
        
    }
    else if(/[A-Za-z]/.test(id)){
        const newdiv=document.createElement("div");
        newdiv.className="alert alert-danger";
        newdiv.role="alert";
        newdiv.style.textAlign="center";
        newdiv.textContent="Alphabets Do Not allowed In ID!";
        const parent=document.getElementById("Alerts");
        parent.appendChild(newdiv);
     }
     else if(/[A-Za-z]/.test(swversion)){
        const newdiv=document.createElement("div");
        newdiv.className="alert alert-danger";
        newdiv.role="alert";
        newdiv.style.textAlign="center";
        newdiv.textContent="Alphabets Do Not allowed In Sw Version!";
        const parent=document.getElementById("Alerts");
        parent.appendChild(newdiv);
     }
     else if(/[A-Za-z]/.test(hwversion)){
        const newdiv=document.createElement("div");
        newdiv.className="alert alert-danger";
        newdiv.role="alert";
        newdiv.style.textAlign="center";
        newdiv.textContent="Alphabets Do Not allowed In Hw Version!";
        const parent=document.getElementById("Alerts");
        parent.appendChild(newdiv);
     }
    else if(specialChars.test(model) || specialChars.test(hwversion) ||specialChars.test(swversion) ||specialChars.test(id) ||specialChars.test(devicename)){
        const newdiv=document.createElement("div");
        newdiv.className="alert alert-danger";
        newdiv.role="alert";
        newdiv.style.textAlign="center";
        newdiv.textContent="Special Character's Do Not Allowed!";
        const parent=document.getElementById("Alerts");
        parent.appendChild(newdiv);
     }
     else{
        details(model,hwversion,swversion,id,devicename);
     }
}