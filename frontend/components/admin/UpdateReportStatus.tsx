"use client";

import { useState } from "react";
import { updateReportStatus } from "../../services/api";

type Props = {
  reportId: number;
  currentStatus?: string | null;
  onUpdated: () => void;
};

const statuses = [
  "reported",
  "pending",
  "assigned",
  "in_progress",
  "repaired",
  "rejected",
];

export default function UpdateReportStatus({
  reportId,
  currentStatus,
  onUpdated,
}: Props) {
  const [status, setStatus] = useState(
    currentStatus || "reported",
  );
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleUpdate() {
    setLoading(true);
    setMessage("");

    try {
      await updateReportStatus(reportId, status);
      setMessage("Status updated.");
      onUpdated();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to update status.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-2">
      <select
        value={status}
        onChange={(event) => setStatus(event.target.value)}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
      >
        {statuses.map((item) => (
          <option key={item} value={item}>
            {item.replace(/_/g, " ")}
          </option>
        ))}
      </select>

      <button
        type="button"
        onClick={handleUpdate}
        disabled={loading}
        className="w-full rounded-lg bg-gray-900 px-3 py-2 text-sm font-semibold text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Updating..." : "Update Status"}
      </button>

      {message && (
        <p className="text-xs text-gray-600">
          {message}
        </p>
      )}
    </div>
  );
}