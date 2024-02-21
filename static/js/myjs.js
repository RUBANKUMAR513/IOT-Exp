document.getElementById("store_inputs").addEventListener("click", function(e){
    e.preventDefault();
});
function hrefFunction(){
    const password="temp"
    const user="user@123"
    let email=document.getElementById("email").value;
    let pass=document.getElementById("password").value;
    if(password==pass && email==user){
        window.location.href="index3.html"
        console.log("well done!!!")
    }
}