// This function runs when the HTML page is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Find the login form and the error message container in the HTML
    const loginForm = document.getElementById('teacher-login-form');
    const errorMessageDiv = document.getElementById('error-message');

    // Make sure the form actually exists before we try to use it
    if (loginForm) {
        // Listen for the 'submit' event on the form
        loginForm.addEventListener('submit', async (event) => {
            // Stop the form from doing its default behavior (reloading the page)
            event.preventDefault();

            // Clear any old error messages and hide the error div
            errorMessageDiv.textContent = '';
            errorMessageDiv.classList.add('hidden');

            // Get the form data (email and password)
            const formData = new FormData(loginForm);

            // The backend's /token endpoint needs the data in a specific format
            // called 'x-www-form-urlencoded', so we convert it here.
            const data = new URLSearchParams();
            for (const pair of formData) {
                // We only need username and password for login
                if (pair[0] === 'username' || pair[0] === 'password') {
                    data.append(pair[0], pair[1]);
                }
            }

            try {
                // Send the login request to the backend API using fetch()
                const response = await fetch('http://127.0.0.1:8000/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: data,
                });

                // Get the JSON data from the backend's response
                const result = await response.json();

                // If the response was successful (HTTP status 200-299)
                if (response.ok) {
                    // Login successful!
                    // Store the access token in the browser's local storage for future use
                    localStorage.setItem('accessToken', result.access_token);
                    
                    // Redirect the user to the teacher dashboard
                    // Make sure you have a teacher-dashboard.html file
                    window.location.href = '/teacher-dashboard.html';
                } else {
                    // If there was an error, display the message from the backend
                    errorMessageDiv.textContent = result.detail || 'An unknown error occurred.';
                    errorMessageDiv.classList.remove('hidden');
                }
            } catch (error) {
                // If there was a network error (e.g., backend is not running)
                errorMessageDiv.textContent = 'Could not connect to the server. Please try again later.';
                errorMessageDiv.classList.remove('hidden');
                console.error('Login Error:', error);
            }
        });
    }
});