// Import the tools you need from YOUR firebase.js file
import { auth, provider, signInWithPopup, onAuthStateChanged, signOut } from './firebase.js';

// --- Login Logic ---
async function handleLogin() {
    try {
        const result = await signInWithPopup(auth, provider);
        console.log("Login successful:", result.user);
        window.location.href = 'student-dashboard.html'; // Redirect on success
    } catch (error) {
        console.error("Login failed:", error);
    }
}

// --- Logout Logic ---
async function handleLogout() {
    try {
        await signOut(auth);
        console.log("Logout successful");
        window.location.href = 'login.html'; // Redirect to login page
    } catch (error) {
        console.error("Logout failed:", error);
    }
}

// --- Authentication State Observer ---
// This checks if the user is already logged in or not
onAuthStateChanged(auth, (user) => {
    const currentPage = window.location.pathname.split('/').pop();

    if (user) {
        // User is signed in.
        console.log("User is logged in:", user.email);
        // If they are on the login page, redirect them to the dashboard.
        if (currentPage === 'login.html' || currentPage === 'index.html') {
            window.location.href = 'student-dashboard.html';
        }
    } else {
        // User is signed out.
        console.log("User is not logged in.");
        // If they are on a protected page (like the dashboard), redirect them to login.
        if (currentPage === 'student-dashboard.html') {
            window.location.href = 'login.html';
        }
    }
});

// --- Attach Event Listeners ---
// Find the login button on the login page and attach the login function
const loginButton = document.getElementById('login-btn');
if (loginButton) {
    loginButton.addEventListener('click', handleLogin);
}

// Find the logout button on the dashboard and attach the logout function
const logoutButton = document.getElementById('logout-btn');
if (logoutButton) {
    logoutButton.addEventListener('click', handleLogout);
}