<!-- dfbb13a1-26de-4ce6-94b5-b05ad544637a df5106ee-fe22-4d08-9af3-d89be016b476 -->
# Plan Servicio Supabase Storage

1. Revisar configuración existente

- Confirmar patrones en `core/config.py` y `core/database_connection.py` para mantener estilo consistente.

2. Diseñar configuración y cliente Supabase

- Proponer nueva clase `SupabaseSettings` en `core/config.py` para URL, keys y bucket por defecto.
- Especificar módulo `core/supabase_client.py` con singleton ligero inspirado en `DatabaseConnection`.

3. Diseñar servicios diferenciados por tipo de documento

- Proponer `services/storage/image_storage_service.py` enfocado en imágenes JPG/PNG/GIF con validación de MIME.
- Proponer `services/storage/pdf_storage_service.py` para PDFs, reutilizando utilidades comunes (subida, URL firmada, eliminación).
- Incluir manejo de errores, logging y retornos estructurados.

4. Documentar pasos de integración

- Indicar variables de entorno necesarias, buckets sugeridos (`images`, `pdfs`) y ejemplos de uso.
- Señalar que no se crearán archivos de pruebas en esta fase.

### To-dos

- [ ] Definir configuración Supabase en `core/config.py` y patrón de cliente singleton
- [ ] Especificar interfaz y detalles de `SupabaseDocumentService` en `services/storage/documents_service.py`
- [ ] Documentar variables, uso y recomendaciones de integración sin tests