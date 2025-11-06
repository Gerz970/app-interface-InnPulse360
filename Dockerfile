# ========================================
# Imagen base: Python 3.11 Slim (Debian)
# ========================================
# Usamos la versión slim para mantener la imagen ligera (~180MB)
# pero agregaremos solo las dependencias necesarias para ODBC
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# ========================================
# PASO 1: Instalar dependencias del sistema
# ========================================
# Estas son bibliotecas a nivel de sistema operativo necesarias para:
# - Descargar e instalar paquetes de Microsoft
# - Compilar y ejecutar pyodbc
# - Conectarse a SQL Server

RUN apt-get update && apt-get install -y \
    # curl: Herramienta para descargar archivos (necesaria para obtener repositorios de Microsoft)
    curl \
    # apt-transport-https: Permite a APT descargar paquetes mediante HTTPS
    apt-transport-https \
    # gnupg: Herramienta de cifrado para verificar firmas digitales de paquetes
    gnupg \
    # unixodbc: Gestor de drivers ODBC para Unix/Linux (proporciona libodbc.so.2)
    # Esta es la librería que estaba faltando en el error original
    unixodbc \
    # unixodbc-dev: Headers de desarrollo de ODBC necesarios para compilar pyodbc
    unixodbc-dev \
    # g++: Compilador de C++ necesario para compilar extensiones de Python (pyodbc)
    g++ \
    # Limpiar caché de APT para reducir el tamaño final de la imagen
    && rm -rf /var/lib/apt/lists/*

# ========================================
# PASO 2: Agregar repositorio de Microsoft
# ========================================
# El ODBC Driver 17 for SQL Server no está en los repositorios estándar de Debian
# Debemos agregar el repositorio oficial de Microsoft
# NOTA: Usamos el método moderno (apt-key está deprecado)

RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    # Descargar y convertir la clave GPG de Microsoft al formato binario (.gpg)
    # La guardamos en /usr/share/keyrings/ (ubicación estándar para claves GPG)
    && echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list
    # Crear el archivo de repositorio manualmente con el formato correcto
    # - arch: arquitecturas soportadas
    # - signed-by: especifica la clave GPG a usar
    # - bullseye: nombre código de Debian 11

# ========================================
# PASO 3: Instalar ODBC Driver 17 for SQL Server
# ========================================
# Este es el driver real que permite la conexión a SQL Server/Azure SQL
# Es el driver que tu aplicación requiere en core/config.py

RUN apt-get update \
    # ACCEPT_EULA=Y: Acepta automáticamente el acuerdo de licencia de Microsoft
    # msodbcsql17: Microsoft ODBC Driver 17 for SQL Server
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    # Limpiar caché nuevamente
    && rm -rf /var/lib/apt/lists/*

# ========================================
# PASO 4: Instalar dependencias de Python
# ========================================
# Copiar solo requirements.txt primero (aprovecha cache de Docker)
COPY requirements.txt .

# Instalar paquetes de Python desde requirements.txt
# --no-cache-dir: No guardar caché de pip para reducir tamaño de imagen
# Ahora pyodbc se instalará correctamente porque ya tenemos unixodbc-dev y g++
RUN pip install --no-cache-dir -r requirements.txt

# ========================================
# PASO 5: Copiar código de la aplicación
# ========================================
# Copiar todo el código fuente al contenedor
# (respeta las exclusiones definidas en .dockerignore)
COPY . .

# ========================================
# PASO 6: Comando de inicio
# ========================================
# Ejecutar uvicorn cuando el contenedor inicie
# --host 0.0.0.0: Escuchar en todas las interfaces de red (necesario para Docker)
# --port 8000: Puerto donde la aplicación estará disponible
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]