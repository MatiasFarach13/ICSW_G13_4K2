import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./css/ConfirmacionEfectivo.css";

export default function ConfirmacionEfectivo() {
  const [compra, setCompra] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem("compraPendiente");
    if (stored) {
      setCompra(JSON.parse(stored));
    } else {
      navigate("/comprar");
    }
  }, []);

  const calcularPrecio = (tipo) => (tipo === "VIP" ? 10000 : 5000);

  const total =
    compra?.participantes.reduce(
      (sum, p) => sum + calcularPrecio(p.tipoPase),
      0
    ) || 0;

  return (
    <div className="efectivo-container">
      <div className="efectivo-card">
        <h2>🎉 ¡Gracias por tu compra!</h2>
        <p className="mensaje">
          Hemos enviado un correo de confirmación con los detalles de tu visita a EcoHarmonyPark 🌳
        </p>
        <p className="fecha">📅 Fecha de visita: {compra?.fecha_visita}</p>

        <div className="resumen">
          <h3>🎟️ Entradas adquiridas</h3>
          <ul>
            {compra?.participantes.map((p, idx) => (
              <li key={idx}>
                <span>{p.tipoPase}</span>
                <span className="precio">${calcularPrecio(p.tipoPase)}</span>
              </li>
            ))}
          </ul>

          <div className="total">
            <strong>Total a abonar en boletería:</strong> <span>${total}</span>
          </div>
        </div>

        <button
          onClick={() => {
            localStorage.removeItem("compraPendiente");
            navigate("/");
          }}
          className="btn-volver"
        >
          🏡 Volver al inicio
        </button>
      </div>
    </div>
  );
}
