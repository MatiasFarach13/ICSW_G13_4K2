import { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import BaseLayout from "./components/BaseLayout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Comprar from "./pages/Comprar";
import ProtectedRoute from "./pages/ProtectedRoute";

export default function App() {
  const [user, setUser] = useState(null);

  // ✅ Al montar la app, verificamos si hay token guardado
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setUser({ isAuthenticated: true });
    } else {
      setUser({ isAuthenticated: false });
    }
  }, []);

  return (
    <Router>
      <BaseLayout user={user} setUser={setUser}>
        <Routes>
          {/* 🔐 Ruta raíz: si no está autenticado, redirige a /login */}
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

          {/* 🧾 Login y registro */}
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/register" element={<Register setUser={setUser} />} />

          {/* 🎟️ Página protegida */}
          <Route
            path="/comprar"
            element={
              <ProtectedRoute user={user}>
                <Comprar />
              </ProtectedRoute>
            }
          />

          {/* 🚧 Rutas no válidas → redirige al login */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BaseLayout>
    </Router>
  );
}
