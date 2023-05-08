function lineplot(data) {
  data = JSON.parse(data);

  const filteredData = data.filter(function(d) {
    return d["Country Name"] === "Belgium";
  });

  var countryValue = filteredData.map(function(d) { return d["Country Name"]; });
  var xValues = filteredData.map(function(d) { return d["year"]; });
  var yValues = getYValues(filteredData, selectedOption.value);

  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var x = d3.scaleLinear()
      .domain(d3.extent(xValues))
      .range([0, width])

  var y = d3.scaleLinear()
      .domain(d3.extent(yValues))
      .range([height, 0]);

  var line = d3.line()
    .x(function(d, i) { return x(xValues[i]); })
    .y(function(d, i) { return y(yValues[i]); });

  svg.append("path")
    .datum(filteredData)
    .attr("class", "line")
    .attr("d", line)
    .style("fill", "none")
    .style("stroke", "black");

  // year format on x axis
  var xAxis = d3.axisBottom(x)
    .tickFormat(d3.format("d")); // Use "d" format specifier to remove comma separator


  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y-axis")
      .call(d3.axisLeft(y));

  // define a function to get y values for the selected option
  function getYValues(data, selectedOption) {
    return data.map(obj => obj[selectedOption]);
  }

  // add a change event listener to the dropdown
  d3.select("#indicator_dropdown").on("change", function() {
    // update the yValues variable
    yValues = getYValues(filteredData, selectedOption.value);
    console.log(yValues)

    // update the y scale domain
    y.domain(d3.extent(yValues));

    // Update the y axis
    svg.select(".y-axis")
      .transition()
      .duration(500)
      .call(d3.axisLeft(y));

    // update the line
    svg.select(".line")
      .datum(filteredData)
      .transition()
      .duration(1000)
      .attr("d", line);
  });
}
