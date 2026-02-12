export type OrderStatus =
  | 'pending'
  | 'confirmed'
  | 'cooking'
  | 'delivering'
  | 'completed'
  | 'cancelled';

export type OrderItem = {
  id: number;
  dish_name: string;
  quantity: number;
  unit_price: string;
};

export type Order = {
  id: number;
  user_id: number | null;
  phone_number: string;
  status: OrderStatus;
  total_amount: string;
  items: OrderItem[];
};
