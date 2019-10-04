setInterval(function (){
    h = document.getElementById("heading");
    if (h.style.color == "red"){
        h.style.color = "blue";
    }
    else{
        h.style.color = "red"
    }
}, 1000)
