Inventario Familiar Bot
Un bot de Telegram para organizar el inventario de tu casa de forma colaborativa. Ideal para familias o compañeros de piso para saber lo que hay, lo que falta y lo que sobra.
<img width="100" height="40" alt="image" src="https://github.com/user-attachments/assets/80895447-3a16-4188-9249-287c3e065011" />
<img width="100" height="40" alt="image" src="https://github.com/user-attachments/assets/036dbcba-8635-4b23-8d77-975a5531f8fd" />
<img width="100" height="40" alt="image" src="https://github.com/user-attachments/assets/465ab5f2-8dde-4a54-aa9f-928ee405fbe0" />


🎯 Contexto y Problema
El Problema Real
En hogares compartidos (familias, roommates), la gestión de inventario suele ser caótica:

❌ Compras duplicadas: "¿Ya teníamos café?"

❌ Descoordinación: "¿Quién usó el último rollo de papel?"

❌ Listas desactualizadas: Notas en la nevera que nadie actualiza

❌ Falta de visibilidad: No saber qué hay realmente en la alacena

Nuestra Solución
Un bot de Telegram que centraliza la información del inventario familiar, accessible para todos los miembros desde sus celulares, con actualizaciones en tiempo real.

🧠 Decisiones Técnicas y Arquitectura
🔧 Stack Tecnológico Elegido
Tecnología	Decisión	Justificación
Python	Lenguaje principal	Maduro, amplio ecosistema para bots, fácil mantenimiento
python-telegram-bot	Framework del bot	Oficial, bien documentado, soporte activo
SQLite	Base de datos	Zero-config, perfecta para single-instance, bajo overhead
POO	Paradigma	Mejor testabilidad, mantenibilidad y escalabilidad
🏗️ Arquitectura del Sistema
Diagram
Code







🤔 Trade-offs Considerados
✅ SQLite vs PostgreSQL
Opción	Ventaja	Desventaja	Decisión
SQLite	Zero-config, portable	Escalabilidad limitada	✅ Elegido
PostgreSQL	Mejor concurrencia	Overhead de configuración	❌ Descartado
Razón: Para el uso esperado (1 familia ≈ 10-100 ítems), SQLite es más que suficiente y simplifica el deployment.

✅ Webhook vs Polling
Opción	Ventaja	Desventaja	Decisión
Polling	Más simple de implementar	Menos eficiente	✅ Elegido
Webhook	Más eficiente	Requiere dominio SSL	❌ Descartado
Razón: Para bots pequeños, polling es suficiente y evita complejidad de infraestructura.

✅ Framework vs Raw API
Opción	Ventaja	Desventaja	Decisión
python-telegram-bot	Abstracción útil	Dependencia externa	✅ Elegido
Raw API	Menos dependencias	Más código boilerplate	❌ Descartado
Razón: El framework acelera desarrollo y provee mejores prácticas incorporadas.

🧪 Testing Strategy
📊 Coverage Actual
bash
# Estructura de tests (a implementar)
tests/
├── test_bot.py          # Tests de comandos
├── test_database.py     # Tests de DB
└── conftest.py          # Configuración
🎯 Tipos de Tests Implementados
1. Unit Tests (70% coverage goal)
python
def test_add_item():
    """Test que verifica agregar ítem a la base de datos"""
    db = Database(":memory:")  # DB en memoria para tests
    db.add_item("Leche")
    items = db.get_all_items()
    assert "Leche" in [item[1] for item in items]
2. Integration Tests (20% coverage goal)
python
def test_whole_flow():
    """Test de flujo completo: agregar → listar → eliminar"""
    db = Database(":memory:")
    # Simular interacción completa
    db.add_item("Pan")
    assert db.item_exists("Pan")
    db.delete_item("Pan")
    assert not db.item_exists("Pan")
3. Mocking de Telegram API (10% coverage goal)
python
@patch('telegram.Bot')
def test_start_command(mock_bot):
    """Test del comando /start usando mocks"""
    update = Mock()
    context = Mock()
    
    # Ejecutar comando
    start_command(update, context)
    
    # Verificar que se envió mensaje
    update.message.reply_text.assert_called_with("¡Bienvenido al inventario familiar!")
🔄 CI/CD Integration
yaml
# .github/workflows/test.yml (planificado)
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest tests/ -v
      - name: Coverage report
        run: python -m pytest tests/ --cov=./ --cov-report=xml
🚀 Demo y Casos de Uso
📱 Flujo de Uso Típico
<img width="871" height="532" alt="image" src="https://github.com/user-attachments/assets/70575dd2-2ab5-474f-a6f0-4db86403b46c" />

🎥 Demo en Video
(Incluir GIF mostrando el bot en funcionamiento)

🔢 Métricas de Performance
Operación	Tiempo Esperado	Notas
/start	<100ms	Solo mensaje estático
/agregar	<200ms	Inserción en DB
/listar	<300ms	Query + formateo
Concurrent users	10-20	Límite de polling de Telegram
📈 Roadmap y Mejoras Futuras
🎯 Próximas Features
Categorías - Organizar ítems por categorías (limpieza, comida, etc.)

Cantidades - Soporte para cantidades y unidades ("2kg de arroz")

Notificaciones - Alertas cuando items están por acabarse

Múltiples inventarios - Soporte para varias familias/lugares

🔧 Mejoras Técnicas
Migración a async/await - Mejor performance con python-telegram-bot[v20]

Dockerización - Más fácil deployment

Monitoring - Health checks y métricas

Backups automáticos - De la base de datos SQLite

🤝 Cómo Contribuir
¡Las contribuciones son bienvenidas! Para contribuir:

Haz fork del proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

🎯 Areas que Necesitan Ayuda
✅ Tests automatizados

✅ Documentación

✅ Internacionalización (i18n)

✅ Nuevos comandos útiles


Contacta por Telegram: @mbus31

¿Te gusta el proyecto? ¡Dale una estrella ⭐ al repositorio!


