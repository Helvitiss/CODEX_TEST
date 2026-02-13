import { Navigate, createBrowserRouter } from 'react-router-dom';
import { AppLayout } from '@/widgets/layout/AppLayout';
import { AdminMenuPage } from '@/pages/AdminMenuPage';
import { AdminOrdersPage } from '@/pages/AdminOrdersPage';
import { CartPage } from '@/pages/CartPage';
import { CheckoutPage } from '@/pages/CheckoutPage';
import { LoginPage } from '@/pages/LoginPage';
import { MenuPage } from '@/pages/MenuPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/menu" replace /> },
      { path: '/menu', element: <MenuPage /> },
      { path: '/cart', element: <CartPage /> },
      { path: '/checkout', element: <CheckoutPage /> },
      { path: '/login', element: <LoginPage /> },
      { path: '/admin/menu', element: <AdminMenuPage /> },
      { path: '/admin/orders', element: <AdminOrdersPage /> }
    ]
  }
]);
