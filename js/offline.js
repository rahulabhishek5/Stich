let queue = JSON.parse(localStorage.getItem("offlineQueue") || "[]");

export function saveOffline(payload) {
  queue.push(payload);
  localStorage.setItem("offlineQueue", JSON.stringify(queue));
}

export async function syncQueue() {
  if (navigator.onLine && queue.length > 0) {
    for (const item of queue) {
      try {
        await apiRequest("/sync", "POST", [item]);
        queue = queue.filter(q => q !== item);
        localStorage.setItem("offlineQueue", JSON.stringify(queue));
      } catch (err) {
        console.log("Sync failed for item:", err);
      }
    }
  }
}

window.addEventListener("online", syncQueue);
