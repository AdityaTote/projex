import LoginLeftPanel from "@/components/login/LoginLeftPanel";
import LoginForm from "@/components/login/LoginForm";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen bg-white font-sans selection:bg-slate-900 selection:text-white">
      <LoginLeftPanel />
      <LoginForm />
    </div>
  );
}
