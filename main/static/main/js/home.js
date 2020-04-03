(function() {
    function latLonToNESW(pos, symbols) {
        if (pos > 180) {
            pos -= 360
        }
        if (pos > 0) {
            return [pos, symbols[0]];
        } else if (pos < 0) {
            return [pos, symbols[1]];
        } else {
            return [pos, ''];
        }
    }
    
    // https://github.com/perfectline/geopoint
    function getCurrentPositionCallback(position) {
        let lon = latLonToNESW(position.coords.longitude, 'EW');
        let lat = latLonToNESW(position.coords.latitude, 'NS');
        let point = new GeoPoint(lon[0], lat[0]);
        $('#lon').html(point.getLonDeg() + ' ' + lon[1]);
        $('#lat').html(point.getLatDeg() + ' ' + lat[1]);
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
            $('#time').html(
                d.toLocaleDateString().replace(/\s/g, "").replace(d.getFullYear().toString(), "") +
                ' <b>' + d.toLocaleTimeString() + '</b>')
    
            this.counter += 1;
            if (this.counter > 60) {  // 15 s
                getLocation();
                this.counter = 0;
            }
        }, 250);
    }
    
    updateTime();
})();
