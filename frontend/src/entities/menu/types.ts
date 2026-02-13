export type Category = {
  id: number;
  name: string;
};

export type Dish = {
  id: number;
  category_id: number;
  name: string;
  description: string;
  price: string;
  is_available: boolean;
};

export type CreateCategoryPayload = { name: string };
export type UpdateCategoryPayload = { name: string };

export type CreateDishPayload = {
  category_id: number;
  name: string;
  description: string;
  price: number;
  is_available: boolean;
};

export type UpdateDishPayload = Partial<CreateDishPayload>;
