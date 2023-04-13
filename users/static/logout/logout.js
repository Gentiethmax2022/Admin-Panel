const form = document.querySelector('form');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  try {
    const response = await fetch('/api/logout/', {
      method: 'POST',
    });

    if (response.ok) {
      alert('Successfully logged out!');
      window.location.href = '/'; // Redirect to homepage
    } else {
      const error = await response.json();
      alert(`Logout failed: ${error.msg}`);
    }
  } catch (error) {
    alert('An error occurred while logging out. Please try again later.');
    console.error(error);
  }
});
