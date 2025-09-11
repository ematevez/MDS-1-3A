function dividir(a, b) {
    return a / b; // ERROR: no valida división por cero
}
console.log(dividir(4, 0)); // Debería manejar el error
