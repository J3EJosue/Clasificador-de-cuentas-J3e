# Clasificador de Cuentas Contables con Inteligencia Artificial

## Descripción
Este proyecto implementa un modelo de inteligencia artificial avanzado para clasificar cuentas contables con rapidez y precisión. Proporciona información detallada sobre la naturaleza de la cuenta, los libros contables relevantes y una descripción completa.

## Características Principales
- 🧠 **Clasificación Inteligente:** Utiliza un modelo de IA entrenado con un extenso conjunto de datos contables.
- 📊 **Análisis Completo:** Ofrece clasificación, naturaleza de la cuenta, libros contables aplicables y descripción detallada.
- 💡 **Sugerencias Contextuales:** Recomienda cuentas similares para facilitar la exploración de opciones relacionadas.
- 🚀 **Rápido y Eficiente:** Proporciona resultados en segundos, optimizando el proceso contable.

## Requisitos del Sistema
- Python 3.7+
- Flask
- Conexión a Internet (para la versión en línea)

## Instalación y Configuración

### Instalación Local
1. Clone el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/clasificador-cuentas-contables.git
   cd clasificador-cuentas-contables
   ```

2. Instale las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicie el servidor:
   ```bash
   flask run
   ```
   El servidor se iniciará en `http://127.0.0.1:5000/`.

### Uso en Línea
Visite [https://conta-ai.onrender.com](https://conta-ai.onrender.com)

**Nota:** Debido a las limitaciones del plan gratuito en Render:
- Si encuentra un error, recargue la página 2 veces.
- La primera carga puede ser lenta mientras se inicializa el modelo de IA.

## Guía de Uso
1. Acceda a la aplicación (local o en línea).
2. Ingrese el nombre de la cuenta contable en el campo de texto.
3. Haga clic en "Clasificar".
4. Revise los resultados: clasificación, naturaleza, libros contables y descripción.

## Arquitectura Técnica
- **Backend:** Flask (Python)
- **Modelo de IA:** Combinación de Naive Bayes y redes neuronales
- **Fuente de Datos:** 
  - PDFs públicos de cuentas contables
  - Libros contables propietarios

## Contribuciones
¡Valoramos su contribución! Puede ayudar:
1. Reportando errores
2. Sugiriendo mejoras
3. Ampliando el conjunto de datos

Consulte `CONTRIBUTING.md` para obtener información sobre nuestro código de conducta y el proceso de pull requests.

## Licencia
Este proyecto está bajo la Licencia MIT. Vea el archivo `LICENSE` para más detalles.

## Contacto y Soporte
- **Desarrollador:** Josué Manuel Cruz (J3eJosue)
- **Proyecto en Línea:** [https://conta-ai.onrender.com](https://conta-ai.onrender.com)
- **Repositorio:** [(https://github.com/J3EJosue/J3eContAI)](https://github.com/J3EJosue/J3eContAI)
- **Soporte:** josuemanuelcruzzz@gmail.com

## Notas Importantes
- **Tiempo de Inicialización:** La carga inicial puede tardar hasta 15 segundos.
- **Precisión:** Aunque el modelo es altamente preciso, se recomienda la verificación por un experto contable en casos críticos.
- **Privacidad:** Los datos ingresados no se almacenan ni comparten.

## Agradecimientos
Un agradecimiento especial a:
- Colegas programadores por su asesoría técnica
- Profesionales contables por su aporte en la validación del modelo
- Comunidad open-source por las herramientas y librerías utilizadas

## Registro de Cambios
- v1.0.0 (2024-08-01): Lanzamiento inicial
- [Añadir futuras versiones y sus cambios]

## Hoja de Ruta
- Integración con sistemas ERP populares
- Soporte para múltiples idiomas
- Interfaz de usuario mejorada con gráficos interactivos

---

Desarrollado con ❤️ por el equipo de J3eJosue