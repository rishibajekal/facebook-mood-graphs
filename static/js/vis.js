/**
 *  This file will hold the first visualization. This will plot time vs. sentiment.
*/


var data = [];

$(document).ready(function(){

    $.getJSON("/api/timeline", function(d){
        data = d;

        var margin = {top: 30, right: 10, bottom: 10, left: 50},
            width = 1200 - margin.left - margin.right,
            interval = 15,
            height = (data.length * interval) - margin.top - margin.bottom;

        var x = d3.scale.linear()
            .domain([-1, 1])
            .range([0, width])
            .nice();

        var y = d3.scale.ordinal()
            .domain(d3.range(data.length))
            .rangeRoundBands([0, height], 0.05);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("top");

        var svg = d3.select("#graph-box").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        function colorPicker(d){
            var val = Math.floor((d.sentiment + 1) * 5);
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

        svg.selectAll(".bar")
            .data(data)
          .enter().append("rect")
            .attr("fill", "rgb(254,224,139)")
            .attr("x", function(d){return x(0);} )
            .attr("y", function(d, i) { return y(i); })
            .attr("width", 0)
            .attr("height", y.rangeBand())
            .transition().duration(2000).delay(function(d,i){return 5*i;})
            .attr("fill", colorPicker)
            .attr("stroke", colorPicker)
            .attr("stroke-width", 1)
            .attr("opacity", 0.9)
            .attr("x", function(d) { return x(Math.min(0, d.sentiment)); })
            .attr("y", function(d, i) { return y(i); })
            .attr("width", function(d) { return Math.abs(x(d.sentiment) - x(0)); })
            .attr("id", function(d,i){return i;})
            .attr("height", y.rangeBand());

        svg.selectAll("rect")
            .on("mouseover", function(d){
                var id = $(this).attr("id");
                console.log(data[id].status);
                $("#status-box").text(data[id].status + " -- " + data[id].month + ' ' + data[id].day + ', ' +data[id].year);
            }).on("mouseout", function(d){
                $("#status-box").text("");
            });

        svg.append("g")
            .attr("class", "x axis")
            .call(xAxis);


       /* $(window).scroll(function(){
            var svg_y = window.pageYOffset- margin.top;
            if (svg_y > 0){
                var week_num = svg_y/interval;
                week_num = Math.ceil(week_num);
                $("#date").children().remove();
                $("#date").append("<p>" + String(data[week_num].month) + ', ' + String(data[week_num].year) + "</p>");
            }
        });*/
    });
});