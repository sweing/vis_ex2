function scatterplot(data) {
  // Set the dimensions of the plot
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 600 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  // Get the max and min values for PC1 and PC2
  var xValues = data.map(function(d) { return d.PC1; });
  var yValues = data.map(function(d) { return d.PC2; });
  var countryValue = data.map(function(d) { return d["Country Name"]; });
  var xMin = d3.min(xValues);
  var xMax = d3.max(xValues);
  var yMin = d3.min(yValues);
  var yMax = d3.max(yValues);

  // Define the scales for the x and y axis
  var x = d3.scaleLinear()
      .domain([xMin, xMax])
      .range([0, width]);

  var y = d3.scaleLinear()
      .domain([yMin, yMax])
      .range([height, 0]);

  // Create the svg element and add it to the scatterplot div
  var svg = d3.select("#scatterplot").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

  // Add the x and y axis to the svg element
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      //.call(d3.axisBottom(x));


  

  // Add the data points to the svg element
  svg.selectAll("circle")
      .data(data)
    .enter().append("circle")
      .attr("cx", function(d) { return x(d.PC1); })
      .attr("cy", function(d) { return y(d.PC2); })
      .attr("r", 5)
      .on("mouseover", function(d) {
        // Get the current circle element
        var currentCircle = d3.select(this);
        var currentCountry = currentCircle.data()[0]["Country Name"];
        //console.log(currentCountry)
        dispatch.call("countryHover", null, currentCountry);
        // Update the style of the current circle     
      })
      .on("mouseout", function(d) {
        d3.select(this).style("stroke", "none");
        dispatch.call("countryHover", null, null);
      });


}
