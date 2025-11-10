class RutasImagenes:
    """
    Clase para manejar las rutas de las imágenes
    """

    def get_ruta_imagenes_perfil(self, id_usuario: int):
        return f"usuarios/perfil/{id_usuario}"
    
    def get_ruta_foto_perfil_hotel(self, id_hotel: int) -> str:
        """
        Obtiene la ruta base para la foto de perfil de un hotel
        La foto de perfil se guarda como: hotel/{id_hotel}/{id_hotel}.{extension}
        
        Args:
            id_hotel (int): ID del hotel
            
        Returns:
            str: Ruta base sin extensión (ej: "hotel/123/123")
        """
        return f"hotel/{id_hotel}/{id_hotel}"
    
    def get_ruta_galeria_hotel(self, id_hotel: int) -> str:
        """
        Obtiene la ruta base para la galería de un hotel
        Las imágenes de galería se guardan en: hotel/{id_hotel}/galeria/
        
        Args:
            id_hotel (int): ID del hotel
            
        Returns:
            str: Ruta de la galería (ej: "hotel/123/galeria")
        """
        return f"hotel/{id_hotel}/galeria"
    
    def get_ruta_default_hotel(self, id_hotel: int) -> str:
        """
        Obtiene la ruta de la imagen por defecto de un hotel
        La imagen por defecto se encuentra en: hotel/{id_hotel}/default.jpg
        
        Args:
            id_hotel (int): ID del hotel
            
        Returns:
            str: Ruta de la imagen por defecto (ej: "hotel/123/default.jpg")
        """
        return f"hotel/{id_hotel}/default.jpg"
    
    def get_ruta_galeria_mantenimiento(self, id_mantenimiento: int) -> str:
        """
        Obtiene la ruta base para la galería de un mantenimiento
        Las imágenes se guardan directamente en: mantenimiento/{id_mantenimiento}/
        
        Args:
            id_mantenimiento (int): ID del mantenimiento
            
        Returns:
            str: Ruta base (ej: "mantenimiento/123")
        """
        return f"mantenimiento/{id_mantenimiento}"
    
    def get_ruta_galeria_limpieza(self, id_limpieza: int) -> str:
        """
        Obtiene la ruta base para la galería de una limpieza
        Las imágenes se guardan directamente en: limpieza/{id_limpieza}/
        
        Args:
            id_limpieza (int): ID de la limpieza
            
        Returns:
            str: Ruta base (ej: "limpieza/123")
        """
        return f"limpieza/{id_limpieza}"
    