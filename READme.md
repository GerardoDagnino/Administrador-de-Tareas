# ADMINISTRADOR DE TAREAS

## Requisitos Previos

- Python: Asegúrate de tener Python instalado. 
## Configuración del Entorno Virtual

1. Abre una terminal y navega al directorio de tu proyecto.

2. Crea un entorno virtual ejecutando el siguiente comando:

   - En Windows:
    
     python -m venv venv
    

   - En Unix o MacOS:
     
     python3 -m venv venv
     

3. Activa el entorno virtual:

   - En Windows:
    
     venv\Scripts\activate
    

   - En Unix o MacOS:
     
     source venv/bin/activate
  

## Instalación de Dependencias

1. Con el entorno virtual activado, instala Flask y Flask-Login ejecutando:

   
   pip install Flask Flask-Login