var i = 0;
var j = 0;
var interval = 0;
var box = [];
var chid = 0;

function makeGrid(){
    box = [];
    grid = document.getElementById("grid");
    grid.innerHTML = "";
    n = Math.floor((window.innerWidth-300)/40);
    m = Math.floor(window.innerHeight/40);
    for(var j=0; j<=m; j++){
        temp = []
        for(var i=0; i<=n; i++){
            cell = document.createElement("div");
            cell.classList = ["cell"];
            cell.id = j+"x"+i;
            drawingElement(cell);
            cell.oncontextmenu = addCheckpoint(cell.id);
            cell.style.left = 40*i+"px";
            cell.style.top = 40*j+"px";
            grid.appendChild(cell);
            temp.push(0);
        }
        box.push(temp);
    }
    start = document.getElementById("start");
    stop = document.getElementById("stop");

    box[Math.floor(m/2)][Math.floor(n/4)]=1;
    document.getElementById(Math.floor(m/2)+"x"+Math.floor(n/4)).classList = "start cell";
    start.style.left = 300+40*Math.floor(n/4)+20+"px";
    start.style.top = 40*Math.floor(m/2)+20+"px";
    start.style.zIndex = Math.floor(m/2);

    box[Math.floor(m/2)][Math.floor(3*n/4)]=1;
    document.getElementById(Math.floor(m/2)+"x"+Math.floor(3*n/4)).classList = "stop cell";
    stop.style.left = 300+40*Math.floor(3*n/4)+20+"px";
    stop.style.top = 40*Math.floor(m/2)+20+"px";
    stop.style.zIndex = Math.floor(m/2);
}

makeGrid();


function addCheckpoint(id){
    function addCheckpoint(){
        i = id.split("x");
        if(box[Number(i[0])][Number(i[1])]){
            return false;
        }
        if(chid>4){
            return false;
        }
        ch = document.createElement("img");
        ch.src = "images/yellow"+(chid+1)+".svg";
        ch.classList = "draggable checkpoint";
        ch.id = "checkpoint"+chid;
        ch.oncontextmenu = removeCheckpoint(chid);
        chid++;
        ch.style.zIndex = Number(i[0]);
        ch.style.top = 40*Number(i[0])+20+"px";
        ch.style.left = 300+40*Number(i[1])+20+"px";
        dragElement(ch);
        box[Number(i[0])][Number(i[1])] = 1;
        document.body.appendChild(ch);
        return false
    }
    return addCheckpoint
}

function removeCheckpoint(id){
    function remove(e){
        e.preventDefault();
        ch = document.getElementById("checkpoint"+id);
        i = ch.style.left;
        i = Number(i.substr(0,i.length-2));
        i = Math.floor((i-300)/40);
        j = ch.style.top;
        j = Number(j.substr(0,j.length-2));
        j = Math.floor(j/40);
        box[j][i] = 0;
        ch.parentNode.removeChild(ch);
        chid--;
        for(var i = id+1; i<5; i++){
            ch = document.getElementById("checkpoint"+i);
            ch.id = "checkpoint"+(i-1);
            ch.oncontextmenu = removeCheckpoint(i-1);
            ch.src = "images/yellow"+i+".svg";
        }
        return false;
    }
    return remove;
}

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0, sx = 0, sy = 0, classes = "";
    elmnt.onmousedown = dragMouseDown;
  
    function dragMouseDown(e) {
      e = e || window.event;
      if(e.button!=0) return false;
      e.preventDefault();
      elmnt.style.transform = "scale(1.2) translate(-35%,-70%)";
      elmnt.style.cursor = "grabbing";
      elmnt.style.zIndex = "1000";
      pos3 = e.clientX;
      pos4 = e.clientY;
      sx = elmnt.style.left;
      sy = elmnt.style.top;
      box[Math.floor(Number(sy.substr(0,sy.length-2))/40)][Math.floor((Number(sx.substr(0,sx.length-2))-300)/40)] = 0;
      thiscell = document.getElementById(Math.floor(Number(sy.substr(0,sy.length-2))/40)+"x"+Math.floor((Number(sx.substr(0,sx.length-2))-300)/40))
      classes = thiscell.classList.value;
      thiscell.classList = "cell";
      document.onmouseup = closeDragElement;
      document.onmousemove = elementDrag;
    }
  
    function elementDrag(e) {
      e = e || window.event;
      e.preventDefault();
      pos1 = pos3 - e.clientX;
      pos2 = pos4 - e.clientY;
      pos3 = e.clientX;
      pos4 = e.clientY;
      elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
      elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }
  
    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
        t = Number(elmnt.style.top.substr(0,elmnt.style.top.length-2));
        l = Number(elmnt.style.left.substr(0,elmnt.style.left.length-2));
        if(box[Math.floor(t/40)][Math.floor((l-300)/40)]!=0){
            elmnt.style.top = sy;
            elmnt.style.left = sx;
            box[Math.floor(Number(sy.substr(0,sy.length-2))/40)][Math.floor((Number(sx.substr(0,sx.length-2))-300)/40)] = 1;
            document.getElementById(Math.floor(Number(sy.substr(0,sy.length-2))/40)+"x"+Math.floor((Number(sx.substr(0,sx.length-2))-300)/40)).classList = classes;
            elmnt.style.zIndex = Math.floor(Number(sy.substr(0,sy.length-2))/40);
        }else{
            elmnt.style.top = 40*Math.floor(t/40)+20+"px";
            elmnt.style.left = Math.max(300 + 40*Math.floor((l-300)/40)+20, 320)+"px";
            box[Math.floor(t/40)][Math.floor((l-300)/40)] = 1;
            document.getElementById(Math.floor(t/40)+"x"+Math.floor((l-300)/40)).classList = classes;
            elmnt.style.zIndex = Math.floor(t/40);
        }
        elmnt.style.transform = "scale(1) translate(-35%,-70%)";
        elmnt.style.cursor = "grab";
    }
}

for(let elmnt of document.getElementsByClassName("draggable")){
    dragElement(elmnt);
}

function drawingElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    elmnt.onmousedown = dragMouseDown;
  
    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        if(e.button!=0) return false;
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        i = elmnt.id.split('x');
        if(box[Number(i[0])][Number(i[1])]==2){
            box[Number(i[0])][Number(i[1])] = 0;
            elmnt.classList = "cell";
            document.onmousemove = elementDragOFF;
        }else if(box[Number(i[0])][Number(i[1])]==0){
            box[Number(i[0])][Number(i[1])] = 2;
            elmnt.classList = "wall cell";
            document.onmousemove = elementDragON;
        }
    }
    
    function elementDragON(e) {
        e = e || window.event;
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        i = Math.floor((pos3-300)/40);
        j = Math.floor(pos4/40);
        if(box[j][i]!=1){
            box[j][i] = 2;
            document.getElementById(j+'x'+i).classList = "wall cell"
        }
    }

    function elementDragOFF(e) {
        e = e || window.event;
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        i = Math.floor((pos3-300)/40);
        j = Math.floor(pos4/40);
        if(box[j][i]!=1){
            box[j][i] = 0;
            document.getElementById(j+'x'+i).classList = "cell";
        }
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}
