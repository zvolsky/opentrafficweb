Page_Home = function() {
    this.timeBeat = 250;  // ms
    this.geoBeat = 15;    // s
    this.beatsToGeo = 1000 / this.timeBeat * this.geoBeat
    this.ps = new PointStack();
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
    },
    
    // https://github.com/perfectline/geopoint
    getCurrentPositionCallback: function(position) {
        let lat = this.latLonToNESW(position.coords.latitude, 'NS');
        let lon = this.latLonToNESW(position.coords.longitude, 'EW');
        let point = new GeoPoint(Math.abs(lon[0]), Math.abs(lat[0]));
        $('#lat').html(point.getLatDeg() + ' ' + lat[1]);
        $('#lon').html(point.getLonDeg() + ' ' + lon[1]);

        this.ps.push(lat[0], lon[0]);
        $('#azimuth').html(this.ps.azimuth(0));
        $('#azimuth_now').html(this.ps.azimuth());
        $('#speed').html(this.ps.speed_kmh(0));
        $('#speed_now').html(this.ps.speed_kmh());
        $('#duration').html(this.ps.sec2hms(this.ps.time_sec(0)));
        $('#distance').html(this.ps.distance_formatted(0));
    },
    
    getLocation: function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(this.getCurrentPositionCallback.bind(this));
        }
    },
    
    updateTime: function() {
        // TODO: better bind ?
        var getLocation = this.getLocation.bind(this);
        var beatsToGeo = this.beatsToGeo;  // make the first immediatelly (xx+1 > xx)
        var counter = beatsToGeo;  // make the first immediatelly (xx+1 > xx)
        var timer = setInterval(function () {
            d = new Date();
            $('#time').html(
                d.toLocaleDateString().replace(/\s/g, "").replace(d.getFullYear().toString(), "") +
                ' <b>' + d.toLocaleTimeString() + '</b>')
    
            counter += 1;
            if (counter > beatsToGeo) {
                getLocation();
                counter = 0;
            }
            // clearInterval(timer) // debug getLocation()
        }, this.timeBeat);
    }
};

ph = new Page_Home();
ph.updateTime();
