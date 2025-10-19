import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./css/ConfirmarCompra.css";

export default function ConfirmarCompra() {
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
    const fechaVisita =
      compra.fecha_visita || compra.fecha || compra.fechaFormateada;

    if (!fechaVisita) {
      setErrorMsg("❌ Faltan datos de la compra. Volvé a intentarlo.");
      setLoading(false);
      return;
    }

    setFecha(fechaVisita);

    const token = localStorage.getItem("token");
    const participantes = compra.participantes || [];

    // 🔄 Pedir al backend el cálculo actualizado (descuentos incluidos)
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
          setErrorMsg("⚠️ No se pudo obtener el detalle de la compra.");
        }
      })
      .catch((err) => {
        console.error("❌ Error en fetch:", err);
        setErrorMsg("Error al comunicarse con el servidor.");
      })
      .finally(() => setLoading(false));
  }, [navigate]);

  // --- Estados de carga o error ---
  if (loading) {
    return (
      <div className="confirmar-container">
        <p className="cargando">Calculando precios y descuentos...</p>
      </div>
    );
  }

  if (errorMsg) {
    return (
      <div className="confirmar-container">
        <div className="confirmar-card">
          <h2>⚠️ Error</h2>
          <p>{errorMsg}</p>
          <button className="btn-volver" onClick={() => navigate("/comprar")}>
            🔄 Volver a intentar
          </button>
        </div>
      </div>
    );
  }

  // --- Pantalla final ---
  return (
    <div className="confirmar-container">
      <div className="confirmar-card">
        <h2>💰 Confirmar compra</h2>
        <p className="fecha-visita">📅 Fecha de visita: {fecha}</p>

        <div className="resumen">
          <h3>🎟️ Entradas con descuentos aplicados</h3>
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
            <strong>Total a pagar:</strong> <span>${total}</span>
          </div>
        </div>

        <button
          onClick={() => navigate("/confirmacion-tarjeta")}
          className="btn-pagar"
        >
          💳 Pagar con MercadoPago
        </button>

        <button onClick={() => navigate("/comprar")} className="btn-volver">
          ← Volver
        </button>
      </div>
    </div>
  );
}
