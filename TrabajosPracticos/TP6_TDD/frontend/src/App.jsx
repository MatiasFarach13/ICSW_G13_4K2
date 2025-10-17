import { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import BaseLayout from "./components/BaseLayout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Comprar from "./pages/Comprar";
import ProtectedRoute from "./pages/ProtectedRoute";
import ConfirmarCompra from "./pages/ConfirmarCompra";
import ConfirmacionEfectivo from "./pages/ConfirmacionEfectivo";
import ConfirmacionTarjeta from "./pages/ConfirmacionTarjeta";

export default function App() {
  const [user, setUser] = useState(null);

  // ✅ Al montar la app, verificamos si hay token guardado
  useEffect(() => {
    const token = localStorage.getItem("token");
    const userData = localStorage.getItem("user");

    if (token && userData) {
      const parsedUser = JSON.parse(userData);
      setUser({ isAuthenticated: true, email: parsedUser.email });
    } else {
      setUser({ isAuthenticated: false });
    }
  }, []);

  return (
    <Router>
      <BaseLayout user={user} setUser={setUser}>
        <Routes>
          {/* 🏠 Página principal (redirige al login si no está autenticado) */}
          <Route
            path="/"
            element={
              user?.isAuthenticated ? (
                <Home />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* 🔐 Login y registro */}
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/register" element={<Register setUser={setUser} />} />

          {/* 🎟️ Comprar entradas (solo si está autenticado) */}
          <Route
            path="/comprar"
            element={
              <ProtectedRoute user={user}>
                <Comprar />
              </ProtectedRoute>
            }
          />

          {/* Simulacion mercado pago */}
          <Route path="/confirmar-compra" element={<ConfirmarCompra />} />

          {/* 💵 Confirmación de pago en efectivo */}
          <Route path="/confirmacion-efectivo" element={<ConfirmacionEfectivo />} />

          {/* 💚 Confirmación de pago con tarjeta */}
          <Route path="/confirmacion-tarjeta" element={<ConfirmacionTarjeta />} />

          {/* 🚧 Rutas no válidas → redirige al login */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BaseLayout>
    </Router>
  );
}
