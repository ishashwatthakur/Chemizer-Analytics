import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Eye, EyeOff, ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { OTPVerification } from "@/components/OTPVerification";
import { GoogleLogin, CredentialResponse } from "@react-oauth/google";
import { apiClient } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showOTP, setShowOTP] = useState(false);
  const [userEmail, setUserEmail] = useState("");
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await apiClient.login(formData.username, formData.password);

      if (result.error) {
        toast.error(result.error);
        setLoading(false);
        return;
      }

      const data = result.data as any;
      if (data.requires_otp) {
        setUserEmail(data.email);
        setShowOTP(true);
        toast.success("OTP sent to your email!");
      }
    } catch (error) {
      toast.error("Network error. Please try again.");
      console.error("Login error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (otp: string) => {
    try {
      const result = await apiClient.verifyOTP(userEmail, otp);

      if (result.error) {
        toast.error(result.error);
        return;
      }

      const data = result.data as any;
      if (data.token) {
        login(data.token, {
          user_id: data.user_id,
          username: data.username,
          email: data.email,
          full_name: data.full_name,
        });
      }

      toast.success("Login successful!");
      setTimeout(() => navigate("/main"), 1000);
    } catch (error) {
      toast.error("Verification failed. Please try again.");
      console.error("OTP verification error:", error);
    }
  };

  const handleResendOTP = async () => {
    try {
      const result = await apiClient.resendOTP(userEmail);

      if (result.error) {
        toast.error(result.error);
        return;
      }

      toast.success("New OTP sent to your email!");
    } catch (error) {
      toast.error("Failed to resend OTP");
      console.error("Resend OTP error:", error);
    }
  };

  const handleGoogleSignIn = async (credentialResponse: CredentialResponse) => {
    setLoading(true);
    try {
      const token = credentialResponse?.credential;
      if (!token) {
        toast.error("No credential returned from Google");
        console.error("Google credential missing", credentialResponse);
        setLoading(false);
        return;
      }

      const result = await apiClient.googleLogin(token);

      if (result.error) {
        toast.error(result.error);
        setLoading(false);
        return;
      }

      const data = result.data as any;
      if (data.token) {
        login(data.token, {
          user_id: data.user_id,
          username: data.username,
          email: data.email,
          full_name: data.full_name,
        });
      }

      toast.success("Login successful!");
      setTimeout(() => navigate("/main"), 1000);
    } catch (error) {
      toast.error("Google sign-in failed. Please try again.");
      console.error("Google sign-in error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleError = () => {
    toast.error("Google sign-in failed");
    console.error("Google sign-in encountered an error");
  };

  if (showOTP) {
    return (
      <OTPVerification
        email={userEmail}
        onVerify={handleVerifyOTP}
        onResend={handleResendOTP}
        onBack={() => setShowOTP(false)}
      />
    );
  }

  return (
    <div className="min-h-screen bg-white flex">
      <div className="flex-1 flex flex-col">
        <div className="p-6 flex items-center justify-between">
          <Button
            variant="ghost"
            onClick={() => navigate("/")}
            className="rounded-md"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
          <h1 
            onClick={() => navigate("/")}
            className="text-xl font-bold cursor-pointer hover:text-accent transition-colors"
          >
            Chemizer Analytics
          </h1>
        </div>

        <div className="flex-1 flex items-center justify-center px-6">
          <div className="w-full max-w-md">
            <h2 className="text-3xl font-bold mb-2 text-black">Welcome back</h2>
            <p className="text-muted-foreground mb-8">Sign in to continue to your account</p>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="username" className="text-black">Username</Label>
                <Input
                  id="username"
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="bg-white border-gray-300 text-black"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-black">Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    className="bg-white border-gray-300 text-black pr-10"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-black"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <div className="flex justify-end">
                <button
                  type="button"
                  className="text-sm text-accent hover:underline"
                >
                  Forgot password?
                </button>
              </div>

              <Button
                type="submit"
                className="w-full bg-black text-white hover:bg-black/90 rounded-md"
                disabled={loading}
              >
                {loading ? "Signing in..." : "Sign In"}
              </Button>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-white px-2 text-muted-foreground">Or continue with</span>
                </div>
              </div>

              <div className="flex justify-center">
                <GoogleLogin
                  onSuccess={handleGoogleSignIn}
                  onError={handleGoogleError}
                  theme="outline"
                  text="signin_with"
                  width="384"
                />
              </div>
            </form>

            <p className="mt-8 text-center text-sm text-muted-foreground">
              Don't have an account?{" "}
              <button
                onClick={() => navigate("/auth/signup")}
                className="text-accent hover:underline font-medium"
              >
                Sign up
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;