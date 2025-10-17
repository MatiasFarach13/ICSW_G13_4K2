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
  limite.setDate(hoy.getDate() + 31);
  const limiteISO = limite.toISOString().split("T")[0];

  const handleFechaChange = (e) => {
    const iso = e.target.value;
    if (!iso) return;

    const seleccionada = new Date(iso);
    const diaSemana = seleccionada.getDay();
    setFechaVisita(iso);

    if (seleccionada < hoy) {
      setErrorFecha("❌ No se pueden comprar entradas para fechas pasadas.");
      return;
    }
    if (seleccionada > limite) {
      setErrorFecha("⚠️ Solo se permiten compras hasta 31 días a futuro.");
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

  async function handleCompra(e) {
    e.preventDefault();

    if (!fechaVisita || errorFecha) {
      setError("Debe seleccionar una fecha válida.");
      return;
    }

    if (participantes.length === 0) {
      setError("Debe agregar al menos un participante.");
      return;
    }

    const compra = {
      fecha_visita: fechaFormateada,
      participantes,
      forma_pago: formaPago,
    };

    localStorage.setItem("compraPendiente", JSON.stringify(compra));

    if (formaPago === "Tarjeta") {
      navigate("/confirmar-compra");
    } else {
      navigate("/confirmacion-efectivo");
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

          {participantes.map((p) => (
            <div key={p.id} className="card-participante">
              <div className="participante-header">
                <h4>Participante #{participantes.indexOf(p) + 1}</h4>
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
