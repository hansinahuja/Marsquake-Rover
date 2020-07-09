function makeChanges(changes){
    var i = 0, int = 0;
    function color(){
        change = changes[i];
        c = document.getElementById(change.x+"x"+change.y);
        if(change.color == 0){
            c.className = "cell";
        }else if(change.color == 1){
            c.className = "inqueue cell";
        }else{
            c.className = "processed cell";
        }
        i++;
        if(i==changes.length){
            clearInterval(int);
        }
    }
    int = setInterval(color, 10);
}

function drawPath(path){
    var i=0, int=0;
    function drawLine(){
        point1 = path[i];
        point2 = path[i+1];
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
        if(i==path.length-1){
            clearInterval(int);
        }
    }
    int = setInterval(drawLine, 500);
}

function gatherData(){
    var start, stop, maze = [], checkpoints = [];
    start = document.getElementById("start");
    start = {y:Math.floor((start.offsetLeft-margin)/40), x:Math.floor(start.offsetTop/40)};
    stop = document.getElementById("stop");
    stop = {y:Math.floor((stop.offsetLeft-margin)/40), x:Math.floor(stop.offsetTop/40)};
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
        checkpoints.push({y:Math.floor((elmnt.offsetLeft-margin)/40), x:Math.floor(elmnt.offsetTop/40)})
    }
    var data = new FormData();
    data.append('algo', parseInt(document.getElementById("algorithm").value))
    data.append('start', JSON.stringify([start]));
    data.append('stop', JSON.stringify([stop]));
    data.append('cutCorners',0);
    data.append('allowDiagonals',1);
    data.append('biDirectional',0);
    data.append('beamWidth',2);
    data.append('checkpoints',JSON.stringify(checkpoints));
    data.append('maze',JSON.stringify(maze));
    return data;
}

function find(){
    showing = true;
    var data = gatherData();
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5000/api/findpath/",false);
    xhr.send(data);
    resp = JSON.parse(xhr.response);
    makeChanges(resp.gridChanges);
    console.log(resp);
}