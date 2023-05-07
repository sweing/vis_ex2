

// - years to x, 1 oder 2 [von value in index.html?] zu y, countryname
function lineplot(data2) {
    var countryValue = data2.map(function(d) { return d["Country Name"]; });
    var xValues = data2.map(function(d) { return d["year"]; });
    var yValues = data2.map(function(d) { return d.value; });

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
        .domain(d3.extent(data, function(d) { return d.x; }))
        .range([0, width]);

    var y = d3.scaleLinear()
      .domain(d3.extent(data, function(d) { return d.y; }))
      .range([height, 0]);

      // Define the line generator function to map data to coordinates
    var line = d3.line()
          .x(function(d) { return x(d.x); })
          .y(function(d) { return y(d.y); });

      // Append the line to the SVG element
      svg.append("path")
          .datum(data)
          .attr("class", "line")
          .attr("d", line);

      // Add the x and y axes
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      svg.append("g")
          .call(d3.axisLeft(y));
  }
