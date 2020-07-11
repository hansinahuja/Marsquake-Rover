var i = 0;
var j = 0;
var interval = 0;
var box = [];
var chid = 0;
var margin = 0;
var showing = false;
var multidest = false;
var multistart = false;

algoChange();
function algoChange(){
    algo = document.getElementById("algorithm").value;
    if(algo!="1"){
        document.getElementById("beamwidth").disabled = true;
        document.getElementById("beamwidthl").style.color = "#555";
    }else{
        document.getElementById("beamwidth").disabled = false;
        document.getElementById("beamwidthl").style.color = "#FFF";
    }
    if(algo=="8"){
        document.getElementById("cutcorners").checked = true;
        document.getElementById("cutcorners").disabled = true;
        document.getElementById("cutcornersl").style.opacity = "0.3";
        document.getElementById("allowdiag").checked = true;
        document.getElementById("allowdiag").disabled = true;
        document.getElementById("allowdiagl").style.opacity = "0.3";
    }else{
        document.getElementById("cutcorners").disabled = false;
        document.getElementById("cutcornersl").style.opacity = "1";
        document.getElementById("allowdiag").disabled = false;
        document.getElementById("allowdiagl").style.opacity = "1";
    }
}

function multiDest(){
    if(!document.getElementById("multidest").checked){
        if(document.getElementById("multistart").checked){
            document.getElementById("multistart").checked = false;
        }
        multistart = false;
        multidest = true;
        for(let elmnt of document.getElementsByClassName("checkpoint")){
            t = Math.floor(elmnt.offsetTop/40);
            l = Math.floor(elmnt.offsetLeft/40-margin/40);
            document.getElementById(t+"x"+l).classList.remove("start");
            document.getElementById(t+"x"+l).classList.add("stop");
            elmnt.src = "images/red.svg";
        }
    }else{
        multistart = false;
        multidest = false;
        let i=0;
        for(let elmnt of document.getElementsByClassName("checkpoint")){
            t = Math.floor(elmnt.offsetTop/40);
            l = Math.floor(elmnt.offsetLeft/40-margin/40);
            document.getElementById(t+"x"+l).classList.remove("stop");
            elmnt.src = "images/yellow"+(i+1)+".svg";
            i++;
        }
    }
}


function multiSource(){
    if(!document.getElementById("multistart").checked){
        if(document.getElementById("multidest").checked){
            document.getElementById("multidest").checked = false;
        }
        multistart = true;
        multidest = false;
        for(let elmnt of document.getElementsByClassName("checkpoint")){
            t = Math.floor(elmnt.offsetTop/40);
            l = Math.floor(elmnt.offsetLeft/40-margin/40);
            document.getElementById(t+"x"+l).classList.remove("stop");
            document.getElementById(t+"x"+l).classList.add("start");
            elmnt.src = "images/green.svg";
        }
    }else{
        multistart = false;
        multidest = false;
        let i=0;
        for(let elmnt of document.getElementsByClassName("checkpoint")){
            t = Math.floor(elmnt.offsetTop/40);
            l = Math.floor(elmnt.offsetLeft/40-margin/40);
            document.getElementById(t+"x"+l).classList.remove("start");
            elmnt.src = "images/yellow"+(i+1)+".svg";
            i++;
        }
    }
}

function changeSlider(){
    document.getElementById("beamwidthl").innerText="Beam Width: "+document.getElementById("beamwidth").value;
}


function showNav() {
    nav = document.getElementsByTagName("nav")[0];
    nav.style.marginLeft = "0px";
}

function hideNav() {
    nav = document.getElementsByTagName("nav")[0];
    nav.style.marginLeft = "-300px";
}

function clearGrid() {
    var inqueue = document.getElementsByClassName("inqueue");
    var l = inqueue.length
    for (var i = 0; i < l; i++) {
        inqueue[0].classList.remove("inqueue");
    }
    var processed = document.getElementsByClassName("processed");
    var l = processed.length
    for (var i = 0; i < l; i++) {
        processed[0].classList.remove("processed");
    }
    var path = document.getElementsByClassName("path");
    var l = path.length
    for (var i = 0; i < l; i++) {
        document.body.removeChild(path[0])
    }
}


function makeGrid() {
    box = [];
    grid = document.getElementById("grid");
    grid.innerHTML = "";
    n = Math.floor((window.innerWidth - margin) / 40);
    m = Math.floor(window.innerHeight / 40);
    for (var j = 0; j <= m; j++) {
        temp = []
        for (var i = 0; i <= n; i++) {
            cell = document.createElement("div");
            cell.classList = ["cell"];
            cell.style.left = 40 * i + "px";
            cell.style.top = 40 * j + "px";
            if(i==n || j==m){
                cell.classList.add("wall");
                temp.push(2);
                grid.appendChild(cell);
                continue;
            }
            cell.id = j + "x" + i;
            drawingElement(cell);
            cell.oncontextmenu = addCheckpoint(cell.id);
            grid.appendChild(cell);
            temp.push(0);
        }
        box.push(temp);
    }
    if (!showing) {
        start = document.getElementById("start");
        stop = document.getElementById("stop");

        box[Math.floor(m / 2)][Math.floor(n / 4)] = 1;
        document.getElementById(Math.floor(m / 2) + "x" + Math.floor(n / 4)).classList = "start cell";
        start.style.left = margin + 40 * Math.floor(n / 4) + 20 + "px";
        start.style.top = 40 * Math.floor(m / 2) + 20 + "px";
        start.style.zIndex = Math.floor(m / 2);

        box[Math.floor(m / 2)][Math.floor(3 * n / 4)] = 1;
        document.getElementById(Math.floor(m / 2) + "x" + Math.floor(3 * n / 4)).classList = "stop cell";
        stop.style.left = margin + 40 * Math.floor(3 * n / 4) + 20 + "px";
        stop.style.top = 40 * Math.floor(m / 2) + 20 + "px";
        stop.style.zIndex = Math.floor(m / 2);
    } else {
        start = document.getElementById("start");
        start = {
            x: Math.floor((start.offsetLeft - margin) / 40),
            y: Math.floor(start.offsetTop / 40)
        };
        stop = document.getElementById("stop");
        stop = {
            x: Math.floor((stop.offsetLeft - margin) / 40),
            y: Math.floor(stop.offsetTop / 40)
        };
        box[start.y][start.x] = 1;
        box[stop.y][stop.x] = 1;
    }
}

makeGrid();


function addCheckpoint(id) {
    function addCheckpoint() {
        if (showing) {
            clearGrid();
            showing = false;
        }
        i = id.split("x");
        if (box[Number(i[0])][Number(i[1])]) {
            return false;
        }
        if (chid > 4) {
            return false;
        }
        ch = document.createElement("img");
        if(multistart){
            ch.src = "images/green.svg";
            document.getElementById(id).classList.add("start");
        }else if(multidest){
            ch.src = "images/red.svg";
            document.getElementById(id).classList.add("stop");
        }else{
            ch.src = "images/yellow" + (chid + 1) + ".svg";
        }
        ch.classList = "draggable checkpoint";
        ch.id = "checkpoint" + chid;
        ch.oncontextmenu = removeCheckpoint(chid);
        chid++;
        ch.style.zIndex = Number(i[0]);
        ch.style.top = 40 * Number(i[0]) + 20 + "px";
        ch.style.left = margin + 40 * Number(i[1]) + 20 + "px";
        dragElement(ch);
        box[Number(i[0])][Number(i[1])] = 1;
        document.body.appendChild(ch);
        return false
    }
    return addCheckpoint
}

function removeCheckpoint(id) {
    function remove(e) {
        if (showing) {
            clearGrid();
            showing = false;
        }
        e.preventDefault();
        ch = document.getElementById("checkpoint" + id);
        i = ch.style.left;
        i = Number(i.substr(0, i.length - 2));
        i = Math.floor((i - margin) / 40);
        j = ch.style.top;
        j = Number(j.substr(0, j.length - 2));
        j = Math.floor(j / 40);
        box[j][i] = 0;
        ch.parentNode.removeChild(ch);
        if(multistart){
            document.getElementById(j+'x'+i).classList.remove("start");
        }else if(multidest){
            document.getElementById(j+'x'+i).classList.remove("stop");
        }
        chid--;
        for (var i = id + 1; i < chid + 1; i++) {
            ch = document.getElementById("checkpoint" + i);
            ch.id = "checkpoint" + (i - 1);
            ch.oncontextmenu = removeCheckpoint(i - 1);
            if(!multistart && !multidest)
                ch.src = "images/yellow" + i + ".svg";
        }
        return false;
    }
    return remove;
}

function dragElement(elmnt) {
    var pos1 = 0,
        pos2 = 0,
        pos3 = 0,
        pos4 = 0,
        sx = 0,
        sy = 0,
        classes = "";
    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        if (showing) {
            clearGrid();
            showing = false;
        }
        e = e || window.event;
        if (e.button != 0) return false;
        e.preventDefault();
        elmnt.style.transform = "scale(1.2) translate(-35%,-70%)";
        elmnt.style.cursor = "grabbing";
        elmnt.style.zIndex = "1000";
        pos3 = e.clientX;
        pos4 = e.clientY;
        sx = elmnt.style.left;
        sy = elmnt.style.top;
        box[Math.floor(Number(sy.substr(0, sy.length - 2)) / 40)][Math.floor((Number(sx.substr(0, sx.length - 2)) - margin) / 40)] = 0;
        thiscell = document.getElementById(Math.floor(Number(sy.substr(0, sy.length - 2)) / 40) + "x" + Math.floor((Number(sx.substr(0, sx.length - 2)) - margin) / 40))
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
        t = Number(elmnt.style.top.substr(0, elmnt.style.top.length - 2));
        l = Number(elmnt.style.left.substr(0, elmnt.style.left.length - 2));
        if (box[Math.floor(t / 40)][Math.floor((l - margin) / 40)] != 0) {
            elmnt.style.top = sy;
            elmnt.style.left = sx;
            box[Math.floor(Number(sy.substr(0, sy.length - 2)) / 40)][Math.floor((Number(sx.substr(0, sx.length - 2)) - margin) / 40)] = 1;
            document.getElementById(Math.floor(Number(sy.substr(0, sy.length - 2)) / 40) + "x" + Math.floor((Number(sx.substr(0, sx.length - 2)) - margin) / 40)).classList = classes;
            elmnt.style.zIndex = Math.floor(Number(sy.substr(0, sy.length - 2)) / 40);
        } else {
            elmnt.style.top = 40 * Math.floor(t / 40) + 20 + "px";
            elmnt.style.left = Math.max(margin + 40 * Math.floor((l - margin) / 40) + 20, margin + 20) + "px";
            box[Math.floor(t / 40)][Math.floor((l - margin) / 40)] = 1;
            document.getElementById(Math.floor(t / 40) + "x" + Math.floor((l - margin) / 40)).classList = classes;
            elmnt.style.zIndex = Math.floor(t / 40);
        }
        elmnt.style.transform = "scale(1) translate(-35%,-70%)";
        elmnt.style.cursor = "grab";
    }
}

for (let elmnt of document.getElementsByClassName("draggable")) {
    dragElement(elmnt);
}

function drawingElement(elmnt) {
    var pos1 = 0,
        pos2 = 0,
        pos3 = 0,
        pos4 = 0;
    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        if (showing) {
            clearGrid();
            showing = false;
        }
        e = e || window.event;
        e.preventDefault();
        if (e.button != 0) return false;
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        i = elmnt.id.split('x');
        if (box[Number(i[0])][Number(i[1])] == 2) {
            box[Number(i[0])][Number(i[1])] = 0;
            elmnt.classList = "cell";
            document.onmousemove = elementDragOFF;
        } else if (box[Number(i[0])][Number(i[1])] == 0) {
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
        i = Math.floor((pos3 - margin) / 40);
        j = Math.floor(pos4 / 40);
        if (box[j][i] != 1) {
            box[j][i] = 2;
            document.getElementById(j + 'x' + i).classList = "wall cell"
        }
    }

    function elementDragOFF(e) {
        e = e || window.event;
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        i = Math.floor((pos3 - margin) / 40);
        j = Math.floor(pos4 / 40);
        if (box[j][i] != 1) {
            box[j][i] = 0;
            document.getElementById(j + 'x' + i).classList = "cell";
        }
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

x = document.createElement("img")
x.src = "images/yellow1.svg";
x = document.createElement("img")
x.src = "images/yellow2.svg";
x = document.createElement("img")
x.src = "images/yellow3.svg";
x = document.createElement("img")
x.src = "images/yellow4.svg";
x = document.createElement("img")
x.src = "images/yellow5.svg";


window.onload = ()=> {
    document.getElementById("loading").style.opacity = 0;
    setTimeout(()=>{
        document.getElementById("loading").style.display = "none";
    }, 300);
};