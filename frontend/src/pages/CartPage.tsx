import { useMemo } from 'react';
import { useCart } from '@/entities/cart/hooks';
import { useDishes } from '@/entities/menu/hooks';
import { Card } from '@/shared/ui/card';

export function CartPage() {
  const { data: cart, isLoading, error } = useCart();
  const { data: dishes = [] } = useDishes();

  const rows = useMemo(() => {
    if (!cart) return [];
    return cart.items.map((item) => {
      const dish = dishes.find((d) => d.id === item.dish_id);
      return {
        ...item,
        name: dish?.name ?? `Dish #${item.dish_id}`,
        lineTotal: Number(item.unit_price) * item.quantity
      };
    });
  }, [cart, dishes]);

  const total = rows.reduce((sum, row) => sum + row.lineTotal, 0);

  if (isLoading) return <p>Loading cart...</p>;
  if (error) return <p className="text-red-600">Failed to load cart.</p>;

  return (
    <Card>
      <h1 className="mb-4 text-2xl font-semibold">Your Cart</h1>
      <div className="space-y-3">
        {rows.length === 0 && <p className="text-slate-500">Cart is empty.</p>}
        {rows.map((row) => (
          <div key={row.id} className="flex items-center justify-between border-b pb-2">
            <div>
              <p className="font-medium">{row.name}</p>
              <p className="text-sm text-slate-500">Qty: {row.quantity}</p>
            </div>
            <p>${row.lineTotal.toFixed(2)}</p>
          </div>
        ))}
      </div>
      <p className="mt-4 text-right text-lg font-semibold">Total: ${total.toFixed(2)}</p>
    </Card>
  );
}
