document.getElementById('clasificar-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nombreCuenta = document.getElementById('nombre-cuenta').value;
    const resultadoDiv = document.getElementById('resultado');
    
    // Mostrar un indicador de carga
    resultadoDiv.innerHTML = '<p>Clasificando cuenta...</p>';
    resultadoDiv.style.display = 'block';
    
    fetch('/clasificar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({nombre_cuenta: nombreCuenta}),
    })
    .then(response => response.json())
    .then(data => {
        resultadoDiv.innerHTML = `
            <h2>Resultado para: ${data.nombre_cuenta}</h2>
            <p><strong>Naturaleza:</strong> ${data.naturaleza}</p>
            <p><strong>Libros:</strong> ${data.libros.join(', ')}</p>
            <p><strong>Descripción:</strong> ${data.descripcion}</p>
            <p><strong>Fuente:</strong> ${data.fuente}</p>
            <p><strong>Confianza:</strong> ${data.confianza}</p>
            <h3>Cuentas similares:</h3>
            <ul>
                ${data.similar_accounts.map(account => `<li>${account['Nombre de la cuenta']}</li>`).join('')}
            </ul>
        `;
        resultadoDiv.style.display = 'block';
    })
    .catch((error) => {
        console.error('Error:', error);
        resultadoDiv.innerHTML = '<p>Ocurrió un error al clasificar la cuenta. Por favor, intenta de nuevo.</p>';
        resultadoDiv.style.display = 'block';
    });
});