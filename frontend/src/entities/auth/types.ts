export type OTPRequestPayload = { phone_number: string };
export type OTPVerifyPayload = { phone_number: string; code: string };

export type OTPSentResponse = {
  phone_number: string;
  expires_in_seconds: number;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};
