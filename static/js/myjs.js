

function hrefFunction(){
    const password="temp"
    const user="user@123"
    let email=document.getElementById("email").value;
    let pass=document.getElementById("password").value;
    if(password==pass && email==user){
        const newdiv=document.createElement("div");
        newdiv.className="alert alert-success";
        newdiv.role="alert";
        newdiv.style.textAlign="center";
        newdiv.textContent="Password Correct!";
        const parent=document.getElementById("alert");
        parent.appendChild(newdiv);
        window.location.href="index3.html"
        console.log("well done!!!")
    }
    else{
        const newdiv=document.createElement("div");
        newdiv.className="alert alert-danger";
        newdiv.role="alert";
        newdiv.style.textAlign="center";
        newdiv.textContent="Password Incorrect!";
        const parent=document.getElementById("alert");
        parent.appendChild(newdiv);
    }
}
