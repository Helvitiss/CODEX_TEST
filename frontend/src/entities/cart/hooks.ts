import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { cartApi } from '@/shared/api/cartApi';
import { AddToCartPayload, Cart } from './types';

export const cartKeys = {
  current: ['cart'] as const
};

export function useCart() {
  return useQuery({ queryKey: cartKeys.current, queryFn: cartApi.getCart });
}

export function useAddToCart() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: AddToCartPayload) => cartApi.addToCart(payload),
    onMutate: async (payload) => {
      await queryClient.cancelQueries({ queryKey: cartKeys.current });
      const previousCart = queryClient.getQueryData<Cart>(cartKeys.current);

      if (previousCart) {
        const existingItem = previousCart.items.find((item) => item.dish_id === payload.dish_id);
        const optimistic: Cart = {
          ...previousCart,
          items: existingItem
            ? previousCart.items.map((item) =>
                item.dish_id === payload.dish_id ? { ...item, quantity: item.quantity + payload.quantity } : item
              )
            : [...previousCart.items, { id: Date.now(), dish_id: payload.dish_id, quantity: payload.quantity, unit_price: '0' }]
        };
        queryClient.setQueryData(cartKeys.current, optimistic);
      }

      return { previousCart };
    },
    onError: (_, __, context) => {
      if (context?.previousCart) {
        queryClient.setQueryData(cartKeys.current, context.previousCart);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: cartKeys.current });
    }
  });
}
