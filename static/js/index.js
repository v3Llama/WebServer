color = "blue"

while(true) {
    setTimeout(function(){
        heading = document.getElementsByTagName("h1");
        heading.style.color = color
        if (color == "blue"){
            color = "red"
        }
        else{
            color = "blue"
        }
    }, 1000)
    
}