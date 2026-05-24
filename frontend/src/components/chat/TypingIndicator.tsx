export default function TypingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="bg-slate-100 px-4 py-2 rounded-full flex gap-1.5 items-center">
        <div className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
        <div className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
        <div className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></div>
      </div>
    </div>
  );
}
