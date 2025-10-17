import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./css/ConfirmarCompra.css";

export default function ConfirmarCompra() {
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

  if (!compra) return null;

  return (
    <div className="confirmar-container">
      <div className="confirmar-card">
        <h2>💰 Confirmar compra</h2>
        <p className="fecha-visita">📅 Fecha de visita: {compra.fecha_visita}</p>

        <div className="resumen">
          <h3>🎟️ Entradas</h3>
          <ul>
            {compra.participantes.map((p, idx) => (
              <li key={idx}>
                <span>{p.tipoPase}</span>
                <span className="precio">${calcularPrecio(p.tipoPase)}</span>
              </li>
            ))}
          </ul>

          <div className="total">
            <strong>Total:</strong> <span>${total}</span>
          </div>
        </div>

        <button onClick={() => navigate("/confirmacion-tarjeta")} className="btn-pagar">
          💳 Pagar con MercadoPago
        </button>

        <button onClick={() => navigate("/comprar")} className="btn-volver">
          ← Volver
        </button>
      </div>
    </div>
  );
}
