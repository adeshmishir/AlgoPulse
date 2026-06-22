import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import StatCard from "../components/StatCard";
import ProblemChart from "../components/ProblemChart";
import ContestCard from "../components/ContestCard";
import Heatmap from "../components/Heatmap";

function Dashboard() {
  const { username } = useParams();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/profile/${username}/dashboard`);
        setData(res.data);
      } catch (err) {
        setError("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, [username]);

  if (loading) {
    return (
      <div className="mx-auto max-w-6xl px-6 py-20">
        <p className="text-slate-400">Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-6xl px-6 py-20">
        <p className="text-red-400">{error}</p>
      </div>
    );
  }

  const profile = data.profile;
  const stats = profile.stats;
  const summary = data.summary;
  const growth = data.growth;
  const contest = data.contest;

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <div className="mb-8 flex items-center gap-4">
        <img
          src={profile.avatar}
          alt={profile.username}
          className="h-16 w-16 rounded-full"
        />

        <div>
          <h1 className="text-3xl font-bold">{profile.real_name || username}</h1>
          <p className="text-slate-400">@{profile.username}</p>
        </div>
      </div>

      <div className="mb-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Ranking" value={profile.ranking} />
        <StatCard title="Total Solved" value={stats.total_solved} />
        <StatCard title="Acceptance" value={`${stats.acceptance_estimate}%`} />
        <StatCard
          title="Contest Rating"
          value={contest ? contest.rating : "N/A"}
        />
      </div>

      <div className="mb-8 grid gap-6 lg:grid-cols-2">
        <ProblemChart
          easy={summary.easy}
          medium={summary.medium}
          hard={summary.hard}
        />

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <h3 className="mb-4 text-lg font-semibold">Growth Analytics</h3>

          {growth ? (
            <div className="grid gap-4 sm:grid-cols-2">
              <StatCard
                title="Solved Growth"
                value={`+${growth.solved_growth}`}
                subtitle={`${growth.first_solved} → ${growth.latest_solved}`}
              />

              <StatCard
                title="Ranking Change"
                value={`+${growth.ranking_change}`}
                subtitle={`${growth.first_ranking} → ${growth.latest_ranking}`}
              />
            </div>
          ) : (
            <p className="text-slate-400">Not enough history data.</p>
          )}
        </div>
      </div>

      <div className="mb-8 grid gap-6 lg:grid-cols-2">
        <ContestCard contest={contest} />
        <Heatmap history={data.history} />
      </div>
    </main>
  );
}

export default Dashboard;