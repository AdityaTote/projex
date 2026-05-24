"use client";

import Link from "next/link";
import { Bot } from "lucide-react";
import { authApi } from "@/lib/api/auth";
import { useState } from "react";

export default function LoginForm() {
  const [isRedirecting, setIsRedirecting] = useState(false);

  const handleZohoLogin = async () => {
    try {
      setIsRedirecting(true);
      const { authorize_url } = await authApi.getAuthUrl();
      window.location.href = authorize_url;
    } catch {
      setIsRedirecting(false);
      // Fallback: just go to chat for now (dev mode)
    }
  };

  return (
    <div className="flex-1 flex flex-col relative p-8">
      <div className="absolute top-8 right-8 text-xs text-slate-400 font-medium">
        Need help?{" "}
        <a
          href="mailto:support@projex.io"
          className="text-slate-900 hover:underline"
        >
          support@projex.io
        </a>
      </div>

      {/* Mobile Header (Hidden on Desktop) */}
      <Link
        href="/"
        className="md:hidden flex items-center gap-3 w-fit mb-12"
      >
        <div className="w-8 h-8 rounded-md bg-slate-900 flex items-center justify-center text-white">
          <Bot className="w-5 h-5" />
        </div>
        <span className="font-bold tracking-tight text-slate-900">
          Projex
        </span>
      </Link>

      <div className="flex-1 flex flex-col items-center justify-center w-full flex-grow">
        <div className="w-full max-w-sm flex flex-col items-start px-4">
          <span className="text-[11px] font-semibold uppercase tracking-widest text-slate-400 mb-4">
            Welcome Back
          </span>
          <h2 className="text-3xl font-bold tracking-tight text-slate-900 mb-2">
            Sign in to Projex
          </h2>
          <p className="text-sm text-slate-500 mb-8">
            Connect your Zoho account to continue
          </p>

          <button
            onClick={handleZohoLogin}
            disabled={isRedirecting}
            className="w-full flex items-center justify-center gap-3 px-6 py-3.5 rounded-md bg-slate-900 text-white font-medium hover:bg-slate-800 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {isRedirecting ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Redirecting...
              </>
            ) : (
              <>
                <div className="w-4 h-4 bg-blue-500 rounded-sm" />
                Continue with Zoho
              </>
            )}
          </button>

          <p className="text-xs text-slate-400 w-full text-center mt-6">
            By continuing, you agree to our{" "}
            <a
              href="#"
              className="underline hover:text-slate-900 hover:no-underline transition-colors"
            >
              Terms of Service
            </a>
          </p>
        </div>
      </div>

      {/* Mobile Footer (Hidden on Desktop) */}
      <div className="md:hidden mt-12 text-center text-xs text-slate-400 font-medium pb-2">
        © 2025 Projex
      </div>
    </div>
  );
}
