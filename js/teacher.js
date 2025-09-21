import { apiRequest } from "./api.js";

document.getElementById("generateQR").addEventListener("click", async () => {
  const data = await apiRequest("/generate_token", "POST", { period_id: 1 });
  new QRCode(document.getElementById("qrcode"), data.token);
});

async function loadAttendance() {
  const data = await apiRequest("/attendance?period_id=1");
  const table = document.getElementById("attendanceTable");
  table.innerHTML = data.map(row => `<tr><td>${row.name}</td><td>${row.status}</td></tr>`).join("");
}
setInterval(loadAttendance, 5000); // poll every 5s
