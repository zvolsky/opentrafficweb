Page_Home = function() {
    this.timeBeat = 250;  // ms
    this.geoBeat = 15;    // s
    this.beatsToGeo = 1000 / this.timeBeat * this.geoBeat
};

Page_Home.prototype = {
    latLonToNESW: function(pos, symbols) {
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
    getCurrentPositionCallback: function(position) {
        let lat = this.latLonToNESW(position.coords.latitude, 'NS');
        let lon = this.latLonToNESW(position.coords.longitude, 'EW');
        let point = new GeoPoint(lon[0], lat[0]);
        $('#lat').html(point.getLatDeg() + ' ' + lat[1]);
        $('#lon').html(point.getLonDeg() + ' ' + lon[1]);
    }
    
    getLocation: function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(this.getCurrentPositionCallback);
        }
    }
    
    updateTime: function() {
        var counter = this.beatsToGeo;  // make the first immediatelly (xx+1 > xx)
        setInterval(function () {
            d = new Date();
            $('#time').html(
                d.toLocaleDateString().replace(/\s/g, "").replace(d.getFullYear().toString(), "") +
                ' <b>' + d.toLocaleTimeString() + '</b>')
    
            counter += 1;
            if (counter > this.beatsToGeo) {
                this.getLocation();
                counter = 0;
            }
        }, this.timeBeat);
    }
};

ph = new Page_Home();
ph.updateTime();
