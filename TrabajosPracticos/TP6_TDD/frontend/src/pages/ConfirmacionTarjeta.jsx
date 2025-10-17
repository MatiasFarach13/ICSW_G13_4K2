import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./css/ConfirmacionTarjeta.css";

export default function ConfirmacionTarjeta() {
  const [compra, setCompra] = useState(null);
  const [usuario, setUsuario] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedCompra = localStorage.getItem("compraPendiente");
    const storedUser = localStorage.getItem("user");

    if (storedCompra) {
      setCompra(JSON.parse(storedCompra));
    } else {
      navigate("/comprar");
    }

    if (storedUser) {
      setUsuario(JSON.parse(storedUser));
    }
  }, []);

  const calcularPrecio = (tipo) => (tipo === "VIP" ? 10000 : 5000);
  const total =
    compra?.participantes.reduce(
      (sum, p) => sum + calcularPrecio(p.tipoPase),
      0
    ) || 0;

  return (
    <div className="confirmacion-container">
      <div className="confirmacion-card">
        <h2>💚 ¡Pago exitoso!</h2>
        <p className="mensaje">
          Tu compra fue procesada correctamente. En breve recibirás un correo
          con todos los detalles de tu visita a <b>EcoHarmonyPark</b>.
        </p>

        <div className="resumen">
          <h3>🎟️ Resumen de la compra</h3>
          <ul>
            <li>
              <strong>Fecha de visita:</strong> {compra?.fecha_visita}
            </li>
            <li>
              <strong>Cantidad de entradas:</strong>{" "}
              {compra?.participantes.length}
            </li>
            <li>
              <strong>Monto total:</strong> ${total}
            </li>
            <li>
              <strong>Correo de confirmación:</strong>{" "}
              <span className="email">{usuario?.email}</span>
            </li>
          </ul>
        </div>

        <div className="icono-gracias">🌱</div>
        <p className="gracias">¡Gracias por elegirnos!</p>

        <button
          className="btn-volver"
          onClick={() => {
            localStorage.removeItem("compraPendiente");
            navigate("/");
          }}
        >
          🏡 Volver al inicio
        </button>
      </div>
    </div>
  );
}
