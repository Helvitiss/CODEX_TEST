import { useMutation } from '@tanstack/react-query';
import { authApi } from '@/shared/api/authApi';

export function useRequestOtp() {
  return useMutation({
    mutationFn: authApi.requestOtp
  });
}

export function useVerifyOtp() {
  return useMutation({
    mutationFn: authApi.verifyOtp
  });
}
