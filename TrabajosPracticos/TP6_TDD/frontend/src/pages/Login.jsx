import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./css/Login.css";

export default function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);

    try {
      const res = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      if (!data.success) throw new Error(data.error || "Error al iniciar sesión");

      // 🔹 Limpiamos cualquier sesión previa
      localStorage.removeItem("token");
      localStorage.removeItem("user");

      // 🔹 Guardamos token y datos del usuario actual
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));

      // 🔹 Actualizamos estado global (si lo usás en App)
      setUser({ isAuthenticated: true, email: data.user.email });

      // 🔹 Redirigimos al inicio
      navigate("/");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Iniciar sesión</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Correo electrónico</label>
            <input
              id="email"
              type="email"
              placeholder="ejemplo@gmail.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              placeholder="********"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="login-btn">
            Entrar
          </button>
        </form>

        {error && <div className="error-msg">{error}</div>}

        <p className="register-text">
          ¿No estás registrado?{" "}
          <Link to="/register" className="register-link">
            Crear una cuenta
          </Link>
        </p>
      </div>
    </div>
  );
}
