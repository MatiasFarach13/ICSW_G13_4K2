import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import "./css/BaseLayout.css";

export default function BaseLayout({ children, user, setUser }) {
  const navigate = useNavigate();
  const location = useLocation();

  function handleLogout() {
    localStorage.removeItem("token");
    setUser(null);
    navigate("/login");
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🎢 Ecoharmonypark - Sistema de Entradas</h1>

        {/* Barra de navegación visible y horizontal */}
        <nav className="navbar">
          <Link
            to="/"
            className={location.pathname === "/" ? "active" : ""}
          >
            Inicio
          </Link>
          <Link
            to="/comprar"
            className={location.pathname === "/comprar" ? "active" : ""}
          >
            Comprar Entradas
          </Link>

          {user?.isAuthenticated ? (
            <button className="logout-btn" onClick={handleLogout}>
              Cerrar sesión
            </button>
          ) : (
            <Link
              to="/login"
              className={location.pathname === "/login" ? "active" : ""}
            >
              Iniciar sesión
            </Link>
          )}
        </nav>
      </header>

      <main className="container">{children}</main>
    </div>
  );
}
