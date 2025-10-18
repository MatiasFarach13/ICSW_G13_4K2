import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./css/ConfirmacionEfectivo.css";

export default function ConfirmacionEfectivo() {
  const [detalleCompra, setDetalleCompra] = useState([]);
  const [total, setTotal] = useState(0);
  const [fecha, setFecha] = useState("");
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem("compraPendiente");
    if (!stored) {
      navigate("/comprar");
      return;
    }

    const compra = JSON.parse(stored);

    // 🧠 Aseguramos que el campo exista con el nombre correcto
    const fechaVisita =
      compra.fecha_visita || compra.fecha || compra.fechaFormateada;

    if (!fechaVisita) {
      console.error("❌ No se encontró fecha_visita en la compra guardada.");
      setErrorMsg("Faltan datos de la compra. Volvé a intentarlo.");
      setLoading(false);
      return;
    }

    setFecha(fechaVisita);

    const token = localStorage.getItem("token");
    const participantes = compra.participantes || [];

    // 🧩 Si ya tenemos los precios calculados (p.ej. tras pago con tarjeta), no se hace fetch
    if (compra.resultado?.detalle) {
      setDetalleCompra(compra.resultado.detalle);
      setTotal(compra.resultado.total_pagado);
      setLoading(false);
      return;
    }

    // 🔄 Consultar backend para obtener los precios y descuentos actualizados
    fetch("http://localhost:5000/api/comprar-detalle", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: token ? `Bearer ${token}` : "",
      },
      body: JSON.stringify({
        fecha_visita: fechaVisita, // 👈 aseguramos que el backend reciba esta clave
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
          console.error("❌ Error al obtener detalle:", data.error);
          setErrorMsg("No se pudo obtener el detalle de la compra.");
        }
      })
      .catch((err) => {
        console.error("Error en fetch:", err);
        setErrorMsg("Error al comunicarse con el servidor.");
      })
      .finally(() => setLoading(false));
  }, [navigate]);

  // 🕒 Estado de carga
  if (loading) {
    return (
      <div className="efectivo-container">
        <p className="cargando">Cargando detalle de tu compra...</p>
      </div>
    );
  }

  // ⚠️ Error amigable en pantalla
  if (errorMsg) {
    return (
      <div className="efectivo-container">
        <div className="efectivo-card">
          <h2>⚠️ Ocurrió un problema</h2>
          <p>{errorMsg}</p>
          <button
            className="btn-volver"
            onClick={() => navigate("/comprar")}
          >
            🔄 Volver a intentar
          </button>
        </div>
      </div>
    );
  }

  // 🎟️ Pantalla de confirmación final
  return (
    <div className="efectivo-container">
      <div className="efectivo-card">
        <h2>🎉 ¡Gracias por tu compra!</h2>
        <p className="mensaje">
          Hemos enviado un correo de confirmación con los detalles de tu visita
          a EcoHarmonyPark 🌳
        </p>

        <p className="fecha">📅 Fecha de visita: {fecha}</p>

        <div className="resumen">
          <h3>🎟️ Entradas adquiridas</h3>
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
