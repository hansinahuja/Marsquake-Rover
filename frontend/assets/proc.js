// Functions related to Path Finding and Path Drawing

var AnimationTime = 10; // How fast the visualisation proceeds
var messageWindow = document.querySelector(".message");
var timeout1 = NaN,
    timeout2 = NaN;

function makeChanges(resp, changes) {
    if (!changes.length) {
        drawPath(resp.path);
        return true;
    }
    // Make the changes returned by the API as an animation
    var i = 0,
        int = 0;
    // This functions is called automatically after AnimationTime delay
    function color() {
        change = changes[i];
        if (change.x == -1) {
            i++;
            return true;
        }
        c = document.getElementById(change.x + "x" + change.y);
        if (change.color == 0) {
            c.classList.remove("inqueue");
            c.classList.remove("processed");
        } else if (change.color == 1) {
            c.classList.add("inqueue");
            c.classList.remove("processed");
        } else {
            c.classList.remove("inqueue");
            c.classList.add("processed");
        }
        i++;
        if (i == changes.length) {
            clearInterval(int);
            drawPath(resp.path);
        }
    }
    int = setInterval(color, AnimationTime);
}

function drawPath(path) {
    // Draw the path at the end
    var i = 0,
        int = 0,
        color = 0,
        off = 0,
        colors = ['#FF0000', "#18008f", "#06a600", "#66008f", "#000000", "#d16200"];
    if (!multidest && !multistart) {
        off = -chid;
    }
    // Error handling
    if (path.length < 2) {
        if (document.getElementById("algorithm").value == "3") {
            alert("No path found! Try increasing the Beam Width. If already maxed out, this terrain is a little too tough for our rover :(");
        }else if (document.getElementById("algorithm").value == "6") {
            alert("No path found! IDA* is a relatively slow algorithm and might've timed out :(");
        } else {
            alert("No path found!");
        }
        document.body.style.pointerEvents = "";
        return 0;
    }
    // Draw line between two adjacent points in the path
    function drawLine() {
        point1 = path[i];
        point2 = path[i + 1];
        if (point2.x == -1) {
            document.getElementById(point1.x + "x" + point1.y).classList.add("final");
        }
        if (point1.x == -1 || point2.x == -1) {
            i++;
            return true;
        }
        if (point1.x == -2 || point2.x == -2) {
            color += 0.5;
            off += 1;
            i++;
            return true;
        }
        if (i)
            document.getElementById(point1.x + "x" + point1.y).classList.add("final");
        var dx = point2.y - point1.y;
        var dy = point2.x - point1.x;
        if (dx * dy) {
            let x = document.createElement("div");
            x.style.transformOrigin = "left";
            x.className = "path";
            x.style.transform = "rotate(" + ((2 - dx) * dy * 45) + "deg)";
            x.style.top = 40 * point1.x + 20 - off + "px";
            x.style.left = 40 * point1.y + margin + 20 - off + "px";
            x.style.backgroundColor = colors[color];
            document.body.appendChild(x);
            setTimeout(() => {
                x.style.width = "59px";
            }, 100);
        } else {
            let x = document.createElement("div");
            x.style.transformOrigin = "left";
            x.className = "path";
            if (dx == 1 && dy == 0) {
                x.style.transform = "rotate(0deg)";
            } else if (dx == 0 && dy == 1) {
                x.style.transform = "rotate(90deg)";
            } else if (dx == -1 && dy == 0) {
                x.style.transform = "rotate(180deg)";
            } else if (dx == 0 && dy == -1) {
                x.style.transform = "rotate(270deg)";
            }
            x.style.top = 40 * point1.x + 20 - off + "px";
            x.style.left = 40 * point1.y + margin + 20 - off + "px";
            x.style.backgroundColor = colors[color];
            document.body.appendChild(x);
            setTimeout(() => {
                x.style.width = "42px";
            }, 10);
        }
        i++;
        if (i == path.length - 1) {
            clearInterval(int);
            document.body.style.pointerEvents = "";
        }
    }
    int = setInterval(drawLine, 10);
}

function gatherData() {
    // Gather the data required for the API call from the environment
    var start, stop, maze = [],
        w = [],
        checkpoints = [];
    start = document.getElementById("start");
    start = {
        y: Math.floor((start.offsetLeft - margin) / 40),
        x: Math.floor(start.offsetTop / 40)
    };
    stop = document.getElementById("stop");
    stop = {
        y: Math.floor((stop.offsetLeft - margin) / 40),
        x: Math.floor(stop.offsetTop / 40)
    };
    portal1 = document.getElementById("portal1");
    portal1 = {
        y: Math.floor((portal1.offsetLeft - margin) / 40),
        x: Math.floor(portal1.offsetTop / 40)
    };
    portal2 = document.getElementById("portal2");
    portal2 = {
        y: Math.floor((portal2.offsetLeft - margin) / 40),
        x: Math.floor(portal2.offsetTop / 40)
    };
    for (var j = 0; j < m; j++) {
        temp = [];
        temp1 = [];
        for (var i = 0; i < n; i++) {
            temp1.push(weights[j][i]);
            if (box[j][i] == 2) {
                temp.push(1);
            } else {
                temp.push(0);
            }
        }
        w.push(temp1);
        maze.push(temp);
    }
    for (var i = 0; i < 5; i++) {
        elmnt = document.getElementById("checkpoint" + i);
        if (!elmnt) break;
        checkpoints.push({
            y: Math.floor((elmnt.offsetLeft - margin) / 40),
            x: Math.floor(elmnt.offsetTop / 40)
        })
    }
    // Send the data as FormData
    var data = new FormData();
    data.append('algo', parseInt(document.getElementById("algorithm").value));
    data.append('heuristic', parseInt(document.getElementById("heuristic").value))
    data.append('relaxation', Number(document.getElementById("relaxation").value))
    data.append('start', JSON.stringify([start]));
    data.append('stop', JSON.stringify([stop]));
    data.append('wormhole', JSON.stringify([portal1, portal2]));
    data.append('wormholeAllowed', document.getElementById("wormhole").checked);
    data.append('cutCorners', 1 * document.getElementById("cutcorners").checked);
    data.append('allowDiagonals', 1 * document.getElementById("allowdiag").checked);
    data.append('biDirectional', 1 * document.getElementById("bidirec").checked);
    data.append('multistart', 1 * document.getElementById("multistart").checked);
    data.append('multidest', 1 * document.getElementById("multidest").checked);
    data.append('beamWidth', document.getElementById("beamwidth").value);
    data.append('checkpoints', JSON.stringify(checkpoints));
    data.append('maze', JSON.stringify(maze));
    data.append('weights', JSON.stringify(w));
    return data;
}

function find() {
    // Handle the API call to the server to find the path
    over = document.getElementById("overlay");
    over.style.display = "block";
    hideNav();
    clearGrid();
    showing = true;
    var data = gatherData();
    // console.log(data.entries());
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/findpath/");
    xhr.onload = () => {
        // When the server responds, make the changes and draw the path
        resp = JSON.parse(xhr.response);
        messageWindow.innerText = "Time Taken: " + resp.timeTaken + "ms";
        messageWindow.style.display = "block";
        messageWindow.style.opacity = "1";
        clearTimeout(timeout1);
        clearTimeout(timeout2);
        timeout1 = setTimeout(
            () => {
                messageWindow.style.opacity = "0";
            }, 5000
        );
        timeout2 = setTimeout(
            () => {
                messageWindow.style.display = "none";
            }, 5500
        );
        over.style.display = "none";
        document.body.style.pointerEvents = "none";
        makeChanges(resp, resp.gridChanges);
        console.log(resp);
    }
    xhr.send(data);
}