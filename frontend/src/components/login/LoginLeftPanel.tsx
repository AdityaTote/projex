import Link from "next/link";
import { Bot, Check } from "lucide-react";

export default function LoginLeftPanel() {
  return (
    <div className="hidden md:flex w-1/2 flex-col justify-between bg-[#0f172a] p-12 text-white">
      <Link href="/" className="flex items-center gap-3 w-fit">
        <div className="w-8 h-8 rounded-md bg-white flex items-center justify-center text-[#0f172a]">
          <Bot className="w-5 h-5" />
        </div>
        <span className="font-bold tracking-tight text-white">Projex</span>
      </Link>

      <div className="max-w-md">
        <h1 className="text-4xl lg:text-5xl font-bold tracking-tight mb-10 text-white">
          Your projects, managed by AI.
        </h1>
        <ul className="space-y-4">
          <li className="flex items-center gap-3">
            <Check className="w-4 h-4 text-white shrink-0" />
            <span className="text-sm text-slate-400 font-medium">
              Query tasks in plain English
            </span>
          </li>
          <li className="flex items-center gap-3">
            <Check className="w-4 h-4 text-white shrink-0" />
            <span className="text-sm text-slate-400 font-medium">
              Create and update via chat
            </span>
          </li>
          <li className="flex items-center gap-3">
            <Check className="w-4 h-4 text-white shrink-0" />
            <span className="text-sm text-slate-400 font-medium">
              Secure Zoho OAuth login
            </span>
          </li>
        </ul>
      </div>

      <div className="text-xs text-slate-500 font-medium">© 2025 Projex</div>
    </div>
  );
}
