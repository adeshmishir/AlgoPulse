function Heatmap({ history }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <h3 className="mb-4 text-lg font-semibold">Recent Progress</h3>

      <div className="space-y-3">
        {history?.length === 0 && (
          <p className="text-slate-400">No history available.</p>
        )}

        {history?.map((item, index) => (
          <div
            key={index}
            className="flex items-center justify-between rounded-xl bg-slate-950 px-4 py-3"
          >
            <span className="text-sm text-slate-400">
              {new Date(item.date).toLocaleString()}
            </span>
            <span className="font-semibold">{item.total_solved} solved</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Heatmap;