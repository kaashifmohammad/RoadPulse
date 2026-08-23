"use client";

import { useEffect, useState } from "react";

import { getReports } from "@/services/api";

type Complaint = {
  id: number;
  title: string;
  severity: string;
  status: string;
  latitude: string;
  longitude: string;
  priority: number;
  contractor: string | null;
};

export default function ComplaintsPage() {
  const [reports, setReports] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getReports()
      .then(setReports)
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
      <div className="max-w-5xl mx-auto">
        <p className="text-blue-400 font-semibold">
          ROADPULSE
        </p>

        <h1 className="text-4xl font-bold mt-2">
          My Complaints
        </h1>

        <p className="text-slate-400 mt-2 mb-8">
          Track your pothole reports.
        </p>

        {loading && (
          <p className="text-slate-400">
            Loading complaints...
          </p>
        )}

        {!loading && reports.length === 0 && (
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-8">
            <p className="text-slate-400">
              No complaints reported yet.
            </p>
          </div>
        )}

        <div className="space-y-4">
          {reports.map((report) => (
            <div
              key={report.id}
              className="rounded-xl border border-slate-800 bg-slate-900 p-6"
            >
              <div className="flex justify-between gap-4">
                <div>
                  <h2 className="text-xl font-semibold">
                    {report.title}
                  </h2>

                  <p className="text-slate-400 text-sm mt-2">
                    Complaint #{report.id}
                  </p>
                </div>

                <span className="h-fit rounded-full bg-blue-500/20 text-blue-300 px-3 py-1 text-sm">
                  {report.status}
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 text-sm">
                <div>
                  <p className="text-slate-500">
                    Severity
                  </p>

                  <p className="font-semibold">
                    {report.severity}
                  </p>
                </div>

                <div>
                  <p className="text-slate-500">
                    Priority
                  </p>

                  <p className="font-semibold">
                    {report.priority}
                  </p>
                </div>

                <div>
                  <p className="text-slate-500">
                    Latitude
                  </p>

                  <p>{report.latitude}</p>
                </div>

                <div>
                  <p className="text-slate-500">
                    Longitude
                  </p>

                  <p>{report.longitude}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}