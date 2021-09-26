  // Taken from https://medium.com/@danny.pule/export-json-to-csv-file-using-javascript-a0b7bc5b00d2
// function convertToCSV(objArray) {
//     var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
//     var str = '';
//
//     for (var i = 0; i < array.length; i++) {
//         var line = '';
//         for (var index in array[i]) {
//             if (line != '') line += ','
//
//             line += array[i][index];
//         }
//
//         str += line + '\r\n';
//     }
//
//     return str;
// }

// function exportCSVFile(headers, items, fileTitle) {
//     if (headers) {
//         items.unshift(headers);
//     }
//
//     // Convert Object to JSON
//     var jsonObject = JSON.stringify(items);
//
//     var csv = this.convertToCSV(jsonObject);
//
//     var exportedFilenmae = fileTitle + '.csv' || 'export.csv';
//
//     var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
//     if (navigator.msSaveBlob) { // IE 10+
//         navigator.msSaveBlob(blob, exportedFilenmae);
//     } else {
//         var link = document.createElement("a");
//         if (link.download !== undefined) { // feature detection
//             // Browsers that support HTML5 download attribute
//             var url = URL.createObjectURL(blob);
//             link.setAttribute("href", url);
//             link.setAttribute("download", exportedFilenmae);
//             link.style.visibility = 'hidden';
//             document.body.appendChild(link);
//             link.click();
//             document.body.removeChild(link);
//         }
//     }
// }

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
          nestedArray.push(feat.properties[head])
        });
        // push nested array to overall results array
        rows.push(nestedArray)
      });
    }
  });
  // console.log(rows)
  // Pass formatted array data to function which converts to CSV
  exportToCsv("TraceResults.csv",rows)
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
