from datetime import datetime

def calcular_edad(fecha_nacimiento):
    hoy = datetime.now()
    nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    return hoy.year - nacimiento.year  # ERROR: no se controla si ya cumplió años

print(calcular_edad("2005-10-20"))
