import { Navigate, Link } from "react-router-dom";
import "./css/ProtectedRoute.css";

export default function ProtectedRoute({ user, children }) {
  // Si está autenticado, renderiza la página normalmente
  if (user?.isAuthenticated) {
    return children;
  }

  // Si no está autenticado, muestra mensaje personalizado
  return (
    <div className="protected-container">
      <div className="protected-box">
        <h2>🚫 Acceso restringido</h2>
        <p>
          No es posible ingresar si no se encuentra registrado.
          <br />
          Por favor, inicie sesión para continuar.
        </p>

        <Link to="/login" className="login-btn">
          Iniciar sesión
        </Link>
      </div>
    </div>
  );
}
