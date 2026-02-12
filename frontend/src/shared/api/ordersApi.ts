import { Order, OrderStatus } from '@/entities/order/types';
import { getOrCreateSessionId } from '@/shared/lib/session';
import { authTokenStore } from '@/shared/providers/AuthProvider';
import { http } from './http';

export const ordersApi = {
  createOrder: async (phone_number: string) => {
    const isAuthenticated = Boolean(authTokenStore.getToken());
    const endpoint = isAuthenticated ? '/orders' : '/orders/guest';
    const { data } = await http.post<Order>(endpoint, { phone_number }, { params: { session_id: getOrCreateSessionId() } });
    return data;
  },
  getOrders: async () => {
    const { data } = await http.get<Order[]>('/orders');
    return data;
  },
  updateOrderStatus: async (orderId: number, status: OrderStatus) => {
    const { data } = await http.patch<Order>(`/orders/${orderId}/status`, { status });
    return data;
  }
};
