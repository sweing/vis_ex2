function lineplot(data) {
    data = JSON.parse(data)

    const filteredData = data.filter(function(d) {
      return d["Country Name"] === countryForLinePlot;
    });

    console.log(filteredData)
      
    var countryValue = filteredData.map(function(d) { return d["Country Name"]; });
    var xValues = filteredData.map(function(d) { return d["year"]; });
    var yValues = filteredData.map(obj => obj["Birth rate, crude (per 1,000 people)"]);
    console.log(yValues)
    // Define the dimensions and margins of the chart area
    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // Create an SVG element and append it to the DOM
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Define the scales for the x and y axes
    var x = d3.scaleLinear()
        .domain(d3.extent(xValues))
        .range([0, width]);

    var y = d3.scaleLinear()
        .domain(d3.extent(yValues))
        .range([height, 0]);

      // Define the line generator function to map data to coordinates
    var line = d3.line()
      .x(function(d, i) { return x(xValues[i]); })
      .y(function(d, i) { return y(yValues[i]); });

      // Append the line to the SVG element
     svg.append("path")
        .datum(filteredData)
        .attr("class", "line")
        .attr("d", line)
        .style("fill", "none")
        .style("stroke", "black");

      // Add the x and y axes
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      svg.append("g")
          .call(d3.axisLeft(y));
  }