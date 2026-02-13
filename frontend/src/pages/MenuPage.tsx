import { useCategories, useDishes } from '@/entities/menu/hooks';
import { AddToCartButton } from '@/features/cart/AddToCartButton';
import { Card } from '@/shared/ui/card';

export function MenuPage() {
  const { data: categories = [], isLoading: categoriesLoading } = useCategories();
  const { data: dishes = [], isLoading: dishesLoading, error } = useDishes();

  if (categoriesLoading || dishesLoading) return <p>Loading menu...</p>;
  if (error) return <p className="text-red-600">Unable to load menu.</p>;

  return (
    <div className="space-y-6">
      {categories.map((category) => {
        const categoryDishes = dishes.filter((dish) => dish.category_id === category.id && dish.is_available);
        return (
          <section key={category.id}>
            <h2 className="mb-3 text-2xl font-semibold">{category.name}</h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {categoryDishes.map((dish) => (
                <Card key={dish.id} className="space-y-3">
                  <div>
                    <h3 className="text-lg font-semibold">{dish.name}</h3>
                    <p className="text-sm text-slate-500">{dish.description}</p>
                  </div>
                  <p className="font-semibold">${dish.price}</p>
                  <AddToCartButton dishId={dish.id} />
                </Card>
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}
