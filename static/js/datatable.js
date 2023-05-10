function datatable(data, country, selectedVars) {
  data = JSON.parse(data);

  if (country === null) {
    d3.select("#datatable-div").remove();
    return;
  } else {
      d3.select("#data-message").remove();
  }

  var filteredData = data.filter(function(d) {
    return d["Country Name"] === country && d.year === d3.max(data, function(d) { return d.year; });
  });

  // Create an array of objects with variable and value
  var tableData = [];
  selectedVariables.forEach(function(key) {
    var value = filteredData[0][key];
    if (typeof value === "number") {
      value = value.toFixed(1); // Round to one decimal
    }
    tableData.push({variable: key, value: value});
  })
 
  d3.select("#datatable-div").remove();
  // Create the table element and add it to the page
  var table = d3.select("#datatable")
                .append("div")
                .attr("id", "datatable-div")
                .append("table");

  // Add the header row to the table
  var header = table.append("thead").append("tr");
  header.selectAll("th")
    .data(["Variable", "Value"])
    .enter().append("th")
      .text(function(d) { return d; });

  // Add the rows to the table
  var tbody = table.append("tbody");
  var rows = tbody.selectAll("tr")
    .data(tableData)
    .enter().append("tr");
  rows.append("td")
    .text(function(d) { return d.variable; });
  rows.append("td")
    .text(function(d) { return d.value; });
}
