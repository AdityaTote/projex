const features = [
  {
    title: "Query Anything",
    description: "Ask about tasks, members, deadlines in plain English.",
  },
  {
    title: "Take Actions",
    description: "Create, update, and delete tasks directly via chat.",
  },
  {
    title: "Approval Flow",
    description: "AI asks for confirmation before any write or delete action.",
  },
  {
    title: "Project Memory",
    description: "Remembers your last active project across sessions.",
  },
  {
    title: "Secure Auth",
    description: "Powered by Zoho OAuth 2.0 and JWT.",
  },
  {
    title: "Fast & Accurate",
    description: "Built on Gemini 2.0 Flash AI for fast responses.",
  },
];

export default function FeaturesSection() {
  return (
    <section className="w-full max-w-5xl mx-auto px-6 py-32">
      <div className="text-[11px] font-semibold uppercase tracking-widest text-slate-400 mb-16">
        FEATURES
      </div>

      <div className="flex flex-col border-t border-slate-200">
        {features.map((feature) => (
          <div
            key={feature.title}
            className="grid grid-cols-1 md:grid-cols-3 py-6 border-b border-slate-200 gap-2 md:gap-8 items-start"
          >
            <div className="font-semibold text-slate-900 md:col-span-1">
              {feature.title}
            </div>
            <div className="text-slate-500 text-sm leading-relaxed md:col-span-2">
              {feature.description}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
