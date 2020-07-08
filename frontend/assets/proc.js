function drawLine(point1, point2){
    var dx = point2.x - point1.x;
    var dy = point2.y - point1.y;
    if(dx*dy){
        x = document.createElement("div");
        x.style.transformOrigin = "left";
        x.className = "path";
        x.style.transform = "rotate("+((2-dx)*dy*45)+"deg)";
        x.style.top = 40*point1.y+20+"px";
        x.style.left = 40*point1.x+margin+20+"px";
        document.body.appendChild(x);
        setTimeout(()=>{x.style.width = "57px";}, 100);
    }else{
        x = document.createElement("div");
        x.style.transformOrigin = "left";
        x.className = "path";
        if(dx==1 && dy==0){
            x.style.transform = "rotate(0deg)";
        }else if(dx==0 && dy==1){
            x.style.transform = "rotate(90deg)";
        }else if(dx==-1 && dy==0){
            x.style.transform = "rotate(180deg)";
        }else if(dx==0 && dy==-1){
            x.style.transform = "rotate(270deg)";
        }
        x.style.top = 40*point1.y+20+"px";
        x.style.left = 40*point1.x+margin+20+"px";
        document.body.appendChild(x);
        setTimeout(()=>{x.style.width = "40px";}, 100);
    }
}

function gatherData(){
    var start, stop, maze = [], checkpoints = [];
    start = document.getElementById("start");
    start = {x:Math.floor((start.offsetLeft-margin)/40), y:Math.floor(start.offsetTop/40)};
    stop = document.getElementById("stop");
    stop = {x:Math.floor((stop.offsetLeft-margin)/40), y:Math.floor(stop.offsetTop/40)};
    for(var j=0; j<m; j++){
        temp = [];
        for(var i=0; i<n; i++){
            if(box[j][i]==2){
                temp.push(1);
            }else{
                temp.push(0);
            }
        }
        maze.push(temp);
    }
    for(var i=0; i<5; i++){
        elmnt = document.getElementById("checkpoint"+i);
        if(!elmnt) break;
        checkpoints.push({x:Math.floor((elmnt.offsetLeft-margin)/40), y:Math.floor(elmnt.offsetTop/40)})
    }
    return JSON.stringify({start:start,stop:stop,checkpoints:checkpoints,maze:maze});
}