

function  assign() {
    const newDiv = document.createElement("div");
    newDiv.className="col-md-6 col-lg-3";
    const newDiv1=document.createElement("div");
    newDiv1.className="statistic__item statistic__item--green";
    const h2=document.createElement("h2");
    h2.textContent="Device 2";
    h2.className="number";
    const btn=document.createElement("button");
    const span=document.createElement("span");
    span.textContent="CLICK";
    span.className="desc";
    btn.appendChild(span);
    const parent = document.getElementById("row");
    console.log("row"+parent);
    parent.appendChild(newDiv);
    newDiv.appendChild(newDiv1);
    newDiv1.appendChild(h2);
    newDiv1.appendChild(btn);
}