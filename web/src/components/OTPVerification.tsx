import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft } from "lucide-react";

interface OTPVerificationProps {
  email: string;
  onVerify: (otp: string) => Promise<void>;
  onResend: () => Promise<void>;
  onBack?: () => void;
}

export const OTPVerification = ({ 
  email, 
  onVerify, 
  onResend,
  onBack 
}: OTPVerificationProps) => {
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);
  const [timer, setTimer] = useState(60);
  const [canResend, setCanResend] = useState(false);

  useEffect(() => {
    if (timer > 0) {
      const interval = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
      return () => clearInterval(interval);
    } else {
      setCanResend(true);
    }
  }, [timer]);

  const handleVerify = async () => {
    if (otp.length !== 6) {
      return;
    }

    setLoading(true);
    await onVerify(otp);
    setLoading(false);
  };

  const handleResend = async () => {
    setResendLoading(true);
    await onResend();
    setResendLoading(false);
    setTimer(60);
    setCanResend(false);
  };

  const handleOtpChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.replace(/\D/g, "").slice(0, 6);
    setOtp(value);
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        {onBack && (
          <Button
            variant="ghost"
            onClick={onBack}
            className="mb-4 rounded-md"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
        )}

        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold mb-2 text-black">Verify Your Email</h2>
          <p className="text-muted-foreground">
            We've sent a verification code to
          </p>
          <p className="text-black font-medium">{email}</p>
        </div>

        <div className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-black">
              Enter 6-digit code
            </label>
            <Input
              type="text"
              inputMode="numeric"
              pattern="[0-9]*"
              maxLength={6}
              value={otp}
              onChange={handleOtpChange}
              placeholder="000000"
              className="text-center text-2xl tracking-widest bg-white border-gray-300 text-black"
            />
          </div>

          <Button
            onClick={handleVerify}
            disabled={otp.length !== 6 || loading}
            className="w-full bg-black text-white hover:bg-black/90 rounded-md"
          >
            {loading ? "Verifying..." : "Verify Email"}
          </Button>

          <div className="text-center">
            {canResend ? (
              <button
                onClick={handleResend}
                disabled={resendLoading}
                className="text-sm text-accent hover:underline font-medium"
              >
                {resendLoading ? "Sending..." : "Resend Code"}
              </button>
            ) : (
              <p className="text-sm text-muted-foreground">
                Resend code in {timer}s
              </p>
            )}
          </div>

          <p className="text-xs text-center text-muted-foreground">
            Didn't receive the code? Check your spam folder or try resending.
          </p>
        </div>
      </div>
    </div>
  );
};