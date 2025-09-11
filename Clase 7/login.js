function login(usuario, clave) {
    if (usuario === "admin" && clave === "1234") {
        return false; // ERROR: debe devolver true
    }
    return true;
}
