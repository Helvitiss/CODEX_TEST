import { Category, CreateCategoryPayload, CreateDishPayload, Dish, UpdateCategoryPayload, UpdateDishPayload } from '@/entities/menu/types';
import { http } from './http';

export const menuApi = {
  getCategories: async () => {
    const { data } = await http.get<Category[]>('/menu/categories');
    return data;
  },
  getDishes: async () => {
    const { data } = await http.get<Dish[]>('/menu/dishes');
    return data;
  },
  createCategory: async (payload: CreateCategoryPayload) => {
    const { data } = await http.post<Category>('/menu/categories', payload);
    return data;
  },
  updateCategory: async (id: number, payload: UpdateCategoryPayload) => {
    const { data } = await http.put<Category>(`/menu/categories/${id}`, payload);
    return data;
  },
  deleteCategory: async (id: number) => {
    await http.delete(`/menu/categories/${id}`);
  },
  createDish: async (payload: CreateDishPayload) => {
    const { data } = await http.post<Dish>('/menu/dishes', payload);
    return data;
  },
  updateDish: async (id: number, payload: UpdateDishPayload) => {
    const { data } = await http.put<Dish>(`/menu/dishes/${id}`, payload);
    return data;
  },
  deleteDish: async (id: number) => {
    await http.delete(`/menu/dishes/${id}`);
  }
};
