/*
 * This file holds the second visualization, a visualization by location vs sentiment
 */

var width = 1460;
var height = 700;
var s = 1460;
var t = [730,350];
var tiny_s = 1;
var tiny_t = [width/2,height/2];
var projection = d3.geo.equirectangular().scale(s).translate(t);
var tiny_projection = d3.geo.equirectangular().scale(tiny_s).translate(tiny_t);

var path = d3.geo.path()
    .projection(projection);

var tiny_path = d3.geo.path()
    .projection(tiny_projection);

var zoom = d3.behavior.zoom()
    .translate(projection.translate())
    .scale(projection.scale())
    .scaleExtent([height, 20 * height])
    .on("zoom", zoom1);

function colorPicker(d){
    var val = Math.floor((d.properties.sentiment + 1) * 5);
    switch(val){
        case 0: return "rgb(165,0,38)";
        case 1: return "rgb(215,48,39)";
        case 2: return "rgb(244,109,67)";
        case 3: return "rgb(253,174,97)";
        case 4: return "rgb(254,224,139)";
        case 5: return "rgb(217,239,139)";
        case 6: return "rgb(166,217,106)";
        case 7: return "rgb(102,189,99)";
        case 8: return "rgb(26,152,80)";
        case 9:
        case 10: return "rgb(0,104,55)";
    }
}

// zoom1 and click take care of zooming functionality
function zoom1() {
    projection.translate(d3.event.translate).scale(d3.event.scale);
    countries.selectAll("path").attr("d", path);

    circles.selectAll('circle')
        .attr("cx", function(d){return projection(d.geometry.coordinates)[0];})
        .attr("cy", function(d){return projection(d.geometry.coordinates)[1];});
}

function click(d) {
    var centroid = path.centroid(d),
        translate = projection.translate();

    projection.translate([
        translate[0] - centroid[0] + width / 2,
        translate[1] - centroid[1] + height / 2
    ]).scale(2000);

    zoom.translate(projection.translate()).scale(projection.scale());

    countries.selectAll("path").transition()
        .duration(1000)
        .attr("d", path);

    circles.selectAll('circle').transition().duration(1000)
        .attr("cx", function(d){return projection(d.geometry.coordinates)[0];})
        .attr("cy", function(d){return projection(d.geometry.coordinates)[1];});
}

function reset(){
    projection.translate(t).scale(s);

    zoom.translate(projection.translate()).scale(projection.scale());

    countries.selectAll("path").transition()
        .duration(1000)
        .attr("d", path);

    circles.selectAll('circle').transition().duration(1000)
        .attr("cx", function(d){return projection(d.geometry.coordinates)[0];})
        .attr("cy", function(d){return projection(d.geometry.coordinates)[1];});
}

$("#reset").click(reset);

// actually manipulate the svg
var svg = d3.select("#map-box").append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .style("position", "relative")
    .style("left", "0px")
    .style("top", "0px")
    .call(zoom)
    .on("dblclick.zoom", null);

var countries = svg.append("svg:g")
    .attr("id", "countries");


var circles = svg.append("svg:g")
    .attr("id", "circles");

function draw() {
    var num = 0;
    d3.json("./static/js/json/world_countries.json", function(json) {
        countries.selectAll("path").remove();
        countries.selectAll("path")
        .data(json.features)
        .enter().append("svg:path")
        .attr("d", tiny_path)
        .attr("fill", "rgb(130, 130, 145)")
        .attr("id", function(d){return ++num;})
        .on("click", click)
        .transition().duration(1500)
        .attr("d", path);
    });
}

draw(); //perform the initial draw

function plot() {
    var statuses = {
        type: "FeatureCollection",
        features: [
            {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [124, -54]
                },
                properties: {sentiment: -0.4}
            },
            {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [-100, 59]
                },
                properties: {sentiment: 0.8}
            },
            {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [0, 9]
                },
                properties: {sentiment: 1}
            },
            {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [-183, 89]
                },
                properties: {sentiment: 0.2}
            },
            {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [134, -54]
                },
                properties: {sentiment: -0.7}
            },
            {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [144, 80]
                },
                properties: {sentiment: 0.4}
            }
        ]
    };

    circles.selectAll("circle")
        .remove();

    circles.selectAll("circle")
        .data(statuses.features)
        .enter().append("svg:circle")
        .attr("cx", width/2)
        .attr("cy", height/2)
        .attr("r", 1)
        .transition().duration(1500)
        .attr("cx", function(d){return projection(d.geometry.coordinates)[0];})
        .attr("cy", function(d){return projection(d.geometry.coordinates)[1];})
        .attr("r", 5)
        .attr("fill-opacity", 0.8)
        .attr("stroke", colorPicker)
        .attr("fill", colorPicker);
}

plot(); //perform the plot of the data

