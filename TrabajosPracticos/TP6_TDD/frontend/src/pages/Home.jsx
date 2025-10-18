import { useEffect, useState } from "react";
import "./css/Home.css";

const imagenes = [
  "/assets/Leon.jpg",
  "/assets/Jirafa.jpg",
  "/assets/Mono.jpg",
  "/assets/Flamencos.jpeg",
  "/assets/Tortuga.jpg",
];

export default function Home() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % imagenes.length);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="home-container">
      <div className="home-hero">
        <img
          src={imagenes[index]}
          alt="Animal del parque"
          className="home-imagen"
        />
        <div className="overlay">
          <h1 className="titulo">Bienvenido a EcoHarmony Park 🌿</h1>
          <p className="subtitulo">
            Un bioparque dedicado al equilibrio entre naturaleza, tecnología y educación ambiental.
          </p>
        </div>
      </div>

      <section className="descripcion">
        <h2>Sobre EcoHarmony Park</h2>
        <p>
          EcoHarmony Park es un bioparque que busca conectar a las personas con
          la naturaleza a través de experiencias únicas. Los visitantes pueden
          recorrer senderos naturales, conocer animales terrestres, acuáticos y
          aéreos, asistir a horarios de alimentación y participar en actividades
          recreativas como tirolesa, safari o jardinería.
        </p>
      </section>

      <section className="cta">
        <h3>🌎 Viví la experiencia EcoHarmony</h3>
        <p>
          Descubrí un espacio donde la naturaleza y la tecnología se unen para
          brindarte una aventura educativa, segura y sustentable.
        </p>
        <a href="/comprar" className="btn-comprar">
          🎟️ Comprar entradas
        </a>
      </section>
    </div>
  );
}
