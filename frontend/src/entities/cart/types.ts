export type CartItem = {
  id: number;
  dish_id: number;
  quantity: number;
  unit_price: string;
};

export type Cart = {
  id: number;
  user_id: number | null;
  session_id: string | null;
  is_active: boolean;
  items: CartItem[];
};

export type AddToCartPayload = {
  dish_id: number;
  quantity: number;
};
