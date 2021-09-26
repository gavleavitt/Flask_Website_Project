function createGeoJSONZIP() {
  // Create JSZip ojbect to hold results
  var zip = new JSZip()
  // Get list of geojson object keys
  var jsonkeys = Object.keys(serverResponse)
  // Iterate over keys
  jsonkeys.forEach((item, i) => {
    // Check if geojson object is populated, skip if not
    if (serverResponse[item].features.length > 0){
      // Use Regex to replace spaces wih underscores, object key will become filename
      fileName = `${item.replace(/ /g,"_")}.geojson`
      // Add geojson object to zip file, JSZip does not recognize the object unless its converted to a json string representation
      zip.file(fileName,JSON.stringify(serverResponse[item]))
    }
  });
  // Generate zip file
  zip.generateAsync({type:"blob"})
  .then(function (blob) {
      // use filesaver.js to set the zip file name and initiate download
      saveAs(blob, "TraceResults.zip");
  });
}
