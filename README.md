# Inventario-familiar-bot
# 🏡 Inventario Familiar Bot

> Un bot de Telegram para organizar el inventario de tu casa de forma colaborativa. Ideal si viven varias personas, para saber lo que hay, lo que falta y lo que sobra.

---

## 📋 Qué es / Para qué sirve

Este bot te permite:

- Listar todos los objetos que hay en tu casa / departamento / hogar familiar.  
- Agregar nuevos ítems al inventario.  
- Eliminar o marcar como usados los ítems que ya no están.  
- Ver lo que “falta” o lo que se va agotando.  
- Servir como “lista de compras familiar”: colaborativo, de modo que todos los que lo usen puedan ver el estado actualizado.

---

## 🚀 Características

- Basado en **Telegram Bot API**.  
- Base de datos local simple (SQLite) para guardar el inventario.  
- Comandos básicos para que cualquier usuario lo use fácilmente.  
- Licencia **MIT**: código abierto, libre para usar, modificar y redistribuir.

---

## 🧰 Comandos

Aquí una lista de los comandos disponibles:

| Comando | Descripción |
|---------|-------------|
| `/start` | Inicia el bot / mensaje de bienvenida. |
| `/agregar <nombre>` | Agrega un nuevo ítem al inventario. |
| `/eliminar <nombre>` | Elimina un ítem del inventario. |
| `/listar` | Muestra todos los ítems que hay actualmente. |
| `/faltar` | Muestra los ítems que han sido marcados como faltantes. |
| `/ayuda` | Muestra este mensaje de ayuda / comandos disponibles. |

> *Nota: adaptar los comandos exactos en base al bot actual.*

---

## 🔧 Requisitos

- Python 3.x  
- Librerías necesarias (por ejemplo: `python-telegram-bot`, `sqlite3`, etc.)  
- Un token de bot de Telegram (lo podés conseguir hablando con BotFather)  
- (Opcional) Servidor o compu que esté corriendo todo el tiempo para que el bot esté disponible  

---

## ⚙️ Instalación / Cómo usarlo localmente

1. Cloná este repositorio:  
   ```bash
   git clone https://github.com/mbus31/Inventario-familiar-bot.git
   cd Inventario-familiar-bot
Instalá dependencias:

bash
Copiar código
pip install -r requirements.txt
Configurá el token de Telegram en una variable de entorno o un archivo .env. Ejemplo .env:


TELEGRAM_TOKEN=TU_TOKEN_AQUI
Ejecutá el bot:


python src/main.py
(Opcional) Si querés que esté funcionando siempre, desplegalo en un servidor, Raspberry Pi, instancia en la nube, etc.

🗂️ Estructura del Proyecto
graphql
Copiar código
Inventario-familiar-bot/
├── src/                  # Código fuente del bot
│   └── main.py           # Punto de entrada
├── lista_compras.db      # Base de datos SQLite para el inventario
├── .gitignore
├── LICENSE               # Licencia MIT
└── README.md             # Este archivo
🛡️ Licencia
Este proyecto está bajo la licencia MIT. Podés hacer lo que quieras con el código, siempre y cuando respetes los términos de la licencia.

Ver LICENSE para más detalles.
