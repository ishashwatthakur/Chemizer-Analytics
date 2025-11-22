import { Button } from "@/components/ui/button";
import { ArrowRight, BarChart3, FileSpreadsheet, TrendingUp, LogOut, User } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";

const Home = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  const handleGetStarted = () => {
    if (isAuthenticated) {
      navigate("/main"); // Go to upload page if logged in
    } else {
      navigate("/auth/signup"); // Go to signup if not logged in
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 blur-backdrop border-b border-border">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold">Chemizer Analytics</h1>
          <div className="flex items-center gap-6">
            <a href="#about" className="text-sm hover:text-accent transition-colors">About</a>
            <a href="#features" className="text-sm hover:text-accent transition-colors">Features</a>
            
            {/* ✅ FIXED: Show username if logged in, otherwise show login buttons */}
            {isAuthenticated && user ? (
              <>
                <div className="flex items-center gap-2 text-sm">
                  <User className="h-4 w-4" />
                  <span className="font-medium">{user.full_name || user.username}</span>
                </div>
                <Button 
                  variant="outline"
                  onClick={() => navigate("/dashboard")}
                  className="rounded-md"
                >
                  Dashboard
                </Button>
                <Button
                  variant="ghost"
                  onClick={handleLogout}
                  className="rounded-md text-destructive"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button 
                  variant="outline" 
                  onClick={() => navigate("/auth/login")}
                  className="rounded-md"
                >
                  Sign In
                </Button>
                <Button 
                  onClick={handleGetStarted}
                  className="rounded-md bg-primary text-primary-foreground hover:bg-primary/90"
                >
                  Get Started
                </Button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-5xl font-bold mb-6 leading-tight">
            Chemical Equipment Parameter Visualizer
          </h2>
          <p className="text-lg text-muted-foreground mb-4">
            Upload your equipment data and get instant analytics with beautiful visualizations
          </p>
          <p className="text-muted-foreground mb-8">
            Analyze flowrate, pressure, temperature, and equipment performance with powerful charts and comprehensive reports
          </p>
          <Button 
            size="lg"
            onClick={handleGetStarted}
            className="rounded-md bg-primary text-primary-foreground hover:bg-primary/90"
          >
            Start Analyzing <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-6 bg-secondary/30">
        <div className="container mx-auto max-w-6xl">
          <h3 className="text-3xl font-bold text-center mb-12">Key Features</h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 bg-background rounded-lg border border-border">
              <FileSpreadsheet className="h-12 w-12 mb-4 text-accent" />
              <h4 className="text-xl font-semibold mb-2">Multi-Format Upload</h4>
              <p className="text-muted-foreground">Support for CSV and Excel files with automatic data parsing</p>
            </div>
            <div className="p-6 bg-background rounded-lg border border-border">
              <BarChart3 className="h-12 w-12 mb-4 text-accent" />
              <h4 className="text-xl font-semibold mb-2">Interactive Charts</h4>
              <p className="text-muted-foreground">Beautiful visualizations with hover effects and detailed insights</p>
            </div>
            <div className="p-6 bg-background rounded-lg border border-border">
              <TrendingUp className="h-12 w-12 mb-4 text-accent" />
              <h4 className="text-xl font-semibold mb-2">PDF Reports</h4>
              <p className="text-muted-foreground">Download comprehensive analysis reports with proper formatting</p>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-6">
        <div className="container mx-auto max-w-4xl text-center">
          <h3 className="text-3xl font-bold mb-6">About Chemizer Analytics</h3>
          <p className="text-lg text-muted-foreground mb-4">
            Chemizer Analytics is a powerful hybrid web and desktop application designed for chemical equipment analysis. 
            Upload your equipment data and receive instant insights through interactive visualizations and detailed reports.
          </p>
          <p className="text-muted-foreground">
            Built with modern technologies to provide seamless analysis of flowrate, pressure, temperature, and equipment performance metrics.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8 px-6">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-8">
            <a href="#about" className="text-sm text-muted-foreground hover:text-foreground transition-colors">About</a>
            <a href="/dashboard" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Dashboard</a>
            <a href="/profile" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Profile</a>
          </div>
          <a 
            href="https://github.com/ishashwatthakur/Chemizer-Analytics" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-muted-foreground hover:text-foreground transition-colors"
          >
            <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
            </svg>
          </a>
        </div>
      </footer>
    </div>
  );
};

export default Home;
