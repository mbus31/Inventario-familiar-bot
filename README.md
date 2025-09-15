# 🏡 Inventario Familiar Bot

> Un bot de Telegram para organizar el inventario de tu casa de forma colaborativa. Ideal para familias o compañeros de piso para saber lo que hay, lo que falta y lo que sobra.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots/api)

---

## 📋 Qué es y para qué sirve

Este bot te permite:

- 📝 Listar todos los objetos que hay en tu hogar
- ➕ Agregar nuevos ítems al inventario
- ❌ Eliminar o marcar como usados los ítems que ya no están
- 🔍 Ver lo que "falta" o lo que se va agotando
- 👥 Funcionar como "lista de compras familiar" colaborativa

---

## 🚀 Características

- Basado en **Telegram Bot API** con `python-telegram-bot`
- Base de datos **SQLite** para persistencia local
- Interfaz intuitiva con comandos sencillos
- Código abierto bajo licencia **MIT**
- Fácil despliegue y configuración

---

## 🧰 Comandos disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/start` | Inicia el bot y muestra bienvenida | `/start` |
| `/agregar <nombre>` | Agrega un nuevo ítem | `/agregar arroz` |
| `/eliminar <nombre>` | Elimina un ítem | `/eliminar arroz` |
| `/listar` | Muestra todos los ítems | `/listar` |
| `/faltar` | Muestra ítems marcados como faltantes | `/faltar` |
| `/ayuda` | Muestra ayuda de comandos | `/ayuda` |

---

## 🔧 Requisitos

- Python 3.7 o superior
- Token de bot de Telegram (obtenido via [BotFather](https://t.me/BotFather))
- Dependencias listadas en `requirements.txt`

---
Instalar dependencias:


pip install -r requirements.txt

Configurar token de Telegram:

Crear archivo .env:


TELEGRAM_TOKEN=tu_token_aqui

O exportar variable de entorno:


export TELEGRAM_TOKEN="tu_token_aqui"

Ejecutar el bot:

python bot.py

🚀 Despliegue
Opciones recomendadas:
Servidor local: Raspberry Pi o computadora siempre encendida

Servicios cloud: Heroku, PythonAnywhere, AWS EC2

🤝 Contribuir
Las contribuciones son bienvenidas. Para contribuir:

Haz fork del proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

🛡️ Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

📞 Soporte
Si tienes problemas o preguntas:

Revisa los issues existentes

Abre un nuevo issue describiendo el problema

Contacta por Telegram: @mbus31
