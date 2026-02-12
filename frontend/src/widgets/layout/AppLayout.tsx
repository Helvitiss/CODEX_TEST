import { Link, NavLink, Outlet } from 'react-router-dom';
import { ShoppingCart } from 'lucide-react';
import { useAuth } from '@/shared/providers/AuthProvider';
import { Button } from '@/shared/ui/button';

export function AppLayout() {
  const { isAuthenticated, setToken } = useAuth();

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 border-b bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <Link to="/menu" className="text-lg font-bold text-blue-600">
            FoodExpress
          </Link>
          <nav className="flex items-center gap-4 text-sm">
            <NavLink to="/menu">Menu</NavLink>
            <NavLink to="/cart" className="flex items-center gap-1">
              <ShoppingCart className="h-4 w-4" /> Cart
            </NavLink>
            <NavLink to="/checkout">Checkout</NavLink>
            <NavLink to="/admin/menu">Admin</NavLink>
            {isAuthenticated ? (
              <Button variant="outline" onClick={() => setToken(null)}>
                Logout
              </Button>
            ) : (
              <NavLink to="/login">Login</NavLink>
            )}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}
