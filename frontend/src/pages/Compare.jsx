import { useState } from "react";
import api from "../services/api";

function Compare() {
  const [user1, setUser1] = useState("");
  const [user2, setUser2] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCompare = async (e) => {
    e.preventDefault();

    if (!user1.trim() || !user2.trim()) return;

    try {
      setLoading(true);
      setError("");
      setData(null);

      const res = await api.get(`/compare/${user1.trim()}/${user2.trim()}`);
      setData(res.data);
    } catch (err) {
      setError("Failed to compare users");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-6xl px-6 py-12">
      <h1 className="mb-3 text-4xl font-bold">Compare Users</h1>
      <p className="mb-8 text-slate-400">
        Compare two LeetCode profiles by ranking, solved problems, acceptance,
        and contest rating.
      </p>

      <form onSubmit={handleCompare} className="mb-10 grid gap-4 md:grid-cols-3">
        <input
          type="text"
          placeholder="First username"
          value={user1}
          onChange={(e) => setUser1(e.target.value)}
          className="rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none focus:border-blue-500"
        />

        <input
          type="text"
          placeholder="Second username"
          value={user2}
          onChange={(e) => setUser2(e.target.value)}
          className="rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none focus:border-blue-500"
        />

        <button
          type="submit"
          className="rounded-xl bg-blue-600 px-6 py-3 font-semibold hover:bg-blue-700"
        >
          Compare
        </button>
      </form>

      {loading && <p className="text-slate-400">Comparing users...</p>}
      {error && <p className="text-red-400">{error}</p>}

      {data && (
        <div className="grid gap-6 md:grid-cols-2">
          <UserCompareCard user={data.user1} winner={data.winner} />
          <UserCompareCard user={data.user2} winner={data.winner} />
        </div>
      )}
    </main>
  );
}

function UserCompareCard({ user, winner }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-5 text-2xl font-bold">@{user.username}</h2>

      <CompareRow
        label="Ranking"
        value={user.ranking}
        won={winner.ranking === user.username}
      />

      <CompareRow
        label="Total Solved"
        value={user.total_solved}
        won={winner.solved === user.username}
      />

      <CompareRow
        label="Acceptance"
        value={`${user.acceptance}%`}
        won={winner.acceptance === user.username}
      />

      <CompareRow
        label="Contest Rating"
        value={user.contest_rating || "N/A"}
        won={winner.contest_rating === user.username}
      />
    </div>
  );
}

function CompareRow({ label, value, won }) {
  return (
    <div className="mb-4 flex items-center justify-between rounded-xl bg-slate-950 px-4 py-3">
      <span className="text-slate-400">{label}</span>
      <span className={won ? "font-bold text-green-400" : "font-semibold"}>
        {value}
      </span>
    </div>
  );
}

export default Compare;