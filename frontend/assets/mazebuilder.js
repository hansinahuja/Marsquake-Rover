// Functions for getting and drawing Random Mazes.

function setMaze(walls) {
    // Set the maze as sent by the API
    var i = 0,
        int = 0;

    function setWall() {
        wall = walls[i];
        var x = wall.x,
            y = wall.y;
        cell = document.getElementById(y + 'x' + x);
        cell.classList.add("wall");
        box[y][x] = 2;
        i++;
        if (i == walls.length) {
            clearInterval(int);
            document.body.style.pointerEvents = "";
            showNav();
        }
    }
    int = setInterval(setWall, 10);
}

function randomMaze() {
    // Request the random maze from the API
    hideNav();
    document.body.style.pointerEvents = "none";
    over = document.getElementById("overlay");
    over.style.display = "block";
    disableWormhole();
    document.getElementById("wormhole").checked = false;
    clearGrid();
    makeGrid();
    document.getElementById("bidirec").disabled = false;
    document.getElementById("bidirecl").style.opacity = "1";

    deleteCheckpoints();

    var data = new FormData();
    data.append('algo', 1 * document.getElementById("mazealgo1").checked);
    data.append('length', box[0].length - 1);
    data.append('breadth', box.length - 1);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/generatemaze/");
    xhr.onload = () => {
        // When the server responds, draw the maze and place the start and end points
        resp = JSON.parse(xhr.response);
        console.log(resp);

        over.style.display = "none";
        var x = resp.source.x,
            y = resp.source.y;
        start = document.getElementById("start");
        t = parseInt(start.style.top.substr(0, start.style.top.length - 2));
        l = parseInt(start.style.left.substr(0, start.style.left.length - 2));
        t = Math.floor(t / 40);
        l = Math.floor((l - margin) / 40);
        box[t][l] = 0;
        box[y][x] = 1;
        document.getElementById(t + "x" + l).classList.remove("start");
        document.getElementById(y + "x" + x).classList.add("start");
        start.style.transition = "0.7s";
        setTimeout(() => start.style.transition = "", 700);
        start.style.top = 40 * y + 20 + "px";
        start.style.left = 40 * x + 20 + margin + "px";

        x = resp.destination.x, y = resp.destination.y;
        stop = document.getElementById("stop");
        t = parseInt(stop.style.top.substr(0, stop.style.top.length - 2));
        l = parseInt(stop.style.left.substr(0, stop.style.left.length - 2));
        t = Math.floor(t / 40);
        l = Math.floor((l - margin) / 40);
        box[t][l] = 0;
        box[y][x] = 1;
        document.getElementById(t + "x" + l).classList.remove("stop");
        document.getElementById(y + "x" + x).classList.add("stop");
        stop.style.transition = "0.7s";
        setTimeout(() => stop.style.transition = "", 700);
        stop.style.top = 40 * y + 20 + "px";
        stop.style.left = 40 * x + 20 + margin + "px";

        setMaze(resp.walls);
    }
    xhr.send(data);
}