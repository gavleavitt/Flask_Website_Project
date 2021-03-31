/* attach a submit handler to the form */
// $("#addActivity").submit(function(event) {
//
//   /* stop form from submitting normally */
//   event.preventDefault();
//
//   /* get the action attribute from the <form action=""> element */
//   var $form = $(this),
//     url = $form.attr('action');
//   console.log(form)
//   /* Send the data using post with element id name and name2*/
//   var posting = $.post(url, {
//     name: $('#actID').val(),
//     // name2: $('#name2').val()
//   });
//
//   /* Alerts the results */
//   posting.done(function(data) {
//     $('#result').text('success');
//   });
//   posting.fail(function() {
//     $('#result').text('failed');
//   });
// });
$("#addActivity").submit(function(event) {
  // Show loader
  document.getElementById("loader-container").style.display = "block";
  /* stop form from submitting normally, stops page from reloading */
  event.preventDefault();
  /* get the action attribute from the <form action=""> element, this is the POST URL */
  var url = $(this).attr('action');
  // Get Activity ID
  var actID = $('#actIDInput').val()
  // Send POST request
  var postRequest = $.post(url, {
    actID:actID
  });
  //get modal
  modal = $('#ResultsModal')
  /* Alerts the results */
  postRequest.done(function(data) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Success!');
    // update body
    modal.find('#modalBody').text('The activity ' + actID + ' has been added!');
  });
  postRequest.fail(function(response) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Failure!');
    // update body
    modal.find('#modalBody').text('The activity ' + actID + ' has failed to be added with the error code: ' + response.status);
  });
});
