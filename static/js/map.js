// Creating map object
var myMap = L.map("map", {
      center: [39.0119, -98.4842],
      zoom: 3

    });
  
  L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
      tileSize: 512,
      maxZoom: 18,
      zoomOffset: -1,
      id: "mapbox/streets-v11",
      accessToken: "pk.eyJ1Ijoic291amk4OCIsImEiOiJja2NodWI2eHUwbDBkMnhsaThuMTR2OTY0In0.9h5D2hS0u5KoOKGW7kNpPg"
    }).addTo(myMap);
    
  d3.json("api/locationdata").then(function (data) {
      

    var greenIcon = L.icon({
      iconUrl: '../static/images/yumminky-pin-06-512.webp',
      // shadowUrl: 'leaf-shadow.png',

      iconSize:     [32, 32], // size of the icon
      // shadowSize:   [50, 64], // size of the shadow
      iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
      shadowAnchor: [4, 62],  // the same for the shadow
      popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
  });


    // var marker = Object.keys(data).forEach(key => L.marker([data[key].lat, data[key].lng],{icon: greenIcon}).bindPopup("Brewery Name:" + data[key].brewery_name + "<hr>"+  "Beer Name:" + data[key].beer_name+ "<hr>"+  "Country:" + data[key].country).addTo(myMap));
    var marker = Object.keys(data).forEach(function(key) {
      var beerNames = " ";
      var beers = data[key].beers.forEach(function(beer) { beerNames = beerNames.concat(beer.beer_name + ", ") });
      L.marker([data[key].lat, data[key].lng],{icon: greenIcon}).bindPopup("Brewery Name:" + data[key].brewery_name + "<hr>"+  "Beer Name:" + beerNames.slice(0,beerNames.length-2)+ "<hr>"+  "Country:" + data[key].country).addTo(myMap);

    });
  });