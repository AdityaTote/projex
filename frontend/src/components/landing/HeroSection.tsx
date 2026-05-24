import Link from "next/link";

export default function HeroSection() {
  return (
    <section className="w-full max-w-5xl mx-auto px-6 py-[200px] flex flex-col items-center text-center">
      <div className="text-[11px] font-semibold uppercase tracking-widest text-slate-400 mb-6">
        ZOHO PROJECTS · AI ASSISTANT
      </div>
      <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-slate-900 mb-8 max-w-3xl text-balance">
        Your Zoho projects, on autopilot.
      </h1>
      <p className="text-lg md:text-xl text-slate-500 mb-12 max-w-2xl text-balance">
        Ask questions. Create tasks. Get things done — in plain chat.
      </p>
      <Link
        href="/login"
        className="inline-flex items-center justify-center px-6 py-3 rounded-md bg-slate-900 text-white font-medium hover:bg-slate-800 transition-colors"
      >
        Get started with Zoho
      </Link>
    </section>
  );
}
