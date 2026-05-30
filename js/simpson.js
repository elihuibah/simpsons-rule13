document.addEventListener('DOMContentLoaded', () => {
    const btnCalcular = document.getElementById('btn-calcular');
    const resultsArea = document.getElementById('results-area');

    btnCalcular.addEventListener('click', () => {
        //Captura de valores de los inputs
        const funcion = document.getElementById('funcion').value;
        const a = parseFloat(document.getElementById('limite-a').value);
        const b = parseFloat(document.getElementById('limite-b').value);
        const n = parseInt(document.getElementById('n-intervalos').value);

        //Validación
        if (!funcion || isNaN(a) || isNaN(b) || isNaN(n)) {
            alert("Por favor, completa todos los campos correctamente.");
            return;
        }

        if (n % 2 !== 0) {
            alert("El valor de 'n' debe ser un número par para el método de Simpson 1/3.");
            return;
        }

        //ESTO ES Simulación de procesamiento (Aquí iría la lógica matemática)
        console.log(`Procesando f(x)=${funcion} de ${a} a ${b} con n=${n}`);

        //Mostrar el área de resultados
        resultsArea.style.display = 'block';
    });
});