import { http } from './http';
import { OTPRequestPayload, OTPSentResponse, OTPVerifyPayload, TokenResponse } from '@/entities/auth/types';

export const authApi = {
  requestOtp: async (payload: OTPRequestPayload) => {
    const { data } = await http.post<OTPSentResponse>('/auth/otp/request', payload);
    return data;
  },
  verifyOtp: async (payload: OTPVerifyPayload) => {
    const { data } = await http.post<TokenResponse>('/auth/otp/verify', payload);
    return data;
  }
};
