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
    
    def get_ruta_galeria_mantenimiento_antes(self, id_mantenimiento: int) -> str:
        """
        Obtiene la ruta para la galería de imágenes "antes" del mantenimiento
        Las imágenes se guardan en: mantenimiento/{id_mantenimiento}/antes/
        
        Args:
            id_mantenimiento (int): ID del mantenimiento
            
        Returns:
            str: Ruta de la galería "antes" (ej: "mantenimiento/123/antes")
        """
        return f"mantenimiento/{id_mantenimiento}/antes"
    
    def get_ruta_galeria_mantenimiento_despues(self, id_mantenimiento: int) -> str:
        """
        Obtiene la ruta para la galería de imágenes "despues" del mantenimiento
        Las imágenes se guardan en: mantenimiento/{id_mantenimiento}/despues/
        
        Args:
            id_mantenimiento (int): ID del mantenimiento
            
        Returns:
            str: Ruta de la galería "despues" (ej: "mantenimiento/123/despues")
        """
        return f"mantenimiento/{id_mantenimiento}/despues"
    
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
    
    def get_ruta_galeria_limpieza_antes(self, id_limpieza: int) -> str:
        """
        Obtiene la ruta para la galería de imágenes "antes" de la limpieza
        Las imágenes se guardan en: limpieza/{id_limpieza}/antes/
        
        Args:
            id_limpieza (int): ID de la limpieza
            
        Returns:
            str: Ruta de la galería "antes" (ej: "limpieza/123/antes")
        """
        return f"limpieza/{id_limpieza}/antes"
    
    def get_ruta_galeria_limpieza_despues(self, id_limpieza: int) -> str:
        """
        Obtiene la ruta para la galería de imágenes "despues" de la limpieza
        Las imágenes se guardan en: limpieza/{id_limpieza}/despues/
        
        Args:
            id_limpieza (int): ID de la limpieza
            
        Returns:
            str: Ruta de la galería "despues" (ej: "limpieza/123/despues")
        """
        return f"limpieza/{id_limpieza}/despues"
    
    def get_ruta_galeria_habitacion(self, id_habitacion_area: int) -> str:
        """
        Obtiene la ruta base para la galería de una habitación
        Las imágenes se guardan directamente en: habitacion/{id_habitacion_area}/
        
        Args:
            id_habitacion_area (int): ID de la habitación área
            
        Returns:
            str: Ruta base (ej: "habitacion/123")
        """
        return f"habitacion/{id_habitacion_area}"
    