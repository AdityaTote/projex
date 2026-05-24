import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-white">
      <div className="max-w-5xl mx-auto px-6 h-24 flex items-center justify-between">
        <span className="font-medium tracking-tight text-slate-900">
          Projex
        </span>
        <Link
          href="/login"
          className="px-4 py-2 text-sm font-medium border border-slate-200 rounded-md text-slate-900 hover:bg-slate-50 transition-colors"
        >
          Login with Zoho
        </Link>
      </div>
    </nav>
  );
}
