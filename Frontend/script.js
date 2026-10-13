const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const form = document.querySelector("#shorten-form");
const urlInput = document.querySelector("#url-input");
const keyInput = document.querySelector("#key-input");
const message = document.querySelector("#form-message");
const deleteForm = document.querySelector("#delete-form");
const shortUrlInput = document.querySelector("#short-url-input");
const deleteMessage = document.querySelector("#delete-message");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button[type=submit]");
  button.disabled = true;
  message.textContent = "Creating your short link...";

  const payload = { Value: urlInput.value.trim() };
  if (keyInput.value.trim()) payload.Key = keyInput.value.trim();

  try {
    const response = await fetch(`${API_BASE}/urls`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "Could not create link");
    message.innerHTML = `Created: <a href="${API_BASE}/${result.Key}" target="_blank">${API_BASE}/${result.Key}</a>`;
    form.reset();
  } catch (error) {
    message.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

function getShortKey(value) {
  const trimmedValue = value.trim();

  try {
    const url = new URL(trimmedValue);
    return url.pathname.split("/").filter(Boolean).pop();
  } catch {
    return trimmedValue.replace(/^\/+|\/+$/g, "");
  }
}

deleteForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = deleteForm.querySelector("button[type=submit]");
  const shortKey = getShortKey(shortUrlInput.value);

  if (!shortKey) {
    deleteMessage.textContent = "Enter a shortened URL or key.";
    return;
  }

  button.disabled = true;
  deleteMessage.textContent = "Deleting...";

  try {
    const response = await fetch(`${API_BASE}/${encodeURIComponent(shortKey)}`, {
      method: "DELETE"
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "Could not delete link");
    deleteMessage.textContent = "Shortened URL deleted.";
    deleteForm.reset();
  } catch (error) {
    deleteMessage.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});
