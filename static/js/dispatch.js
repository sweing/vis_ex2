var dispatch = d3.dispatch("countryHover");
dispatch.on("countryHover", function(countryName) {
    map.attr('fill', function(d) {
        if (d.properties.admin === countryName) {
            return "red"; // color the selected country
        } else if (selected_countries.includes(d.properties.admin)) {
            return "black"; // color the other selected countries
        } else {
            return "white"; // color the rest of the countries
        }
    });


    d3.select("#scatterplot")
        .selectAll("circle")
        .filter(function(d) {
            return d["Country Name"] === countryName;
        })
        .attr("fill", "red");

    d3.select("#scatterplot")
        .selectAll("circle")
        .filter(function(d) {
            return d["Country Name"] != countryName;
        })
        .attr("fill", "black"); 

    d3.select("#scatterplot-title")
          .text(countryName); 

    datatable(data, countryName, selectedVariables)
    
});