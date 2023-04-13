const form = document.querySelector('#registration-form');
const emailInput = document.querySelector('#email');
const dateOfBirthInput = document.querySelector('#date_of_birth');
const passwordInput = document.querySelector('#password');
const password2Input = document.querySelector('#password2');
const errorMessages = document.querySelectorAll('.error-message');
const submitButton = document.querySelector('#submit-button');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  resetErrorMessages();

  const formData = new FormData(form);
  const requestBody = Object.fromEntries(formData);

  fetch('/api/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(requestBody),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Registration failed');
      }
      window.location.href = '/login/';
    })
    .catch((error) => {
      const errors = Object.entries(JSON.parse(error.message));
      for (const [fieldName, errorMessages] of errors) {
        const inputField = document.querySelector(`#${fieldName}`);
        const errorField = inputField.nextElementSibling;
        inputField.classList.add('is-invalid');
        errorField.textContent = errorMessages[0];
      }
    });
});

function resetErrorMessages() {
  emailInput.classList.remove('is-invalid');
  dateOfBirthInput.classList.remove('is-invalid');
  passwordInput.classList.remove('is-invalid');
  password2Input.classList.remove('is-invalid');
  errorMessages.forEach((errorMessage) => {
    errorMessage.textContent = '';
  });
}

$(document).ready(function() {
  $('#register-form').submit(function(event) {
      event.preventDefault();
      var formData = $(this).serialize();
      $.ajax({
          url: '/api/register/',
          type: 'POST',
          data: formData,
          success: function(response) {
              alert('User registered successfully.');
          },
          error: function(error) {
              var errorData = JSON.parse(error.responseText);
              var errorMsg = '';
              for (var key in errorData) {
                  errorMsg += key + ': ' + errorData[key] + '\n';
              }
              alert(errorMsg);
          }
      });
  });
});
