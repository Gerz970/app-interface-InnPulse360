-- Script para crear tablas del módulo de Mensajería
-- Schema: MENSAJERIA
-- Fecha: 2024

-- Crear schema si no existe
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'MENSAJERIA')
BEGIN
    EXEC('CREATE SCHEMA MENSAJERIA')
END
GO

-- Tabla: Tb_Conversacion
-- Almacena las conversaciones entre usuarios
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[MENSAJERIA].[Tb_Conversacion]') AND type in (N'U'))
BEGIN
    CREATE TABLE [MENSAJERIA].[Tb_Conversacion] (
        id_conversacion INT PRIMARY KEY IDENTITY(1,1),
        tipo_conversacion VARCHAR(20) NOT NULL, -- 'cliente_admin', 'empleado_empleado'
        usuario1_id INT NOT NULL, -- Usuario que inicia la conversación
        usuario2_id INT NOT NULL, -- Usuario destinatario
        cliente_id INT NULL, -- Si es conversación cliente-admin
        empleado1_id INT NULL, -- Si es conversación empleado-empleado
        empleado2_id INT NULL,
        fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
        fecha_ultimo_mensaje DATETIME NULL,
        id_estatus INT NOT NULL DEFAULT 1, -- 1=Activa, 0=Archivada
        
        -- Foreign Keys
        CONSTRAINT FK_Conversacion_Usuario1 FOREIGN KEY (usuario1_id) 
            REFERENCES SEGURIDAD.Tb_usuario(id_usuario),
        CONSTRAINT FK_Conversacion_Usuario2 FOREIGN KEY (usuario2_id) 
            REFERENCES SEGURIDAD.Tb_usuario(id_usuario),
        CONSTRAINT FK_Conversacion_Cliente FOREIGN KEY (cliente_id) 
            REFERENCES CLIENTE.Tb_cliente(id_cliente),
        CONSTRAINT FK_Conversacion_Empleado1 FOREIGN KEY (empleado1_id) 
            REFERENCES EMPLEADOS.Tb_empleado(id_empleado),
        CONSTRAINT FK_Conversacion_Empleado2 FOREIGN KEY (empleado2_id) 
            REFERENCES EMPLEADOS.Tb_empleado(id_empleado)
    )
    
    -- Índices para optimizar consultas
    CREATE INDEX IX_Conversacion_Usuario1 ON [MENSAJERIA].[Tb_Conversacion](usuario1_id)
    CREATE INDEX IX_Conversacion_Usuario2 ON [MENSAJERIA].[Tb_Conversacion](usuario2_id)
    CREATE INDEX IX_Conversacion_Cliente ON [MENSAJERIA].[Tb_Conversacion](cliente_id)
    CREATE INDEX IX_Conversacion_Empleado1 ON [MENSAJERIA].[Tb_Conversacion](empleado1_id)
    CREATE INDEX IX_Conversacion_Empleado2 ON [MENSAJERIA].[Tb_Conversacion](empleado2_id)
    CREATE INDEX IX_Conversacion_FechaUltimoMensaje ON [MENSAJERIA].[Tb_Conversacion](fecha_ultimo_mensaje DESC)
    CREATE INDEX IX_Conversacion_Estatus ON [MENSAJERIA].[Tb_Conversacion](id_estatus)
END
GO

-- Tabla: Tb_Mensaje
-- Almacena los mensajes individuales de cada conversación
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[MENSAJERIA].[Tb_Mensaje]') AND type in (N'U'))
BEGIN
    CREATE TABLE [MENSAJERIA].[Tb_Mensaje] (
        id_mensaje INT PRIMARY KEY IDENTITY(1,1),
        conversacion_id INT NOT NULL,
        remitente_id INT NOT NULL, -- Usuario que envía el mensaje
        contenido TEXT NOT NULL,
        fecha_envio DATETIME NOT NULL DEFAULT GETDATE(),
        fecha_leido DATETIME NULL,
        id_estatus INT NOT NULL DEFAULT 1, -- 1=Enviado, 2=Leído, 3=Eliminado
        
        -- Foreign Keys
        CONSTRAINT FK_Mensaje_Conversacion FOREIGN KEY (conversacion_id) 
            REFERENCES [MENSAJERIA].[Tb_Conversacion](id_conversacion) ON DELETE CASCADE,
        CONSTRAINT FK_Mensaje_Remitente FOREIGN KEY (remitente_id) 
            REFERENCES SEGURIDAD.Tb_usuario(id_usuario)
    )
    
    -- Índices para optimizar consultas
    CREATE INDEX IX_Mensaje_Conversacion ON [MENSAJERIA].[Tb_Mensaje](conversacion_id)
    CREATE INDEX IX_Mensaje_Remitente ON [MENSAJERIA].[Tb_Mensaje](remitente_id)
    CREATE INDEX IX_Mensaje_FechaEnvio ON [MENSAJERIA].[Tb_Mensaje](fecha_envio DESC)
    CREATE INDEX IX_Mensaje_Estatus ON [MENSAJERIA].[Tb_Mensaje](id_estatus)
    CREATE INDEX IX_Mensaje_FechaLeido ON [MENSAJERIA].[Tb_Mensaje](fecha_leido)
END
GO

-- Tabla: Tb_MensajeAdjunto (Opcional - para futura implementación)
-- Almacena archivos adjuntos a los mensajes
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[MENSAJERIA].[Tb_MensajeAdjunto]') AND type in (N'U'))
BEGIN
    CREATE TABLE [MENSAJERIA].[Tb_MensajeAdjunto] (
        id_adjunto INT PRIMARY KEY IDENTITY(1,1),
        mensaje_id INT NOT NULL,
        nombre_archivo VARCHAR(255) NOT NULL,
        tipo_archivo VARCHAR(50) NOT NULL, -- 'imagen', 'pdf', 'documento', etc.
        ruta_archivo VARCHAR(500) NOT NULL, -- Ruta en Supabase Storage
        tamanio_bytes BIGINT NOT NULL,
        fecha_subida DATETIME NOT NULL DEFAULT GETDATE(),
        
        -- Foreign Key
        CONSTRAINT FK_MensajeAdjunto_Mensaje FOREIGN KEY (mensaje_id) 
            REFERENCES [MENSAJERIA].[Tb_Mensaje](id_mensaje) ON DELETE CASCADE
    )
    
    -- Índices
    CREATE INDEX IX_MensajeAdjunto_Mensaje ON [MENSAJERIA].[Tb_MensajeAdjunto](mensaje_id)
END
GO

-- Comentarios en las tablas
EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Tabla que almacena las conversaciones entre usuarios del sistema', 
    @level0type = N'SCHEMA', @level0name = N'MENSAJERIA',
    @level1type = N'TABLE', @level1name = N'Tb_Conversacion'
GO

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Tabla que almacena los mensajes individuales de cada conversación', 
    @level0type = N'SCHEMA', @level0name = N'MENSAJERIA',
    @level1type = N'TABLE', @level1name = N'Tb_Mensaje'
GO

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Tabla que almacena archivos adjuntos a los mensajes', 
    @level0type = N'SCHEMA', @level0name = N'MENSAJERIA',
    @level1type = N'TABLE', @level1name = N'Tb_MensajeAdjunto'
GO

