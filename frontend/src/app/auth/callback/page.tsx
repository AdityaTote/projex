"use client";

import { Suspense, useEffect, useRef } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useAuthCallback } from "@/hooks/useAuth";
import { Bot } from "lucide-react";

function CallbackHandler() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { mutate, isPending, isError, error } = useAuthCallback();
  const calledRef = useRef(false);

  useEffect(() => {
    // Prevent duplicate calls — mutate/router reference changes must not re-trigger
    if (calledRef.current) return;

    const code = searchParams.get("code");
    if (code) {
      calledRef.current = true;
      mutate(code);
    } else {
      // router.replace("/login");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  return (
    <>
      {isPending && (
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-2 border-slate-200 border-t-slate-900 rounded-full animate-spin" />
          <p className="text-sm text-slate-500">Authenticating with Zoho...</p>
        </div>
      )}

      {isError && (
        <div className="flex flex-col items-center gap-4 max-w-sm text-center">
          <div className="w-12 h-12 rounded-full bg-rose-50 flex items-center justify-center text-rose-500 text-xl">
            ✕
          </div>
          <p className="text-sm text-slate-700 font-medium">
            Authentication failed
          </p>
          <p className="text-xs text-slate-400">
            {error instanceof Error ? error.message : "Something went wrong"}
          </p>
          <button
            onClick={() => router.replace("/login")}
            className="px-4 py-2 text-sm font-medium bg-slate-900 text-white rounded-md hover:bg-slate-800 transition-colors"
          >
            Try again
          </button>
        </div>
      )}
    </>
  );
}

export default function AuthCallbackPage() {
  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center font-sans">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 bg-slate-900 rounded-lg flex items-center justify-center text-white">
          <Bot className="w-6 h-6" />
        </div>
        <span className="font-bold text-xl tracking-tight text-slate-900">
          Projex
        </span>
      </div>

      <Suspense
        fallback={
          <div className="flex flex-col items-center gap-4">
            <div className="w-8 h-8 border-2 border-slate-200 border-t-slate-900 rounded-full animate-spin" />
            <p className="text-sm text-slate-500">Loading...</p>
          </div>
        }
      >
        <CallbackHandler />
      </Suspense>
    </div>
  );
}
