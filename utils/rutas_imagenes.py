class RutasImagenes:
    """
    Clase para manejar las rutas de las imágenes
    """

    def get_ruta_imagenes_perfil(self, id_usuario: int):
        return f"usuarios/perfil/{id_usuario}"
    
    