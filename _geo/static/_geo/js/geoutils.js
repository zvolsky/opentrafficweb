PointStack = function(interval) {
    this.stack = [];
    this.interval = interval;
    this.beat = typeof interval === "number";
};

PointStack.prototype = {
    clear: function() {
        this.stack = [];
    },

    points: function() {
        return this.stack.length;
    },
};

GeoUtils = function() {
};

GeoUtils.prototype = {
    // https://www.movable-type.co.uk/scripts/latlong.html
    R = 6371; // in km; 6371e3 in metres

    // haversine formula to calculate the great-circle distance between two points
    distance: function(lat1, lon1, lat2, lon2) {
        var φ1 = lat1.toRadians();
        var φ2 = lat2.toRadians();
        var Δφ = (lat2-lat1).toRadians();
        var Δλ = (lon2-lon1).toRadians();
        var a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
                Math.cos(φ1) * Math.cos(φ2) *
                Math.sin(Δλ/2) * Math.sin(Δλ/2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        var d = this.R * c;
        return d;
    },

    // Spherical Law of Cosines
    // ... While simpler, the law of cosines is slightly slower than the haversine, in my tests
    distance_slc: function(lat1, lon1, lat2, lon2) {
        var φ1 = lat1.toRadians();
        var φ2 = lat2.toRadians();
        var Δλ = (lon2-lon1).toRadians();
        var d = Math.acos( Math.sin(φ1)*Math.sin(φ2) + Math.cos(φ1)*Math.cos(φ2) * Math.cos(Δλ) ) * this.R;
        return d;
    },

    // Equirectangular approximation
    // ... fast ; Praha-Brno 184 km cca +10m
    distance_era: function(lat1, lon1, lat2, lon2) {
        var φ1 = lat1.toRadians();
        var φ2 = lat2.toRadians();
        var λ1 = lon1.toRadians();
        var λ2 = lon2.toRadians();
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
        return this.bearing_rad(lat1, lon1, lat2, lon2).toDegrees();
    },
    bearing_rad: function(lat1, lon1, lat2, lon2) {  // <-PI, +PI>, 0 to the North, + to the East
        var φ1 = lat1.toRadians();
        var φ2 = lat2.toRadians();
        var λ1 = lon1.toRadians();
        var λ2 = lon2.toRadians();
        var y = Math.sin(λ2-λ1) * Math.cos(φ2);
        var x = Math.cos(φ1)*Math.sin(φ2) - Math.sin(φ1)*Math.cos(φ2)*Math.cos(λ2-λ1);
        var brng = Math.atan2(y, x);
        return brng;
    },

    // https://www.movable-type.co.uk/scripts/latlong.html (end)

    /*
    // Spherical Law of Cosines
    // LGPLv3 : https://www.geodatasource.com/developers/javascript
    distance: function(lat1, lon1, lat2, lon2, unit) {  // unit: (K)ilometers, (M)iles, (N)autilus
        if ((lat1 == lat2) && (lon1 == lon2)) {
            return 0;
        }
        else {
            var radlat1 = Math.PI * lat1/180;
            var radlat2 = Math.PI * lat2/180;
            var theta = lon1-lon2;
            var radtheta = Math.PI * theta/180;
            var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
            if (dist > 1) {
                dist = 1;
            }
            dist = Math.acos(dist);
            dist = dist * 180/Math.PI;
            dist = dist * 60 * 1.1515;
            if (unit=="K") { dist = dist * 1.609344 }
            if (unit=="N") { dist = dist * 0.8684 }
            return dist;
        }
    }
    */

    k2m: function(k) {return k / 1.609344},
    m2k: function(m) {return m * 1.609344},
    n2m: function(n) {return n / 0.8684},
    m2n: function(m) {return m * 0.8684},
    k2n: function(k) {return k / 0.5395987},
    n2k: function(n) {return n * 0.5395987},
};
