const API_BASE = "http://localhost:8000"; // change if deployed

export async function apiRequest(endpoint, method="GET", data=null) {
  const idToken = localStorage.getItem("idToken");

  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${idToken}`
    }
  };
  if (data) options.body = JSON.stringify(data);

  const res = await fetch(`${API_BASE}${endpoint}`, options);
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}
