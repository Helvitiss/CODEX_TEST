import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { menuApi } from '@/shared/api/menuApi';
import { CreateCategoryPayload, CreateDishPayload, UpdateDishPayload } from './types';

export const menuKeys = {
  all: ['menu'] as const,
  categories: ['menu', 'categories'] as const,
  dishes: ['menu', 'dishes'] as const
};

export function useCategories() {
  return useQuery({ queryKey: menuKeys.categories, queryFn: menuApi.getCategories });
}

export function useDishes() {
  return useQuery({ queryKey: menuKeys.dishes, queryFn: menuApi.getDishes });
}

export function useCreateCategory() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateCategoryPayload) => menuApi.createCategory(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: menuKeys.categories })
  });
}

export function useCreateDish() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateDishPayload) => menuApi.createDish(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: menuKeys.all })
  });
}

export function useUpdateDish() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: UpdateDishPayload }) => menuApi.updateDish(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: menuKeys.dishes })
  });
}

export function useDeleteDish() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => menuApi.deleteDish(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: menuKeys.dishes })
  });
}
