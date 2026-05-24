export default function HowItWorks() {
  return (
    <section className="w-full max-w-5xl mx-auto px-6 py-32">
      <div className="text-[11px] font-semibold uppercase tracking-widest text-slate-400 mb-16">
        HOW IT WORKS
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-16 md:gap-8">
        {/* Step 1 */}
        <div className="flex flex-col items-start">
          <div className="text-4xl font-light text-slate-300 mb-4 tracking-tighter">
            01
          </div>
          <h3 className="text-lg font-semibold text-slate-900 mb-2">
            Login with Zoho
          </h3>
          <p className="text-slate-500 text-sm leading-relaxed">
            Authenticate securely via Zoho OAuth.
          </p>
        </div>

        {/* Step 2 */}
        <div className="flex flex-col items-start">
          <div className="text-4xl font-light text-slate-300 mb-4 tracking-tighter">
            02
          </div>
          <h3 className="text-lg font-semibold text-slate-900 mb-2">
            Select a Project
          </h3>
          <p className="text-slate-500 text-sm leading-relaxed">
            Choose from your existing Zoho projects.
          </p>
        </div>

        {/* Step 3 */}
        <div className="flex flex-col items-start">
          <div className="text-4xl font-light text-slate-300 mb-4 tracking-tighter">
            03
          </div>
          <h3 className="text-lg font-semibold text-slate-900 mb-2">
            Start Chatting
          </h3>
          <p className="text-slate-500 text-sm leading-relaxed">
            Query, create, or update tasks via chat.
          </p>
        </div>
      </div>
    </section>
  );
}
