import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./css/Login.css"; // reutilizamos los mismos estilos que Login

export default function Register({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleRegister(e) {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden");
      return;
    }

    try {
      const res = await fetch("http://localhost:5000/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      if (!data.success) throw new Error(data.error || "Error en el registro");

      localStorage.setItem("token", data.token);
      setUser({ isAuthenticated: true, email: data.user.email });
      navigate("/");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Crear nueva cuenta</h2>
        <form onSubmit={handleRegister}>
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

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirmar contraseña</label>
            <input
              id="confirmPassword"
              type="password"
              placeholder="********"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="login-btn">
            Registrarse
          </button>
        </form>

        {error && <div className="error-msg">{error}</div>}

        <p className="register-text">
          ¿Ya tenés una cuenta?{" "}
          <Link to="/login" className="register-link">
            Iniciar sesión
          </Link>
        </p>
      </div>
    </div>
  );
}
