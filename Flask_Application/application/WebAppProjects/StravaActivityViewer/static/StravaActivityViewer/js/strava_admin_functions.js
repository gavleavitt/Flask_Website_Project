// Add/remove Activity
$("#processActivity").submit(function(event) {
  // Show loader
  document.getElementById("loader-container").style.display = "block";
  /* stop form from submitting normally, stops page from reloading */
  event.preventDefault();
  /* get the action attribute from the <form action=""> element, this is the POST URL */
  var url = $(this).attr('action');
  // Get Activity ID
  var actID = $('#actIDInput').val()
  // Get athlete ID
  var athID = $('#athIDInput').val()
  // Get action type
  var type = $("#processActivity input[type='radio']:checked").val();
  // Get processing scope
  scope = $("#scope option:selected").attr('id')
  // Send POST request
  var postRequest = $.post(url, {
    actID:actID,
    athID:athID,
    actionType:type,
    scope:scope
  });
  //get modal
  modal = $('#ResultsModal')
  // Open modal with results
  postRequest.done(function(data) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Success!');
    // update body
    modal.find('#modalBody').html('The activity <b>' + actID + '</b> has been added!');
  });
  postRequest.fail(function(response) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Failure!');
    // update body
    modal.find('#modalBody').html('The activity <b>' + actID + '</b> has failed to be added with the error code: ' + '<b>' + response.status + '</b>');
  });
});

// Remove webhook subscription
$("#removeWebHookSub").submit(function(event) {
  // Show loader
  document.getElementById("loader-container").style.display = "block";
  /* stop form from submitting normally, stops page from reloading */
  event.preventDefault();
  /* get the action attribute from the <form action=""> element, this is the POST URL */
  var url = $(this).attr('action');
  // Get athlete ID
  var athID = $('#removeSubAthIDInput').val()
  console.log(athID)
  // Get Subscription ID
  var subID = $("#subIDInput").val();
  // Send POST request
  var postRequest = $.post(url, {
    subID:subID,
    athID:athID
  });
  //get modal
  modal = $('#ResultsModal')
  // Open modal with results
  postRequest.done(function(data) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Success!');
    // update body
    modal.find('#modalBody').html('The webhook subscription <b>' + athID + '</b> for athlete <b>' + athID + '</b> has been removed!');
  });
  postRequest.fail(function(response) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Failure!');
    // update body
    modal.find('#modalBody').html('The webhook subscription <b>' + athID + '</b> for athlete <b>' + athID + '</b> has failed to be added with the error code: ' + '<b>' + response.status + '</b>');
  });
});

// Add webhook subscription
$("#addWebHookSub").submit(function(event) {
  // Show loader
  document.getElementById("loader-container").style.display = "block";
  /* stop form from submitting normally, stops page from reloading */
  event.preventDefault();
  /* get the action attribute from the <form action=""> element, this is the POST URL */
  var url = $(this).attr('action');
  // Get athlete ID
  var athID = $('#AddSubAthIDInput').val()
  // Get callbackURL
  var callbackURL = $('#callbackURLinput').val()
  // Send POST request
  var postRequest = $.post(url, {
    athID:athID,
    callbackURL:callbackURL
  });
  //get modal
  modal = $('#ResultsModal')
  // Open modal with results
  postRequest.done(function(data) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Success!');
    // update body
    modal.find('#modalBody').html('The activity ' + actID + ' has been added!');
  });
  postRequest.fail(function(response) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Failure!');
    // update body
    modal.find('#modalBody').html('Failed to add a new webhook subscription to the callbackURL <b>' + callbackURL + '</b> wih the code: ' + '<b>' + response.status + '</b>');
  });
});

// Regenerate/update topoJSON
$("#genTopoJSON").submit(function(event) {
  // Show loader
  document.getElementById("loader-container").style.display = "block";
  /* stop form from submitting normally, stops page from reloading */
  event.preventDefault();
  /* get the action attribute from the <form action=""> element, this is the POST URL */
  var url = $(this).attr('action');
  // Get athlete ID
  var athID = $('#athIDInput').val()
  // Send POST request
  var postRequest = $.post(url, {
    athID:athID
  });
  //get modal
  modal = $('#ResultsModal')
  // Open modal with results
  postRequest.done(function(data) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Success!');
    // update body
    // modal.find('#modalBody').text('The TopoJSON for athelete ' + athID + 'has been updated!');
    modal.find('#modalBody').html('The TopoJSON for athelete <b>' + athID + '</b> has been updated!');
  });
  postRequest.fail(function(response) {
    // Hide loader
    document.getElementById("loader-container").style.display = "none";
    // Show modal
    modal.modal('show');
    // update title
    modal.find('#modalTitle').text('Failure!');
    // update body
    modal.find('#modalBody').html('Failed to update the TopoJSON for athlete <b>' + athID + '</b> wih the code: ' + response.status);
  });
});
