import Navbar from "@/components/landing/Navbar";
import HeroSection from "@/components/landing/HeroSection";
import HowItWorks from "@/components/landing/HowItWorks";
import FeaturesSection from "@/components/landing/FeaturesSection";
import Footer from "@/components/landing/Footer";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white text-slate-900 font-sans flex flex-col selection:bg-slate-900 selection:text-white">
      <Navbar />
      <main className="flex-1 flex flex-col items-center w-full">
        <HeroSection />
        <HowItWorks />
        <FeaturesSection />
      </main>
      <Footer />
    </div>
  );
}
