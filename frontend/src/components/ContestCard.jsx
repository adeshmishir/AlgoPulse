function ContestCard({ contest }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <h3 className="mb-4 text-lg font-semibold">Contest Analytics</h3>

      {!contest ? (
        <p className="text-slate-400">No contest data found.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <p className="text-sm text-slate-400">Rating</p>
            <h4 className="text-2xl font-bold">{contest.rating}</h4>
          </div>

          <div>
            <p className="text-sm text-slate-400">Attended</p>
            <h4 className="text-2xl font-bold">{contest.attended_contests}</h4>
          </div>

          <div>
            <p className="text-sm text-slate-400">Global Rank</p>
            <h4 className="text-2xl font-bold">{contest.global_ranking}</h4>
          </div>

          <div>
            <p className="text-sm text-slate-400">Top Percentage</p>
            <h4 className="text-2xl font-bold">{contest.top_percentage}%</h4>
          </div>
        </div>
      )}
    </div>
  );
}

export default ContestCard;