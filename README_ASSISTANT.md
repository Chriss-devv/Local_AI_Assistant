# 🤖 AI Assistant v7.82

Un asistente de IA personalizable con búsqueda web contextual, enriquecimiento inteligente de queries y auto-guardado.

![Version](https://img.shields.io/badge/version-7.82-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ Características

### 🎯 Personalización Completa
- **Wizard de configuración** en primera ejecución
- Nombre personalizable del asistente y usuario
- Rol y personalidad customizable
- Directorio de logs configurable
- Intervalo de auto-guardado ajustable

### 🌐 Búsqueda Web Contextual (v7.82)
- **Enriquecimiento inteligente**: "busca mejorarlo" → "busca mejorar código Python"
- **Contexto conversacional**: Incluye últimos 3 intercambios automáticamente
- **Queries optimizadas**: Detecta referencias vagas y las enriquece
- **Implementación directa**: Genera código basándose en búsquedas

### 📅 Conciencia Temporal
- Sabe qué día es HOY, AYER y MAÑANA
- Prioriza información del año actual (2026)
- Solicita búsquedas web para eventos recientes

### 💾 Auto-Guardado Inteligente
- Guarda sesiones automáticamente cada N mensajes
- Logs en formato Markdown
- Historial completo de conversaciones

### 📝 Modo Multi-Línea
- Pega código completo usando ` ``` `
- Preserva indentación y formato
- Perfecto para revisar/mejorar código

### 🔄 Hot-Swapping de Modelos
- Cambia modelo en medio de conversación
- Preserva todo el historial
- Soporta cualquier modelo de Ollama

---

## 🚀 Instalación

### Requisitos Previos

```bash
# 1. Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Descargar un modelo
ollama pull llama3.2:latest
# o
ollama pull mistral:latest
```

### Instalación del Asistente

```bash
# Clonar repositorio
git clone https://github.com/[tu-usuario]/ai-assistant.git
cd ai-assistant

# Instalar dependencias
pip install ollama ddgs

# Ejecutar por primera vez (wizard de configuración)
python3 assistant.py
```

---

## 📖 Uso

### Primera Ejecución

Al ejecutar por primera vez, verás el wizard de configuración:

```
🤖 CONFIGURACIÓN INICIAL - AI Assistant v7.82
============================================================

Bienvenido! Vamos a personalizar tu asistente.

¿Cómo quieres llamar a tu asistente? [Assistant]: Jarvis
¿Cuál es tu nombre? [User]: Chris

¿Qué rol debe tener tu asistente?
  1. Asistente técnico/programación
  2. Asistente general/conversacional
  3. Tutor educativo
  4. Personalizado
Selecciona [1-4]: 1

✅ Configuración guardada!
```

### Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `salir` / `exit` | Termina y guarda sesión |
| `limpiar` | Borra memoria de conversación |
| `guardar` | Guarda sesión manualmente |
| `modelo` | Cambia modelo (preserva historial) |
| `modelos` | Lista modelos disponibles |
| `buscar <query>` | Búsqueda web manual |
| ` ``` ` | Modo multi-línea (terminar con ```) |
| `config` | Reconfigurar asistente |

---

## 🎮 Ejemplos de Uso

### Ejemplo 1: Búsqueda Web Contextual

```
User> dame un código para escanear red con Python

[Assistant]: Aquí tienes un script con Scapy...
```python
import scapy.all as scapy
...
```

User> busca como mejorarlo
🌐 [Buscando]: 'busca como mejorarlo'...
   💡 Query mejorada: 'como mejorar código Python escanear red'
   📋 Con contexto conversacional
   Se encontraron 10 resultados

[Assistant]: Basándome en los resultados, aquí está el código mejorado:
```python
import scapy.all as scapy
import argparse
# [código mejorado completo]
```
✅ Ahora entiende el contexto y genera solución!
```

### Ejemplo 2: Modo Multi-Línea

```
User> ```
📝 Modo multi-línea activado...
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
```
✓ Código capturado (4 líneas)

User> optimiza esto
[Assistant]: Aquí está optimizado con memoización...
```

### Ejemplo 3: Cambio de Modelo

```
User> modelo

Modelo actual: llama3.2:latest

Modelos disponibles:
------------------------------------------------------------
► 1. llama3.2:latest                   (2.02 GB)
  2. mistral:latest                    (4.11 GB)
  3. codellama:latest                  (3.83 GB)
------------------------------------------------------------

Selecciona nuevo modelo [1-3]: 2
✓ Historial de conversación preservado
```

---

## ⚙️ Configuración

La configuración se guarda en `~/.ai_assistant/config.json`:

```json
{
  "assistant_name": "Assistant",
  "user_name": "User",
  "timezone": "America/Mexico_City",
  "logs_dir": "/home/user/.ai_assistant/logs",
  "max_messages_context": 20,
  "auto_save_interval": 10,
  "assistant_role": "asistente de IA",
  "user_expertise": "usuario técnico",
  "language": "español",
  "temperature": 0.7,
  "top_p": 0.9,
  "num_ctx": 8192,
  "num_predict": 800
}
```

### Parámetros Editables

- **assistant_name**: Nombre del asistente
- **user_name**: Tu nombre
- **logs_dir**: Directorio de logs
- **max_messages_context**: Ventana deslizante de contexto
- **auto_save_interval**: Auto-guardar cada N mensajes
- **assistant_role**: Rol del asistente
- **temperature**: Creatividad (0.0 = determinista, 1.0 = creativo)
- **top_p**: Diversidad de respuestas
- **num_ctx**: Tokens de contexto
- **num_predict**: Tokens máximos de respuesta

---

## 📂 Estructura de Archivos

```
~/.ai_assistant/
├── config.json          # Configuración personalizada
└── logs/               # Logs de sesiones
    ├── session_20260104_120000.md
    ├── session_20260104_130000.md
    └── ...
```

### Formato de Logs

```markdown
# Sesión de Assistant - 2026-01-04 12:00:00

**Usuario**: User  
**Modelo**: llama3.2:latest  
**Mensajes**: 15  
**Cambios de modelo**: 0

---

## Conversación

### > User (Mensaje #1)
Hola

### [Assistant] Respuesta #1
¡Hola! ¿En qué puedo ayudarte?
```

---

## 🐛 Troubleshooting

### Error: "No se encontraron modelos instalados"

```bash
# Solución: Instalar un modelo
ollama pull llama3.2:latest
```

### Error: "¿Está Ollama corriendo?"

```bash
# Solución: Iniciar Ollama
ollama serve
# o verificar
ollama list
```

### Error: "ModuleNotFoundError: No module named 'ddgs'"

```bash
# Solución: Instalar dependencia
pip install ddgs
```

---

## 🔧 Desarrollo

### Testing

```bash
# Verificar sintaxis
python3 -m py_compile assistant.py

# Ejecutar en modo debug
python3 assistant.py
```

### Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Añade nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📊 Changelog

### v7.82 (2026-01-04)
- ✨ Enriquecimiento inteligente de queries
- 🎯 System prompt con acción directa
- 💡 Genera código basándose en búsquedas
- 🐛 Fix: Pasividad al recibir datos de búsqueda

### v7.8 (2026-01-04)
- 🔍 Enriquecimiento de queries vagas
- 💡 "mejorarlo" → "como mejorar [contexto]"
- 📋 Feedback visual de query mejorada

### v7.75 (2026-01-04)
- 🌐 Búsqueda contextual universal
- 📋 Contexto en TODAS las búsquedas
- ✨ Nueva función `extraer_contexto_conversacional()`

### v7.7 (2026-01-04)
- 📅 Contexto temporal mejorado
- ⏰ HOY/AYER/MAÑANA explícitos
- 🐛 Fix: Variables de fecha correctamente expandidas

### v7.65 (2026-01-04)
- 🔍 Búsqueda contextual (comando manual)
- 💾 Auto-guardado cada 10 mensajes

### v7.6 (2026-01-03)
- 📝 Modo multi-línea con ` ``` `
- 🔄 Hot-swapping de modelos
- 🔍 Auto-búsqueda inteligente

---

## 📄 Licencia

MIT License - Úsalo, modifícalo, compártelo libremente.

---

## 🙏 Agradecimientos

- **Ollama Team** - Por la plataforma de LLM local
- **DuckDuckGo** - Por la API de búsqueda
- Basado en **Jarvis** by Chris (@UPSLP)

---

## 📞 Soporte

¿Problemas o sugerencias?

1. Abre un [issue en GitHub](https://github.com/[tu-usuario]/ai-assistant/issues)
2. Revisa la [documentación](#uso)
3. Consulta el [troubleshooting](#troubleshooting)

---

**🚀 AI Assistant v7.82 - Tu asistente personalizable con IA local**
