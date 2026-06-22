import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="border-b border-slate-800 bg-slate-950">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link to="/" className="text-xl font-bold text-white">
          AlgoPulse
        </Link>

        <div className="flex gap-6 text-sm text-slate-300">
          <Link to="/" className="hover:text-white">
            Home
          </Link>
          <Link to="/compare" className="hover:text-white">
            Compare
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;