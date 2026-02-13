import { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRequestOtp, useVerifyOtp } from './hooks';
import { useAuth } from '@/shared/providers/AuthProvider';
import { Button } from '@/shared/ui/button';
import { Card } from '@/shared/ui/card';
import { Input } from '@/shared/ui/input';

export function LoginForm() {
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpRequested, setOtpRequested] = useState(false);
  const requestOtp = useRequestOtp();
  const verifyOtp = useVerifyOtp();
  const { setToken } = useAuth();
  const navigate = useNavigate();

  const onRequestOtp = async (e: FormEvent) => {
    e.preventDefault();
    await requestOtp.mutateAsync({ phone_number: phone });
    setOtpRequested(true);
  };

  const onVerifyOtp = async (e: FormEvent) => {
    e.preventDefault();
    const result = await verifyOtp.mutateAsync({ phone_number: phone, code: otp });
    setToken(result.access_token);
    navigate('/menu');
  };

  return (
    <Card className="mx-auto max-w-md space-y-4">
      <h1 className="text-2xl font-semibold">Login with OTP</h1>
      <form onSubmit={onRequestOtp} className="space-y-3">
        <Input value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Phone number" required />
        <Button className="w-full" disabled={requestOtp.isPending}>
          {requestOtp.isPending ? 'Requesting...' : 'Request OTP'}
        </Button>
      </form>

      {otpRequested && (
        <form onSubmit={onVerifyOtp} className="space-y-3 border-t pt-4">
          <Input value={otp} onChange={(e) => setOtp(e.target.value)} placeholder="6-digit OTP" maxLength={6} required />
          <Button className="w-full" disabled={verifyOtp.isPending}>
            {verifyOtp.isPending ? 'Verifying...' : 'Verify & Login'}
          </Button>
        </form>
      )}

      {(requestOtp.error || verifyOtp.error) && <p className="text-sm text-red-600">Failed authentication request.</p>}
    </Card>
  );
}
