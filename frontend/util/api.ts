export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "https://api.ramferno.com"
).replace(/\/$/, "");

export function buildApiUrl(path: string) {
  if (/^https?:\/\//.test(path)) {
    return path;
  }

  if (path.startsWith("/")) {
    return `${API_BASE_URL}${path}`;
  }

  return `${API_BASE_URL}/${path}`;
}

export function apiFetch(path: string, init: RequestInit = {}) {
  return fetch(buildApiUrl(path), {
    ...init,
    credentials: "include",
  });
}
