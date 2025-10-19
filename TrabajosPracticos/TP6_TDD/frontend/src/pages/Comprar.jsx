import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./css/Comprar.css";

export default function Comprar() {
  const [fechaVisita, setFechaVisita] = useState("");
  const [fechaFormateada, setFechaFormateada] = useState("");
  const [errorFecha, setErrorFecha] = useState("");
  const [participantes, setParticipantes] = useState([]);
  const [formaPago, setFormaPago] = useState("Efectivo");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const maxParticipantes = 10;
  const hoy = new Date();
  const hoyISO = hoy.toISOString().split("T")[0];
  const limite = new Date();
  limite.setDate(hoy.getDate() + 30);
  const limiteISO = limite.toISOString().split("T")[0];

  // --- Manejo de fecha ---
  const handleFechaChange = (e) => {
    const iso = e.target.value;
    if (!iso) return;

    // ✅ Ajuste local
    const [year, month, day] = iso.split("-").map(Number);
    const seleccionada = new Date(year, month - 1, day);
    const diaSemana = seleccionada.getDay(); // 0=domingo, 1=lunes...

    setFechaVisita(iso);

    if (seleccionada < hoy) {
      setErrorFecha("❌ No se pueden comprar entradas para fechas pasadas.");
      return;
    }
    if (seleccionada > limite) {
      setErrorFecha("⚠️ Solo se permiten compras hasta 30 días a futuro.");
      return;
    }
    if (diaSemana === 1) {
      setErrorFecha("🚫 El parque no abre los lunes.");
      return;
    }

    setErrorFecha("");
    const [yyyy, mm, dd] = iso.split("-");
    setFechaFormateada(`${dd}/${mm}/${yyyy}`);
  };

  // --- Participantes ---
  const agregarParticipante = () => {
    if (participantes.length >= maxParticipantes) return;
    setParticipantes([
      ...participantes,
      { id: Date.now(), edad: "", tipoPase: "Regular" },
    ]);
  };

  const actualizarParticipante = (id, campo, valor) => {
    setParticipantes(
      participantes.map((p) =>
        p.id === id ? { ...p, [campo]: valor } : p
      )
    );
  };

  const quitarParticipante = (id) => {
    if (window.confirm("¿Está seguro que desea eliminar este participante?")) {
      setParticipantes(participantes.filter((p) => p.id !== id));
    }
  };

  // --- Confirmar compra ---
  async function handleCompra(e) {
    e.preventDefault();
    setError(null);

    if (!fechaVisita || errorFecha) {
      setError("Debe seleccionar una fecha válida.");
      return;
    }
    if (participantes.length === 0) {
      setError("Debe agregar al menos un participante.");
      return;
    }

    const token = localStorage.getItem("token");
    const userData = JSON.parse(localStorage.getItem("user"));
    const email = userData?.email || "sin_email@ejemplo.com";

    const edadesLista = participantes.map((p) => parseInt(p.edad, 10));
    const tiposLista = participantes.map((p) => p.tipoPase);

    const body = {
      fecha_visita: fechaVisita, // formato ISO
      edades: edadesLista,
      tipos_pase: tiposLista,
      forma_pago: formaPago,
      email: email,
    };

    try {
      const res = await fetch("http://localhost:5000/api/comprar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      if (!data.success) throw new Error(data.error || "Error en la compra");

      // Guardamos la compra en localStorage (para la pantalla de resumen)
      // Guardamos la compra en localStorage con los participantes
      localStorage.setItem(
        "compraPendiente",
        JSON.stringify({
          ...data.resultado, // lo que devuelve el backend
          participantes,     // edades y tipos de pase del usuario
          fecha_visita: fechaVisita, // ISO
        })
      );

      // Redirigimos según forma de pago
      if (formaPago === "Tarjeta") {
        navigate("/confirmar-compra");
      } else {
        navigate("/confirmacion-efectivo");
      }
    } catch (err) {
      console.error("❌ Error al crear la compra:", err);
      setError(err.message);
    }
  }

  return (
    <div className="container">
      <h2>🎟️ Comprar Entradas</h2>
      <form onSubmit={handleCompra}>
        {/* === FECHA === */}
        <label>
          Fecha de visita:
          <input
            type="date"
            value={fechaVisita}
            min={hoyISO}
            max={limiteISO}
            onChange={handleFechaChange}
            required
            className="input-select"
          />
        </label>
        {errorFecha && <p className="error">{errorFecha}</p>}

        {/* === PARTICIPANTES === */}
        <div className="participantes">
          <h3>👥 Participantes</h3>
          <button
            type="button"
            onClick={agregarParticipante}
            className="btn-agregar"
          >
            ➕ Agregar participante
          </button>

          {participantes.map((p, i) => (
            <div key={p.id} className="card-participante">
              <div className="participante-header">
                <h4>Participante #{i + 1}</h4>
              </div>

              <label>
                Edad:
                <input
                  type="number"
                  className="input-edad"
                  value={p.edad}
                  onChange={(e) =>
                    actualizarParticipante(p.id, "edad", e.target.value)
                  }
                  required
                  placeholder="Ej: 25"
                />
              </label>

              <label>
                Tipo de pase:
                <select
                  className="input-select"
                  value={p.tipoPase}
                  onChange={(e) =>
                    actualizarParticipante(p.id, "tipoPase", e.target.value)
                  }
                >
                  <option value="Regular">Regular</option>
                  <option value="VIP">VIP</option>
                </select>
              </label>

              <button
                type="button"
                onClick={() => quitarParticipante(p.id)}
                className="btn-eliminar"
              >
                🗑️ Eliminar
              </button>
            </div>
          ))}
        </div>

        {/* === FORMA DE PAGO === */}
        <div className="forma-pago">
          <h3>💰 Forma de pago</h3>
          <div className="pago-opciones">
            <button
              type="button"
              className={`btn-pago ${formaPago === "Efectivo" ? "activo" : ""}`}
              onClick={() => setFormaPago("Efectivo")}
            >
              💵 Efectivo
            </button>
            <button
              type="button"
              className={`btn-pago ${formaPago === "Tarjeta" ? "activo" : ""}`}
              onClick={() => setFormaPago("Tarjeta")}
            >
              💳 Tarjeta
            </button>
          </div>
        </div>

        {/* === CONFIRMAR COMPRA === */}
        <button type="submit" className="btn-comprar">
          💚 Continuar al pago
        </button>

        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}
