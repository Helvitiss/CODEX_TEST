import { FormEvent, useState } from 'react';
import { useCreateOrder } from '@/entities/order/hooks';
import { Button } from '@/shared/ui/button';
import { Card } from '@/shared/ui/card';
import { Input } from '@/shared/ui/input';

export function CheckoutForm() {
  const [phone, setPhone] = useState('');
  const createOrder = useCreateOrder();

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    await createOrder.mutateAsync(phone);
    setPhone('');
  };

  return (
    <Card className="max-w-lg">
      <h1 className="mb-4 text-2xl font-semibold">Checkout</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <Input value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Phone number" required />
        <Button disabled={createOrder.isPending}>{createOrder.isPending ? 'Placing...' : 'Place order'}</Button>
      </form>
      {createOrder.isSuccess && <p className="mt-3 text-green-600">Order placed successfully.</p>}
      {createOrder.isError && <p className="mt-3 text-red-600">Failed to place order.</p>}
    </Card>
  );
}
