"use client";

import { useState } from "react";
import { assignContractor } from "../../services/api";

type Props = {
  reportId: number;
  currentContractor?: string | null;
  onUpdated: () => void;
};

export default function AssignContractor({
  reportId,
  currentContractor,
  onUpdated,
}: Props) {
  const [contractor, setContractor] = useState(currentContractor || "");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleAssign() {
    if (!contractor.trim()) {
      setMessage("Enter a contractor name.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      await assignContractor(reportId, contractor.trim());
      setMessage("Assigned successfully.");
      onUpdated();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to assign contractor.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-2">
      <input
        type="text"
        value={contractor}
        onChange={(event) => setContractor(event.target.value)}
        placeholder="Contractor name"
        className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
      />

      <button
        type="button"
        onClick={handleAssign}
        disabled={loading}
        className="w-full rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Assigning..." : "Assign Contractor"}
      </button>

      {message && (
        <p className="text-xs text-gray-600">
          {message}
        </p>
      )}
    </div>
  );
}