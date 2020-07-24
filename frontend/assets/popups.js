function getCookieValue(a) {
    var b = document.cookie.match('(^|;)\\s*' + a + '\\s*=\\s*([^;]+)');
    return b ? b.pop() : '';
}

let show = getCookieValue("show");

if (!show || show == 'true') {
    xhr = new XMLHttpRequest();
    xhr.open("GET", "assets/popups.html");
    xhr.onload = () => {
        document.getElementById("popups").innerHTML = xhr.response;
        let z = 1500;
        var ppups = document.getElementsByClassName('ppup')
        for (let elmnt of ppups) {
            if (z != 1500) {
                elmnt.style.opacity = 0;
            }
            elmnt.style.zIndex = z;
            z--;
        }
    };
    xhr.send();
}

let currentPop = 0;

function nextPop() {
    var ppups = document.getElementsByClassName('ppup');
    ppups[currentPop].style.opacity = "0";

    function hide(id) {
        function temp() {
            ppups[id].style.display = "none";
            ppups[id].style.zIndex = 1500 - id;
            ppups[id + 1].style.zIndex = 1501;
        }
        return temp;
    }
    setTimeout(hide(currentPop), 500);
    if (currentPop == ppups.length - 1) {
        currentPop++;
        return true;
    }
    ppups[currentPop + 1].style.display = "block";
    ppups[currentPop + 1].style.opacity = "1";
    currentPop++;
}

function prevPop() {
    var ppups = document.getElementsByClassName('ppup');
    ppups[currentPop].style.opacity = "0";

    function hide(id) {
        function temp() {
            ppups[id].style.display = "none";
            ppups[id].style.zIndex = 1500 - id;
            ppups[id - 1].style.zIndex = 1501;
        }
        return temp;
    }
    setTimeout(hide(currentPop), 500);
    ppups[currentPop - 1].style.display = "block";
    ppups[currentPop - 1].style.opacity = "1";
    currentPop--;
}