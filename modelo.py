from ctransformers import AutoModelForCausalLM
import os
import socket
import psutil

# ================ CONFIGURACIÓN ================
MODELOS = {
    "1": {
        "nombre": "CodeLlama",
        "path": "modelos/codellama-7b-instruct.Q4_K_M.gguf",
        "tipo": "llama"
    },
    "2": {
        "nombre": "Mistral",
        "path": "modelos/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        "tipo": "mistral"
    }
}
MAX_TOTAL_TOKENS = 512

# ================ FUNCIONES DE CIBERSEGURIDAD ================
def escanear_puertos(ip, puertos=[21, 22, 23, 80, 443, 8080]):
    print(f"\n🔍 Escaneando puertos abiertos en {ip}...")
    for puerto in puertos:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        resultado = s.connect_ex((ip, puerto))
        if resultado == 0:
            print(f"🟢 Puerto {puerto} abierto")
        s.close()

def detectar_procesos_sospechosos():
    print("\n🧪 Procesos en ejecución con uso elevado de CPU (>20%) o nombres sospechosos:")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > 20 or any(term in proc.info['name'].lower() for term in ['key', 'logger', 'sniffer']):
                print(f"⚠️ PID {proc.info['pid']}: {proc.info['name']} ({proc.info['cpu_percent']}% CPU)")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

# ================ ELECCIÓN DEL MODELO ================
print("🎛️ Selecciona el modelo a utilizar:")
for k, v in MODELOS.items():
    print(f"{k}. {v['nombre']}")

opcion = input("🧠 Opción (1 o 2): ").strip()
modelo = MODELOS.get(opcion)

if not modelo or not os.path.exists(modelo['path']):
    print("❌ Opción inválida o modelo no encontrado.")
    exit()

# ================ CARGA DEL MODELO ================
print(f"\n⏳ Cargando modelo {modelo['nombre']}...")
llm = AutoModelForCausalLM.from_pretrained(
    modelo['path'],
    model_type=modelo['tipo'],
    gpu_layers=0
)

print("✅ Modelo cargado correctamente.\n")

# ================ LOOP INTERACTIVO ================
while True:
    print("\n🧠 ¿Qué deseas hacer?")
    print("1. Solicitud de código asistido por IA")
    print("2. Escanear puertos (modo laboratorio)")
    print("3. Detectar procesos sospechosos")
    print("4. Salir")
    opcion = input("> ").strip()

    if opcion == "4":
        print("👋 Hasta luego.")
        break

    elif opcion == "2":
        ip = input("🔎 IP a escanear (ej: 192.168.0.1): ")
        escanear_puertos(ip)

    elif opcion == "3":
        detectar_procesos_sospechosos()

    elif opcion == "1":
        user_input = input("\n✍️ Escribí tu solicitud ('salir' para volver al menú):\n> ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            continue

        # Armar prompt
        prompt = f"""### Instrucción:
Eres un experto en programación y ciberseguridad ofensiva y defensiva.
Responde limpiamente a la siguiente solicitud:

### Solicitud:
{user_input}

### Código generado:
"""
        tokens_usados = len(prompt.split())
        max_new_tokens = max(64, MAX_TOTAL_TOKENS - tokens_usados)

        print(f"🔢 Tokens usados: {tokens_usados} | Tokens permitidos: {max_new_tokens}")
        print("⏳ Generando respuesta...\n")

        try:
            output = llm(prompt, max_new_tokens=max_new_tokens)
            print("🧾 Respuesta generada:\n")
            print(output)

            with open("historial_cyber.txt", "a", encoding="utf-8") as f:
                f.write(f">>> {user_input}\n{output}\n{'='*60}\n\n")

        except Exception as e:
            print(f"❌ Error al generar: {e}")
    else:
        print("❌ Opción inválida.")