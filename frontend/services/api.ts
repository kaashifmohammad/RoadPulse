const API_URL = "http://127.0.0.1:8000/api";

async function handleResponse(response: Response) {
  if (!response.ok) {
    let message = "Request failed";

    try {
      const data = await response.json();
      message =
        typeof data?.detail === "string"
          ? data.detail
          : data?.message || message;
    } catch {
      // Keep default error message.
    }

    throw new Error(message);
  }

  return response.json();
}

export async function getHealth() {
  const response = await fetch(`${API_URL}/health`, {
    cache: "no-store",
  });

  return handleResponse(response);
}

export async function createReport(formData: FormData) {
  const response = await fetch(`${API_URL}/reports/`, {
    method: "POST",
    body: formData,
  });

  return handleResponse(response);
}

export async function getReports() {
  const response = await fetch(`${API_URL}/reports/`, {
    cache: "no-store",
  });

  return handleResponse(response);
}

export async function assignContractor(
  reportId: number,
  contractor: string,
) {
  const response = await fetch(
    `${API_URL}/reports/${reportId}/contractor`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        contractor,
      }),
    },
  );

  return handleResponse(response);
}

export async function updateReportStatus(
  reportId: number,
  status: string,
) {
  const response = await fetch(
    `${API_URL}/reports/${reportId}/status`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        status,
      }),
    },
  );

  return handleResponse(response);
}
export async function getUserPoints(userId: number) {
  const response = await fetch(
    `${API_URL}/reports/points/${userId}`,
    {
      cache: "no-store",
    },
  );

  return handleResponse(response);
}