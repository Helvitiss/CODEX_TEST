import { useOrders, useUpdateOrderStatus } from '@/entities/order/hooks';
import { OrderStatus } from '@/entities/order/types';
import { Badge } from '@/shared/ui/badge';
import { Card } from '@/shared/ui/card';

const statuses: OrderStatus[] = ['pending', 'confirmed', 'cooking', 'delivering', 'completed', 'cancelled'];

export function OrdersAdminTable() {
  const { data: orders = [], isLoading, error } = useOrders();
  const updateStatus = useUpdateOrderStatus();

  if (isLoading) return <p>Loading orders...</p>;
  if (error) return <p className="text-red-600">Failed to load orders.</p>;

  return (
    <Card>
      <h2 className="mb-4 text-xl font-semibold">Orders</h2>
      <div className="space-y-3">
        {orders.map((order) => (
          <div key={order.id} className="rounded-md border p-3">
            <div className="mb-2 flex items-center justify-between">
              <p className="font-semibold">Order #{order.id}</p>
              <Badge>{order.status}</Badge>
            </div>
            <p className="text-sm text-slate-500">Phone: {order.phone_number}</p>
            <p className="text-sm text-slate-500">Total: ${order.total_amount}</p>
            <select
              className="mt-2 h-9 rounded-md border px-2"
              value={order.status}
              onChange={(e) => updateStatus.mutate({ orderId: order.id, status: e.target.value as OrderStatus })}
            >
              {statuses.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
    </Card>
  );
}
