"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { createReport } from "@/services/api";

export default function ReportPage() {
  const router = useRouter();

  const [title, setTitle] = useState("");
  const [image, setImage] = useState<File | null>(null);

  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");

  const [locationLoading, setLocationLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const [message, setMessage] = useState("");

  function getLocation() {
    if (!navigator.geolocation) {
      setMessage("Geolocation is not supported by this browser.");
      return;
    }

    setLocationLoading(true);
    setMessage("");

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLatitude(position.coords.latitude.toString());
        setLongitude(position.coords.longitude.toString());

        setLocationLoading(false);
        setMessage("📍 Location captured successfully.");
      },
      () => {
        setLocationLoading(false);
        setMessage("Unable to get your location.");
      },
    );
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    if (!title || !image || !latitude || !longitude) {
      setMessage(
        "Please provide a title, photo, and location.",
      );
      return;
    }

    setSubmitting(true);
    setMessage("");

    try {
      const formData = new FormData();

      formData.append("title", title);
      formData.append("latitude", latitude);
      formData.append("longitude", longitude);
      formData.append("user_id", "1");
      formData.append("image", image);

      const result = await createReport(formData);

      setMessage(
        `✅ Complaint created successfully. ID: ${result.complaint_id}`,
      );

      setTimeout(() => {
        router.push("/complaints");
      }, 1200);
    } catch {
      setMessage(
        "❌ Failed to create complaint. Please try again.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <p className="text-blue-400 font-semibold">
            ROADPULSE
          </p>

          <h1 className="text-4xl font-bold mt-2">
            Report a Pothole
          </h1>

          <p className="text-slate-400 mt-2">
            Help make your roads safer.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-slate-800 bg-slate-900 p-8 space-y-6"
        >
          <div>
            <label className="block text-sm mb-2">
              Report Title
            </label>

            <input
              value={title}
              onChange={(event) =>
                setTitle(event.target.value)
              }
              placeholder="Large pothole near main road"
              className="w-full rounded-lg bg-slate-800 border border-slate-700 px-4 py-3 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm mb-2">
              Pothole Photo
            </label>

            <input
              type="file"
              accept="image/*"
              onChange={(event) =>
                setImage(event.target.files?.[0] ?? null)
              }
              className="w-full rounded-lg bg-slate-800 border border-slate-700 px-4 py-3"
            />

            {image && (
              <p className="text-sm text-slate-400 mt-2">
                Selected: {image.name}
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm mb-2">
              Location
            </label>

            <button
              type="button"
              onClick={getLocation}
              className="rounded-lg bg-emerald-600 hover:bg-emerald-700 px-5 py-3 font-semibold"
            >
              {locationLoading
                ? "Getting Location..."
                : "📍 Get Current Location"}
            </button>

            {latitude && longitude && (
              <div className="mt-3 rounded-lg bg-slate-800 p-4 text-sm">
                <p>Latitude: {latitude}</p>
                <p>Longitude: {longitude}</p>
              </div>
            )}
          </div>

          {message && (
            <div className="rounded-lg bg-slate-800 p-4 text-sm">
              {message}
            </div>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-lg bg-blue-500 hover:bg-blue-600 disabled:opacity-50 py-3 font-semibold"
          >
            {submitting
              ? "Submitting..."
              : "Submit Pothole Report"}
          </button>
        </form>
      </div>
    </main>
  );
}