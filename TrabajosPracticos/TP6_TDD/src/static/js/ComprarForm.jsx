const { useState } = React;

const ComprarForm = () => {
    const [formData, setFormData] = useState({
        fecha_visita: '',
        email: '',
        forma_pago: '',
        personas: [{ edad: '', tipo_pase: 'Regular' }]
    });

    const [loading, setLoading] = useState(false);
    const [resultado, setResultado] = useState(null);
    const [error, setError] = useState('');

    // Fechas mínima y máxima (igual que tu lógica actual)
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    const maxDate = new Date(today);
    maxDate.setDate(today.getDate() + 30);

    const formatDate = (date) => date.toISOString().split('T')[0];

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handlePersonaChange = (index, field, value) => {
        const newPersonas = [...formData.personas];
        newPersonas[index][field] = value;
        setFormData({ ...formData, personas: newPersonas });
    };

    const agregarPersona = () => {
        if (formData.personas.length >= 10) {
            alert('Máximo 10 entradas por compra');
            return;
        }
        setFormData({
            ...formData,
            personas: [...formData.personas, { edad: '', tipo_pase: 'Regular' }]
        });
    };

    const eliminarPersona = (index) => {
        if (formData.personas.length <= 1) {
            alert('Debe haber al menos una persona');
            return;
        }
        const newPersonas = formData.personas.filter((_, i) => i !== index);
        setFormData({ ...formData, personas: newPersonas });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const requestData = {
                fecha_visita: formData.fecha_visita,
                email: formData.email,
                forma_pago: formData.forma_pago,
                edades: formData.personas.map(p => parseInt(p.edad)),
                tipos_pase: formData.personas.map(p => p.tipo_pase)
            };

            const response = await fetch('/api/comprar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            if (data.success) {
                setResultado(data.resultado);
            } else {
                setError(data.error || 'Error en la compra');
            }
        } catch (err) {
            setError('Error de conexión: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    // Si hay resultado exitoso, mostrar confirmación
    if (resultado) {
        return React.createElement('div', {
            style: {
                backgroundColor: '#3da35d',
                color: '#e8fccf', 
                padding: '20px', 
                borderRadius: '8px',
                margin: '20px 0',
                border: '2px solid #134611'
            }
        }, [
            React.createElement('h3', { key: 'title' }, '✅ ¡Compra Confirmada!'),
            React.createElement('p', { key: 'status' }, `Estado: ${resultado.status}`),
            React.createElement('p', { key: 'fecha' }, `Fecha de Visita: ${resultado.fecha}`),
            React.createElement('p', { key: 'cantidad' }, `Cantidad: ${resultado.cantidad} entradas`),
            React.createElement('p', { key: 'total' }, `Total: $${resultado.total_pagado.toLocaleString()}`),
            React.createElement('p', { key: 'email' }, `Email: ${resultado.email}`),
            React.createElement('button', {
                key: 'nuevo',
                style: { backgroundColor: '#3e8914', color: '#e8fccf', padding: '10px 20px', border: 'none', borderRadius: '4px', margin: '10px 5px', cursor: 'pointer' },
                onClick: () => { setResultado(null); setFormData({ fecha_visita: '', email: '', forma_pago: '', personas: [{ edad: '', tipo_pase: 'Regular' }] }); }
            }, '🎫 Nueva Compra'),
            React.createElement('a', { 
                key: 'inicio', 
                href: '/'
            }, React.createElement('button', {
                style: { backgroundColor: '#134611', color: '#e8fccf', padding: '10px 20px', border: 'none', borderRadius: '4px', margin: '10px 5px', cursor: 'pointer' }
            }, '🏠 Inicio'))
        ]);
    }

    return React.createElement('form', { onSubmit: handleSubmit }, [
        // Fecha de visita
        React.createElement('div', { key: 'fecha-div', style: { margin: '20px 0' } }, [
            React.createElement('label', { 
                key: 'fecha-label',
                style: { color: '#3e8914', fontWeight: 'bold', display: 'block' }
            }, 'Fecha de Visita:'),
            React.createElement('input', {
                key: 'fecha-input',
                type: 'date',
                name: 'fecha_visita',
                value: formData.fecha_visita,
                onChange: handleInputChange,
                required: true,
                min: formatDate(tomorrow),
                max: formatDate(maxDate),
                style: { padding: '8px', margin: '5px', border: '1px solid #3da35d', borderRadius: '4px', backgroundColor: '#e8fccf', color: '#134611' }
            })
        ]),

        // Email
        React.createElement('div', { key: 'email-div', style: { margin: '20px 0' } }, [
            React.createElement('label', { 
                key: 'email-label',
                style: { color: '#3e8914', fontWeight: 'bold', display: 'block' }
            }, 'Email:'),
            React.createElement('input', {
                key: 'email-input',
                type: 'email',
                name: 'email',
                value: formData.email,
                onChange: handleInputChange,
                placeholder: 'tu@email.com',
                required: true,
                style: { padding: '8px', margin: '5px', border: '1px solid #3da35d', borderRadius: '4px', backgroundColor: '#e8fccf', color: '#134611' }
            })
        ]),

        // Forma de pago
        React.createElement('div', { key: 'pago-div', style: { margin: '20px 0' } }, [
            React.createElement('label', { 
                key: 'pago-label',
                style: { color: '#3e8914', fontWeight: 'bold', display: 'block' }
            }, 'Forma de Pago:'),
            React.createElement('select', {
                key: 'pago-select',
                name: 'forma_pago',
                value: formData.forma_pago,
                onChange: handleInputChange,
                required: true,
                style: { padding: '8px', margin: '5px', border: '1px solid #3da35d', borderRadius: '4px', backgroundColor: '#e8fccf', color: '#134611' }
            }, [
                React.createElement('option', { key: 'empty', value: '' }, 'Seleccione...'),
                React.createElement('option', { key: 'mp', value: 'MercadoPago' }, 'MercadoPago'),
                React.createElement('option', { key: 'tc', value: 'Tarjeta' }, 'Tarjeta de Crédito'),
                React.createElement('option', { key: 'transf', value: 'Transferencia' }, 'Transferencia')
            ])
        ]),

        // Personas
        React.createElement('div', { key: 'personas-div', style: { margin: '20px 0' } }, [
            React.createElement('h3', { key: 'personas-title', style: { color: '#3e8914' } }, 'Personas'),
            ...formData.personas.map((persona, index) =>
                React.createElement('div', {
                    key: `persona-${index}`,
                    style: { 
                        border: '1.5px solid #3da35d', 
                        padding: '15px', 
                        margin: '10px 0', 
                        borderRadius: '4px', 
                        backgroundColor: '#e8fccf', 
                        color: '#134611' 
                    }
                }, [
                    React.createElement('label', { key: `edad-label-${index}` }, 'Edad: '),
                    React.createElement('input', {
                        key: `edad-${index}`,
                        type: 'number',
                        min: 0,
                        max: 120,
                        value: persona.edad,
                        onChange: (e) => handlePersonaChange(index, 'edad', e.target.value),
                        required: true,
                        style: { padding: '5px', margin: '5px', border: '1px solid #3da35d', borderRadius: '4px' }
                    }),
                    React.createElement('label', { key: `tipo-label-${index}`, style: { marginLeft: '15px' } }, 'Tipo: '),
                    React.createElement('select', {
                        key: `tipo-${index}`,
                        value: persona.tipo_pase,
                        onChange: (e) => handlePersonaChange(index, 'tipo_pase', e.target.value),
                        required: true,
                        style: { padding: '5px', margin: '5px', border: '1px solid #3da35d', borderRadius: '4px' }
                    }, [
                        React.createElement('option', { key: 'regular', value: 'Regular' }, 'Regular ($5,000)'),
                        React.createElement('option', { key: 'vip', value: 'VIP' }, 'VIP ($10,000)')
                    ]),
                    formData.personas.length > 1 ? React.createElement('button', {
                        key: `eliminar-${index}`,
                        type: 'button',
                        onClick: () => eliminarPersona(index),
                        style: { backgroundColor: '#3e8914', color: '#e8fccf', padding: '5px 10px', border: 'none', borderRadius: '4px', marginLeft: '15px', cursor: 'pointer' }
                    }, 'Eliminar') : null
                ])
            ),
            React.createElement('div', { key: 'controles-personas' }, [
                React.createElement('button', {
                    key: 'agregar',
                    type: 'button',
                    onClick: agregarPersona,
                    style: { backgroundColor: '#3e8914', color: '#e8fccf', padding: '10px 20px', border: 'none', borderRadius: '4px', margin: '10px 5px', cursor: 'pointer' }
                }, '➕ Agregar Persona'),
                React.createElement('span', {
                    key: 'contador',
                    style: { marginLeft: '10px', color: '#134611' }
                }, `Personas: ${formData.personas.length}/10`)
            ])
        ]),

        // Error
        error ? React.createElement('div', {
            key: 'error',
            style: { backgroundColor: '#3e8914', color: '#e8fccf', padding: '15px', borderRadius: '4px', margin: '10px 0', border: '2px solid #134611' }
        }, `❌ ${error}`) : null,

        // Botones
        React.createElement('div', { key: 'botones', style: { textAlign: 'center', margin: '30px 0' } }, [
            React.createElement('button', {
                key: 'submit',
                type: 'submit',
                disabled: loading,
                style: { 
                    fontSize: '16px', 
                    padding: '15px 30px', 
                    backgroundColor: loading ? '#96e072' : '#3e8914', 
                    color: '#e8fccf',
                    border: 'none',
                    borderRadius: '4px',
                    margin: '5px',
                    cursor: loading ? 'not-allowed' : 'pointer'
                }
            }, loading ? '⏳ Procesando...' : '💳 Procesar Compra'),
            React.createElement('a', { 
                key: 'volver', 
                href: '/'
            }, React.createElement('button', {
                type: 'button',
                style: { backgroundColor: '#134611', color: '#e8fccf', padding: '15px 30px', border: 'none', borderRadius: '4px', margin: '5px', cursor: 'pointer' }
            }, '🔙 Volver'))
        ])
    ]);
};

// Renderizar el componente
ReactDOM.render(React.createElement(ComprarForm), document.getElementById('react-comprar-form'));