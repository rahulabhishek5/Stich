// Import the 'auth' object from your firebase.js file.
// This is crucial for the new syntax to work.
import { auth } from './firebase.js';

// This is the main function to call the backend.
async function performCheckIn() {
    // USE the imported 'auth' object, NOT firebase.auth()
    const user = auth.currentUser; 

    if (!user) {
        alert("You must be logged in to check in!");
        return;
    }

    try {
        const idToken = await user.getIdToken();
        const response = await fetch('http://127.0.0.1:8000/checkin', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${idToken}`,
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();

        if (!response.ok) {
            alert(`Error: ${data.detail || 'Check-in failed.'}`);
        } else {
            alert(`Success: ${data.message}`);
        }
    } catch (error) {
        console.error("Failed to communicate with the backend:", error);
        alert("An error occurred. Could not reach the server.");
    }
}

// Find the button by its ID and attach the function to its click event.
// This code runs after the page loads.
const checkInButton = document.getElementById('checkin-btn');
if (checkInButton) {
    checkInButton.addEventListener('click', performCheckIn);
}