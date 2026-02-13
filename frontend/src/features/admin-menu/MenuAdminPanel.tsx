import { FormEvent, useState } from 'react';
import { useCategories, useCreateCategory, useCreateDish, useDeleteDish, useDishes } from '@/entities/menu/hooks';
import { Button } from '@/shared/ui/button';
import { Card } from '@/shared/ui/card';
import { Input } from '@/shared/ui/input';
import { Textarea } from '@/shared/ui/textarea';

export function MenuAdminPanel() {
  const { data: categories = [] } = useCategories();
  const { data: dishes = [] } = useDishes();
  const createCategory = useCreateCategory();
  const createDish = useCreateDish();
  const deleteDish = useDeleteDish();

  const [categoryName, setCategoryName] = useState('');
  const [dishForm, setDishForm] = useState({ name: '', description: '', price: '0', category_id: '' });

  const addCategory = async (e: FormEvent) => {
    e.preventDefault();
    await createCategory.mutateAsync({ name: categoryName });
    setCategoryName('');
  };

  const addDish = async (e: FormEvent) => {
    e.preventDefault();
    await createDish.mutateAsync({
      name: dishForm.name,
      description: dishForm.description,
      price: Number(dishForm.price),
      category_id: Number(dishForm.category_id),
      is_available: true
    });
    setDishForm({ name: '', description: '', price: '0', category_id: '' });
  };

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <h2 className="mb-4 text-lg font-semibold">Add Category</h2>
        <form onSubmit={addCategory} className="space-y-3">
          <Input value={categoryName} onChange={(e) => setCategoryName(e.target.value)} placeholder="Category name" required />
          <Button disabled={createCategory.isPending}>Save category</Button>
        </form>
      </Card>

      <Card>
        <h2 className="mb-4 text-lg font-semibold">Add Dish</h2>
        <form onSubmit={addDish} className="space-y-3">
          <Input placeholder="Dish name" value={dishForm.name} onChange={(e) => setDishForm({ ...dishForm, name: e.target.value })} required />
          <Textarea
            placeholder="Description"
            value={dishForm.description}
            onChange={(e) => setDishForm({ ...dishForm, description: e.target.value })}
            required
          />
          <Input type="number" step="0.01" value={dishForm.price} onChange={(e) => setDishForm({ ...dishForm, price: e.target.value })} />
          <select
            className="h-10 w-full rounded-md border border-slate-300 px-3"
            value={dishForm.category_id}
            onChange={(e) => setDishForm({ ...dishForm, category_id: e.target.value })}
            required
          >
            <option value="">Select category</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
          <Button disabled={createDish.isPending}>Save dish</Button>
        </form>
      </Card>

      <Card className="lg:col-span-2">
        <h2 className="mb-4 text-lg font-semibold">Dishes</h2>
        <div className="space-y-2">
          {dishes.map((dish) => (
            <div key={dish.id} className="flex items-center justify-between rounded-md border p-3">
              <div>
                <p className="font-medium">{dish.name}</p>
                <p className="text-sm text-slate-500">${dish.price}</p>
              </div>
              <Button variant="destructive" onClick={() => deleteDish.mutate(dish.id)}>
                Delete
              </Button>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
