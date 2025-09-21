// frontend/js/api.js

// The address of your running FastAPI backend
const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * This function attempts to call the protected /checkin endpoint on the backend.
 */
async function performCheckIn() {
    const user = firebase.auth().currentUser;

    // 1. Check if a user is actually logged in.
    if (!user) {
        alert("You must be logged in to check in!");
        return;
    }

    try {
        // 2. Get the Firebase ID token. This is the user's "ID card".
        const idToken = await user.getIdToken();

        // 3. Make the request to the backend.
        //    The most important part is the 'headers' section, where we include the token.
        const response = await fetch(`${API_BASE_URL}/checkin`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${idToken}`, // This is the bridge!
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();

        if (!response.ok) {
            // If the backend returns an error (like 401 Unauthorized), show it.
            alert(`Error: ${data.detail || 'Check-in failed.'}`);
        } else {
            // If successful, show the success message from the backend.
            alert(`Success: ${data.message}`);
        }
    } catch (error) {
        console.error("Failed to communicate with the backend:", error);
        alert("An error occurred. Could not reach the server.");
    }
}