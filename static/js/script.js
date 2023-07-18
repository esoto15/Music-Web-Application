// script.js
$(document).ready(function() {
  // Toggle password visibility
  $('#password-toggle').click(function() {
    var passwordInput = $('#password');
    var icon = $(this).find('i');

    if (passwordInput.attr('type') === 'password') {
      passwordInput.attr('type', 'text');
      icon.removeClass('fa-eye').addClass('fa-eye-slash');
    } else {
      passwordInput.attr('type', 'password');
      icon.removeClass('fa-eye-slash').addClass('fa-eye');
    }
  });
});
