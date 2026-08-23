const API_URL = "http://127.0.0.1:8000/api";

export async function getHealth() {
  const response = await fetch(`${API_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend unavailable");
  }

  return response.json();
}

export async function createReport(formData: FormData) {
  const response = await fetch(`${API_URL}/reports/`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to create report");
  }

  return response.json();
}

export async function getReports() {
  const response = await fetch(`${API_URL}/reports/`);

  if (!response.ok) {
    throw new Error("Failed to fetch reports");
  }

  return response.json();
}