import { AddToCartPayload, Cart } from '@/entities/cart/types';
import { getOrCreateSessionId } from '@/shared/lib/session';
import { authTokenStore } from '@/shared/providers/AuthProvider';
import { http } from './http';

export const cartApi = {
  getCart: async () => {
    const isAuthenticated = Boolean(authTokenStore.getToken());
    const sessionId = getOrCreateSessionId();
    const endpoint = isAuthenticated ? '/cart' : '/cart/guest';
    const { data } = await http.get<Cart>(endpoint, { params: { session_id: sessionId } });
    return data;
  },
  addToCart: async (payload: AddToCartPayload) => {
    const isAuthenticated = Boolean(authTokenStore.getToken());
    const sessionId = getOrCreateSessionId();
    const endpoint = isAuthenticated ? '/cart' : '/cart/guest';
    const { data } = await http.post<Cart>(endpoint, payload, { params: { session_id: sessionId } });
    return data;
  }
};
