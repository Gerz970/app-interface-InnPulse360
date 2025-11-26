import os
from openai import OpenAI
from typing import List, Dict, Optional
from datetime import datetime
from .documentation_service import DocumentationService

class ChatService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_API_KEY no está configurada")
        self.client = OpenAI(api_key=api_key)
        
        # Inicializar servicio de documentación
        self.docs_service = DocumentationService()
        self.documents = self.docs_service.load_documents()
        
        # Historial de conversaciones
        self.conversations: Dict[str, List[Dict]] = {}
    
    def get_system_prompt(self) -> str:
        """Define el contexto del asistente"""
        return """Eres un asistente virtual experto del sistema de gestión hotelera InnPulse360.

Tu función es ayudar a usuarios con preguntas sobre cómo usar la aplicación móvil.

IMPORTANTE: 
- Solo puedes responder basándote en la documentación proporcionada
- Si la información no está en la documentación, di: "Lo siento, no tengo información sobre eso en la documentación. Te recomiendo contactar con soporte."
- Responde siempre de forma amigable, profesional y en español
- Si te proporcionan contexto de documentación, úsalo para responder de manera precisa"""

    def chat(self, user_id: str, message: str) -> Dict:
        """
        Procesa un mensaje del usuario usando RAG (Retrieval Augmented Generation).
        """
        try:
            # Buscar documentos relevantes
            relevant_docs = self.docs_service.search_relevant_docs(message, self.documents, top_k=3)
            
            # Construir contexto de documentación
            context = ""
            if relevant_docs:
                context = "\n\n--- DOCUMENTACIÓN RELEVANTE ---\n\n"
                for i, doc in enumerate(relevant_docs, 1):
                    context += f"[Documento {i} - {doc['file']}]\n{doc['content']}\n\n"
                context += "--- FIN DE DOCUMENTACIÓN ---\n\n"
            
            # Obtener historial de conversación
            if user_id not in self.conversations:
                self.conversations[user_id] = []
            
            historial = self.conversations[user_id]
            
            # Construir mensajes para OpenAI
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ]
            
            # Agregar contexto de documentación si existe
            if context:
                messages.append({
                    "role": "system", 
                    "content": f"Usa la siguiente documentación para responder:\n{context}"
                })
            
            # Agregar historial (últimos 10 mensajes)
            for msg in historial[-10:]:
                messages.append(msg)
            
            # Agregar mensaje actual del usuario
            messages.append({"role": "user", "content": message})
            
            # Llamar a OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_response = response.choices[0].message.content.strip()
            
            # Guardar en historial
            historial.append({"role": "user", "content": message})
            historial.append({"role": "assistant", "content": assistant_response})
            
            # Limitar historial
            if len(historial) > 20:
                historial[:] = historial[-20:]
            
            return {
                "response": assistant_response,
                "timestamp": datetime.now().isoformat(),
                "sources": [doc['file'] for doc in relevant_docs] if relevant_docs else []
            }
            
        except Exception as e:
            return {
                "response": "Lo siento, hubo un error al procesar tu mensaje. Por favor intenta de nuevo.",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def limpiar_historial(self, user_id: str):
        """Limpia el historial de conversación de un usuario"""
        if user_id in self.conversations:
            del self.conversations[user_id]
    
    def recargar_documentacion(self):
        """Recarga la documentación (útil después de actualizar archivos)"""
        self.documents = self.docs_service.load_documents()
        return len(self.documents)

