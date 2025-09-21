import { auth, provider, signInWithPopup, onAuthStateChanged, signOut } from "./firebase.js";

// Google Login
export function loginWithGoogle() {
  signInWithPopup(auth, provider)
    .then(async (result) => {
      const user = result.user;
      const idToken = await user.getIdToken();
      localStorage.setItem("idToken", idToken);
      console.log("User logged in:", user.email);

      // Temporary role check (hackathon shortcut)
      if (user.email.includes("teacher")) {
        window.location.href = "teacher-dashboard.html";
      } else {
        window.location.href = "student-checkin.html";
      }
    })
    .catch((error) => {
      console.error("Login error:", error.message);
    });
}

// Auto-redirect if already logged in
onAuthStateChanged(auth, (user) => {
  if (user) {
    console.log("Already logged in:", user.email);
  }
});

// Logout
export function logout() {
  signOut(auth).then(() => {
    localStorage.removeItem("idToken");
    window.location.href = "index.html";
  });
}
