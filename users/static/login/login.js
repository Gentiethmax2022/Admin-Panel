const loginButton = document.getElementById('login-button');

loginButton.addEventListener('click', () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const rememberMe = document.getElementById('remember-me').checked;

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/accounts/login/');
  xhr.setRequestHeader('Content-Type', 'application/json');

  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        const authToken = response.token;
        if (rememberMe) {
          localStorage.setItem('authToken', authToken);
        } else {
          sessionStorage.setItem('authToken', authToken);
        }
        window.location.href = '/dashboard/';
      } else {
        alert('Invalid email or password');
      }
    }
  };

  xhr.send(JSON.stringify({email: email, password: password}));
});

