function recursiveMaze(startx, starty, endx, endy, prevx, prevy){
    if(endx-startx<3 || endy-starty<3){
        return true;
    }
    function buildWall(x,y,a,startx, starty, endx, endy){
        if(a){
            for(var i=starty; i<=endy; i++){
                if(i==y) continue;
                document.getElementById(i+"x"+x).classList.add("wall");
                box[i][x] = 2;
            }
        }else{
            for(var i=startx; i<=endx; i++){
                if(i!=x){
                    document.getElementById(y+"x"+i).classList.add("wall");
                    box[y][i] = 2;
                }
            }
        }
    }
    if(Math.random()>0.5){
        var x = startx+ 1 + Math.floor((endx-startx-1)*Math.random());
        while(x==prevx){
            x = startx+ 1 + Math.floor((endx-startx-1)*Math.random());
        }
        var y = starty + Math.floor(Math.random()*(endy-starty));
        while(y==prevy){
            y = starty + Math.floor(Math.random()*(endy-starty));
        }
        buildWall(x,y,1,startx, starty, endx, endy);
        recursiveMaze(startx, starty, x-1, endy, prevx, y);
        recursiveMaze(x+1, starty, endx, endy, prevx, y);
    }else{
        var x = startx + Math.floor((endx-startx)*Math.random());
        while(x==prevx){
            x = startx+ 1 + Math.floor((endx-startx)*Math.random());
        }
        var y = starty + 1 + Math.floor(Math.random()*(endy-starty-1));
        while(y==prevy){
            y = starty + 1 + Math.floor(Math.random()*(endy-starty-1));
        }
        buildWall(x,y,0,startx, starty, endx, endy);
        recursiveMaze(startx, y+1, endx, endy, x, prevy);
        recursiveMaze(startx, starty, endx, y-1, x, prevy);
    }
}


function randomMaze(){
    clearGrid();
    makeGrid();
    recursiveMaze(0,0,box[0].length-2, box.length-1,-1,-1);
    var x, y, flag = false;
    for(x=6; x<box[0].length; x++){
        for(y=1; y<box.length; y++){
            if(!box[y][x]){
                flag = true;
                break;
            }
        }
        if(flag) break;
    }
    start = document.getElementById("start");
    t = parseInt(start.style.top.substr(0,start.style.top.length-2));
    l = parseInt(start.style.left.substr(0,start.style.left.length-2));
    t = Math.floor(t/40);
    l = Math.floor((l-margin)/40);
    document.getElementById(t+"x"+l).classList.remove("start");
    document.getElementById(y+"x"+x).classList.add("start");
    start.style.transition = "0.7s";
    setTimeout(()=>start.style.transition = "", 700);
    start.style.top = 40*y+20+"px";
    start.style.left = 40*x+20+margin+"px";
    flag = false;
    for(x=box[0].length-3; x>=0; x--){
        for(y=box.length-3; y>=0; y--){
            if(!box[y][x]){
                flag = true;
                break;
            }
        }
        if(flag) break;
    }
    stop = document.getElementById("stop");
    t = parseInt(stop.style.top.substr(0,stop.style.top.length-2));
    l = parseInt(stop.style.left.substr(0,stop.style.left.length-2));
    t = Math.floor(t/40);
    l = Math.floor((l-margin)/40);
    document.getElementById(t+"x"+l).classList.remove("stop");
    document.getElementById(y+"x"+x).classList.add("stop");
    stop.style.transition = "0.7s";
    setTimeout(()=>stop.style.transition = "", 700);
    stop.style.top = 40*y+20+"px";
    stop.style.left = 40*x+20+margin+"px";
}
