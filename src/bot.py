import os
from dotenv import load_dotenv  # type: ignore
from telegram import Update  # type: ignore
from telegram.ext import Application, CommandHandler, ContextTypes # type: ignore
from database import DatabaseManager

# Configuración inicial
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Inicializamos el manejador de la base de datos
db = DatabaseManager()

# 🔧 Crear nueva categoría
async def nueva_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    
    if context.args:
        categoria_nombre = ' '.join(context.args).lower()
        db.get_or_create_user(user_id, username)
        
        if db.crear_categoria(user_id, categoria_nombre):
            await update.message.reply_text(f"📁 Categoría creada: {categoria_nombre.capitalize()}")
        else:
            await update.message.reply_text("⚠️ Ya tienes una categoría con ese nombre.")
    else:
        await update.message.reply_text("⚠️ Usa: /nueva_categoria [nombre]")

# 🗑️ Eliminar categoría
async def eliminar_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    
    if context.args:
        categoria_nombre = ' '.join(context.args).lower()
        
        if db.eliminar_categoria(user_id, categoria_nombre):
            await update.message.reply_text(f"🗑️ Categoría eliminada: {categoria_nombre.capitalize()}")
        else:
            await update.message.reply_text("⚠️ Categoría no encontrada.")
    else:
        await update.message.reply_text("⚠️ Usa: /eliminar_categoria [nombre]")

# 📂 Listar categorías disponibles
async def listar_categorias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    categorias = db.obtener_categorias(user_id)
    
    if not categorias:
        await update.message.reply_text("No tienes categorías creadas aún.")
        return

    mensaje = "📂 *Tus categorías:*\n"
    for nombre, num_productos in categorias:
        mensaje += f"\n- {nombre.capitalize()} ({num_productos} producto{'s' if num_productos != 1 else ''})"
    
    await update.message.reply_text(mensaje)

# ➕ Añadir producto con categoría
async def anadir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usa: /anadir [producto] [categoria]")
        return

    producto_nombre = ' '.join(context.args[:-1]).lower()
    categoria_nombre = context.args[-1].lower()
    
    if db.agregar_producto(user_id, categoria_nombre, producto_nombre):
        await update.message.reply_text(f"✅ Añadido: {producto_nombre.capitalize()} en {categoria_nombre.capitalize()}")
    else:
        await update.message.reply_text("⚠️ Categoría no encontrada o producto ya existe.")

# ❌ Quitar producto
async def quitar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usa: /quitar [producto] [categoria]")
        return

    producto_nombre = ' '.join(context.args[:-1]).lower()
    categoria_nombre = context.args[-1].lower()
    
    if db.eliminar_producto(user_id, categoria_nombre, producto_nombre):
        await update.message.reply_text(f"❌ Eliminado: {producto_nombre.capitalize()} de {categoria_nombre.capitalize()}")
    else:
        await update.message.reply_text("⚠️ Producto o categoría no encontrado.")

# 📋 Listar productos
async def listar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    productos = db.obtener_productos(user_id)
    
    if not productos:
        await update.message.reply_text("Tu lista de compras está vacía.")
        return

    mensaje = "📝 *Tu lista de compras:*\n"
    current_categoria = None
    
    for categoria_nombre, producto_nombre, comprado in productos:
        if categoria_nombre != current_categoria:
            mensaje += f"\n📁 *{categoria_nombre.capitalize()}*:\n"
            current_categoria = categoria_nombre
        mensaje += f"  - {producto_nombre.capitalize()} {'✅' if comprado else '❌'}\n"
    
    await update.message.reply_text(mensaje)

# ✅ Marcar producto
async def marcar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    
    if len(context.args) < 3:
        await update.message.reply_text("⚠️ Usa: /marcar [producto] [categoria] [si/no]")
        return

    producto_nombre = ' '.join(context.args[:-2]).lower()
    categoria_nombre = context.args[-2].lower()
    estado_str = context.args[-1].lower()
    nuevo_estado = estado_str in ("si", "true", "1", "sí")
    
    if db.marcar_producto(user_id, categoria_nombre, producto_nombre, nuevo_estado):
        await update.message.reply_text(
            f"📝 Estado actualizado:\n{producto_nombre.capitalize()} en {categoria_nombre.capitalize()} → {'✅ Comprado' if nuevo_estado else '❌ Pendiente'}"
        )
    else:
        await update.message.reply_text("⚠️ Producto o categoría no encontrado.")

# 📖 Ayuda actualizada
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = '''
🛒 *Bot de Compras* - Comandos disponibles:

- /nueva_categoria [nombre] → Crea una nueva categoría
- /eliminar_categoria [nombre] → Elimina una categoría entera
- /categorias → Lista todas tus categorías
- /anadir [producto] [categoria] → Añade un producto
- /quitar [producto] [categoria] → Elimina un producto
- /listar → Muestra tu lista completa
- /marcar [producto] [categoria] [si/no] → Cambia el estado
- /ayuda → Muestra este mensaje

*Nota:* Cada usuario tiene su propia lista independiente.
'''
    await update.message.reply_text(help_text)

# 🔄 Registro de comandos
def run_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("nueva_categoria", nueva_categoria))
    application.add_handler(CommandHandler("eliminar_categoria", eliminar_categoria))
    application.add_handler(CommandHandler("categorias", listar_categorias))
    application.add_handler(CommandHandler("anadir", anadir))
    application.add_handler(CommandHandler("quitar", quitar))
    application.add_handler(CommandHandler("listar", listar))
    application.add_handler(CommandHandler("marcar", marcar))
    application.add_handler(CommandHandler("ayuda", ayuda))
    application.add_handler(CommandHandler("start", ayuda))

    print("Bot en ejecución... Presiona Ctrl+C para detener")
    application.run_polling()

if __name__ == "__main__":
    run_bot()