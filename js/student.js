import { apiRequest } from "./api.js";

function onScanSuccess(decodedText) {
  navigator.geolocation.getCurrentPosition(async (pos) => {
    const payload = {
      token: decodedText,
      student_id: 123, // demo value, can map from Firebase UID
      lat: pos.coords.latitude,
      lon: pos.coords.longitude
    };
    try {
      const res = await apiRequest("/checkin", "POST", payload);
      alert("Check-in success: " + res.status);
    } catch (err) {
      alert("Check-in failed: " + err.message);
    }
  });
}

// Initialize scanner
new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 }).render(onScanSuccess);
