"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleLogin(event: React.FormEvent) {
    event.preventDefault();

    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    localStorage.setItem(
      "roadpulse_user",
      JSON.stringify({
        id: 1,
        name: "RoadPulse Citizen",
        email,
        role: "citizen",
      }),
    );

    router.push("/report");
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-6">
      <form
        onSubmit={handleLogin}
        className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-8"
      >
        <h1 className="text-3xl font-bold mb-2">
          Road<span className="text-blue-400">Pulse</span>
        </h1>

        <p className="text-slate-400 mb-8">
          Citizen Login
        </p>

        <label className="block text-sm mb-2">
          Email
        </label>

        <input
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="you@example.com"
          className="w-full mb-5 rounded-lg bg-slate-800 border border-slate-700 px-4 py-3 outline-none"
        />

        <label className="block text-sm mb-2">
          Password
        </label>

        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="••••••••"
          className="w-full mb-6 rounded-lg bg-slate-800 border border-slate-700 px-4 py-3 outline-none"
        />

        <button
          type="submit"
          className="w-full rounded-lg bg-blue-500 hover:bg-blue-600 py-3 font-semibold"
        >
          Login
        </button>
      </form>
    </main>
  );
}