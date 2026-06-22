import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();

    if (!username.trim()) return;

    navigate(`/dashboard/${username.trim()}`);
  };

  return (
    <main className="mx-auto max-w-6xl px-6 py-20">
      <section className="grid items-center gap-12 md:grid-cols-2">
        <div>
          <p className="mb-3 text-sm font-semibold uppercase tracking-widest text-blue-400">
            LeetCode Analytics
          </p>

          <h1 className="mb-6 text-5xl font-bold leading-tight text-white">
            Track your coding progress with clean analytics.
          </h1>

          <p className="mb-8 max-w-xl text-lg text-slate-400">
            AlgoPulse helps you analyze LeetCode profiles, contest performance,
            growth history, problem distribution, and compare users in one place.
          </p>

          <form onSubmit={handleSearch} className="flex max-w-xl gap-3">
            <input
              type="text"
              placeholder="Enter LeetCode username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none focus:border-blue-500"
            />

            <button
              type="submit"
              className="rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
            >
              Analyze
            </button>
          </form>
        </div>
      </section>
    </main>
  );
}

export default Home;