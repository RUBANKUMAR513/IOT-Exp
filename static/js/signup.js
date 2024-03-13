document.getElementById("submit").addEventListener("click",function(e){
    e.preventDefault();
});
const checkPasswordValidity = (value) => {
    const isNonWhiteSpace = /^\S*$/;
    if (!isNonWhiteSpace.test(value)) {
      return "Password must not contain Whitespaces.";
    }
  
    const isContainsUppercase = /^(?=.*[A-Z]).*$/;
    if (!isContainsUppercase.test(value)) {
      return "Password must have at least one Uppercase Character.";
    }
  
    const isContainsLowercase = /^(?=.*[a-z]).*$/;
    if (!isContainsLowercase.test(value)) {
      return "Password must have at least one Lowercase Character.";
    }
  
    const isContainsNumber = /^(?=.*[0-9]).*$/;
    if (!isContainsNumber.test(value)) {
      return "Password must contain at least one Digit.";
    }
  
    const isContainsSymbol =
      /^(?=.*[~`!@#$%^&*()--+={}\[\]|\\:;"'<>,.?/_₹]).*$/;
    if (!isContainsSymbol.test(value)) {
      return "Password must contain at least one Special Symbol.";
    }
  
    const isValidLength = /^.{10,16}$/;
    if (!isValidLength.test(value)) {
      return "Password must be 10-16 Characters Long.";
    }
  
    return null;
  }

function formdata(){
let form=document.getElementById("signupform");
let username=form[0].value;
let email=form[1].value;
let password=form[2].value;
let terms=form[3].checked;
const isWhitespaceString = str => !str.replace(/\s/g, '').length
var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if(!re.test(email)){
    const newDiv = document.createElement("div");
    newDiv.className="alert alert-danger";
    newDiv.id="div"
    newDiv.style.textAlign="center";
    newDiv.role="alert";
    newDiv.textContent="Email format wrong EX:ruban@gmail.com!";
    const parent = document.getElementById("row");
    console.log("row"+parent);
    parent.appendChild(newDiv);
    setTimeout(() => {
        $("#div").delay(5000).fadeOut(500);
}, 1000);
} 
else if(isWhitespaceString(password)|| isWhitespaceString(username) || isWhitespaceString(email)){
    console.log("hii")
        const newDiv = document.createElement("div");
        newDiv.className="alert alert-danger";
        newDiv.id="div"
        newDiv.style.textAlign="center";
        newDiv.role="alert";
        newDiv.textContent="Space Not allowed!";
        const parent = document.getElementById("row");
        console.log("row"+parent);
        parent.appendChild(newDiv);
        setTimeout(() => {
            $("#div").delay(5000).fadeOut(500);
    }, 1000);
}
else{
    message=checkPasswordValidity(password)
    if (!message) {
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
      else {
        const newDiv = document.createElement("div");
            newDiv.className="alert alert-danger";
            newDiv.id="div"
            newDiv.style.textAlign="center";
            newDiv.role="alert";
            newDiv.textContent=message;
            const parent = document.getElementById("row");
            console.log("row"+parent);
            parent.appendChild(newDiv);
            setTimeout(() => {
                $("#div").delay(5000).fadeOut(500);
        }, 1000);
    } 
    
}

}

function  assign(msg) {
    if(msg=="Email already exists"){
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
    else if(msg=="Missing required fields"){
        console.log("hii")
        const newDiv = document.createElement("div");
        newDiv.className="alert alert-danger";
        newDiv.id="div"
        newDiv.style.textAlign="center";
        newDiv.role="alert";
        newDiv.textContent="Missing required fields";
        const parent = document.getElementById("row");
        console.log("row"+parent);
        parent.appendChild(newDiv);
        setTimeout(() => {
            $("#div").delay(5000).fadeOut(500);
    }, 1000);
}
else if(msg=="Failed to insert user"){
    console.log("hii")
    const newDiv = document.createElement("div");
    newDiv.className="alert alert-danger";
    newDiv.id="div"
    newDiv.style.textAlign="center";
    newDiv.role="alert";
    newDiv.textContent="Failed to insert user";
    const parent = document.getElementById("row");
    console.log("row"+parent);
    parent.appendChild(newDiv);
    setTimeout(() => {
        $("#div").delay(5000).fadeOut(500);
}, 1000);
}
else if(msg=="Something went wrong"){
    console.log("hii")
    const newDiv = document.createElement("div");
    newDiv.className="alert alert-danger";
    newDiv.id="div"
    newDiv.style.textAlign="center";
    newDiv.role="alert";
    newDiv.textContent="Something went wrong";
    const parent = document.getElementById("row");
    console.log("row"+parent);
    parent.appendChild(newDiv);
    setTimeout(() => {
        $("#div").delay(5000).fadeOut(500);
}, 1000);
}
    else if(msg=="Success"){
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
            window.location.href="/login"
    }, 1000);
    
    }

}
