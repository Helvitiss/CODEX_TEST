import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { ordersApi } from '@/shared/api/ordersApi';
import { OrderStatus } from './types';

export const ordersKeys = {
  all: ['orders'] as const
};

export function useOrders() {
  return useQuery({ queryKey: ordersKeys.all, queryFn: ordersApi.getOrders });
}

export function useCreateOrder() {
  return useMutation({ mutationFn: (phoneNumber: string) => ordersApi.createOrder(phoneNumber) });
}

export function useUpdateOrderStatus() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ orderId, status }: { orderId: number; status: OrderStatus }) => ordersApi.updateOrderStatus(orderId, status),
    onSuccess: () => qc.invalidateQueries({ queryKey: ordersKeys.all })
  });
}
