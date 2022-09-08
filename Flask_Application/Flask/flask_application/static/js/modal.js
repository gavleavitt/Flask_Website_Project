// Set modal function to load when page loads
// document.onload = function(){
window.onload = function(){
  // Modal from https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_modal
  // Get the modal
  var modal = document.getElementById("myModal");
  // Open modal
  modal.style.display = "block";
  // Get the button that opens the modal
  var btn = document.getElementById("btn");

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
  // var span = document.getElementById("infoClose");

  // When the user clicks the button, open the modal
  btn.onclick = function() {
    modal.style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    // console.log("close modal!")
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
};
