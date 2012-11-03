$(document).ready(function() {
      navigator.geolocation.getCurrentPosition(function(position) {
        var lat = "";
        var lng = "";
        lat = position.coords.latitude;
        lng = position.coords.longitude;

        if(lat!=="" && lng!=="")
        {
          $.cookie('geo_lat', lat , { expires: 10, path: '/' });
          $.cookie('geo_lng', lng , { expires: 10, path: '/' });
        }
      });

      var geo_lat = $.cookie('geo_lat');
      var geo_lng = $.cookie('geo_lng');

      if(geo_lat===null && geo_lng===null)
      {
        window.location.replace('/');
      }

});