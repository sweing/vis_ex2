let mapWidth = 800;
let mapHeight = 500;
let map = null;
let mapData = null;

function initMap(selected_countries) {

    // loads the world map as topojson
    d3.json("../static/data/world-topo.json").then(function (countries) {

        // defines the map projection method and scales the map within the SVG
        let projection = d3.geoEqualEarth()
            .scale(180)
            .translate([mapWidth / 2, mapHeight / 2]);

        // generates the path coordinates from topojson
        let path = d3.geoPath()
            .projection(projection);

        // configures the SVG element
        let svg = d3.select("#svg_map")
            .attr("width", mapWidth)
            .attr("height", mapHeight);

        // map geometry
        mapData = topojson.feature(countries, countries.objects.countries).features;

        // generates and styles the SVG path
        map = svg.append("g")
            .selectAll('path')
            .data(mapData)
            .enter().append('path')
            .attr('d', path)
            .attr('stroke', 'black')
            .attr('stroke-width', 0.5)
            .attr('fill', 'white')
            .on('mouseover', function(d, event) {
                //console.log(d3.select(this).data()[0].properties.admin)
                mouseOverCountry = d3.select(this).data()[0].properties.admin
                if (selected_countries.includes(mouseOverCountry)) {
                    d3.select(this).attr('fill', 'red');
                    dispatch.call("countryHover", null, mouseOverCountry);
                }
            })
            .on("click", function(d, event) {
            mouseClickCountry = d3.select(this).data()[0].properties.admin
            if (selected_countries.includes(mouseClickCountry)) {
                lineplot.call(mouseClickCountry);
                }
            });
            .on('mouseout', function(d) {
                if (selected_countries.includes(d3.select(this).data()[0].properties.admin)) {
                    d3.select(this).attr('fill', 'black');
                    dispatch.call("countryHover", null, null);
                }
            });

            
        map.filter(function(d) {
                return selected_countries.includes(d.properties.admin);
             })
             .attr('fill', 'black');

        
    });
}

