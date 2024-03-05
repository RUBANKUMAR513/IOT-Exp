document.getElementById("submit").addEventListener("click",function(e){
    e.preventDefault();
});
function formdata(){
let form=document.getElementById("signupform");
let username=form[0].value;
let email=form[1].value;
let password=form[2].value;
let terms=form[3].checked;
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
if (this.readyState == 4 && this.status == 200) {
    let msg=this.responseText;
    console.log(msg)
    assign(msg);
}
};
xhttp.open("POST","/store_inputs", true);
xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
xhttp.send("username="+username+"&email="+email+"&password="+password+"&terms="+terms);
}
function  assign(msg) {
    if(msg=="Erorr"){
        console.log("hii")
        const newDiv = document.createElement("div");
        newDiv.className="alert alert-danger";
        newDiv.id="div"
        newDiv.style.textAlign="center";
        newDiv.role="alert";
        newDiv.textContent="Email already exists!";
        const parent = document.getElementById("row");
        console.log("row"+parent);
        parent.appendChild(newDiv);
        setTimeout(() => {
            $("#div").delay(5000).fadeOut(500);
    }, 1000);
    }
    else if(msg=="success"){
        const newDiv = document.createElement("div");
        newDiv.className="alert alert-success";
        newDiv.id="div"
        newDiv.style.textAlign="center";
        newDiv.role="alert";
        newDiv.textContent="Successfully Created!";
        const parent = document.getElementById("row");
        console.log("row"+parent);
        parent.appendChild(newDiv);
        setTimeout(() => {
            $("#div").delay(5000).fadeOut(500);
    }, 1000);
    window.location.href="/login"
    }

}
