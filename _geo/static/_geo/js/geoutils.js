// PointStack - saved geopoints
// GeoUtils

/*************
* PointStack *
*************/
/* examples:
azimuth(0)   // average azimuth
azimuth()    // current azimuth
speed_kmh(0) // average speed
speed_kmh()  // current speed
sec2hms(time_sec(0))  // full time
distance_formatted(0) // full distance
*/

PointStack = function() {
    this.stack = [];
    this.gu = null;  // methods which need this will instantiate GeoUtils here
};

PointStack.prototype = {
    minTimeForSpeed: 3,     // refuse count speed (ei. return 0) if time interval is shorter

    clear: function() {
        this.stack = [];
    },

    push: function(lat, lon) {
        this.stack.push([lat, lon, Date.now()]);
    },

    points: function() {
        return this.stack.length;
    },

    fix_pointPar: function(point) {
        if (typeof point === "undefined") {
            let points = this.points();
            return this.goodStartPointForCalc(points)  // give point >33m distant
        } else if (point < 0) {
            return Math.max(0, this.points() + point);
        } else {
            return point;
        }
    },

    // time in seconds from some point (backwards if negative, for whole stack if undefined)
    time_sec: function(point) {
        if (!this.points()) {
            return 0;
        }
        point = this.fix_pointPar(point);
        let n = Date.now();
        return Math.round((n - this.stack[point][2]) / 1000);
    },

    // sec -> n:nn:nn
    sec2hms: function(sec) {
        let min = Math.floor(sec/60);
        sec = sec % 60;
        if (min >= 60) {
            return '' + Math.floor(min/60) + ':' + ("0" + (min % 60)).slice(-2) + ':' + ("0" + sec).slice(-2);
        } else {
            return '' + min + ':' + ("0" + sec).slice(-2);
        }
    },

    // TODO last time -> last points (or index of the starting point)

    // speed from some point to end (backwards if negative, for whole stack if undefined)
    speed_ms: function(point) {
        let points = this.points();
        if (points <= 1) {
            return 0;
        }
        point = this.fix_pointPar(point);
        let time = this.time_sec(point);
        if (time < this.minTimeForSpeed) {
            return 0;
        }
        let dist = this._distance(point, points);
        return dist * 1000 / time;
    },

    speed_kmh: function(point) {
        return Math.round(this.raw_speed_kmh(point) * 10) / 10;
    },
    raw_speed_kmh: function(point) {
        return this.speed_ms(point) * 3.6;
    },

    azimuth: function(point) {
        return '' + Math.round(this.raw_azimuth(point)) + '°';
    },
    raw_azimuth: function(point) {
        let points = this.points();
        if (points <= 1) {
            return '*';
        }
        point = this.fix_pointPar(point);
        let start = this.stack[point];
        let stop = this.stack[points - 1];
        return this.getGU().azimuth(start[0], start[1], stop[0], stop[1])
    },

    distance_formatted: function(point) {
        let dist = this.distance(point);
        if (dist < 1) {
            return '' + Math.round(dist * 1000) + ' m';
        } else {
            return '' + Math.round(dist * 100) / 100 + ' km'
        }
    },

    distance: function(point) {
        let points = this.points();
        if (points <= 1) {
            return 0;
        }
        point = this.fix_pointPar(point);
        return this._distance(point, points);
    },

    _distance: function(point, points) {
        let distance = 0;
        let previous_step = 0;
        for (let i = point; i < points - 1; i++) {
            // basic
            let start = this.stack[i];
            let stop = this.stack[i+1];
            let step = this.getGU().distance_era(start[0], start[1], stop[0], stop[1]);
            distance += step;

            // correction
            if (previous_step > 0) {
                let start = this.stack[i-1];
                let s1 = this.getGU().distance_era(start[0], start[1], stop[0], stop[1]);
                let s2 = previous_step + step;
                if (s1) {
                    distance += (s2 / s1 - 1) * s1;
                }
            }

            let previous_step = step;
            make_correction = true;
        }
        return distance;
    },

    goodStartPointForCalc: function(points) {
        let stop = this.stack[points - 1];
        let absLat = Math.abs(stop[0]);
        let lonCoef = (90 - absLat) / 60;  // multiply longitude Δ to get better estimate with regard to latitude
        let minDist = 0.0003; // such Δ of lat/lon is about 33m and we use this to take well far starting point
        for (let i = points-2; i >=0; i--) {
            let thisOne = this.stack[i];
            let estimate1 = Math.abs(thisOne[0] - stop[0] + 0.3 * lonCoef * (thisOne[1] - stop[1]));
            let estimate2 = Math.abs(0.3 * (thisOne[0] - stop[0]) + lonCoef * (thisOne[1] - stop[1]));
            if (Math.max(estimate1, estimate2) >= minDist) {
                return i;
            }
        }
        return 0;
    },

    // property behaviour for this.gu
    getGU: function() {
        if (!this.gu) {
            this.gu = new GeoUtils();
        }
        return this.gu;
    }
};

/***********
* GeoUtils *
***********/
GeoUtils = function() {
};

GeoUtils.prototype = {
    // https://www.movable-type.co.uk/scripts/latlong.html ku.oc.epyt-elbavom@oeg-stpircs
    // python port here: https://github.com/mrJean1/PyGeodesy
    
    R: 6371, // in km; 6371e3 in metres

    toRadians: function(arg) {
        return arg * Math.PI / 180;
    },
    toDegrees: function(arg) {
        return arg * 180 / Math.PI;
    },

    // haversine formula to calculate the great-circle distance between two points
    distance: function(lat1, lon1, lat2, lon2) {
        var φ1 = this.toRadians(lat1);
        var φ2 = this.toRadians(lat2);
        var Δφ = this.toRadians(lat2-lat1);
        var Δλ = this.toRadians(lon2-lon1);
        var a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
                Math.cos(φ1) * Math.cos(φ2) *
                Math.sin(Δλ/2) * Math.sin(Δλ/2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        var d = this.R * c;
        return d;
    },

    // Spherical Law of Cosines
    // ... While simpler, the law of cosines is slightly slower than the haversine, in my tests
    // see also: https://www.geodatasource.com/developers/javascript
    distance_slc: function(lat1, lon1, lat2, lon2) {
        var φ1 = this.toRadians(lat1);
        var φ2 = this.toRadians(lat2);
        var Δλ = this.toRadians(lon2-lon1);
        var d = Math.acos( Math.sin(φ1)*Math.sin(φ2) + Math.cos(φ1)*Math.cos(φ2) * Math.cos(Δλ) ) * this.R;
        return d;
    },

    // Equirectangular approximation
    // ... fast ; Praha-Brno 184 km cca +10m
    distance_era: function(lat1, lon1, lat2, lon2) {
        var φ1 = this.toRadians(lat1);
        var φ2 = this.toRadians(lat2);
        var λ1 = this.toRadians(lon1);
        var λ2 = this.toRadians(lon2);
        var x = (λ2-λ1) * Math.cos((φ1+φ2)/2);
        var y = (φ2-φ1);
        var d = Math.sqrt(x*x + y*y) * this.R;
        return d;
    },

    // initial bearing ie. forward azimuth (ie. outgoing bearing; the later and final bearing differs)
    // for final bearing: count the initial bearing from the end point and reverse it: θ = (θ+180) % 360.
    azimuth: function(lat1, lon1, lat2, lon2) {      // <0, +360), 0 to the North, then E->S->W
        return (this.bearing(lat1, lon1, lat2, lon2) + 360) % 360;
    },
    bearing: function(lat1, lon1, lat2, lon2) {      // <-180, +180>, 0 to the North, + to the East
        return this.toDegrees(this.bearing_rad(lat1, lon1, lat2, lon2));
    },
    bearing_rad: function(lat1, lon1, lat2, lon2) {  // <-PI, +PI>, 0 to the North, + to the East
        var φ1 = this.toRadians(lat1);
        var φ2 = this.toRadians(lat2);
        var λ1 = this.toRadians(lon1);
        var λ2 = this.toRadians(lon2);
        var y = Math.sin(λ2-λ1) * Math.cos(φ2);
        var x = Math.cos(φ1)*Math.sin(φ2) - Math.sin(φ1)*Math.cos(φ2)*Math.cos(λ2-λ1);
        var brng = Math.atan2(y, x);
        return brng;
    },

    // https://www.movable-type.co.uk/scripts/latlong.html (end)

    k2m: function(k) {return k / 1.609344},
    m2k: function(m) {return m * 1.609344},
    n2m: function(n) {return n / 0.8684},
    m2n: function(m) {return m * 0.8684},
    k2n: function(k) {return k / 0.5395987},
    n2k: function(n) {return n * 0.5395987},
};
