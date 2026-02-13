import { useAddToCart } from '@/entities/cart/hooks';
import { Button } from '@/shared/ui/button';

export function AddToCartButton({ dishId }: { dishId: number }) {
  const mutation = useAddToCart();

  return (
    <Button onClick={() => mutation.mutate({ dish_id: dishId, quantity: 1 })} disabled={mutation.isPending}>
      {mutation.isPending ? 'Adding...' : 'Add to cart'}
    </Button>
  );
}
