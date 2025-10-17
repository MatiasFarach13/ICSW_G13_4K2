import { useState } from "react";

export default function Comprar() {
  const [fechaVisita, setFechaVisita] = useState("");
  const [edades, setEdades] = useState("");
  const [tiposPase, setTiposPase] = useState("");
  const [formaPago, setFormaPago] = useState("Efectivo");
  const [mensaje, setMensaje] = useState(null);
  const [error, setError] = useState(null);

  async function handleCompra(e) {
    e.preventDefault();
    setError(null);
    setMensaje(null);

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("Debe iniciar sesión antes de comprar.");
        return;
      }

      // Parsear edades y tipos de pase como listas
      const edadesLista = edades.split(",").map((n) => parseInt(n.trim()));
      const tiposLista = tiposPase.split(",").map((t) => t.trim());

      const res = await fetch("http://localhost:5000/api/comprar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          fecha_visita: fechaVisita,
          edades: edadesLista,
          tipos_pase: tiposLista,
          forma_pago: formaPago,
          email: "usuario@gmail.com", // Podés sacar esto del JWT o de user.email
        }),
      });

      const data = await res.json();
      if (!data.success) throw new Error(data.error || "Error en la compra");

      setMensaje(`✅ Compra realizada con éxito. Total pagado: $${data.resultado.total_pagado}
      (${data.resultado.instrucciones_pago})`);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="container">
      <h2>🎟️ Comprar Entradas</h2>
      <form onSubmit={handleCompra}>
        <label>
          Fecha de visita:
          <input
            type="date"
            value={fechaVisita}
            onChange={(e) => setFechaVisita(e.target.value)}
            required
          />
        </label>

        <label>
          Edades (separadas por coma):
          <input
            type="text"
            placeholder="Ej: 25, 30"
            value={edades}
            onChange={(e) => setEdades(e.target.value)}
            required
          />
        </label>

        <label>
          Tipos de pase (separados por coma):
          <input
            type="text"
            placeholder="Ej: VIP, General"
            value={tiposPase}
            onChange={(e) => setTiposPase(e.target.value)}
            required
          />
        </label>

        <label>
          Forma de pago:
          <select
            value={formaPago}
            onChange={(e) => setFormaPago(e.target.value)}
          >
            <option value="Efectivo">Efectivo</option>
            <option value="Tarjeta">Tarjeta</option>
          </select>
        </label>

        <button type="submit">Comprar</button>
      </form>

      {mensaje && <div className="success">{mensaje}</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
}
