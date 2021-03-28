// Remove home link from iframe, not needed since it will just open another home within the larger webpage
window.onload = function (){
  if (document.getElementById("iframe1")){
    document.getElementById("iframe1").contentWindow.document.getElementsByClassName("home-link")[0].remove();
  }
};


// Set onscroll event to close the navbar menu if open
window.onscroll = function(){closeMenu()};

window.onload = function(){
  // Set footer contact email using JS, makes it a little harder for bots to grab the email for spamming
  var email = "gav" + "lea" + "web" + "@g" + "mail" + ".com";
  document.getElementById("emailaddr").innerHTML = "<a href='mailto:" + email + "'>" + email + "</a>"
  // Deal with contact page having two email addr locations, consider making a form with WTForms to handle contact me
  if (document.getElementById("emailaddrcontact")){
    document.getElementById("emailaddrcontact").innerHTML = "<a href='mailto:" + email + "'>" + email + "</a>"
  }
}

function menuHover(){
  document.getElementById("menu-icon-img").setAttribute('src', '/static/images/menu-icon-blue.svg')
};

function menuUnhover(){
  document.getElementById("menu-icon-img").setAttribute('src', '/static/images/menu-icon-gray.svg')
};


function closeMenu(){
  var menu = document.getElementById("interactiveBarRight")
  if (menu.className = ("navbarright responsive")){
    menu.className = "navbarright";
  }
};

/* Toggle between adding and removing the "responsive" class to navbarright when the user clicks on the icon */
function navBarFunction() {
  var x = document.getElementById("interactiveBarRight");
  if (x.className === "navbarright") {
    x.className += " responsive";
  } else {
    x.className = "navbarright";
  }
};


function setCurrentYear(){
  // Get current year for copyright date, currently not used
  document.getElementById("year").innerHTML = new Date().getFullYear()
}
