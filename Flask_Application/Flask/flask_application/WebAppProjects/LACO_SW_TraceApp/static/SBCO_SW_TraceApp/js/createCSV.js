
function createCSV(data){
  // Convert trace result objects to array format from GeoJSON format
  rows = []
  // Set CSV headers
  csvHeaders = ["factype","uuid","facid","facsubtype","material","size","linearpipefeetfromstart", "dwgno"]
  rows.push(csvHeaders)
  // Loop over each trace result feature collection
  Object.keys(data).forEach((objItem) => {
    // Check if feature collection has results, if not skip
    if (data[objItem].features.length > 0){
      // console.log(`Prcoessing ${objItem} attributes to array format`)
      // console.log(objData[objItem].features)
      // Iteralte over each feature result in collection
      data[objItem].features.forEach((feat) => {
        nestedArray = []
        // Iterate over csvheaders adding data from the header title to the nested array
        // Only interested in some of the trace result data
        csvHeaders.forEach((head) => {
          if (feat.properties[head] !== undefined){
            nestedArray.push(feat.properties[head])
          }
          // nestedArray.push(feat.properties[head])
        });
        // push nested array to overall results array
        rows.push(nestedArray)
      });
    }
  });
  // console.log(rows)
  // Pass formatted array data to function which converts to CSV
  // Check if rows is defined/populated, skip if not
  if (rows.length > 1){
    exportToCsv("TraceResults.csv",rows)
  }
}


function exportToCsv(filename, rows){
//converts array of data to csv, take from StackOverflow:
//https://stackoverflow.com/a/24922761
// This function handles special characters properly
    var processRow = function (row) {
        var finalVal = '';
        for (var j = 0; j < row.length; j++) {
            var innerValue = row[j] === null ? '' : row[j].toString();
            if (row[j] instanceof Date) {
                innerValue = row[j].toLocaleString();
            };
            var result = innerValue.replace(/"/g, '""');
            if (result.search(/("|,|\n)/g) >= 0)
                result = '"' + result + '"';
            if (j > 0)
                finalVal += ',';
            finalVal += result;
        }
        return finalVal + '\n';
    };

    var csvFile = '';
    for (var i = 0; i < rows.length; i++) {
        csvFile += processRow(rows[i]);
    }

    var blob = new Blob([csvFile], { type: 'text/csv;charset=utf-8;' });
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, filename);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}
