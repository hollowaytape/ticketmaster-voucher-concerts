var settlementUrl = "http://concerts.livenation.com/microsite/settlement#colMainWrap";


var lat = 38.889931;   // default: washington, DC
var lng = -77.009003;

navigator.geolocation.getCurrentPosition(function(location) {
  lat = location.coords.latitude;
  lng = location.coords.longitude;
});

var myLatlng = new google.maps.LatLng(lat, lng);
var mapOptions = {
  zoom: 8,
  center: myLatlng,
  mapTypeId: 'roadmap'
};
var map = new google.maps.Map(document.getElementById('map'),
    mapOptions);

