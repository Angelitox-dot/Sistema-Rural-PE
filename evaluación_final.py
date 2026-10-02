class Persona:
    def __init__(self, nombre: str, apellido: str, dni: str, edad: int, servicio: str):
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni
        self.edad = edad
        self.servicio = servicio

    @property
    def dni(self):
        return self._dni

    def obtener_identidad_segura(self) -> str:
        # Enmascaramiento conforme a la Ley N.º 29733 (estilo ***102)
        dni_enmascarado = f"*{self._dni[-3:]}"
        return dni_enmascarado
    

class Paciente(Persona):
    def __init__(self, nombre: str, apellido: str, dni: str, historia_clinica: str, edad: int, servicio: str):
        super().__init__(nombre, apellido, dni, edad, servicio)
        self._historia_clinica = historia_clinica

    @property
    def historia_clinica(self):
        return self._historia_clinica

class PersonalSalud(Persona):
    def __init__(self, nombre: str, apellido: str, dni: str, especialidad: str, colegiatura: str, rol: str):
        super().__init__(nombre, apellido, dni, 0, "")
        self._especialidad = especialidad
        self._colegiatura = colegiatura
        self.rol = rol

    def firmar_atencion(self, codigo_atencion: str) -> str:
        prefijo = "CMP" if self.rol == "MEDICO" else "CEP"
        return f"FIRMA_{prefijo}{self._colegiatura}_ATENCION{codigo_atencion}"

class Medicamento:
    def __init__(self, codigo: str, nombre: str, stock: int):
        self.codigo = codigo
        self._nombre = nombre
        self._stock = stock

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, nuevo_stock: int):
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = nuevo_stock

    def __repr__(self):
        return f"Medicamento({self._nombre}, Stock: {self._stock})"

class GestorSistemaSalud:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GestorSistemaSalud, cls).__new__(cls)
            cls._instancia._conexion_db = {"estado": "Conectado a SQLite local (Modo Offline)"}
        return cls._instancia

    @classmethod
    def obtener_instancia(cls):
        if cls._instancia is None:
            cls._instancia = GestorSistemaSalud()
        return cls._instancia

    def ejecutar_consulta(self, sql: str):
        return f"Ejecutando: {sql} [{self._conexion_db['estado']}]"

def filtrar_stock_critico(lista_medicamentos: list, umbral: int = 10) -> list:
    return list(filter(lambda m: m.stock < umbral, lista_medicamentos))

# ==========================================
# BLOQUE DE PRUEBA Y DEMOSTRACIÓN OPERATIVA
# ==========================================
if __name__ == "__main__":
    print("=============================================================")
    print(" Iniciando SistemaRural-PE (Python) - Hospital Simón Bolívar")
    print("=============================================================")
    
    # 1. Patrón Singleton
    repo1 = GestorSistemaSalud.obtener_instancia()
    repo2 = GestorSistemaSalud.obtener_instancia()
    print(f"Patrón Singleton verificado: ¿repo1 es repo2? -> {repo1 is repo2} (Misma instancia en memoria)")
    print(repo1.ejecutar_consulta("SELECT * FROM configuracion_simon_bolivar"))

    # 2. Factory Method y Asignación de Personal
    print("\n--- Asignación con Factory Method ---")
    medico = PersonalSalud("Carlos", "Mendoza", "45123698", "Medicina General", "CMP-89421", "MEDICO")
    enfermero = PersonalSalud("Ana", "Torres", "12345678", "Enfermería", "CEP-12345", "ENFERMERO")
    print(f"Profesional: {medico._apellido}, {medico._nombre} | Rol: {medico.rol}")
    print(f"Firma: {medico.firmar_atencion('AT-001')}")
    print(f"Profesional: {enfermero._apellido}, {enfermero._nombre} | Rol: {enfermero.rol}")
    print(f"Firma: {enfermero.firmar_atencion('AT-002')}")

    # 3. Reporte Sanitizado (Ley N.° 29733)
    pacientes = [
        Paciente("Roinson", "Otiano", "61083390", "HC-2026-001", 41, "Medicina General"),
        Paciente("Juan", "Rivero", "45123699", "HC-2026-002", 28, "Emergencia"),
        Paciente("Luis", "Vicuña", "61502755", "HC-2026-003", 55, "Medicina General")
    ]

    print("\n--- Reporte Sanitizado (Ley N.º 29733) ---")
    for p in pacientes:
        print(f"Historia: {p.historia_clinica} | DNI: {p.obtener_identidad_segura()} | Edad: {p.edad} años | Servicio: {p.servicio}")

    # 4. Programación Funcional (Inventario de Medicamentos y Filtros)
    inventario = [
        Medicamento("M01", "Paracetamol 500mg", 5),
        Medicamento("M02", "Amoxicilina 500mg", 45),
        Medicamento("M03", "Ibuprofeno 400mg", 8),
        Medicamento("M04", "Suero Fisiológico 1L", 3)
    ]
    
    criticos = filtrar_stock_critico(inventario, umbral=10)
    print(f"\nAlerta de stock crítico (< 10 para código {criticos[0].codigo}): {criticos}")

    # 5. Filtrado funcional por servicio de pacientes
    print("\n--- Pacientes en el Servicio de Medicina General ---")
    medicina = list(filter(lambda p: p.servicio == "Medicina General", pacientes))
    for p in medicina:
        print(f"{p._apellido}, {p._nombre} (DNI: {p.obtener_identidad_segura()})")

    total_edades = sum(map(lambda p: p.edad, medicina))
    print(f"\nTotal acumulado de edades: {total_edades} años")
    print("--- EJECUCIÓN OPERATIVA FINALIZADA CON ÉXITO ---")
