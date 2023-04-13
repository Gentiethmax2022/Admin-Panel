$(document).ready(function() {
  // Attach a submit handler to the form
  $("#change-password-form").submit(function(event) {
    // Stop the default form submission behavior
    event.preventDefault();

    // Get the form data
    var formData = $(this).serialize();

    // Send an AJAX request to the backend API
    $.ajax({
      type: "POST",
      url: "/api/change-password/",
      data: formData,
      dataType: "json",
      success: function(data) {
        // Show a success message to the user
        alert("Your password has been changed successfully!");
      },
      error: function(xhr, textStatus, errorThrown) {
        // Show an error message to the user
        alert("Failed to change your password. Please try again.");
      }
    });
  });
});
