"use client";

import { useCallback, useEffect, useState } from "react";
import { getReports } from "../../../services/api";
import ReportStatusBadge from "../../../components/admin/ReportStatusBadge";
import AssignContractor from "../../../components/admin/AssignContractor";
import UpdateReportStatus from "../../../components/admin/UpdateReportStatus";

type Report = {
  id: number;
  latitude?: number | null;
  longitude?: number | null;
  severity?: string | null;
  confidence?: number | null;
  ai_confidence?: number | null;
  status?: string | null;
  contractor?: string | null;
  image_url?: string | null;
  image_path?: string | null;
  created_at?: string | null;
};

function getSeverityClass(severity?: string | null) {
  const value = (severity || "unknown").toLowerCase();

  if (value === "high") {
    return "bg-red-100 text-red-800";
  }

  if (value === "medium") {
    return "bg-yellow-100 text-yellow-800";
  }

  if (value === "low") {
    return "bg-green-100 text-green-800";
  }

  return "bg-gray-100 text-gray-800";
}

function formatConfidence(report: Report) {
  const value = report.confidence ?? report.ai_confidence;

  if (value === null || value === undefined) {
    return "N/A";
  }

  const numeric = Number(value);

  if (Number.isNaN(numeric)) {
    return "N/A";
  }

  return `${numeric <= 1 ? numeric * 100 : numeric}%`;
}

export default function AdminReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadReports = useCallback(async () => {
    await Promise.resolve();

    setLoading(true);
    setError("");

    try {
      const data = await getReports();

      const result = Array.isArray(data)
        ? data
        : data?.reports || data?.items || [];

      setReports(result);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to load reports.",
      );
    } finally {
      setLoading(false);
    }
  }, []);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void loadReports();
  }, [loadReports]);
  
  return (
    <main className="min-h-screen bg-gray-50 px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-blue-600">
              RoadPulse Admin
            </p>

            <h1 className="mt-1 text-3xl font-bold text-gray-900">
              Pothole Reports
            </h1>

            <p className="mt-2 text-sm text-gray-600">
              Monitor AI-analyzed reports, assign contractors,
              and manage repair status.
            </p>
          </div>

          <button
            type="button"
            onClick={() => void loadReports()}
            disabled={loading}
            className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm transition hover:bg-gray-100 disabled:opacity-50"
          >
            {loading ? "Refreshing..." : "Refresh Reports"}
          </button>
        </div>

        {error && (
          <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            <strong>Error:</strong> {error}
          </div>
        )}

        {loading && (
          <div className="rounded-xl border border-gray-200 bg-white p-10 text-center text-gray-500 shadow-sm">
            Loading reports...
          </div>
        )}

        {!loading && !error && reports.length === 0 && (
          <div className="rounded-xl border border-gray-200 bg-white p-10 text-center shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900">
              No reports found
            </h2>

            <p className="mt-2 text-sm text-gray-500">
              New pothole reports will appear here.
            </p>
          </div>
        )}

        {!loading && reports.length > 0 && (
          <div className="grid gap-6">
            {reports.map((report) => (
              <article
                key={report.id}
                className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm"
              >
                <div className="p-5 sm:p-6">
                  <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-3">
                        <h2 className="text-lg font-bold text-gray-900">
                          Report #{report.id}
                        </h2>

                        <span
                          className={`rounded-full px-3 py-1 text-xs font-semibold capitalize ${getSeverityClass(
                            report.severity,
                          )}`}
                        >
                          {report.severity || "Unknown"} severity
                        </span>

                        <ReportStatusBadge status={report.status} />
                      </div>

                      <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                        <div>
                          <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
                            AI Confidence
                          </p>
                          <p className="mt-1 font-semibold text-gray-900">
                            {formatConfidence(report)}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
                            Latitude
                          </p>
                          <p className="mt-1 font-semibold text-gray-900">
                            {report.latitude ?? "N/A"}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
                            Longitude
                          </p>
                          <p className="mt-1 font-semibold text-gray-900">
                            {report.longitude ?? "N/A"}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
                            Contractor
                          </p>
                          <p className="mt-1 font-semibold text-gray-900">
                            {report.contractor || "Not assigned"}
                          </p>
                        </div>
                      </div>

                      {report.created_at && (
                        <p className="mt-5 text-xs text-gray-400">
                          Created:{" "}
                          {new Date(report.created_at).toLocaleString()}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="mt-6 grid gap-4 border-t border-gray-100 pt-6 md:grid-cols-2">
                    <div className="rounded-xl bg-gray-50 p-4">
                      <h3 className="mb-3 text-sm font-bold text-gray-900">
                        Contractor Assignment
                      </h3>

                      <AssignContractor
                        reportId={report.id}
                        currentContractor={report.contractor}
                        onUpdated={loadReports}
                      />
                    </div>

                    <div className="rounded-xl bg-gray-50 p-4">
                      <h3 className="mb-3 text-sm font-bold text-gray-900">
                        Report Status
                      </h3>

                      <UpdateReportStatus
                        reportId={report.id}
                        currentStatus={report.status}
                        onUpdated={loadReports}
                      />
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}