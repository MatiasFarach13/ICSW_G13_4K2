import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./css/ConfirmacionTarjeta.css";

export default function ConfirmacionTarjeta() {
  const [detalleCompra, setDetalleCompra] = useState([]);
  const [total, setTotal] = useState(0);
  const [usuario, setUsuario] = useState(null);
  const [fecha, setFecha] = useState("");
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const storedCompra = localStorage.getItem("compraPendiente");
    const storedUser = localStorage.getItem("user");

    if (!storedCompra) {
      navigate("/comprar");
      return;
    }

    const compra = JSON.parse(storedCompra);
    const fechaVisita =
      compra.fecha_visita || compra.fecha || compra.fechaFormateada;

    if (!fechaVisita) {
      setErrorMsg("Faltan datos de la compra. Volvé a intentarlo.");
      setLoading(false);
      return;
    }

    setFecha(fechaVisita);
    if (storedUser) setUsuario(JSON.parse(storedUser));

    const token = localStorage.getItem("token");
    const participantes = compra.participantes || [];

    // 🔄 Consultar backend para obtener descuentos actualizados
    fetch("http://localhost:5000/api/comprar-detalle", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: token ? `Bearer ${token}` : "",
      },
      body: JSON.stringify({
        fecha_visita: fechaVisita,
        edades: participantes.map((p) => parseInt(p.edad, 10)),
        tipos_pase: participantes.map((p) => p.tipoPase),
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success && data.resultado) {
          setDetalleCompra(data.resultado.detalle || []);
          setTotal(data.resultado.total_pagado || 0);
        } else {
          setErrorMsg("No se pudo obtener el detalle de la compra.");
        }
      })
      .catch((err) => {
        console.error("Error en fetch:", err);
        setErrorMsg("Error al comunicarse con el servidor.");
      })
      .finally(() => setLoading(false));
  }, [navigate]);

  // --- Estado de carga
  if (loading) {
    return (
      <div className="confirmacion-container">
        <p className="cargando">Cargando detalles de tu compra...</p>
      </div>
    );
  }

  // --- Error amigable
  if (errorMsg) {
    return (
      <div className="confirmacion-container">
        <div className="confirmacion-card">
          <h2>⚠️ Ocurrió un problema</h2>
          <p>{errorMsg}</p>
          <button className="btn-volver" onClick={() => navigate("/comprar")}>
            🔄 Volver a intentar
          </button>
        </div>
      </div>
    );
  }

  // --- Pantalla final
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
              <strong>Fecha de visita:</strong> {fecha}
            </li>
            <li>
              <strong>Cantidad de entradas:</strong> {detalleCompra.length}
            </li>
            <li>
              <strong>Monto total:</strong> ${total}
            </li>
            <li>
              <strong>Correo de confirmación:</strong>{" "}
              <span className="email">{usuario?.email}</span>
            </li>
          </ul>

          <h3>🎫 Detalle de entradas</h3>
          <ul>
            {detalleCompra.map((item, idx) => (
              <li key={idx}>
                <span>
                  {item.tipo} ({item.categoria})
                </span>
                <span className="precio">${item.precio}</span>
              </li>
            ))}
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
