function convertLatLon(pos, symbols) {
    if (pos > 180) {
        pos -= 360
    }
    if (pos > 0) {
        return '' + pos + ' ' + symbol[0];
    } else if (pos < 0) {
        return '' + pos + ' ' + symbol[1];
    } else {
        return '' + pos;
    }
}

function getCurrentPositionCallback(position) {
    $('#lat').html(position.coords.latitude);
    $('#lon').html(position.coords.longitude);
    //$('#lat').html(convertLatLon(position.coords.latitude, 'NS'));
    //$('#lon').html(convertLatLon(position.coords.longitude, 'EW'));
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getCurrentPositionCallback);
    }
}

function updateTime() {
    counter = 1000;
    setInterval(function () {
        d = new Date();
        $('#time').html(d.toLocaleDateString().replace(/\s/g, "") + ' <b>' + d.toLocaleTimeString() + '</b>')

        this.counter += 1;
        if (this.counter > 60) {  // 15 s
            getLocation();
            this.counter = 0;
        }
    }, 250);
}

updateTime();
