#!/usr/bin/env python3

import ollama
import sys
import time
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    from ddgs import DDGS
except ImportError:
    print("Installing web search library...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ddgs"])
    from ddgs import DDGS

CONFIG_FILE = Path.home() / ".ai_assistant" / "config.json"
DEFAULT_CONFIG = {
    "assistant_name": "Assistant",
    "user_name": "User",
    "timezone": "America/New_York",
    "logs_dir": str(Path.home() / ".ai_assistant" / "logs"),
    "max_messages_context": 20,
    "auto_save_interval": 10,
    "assistant_role": "AI assistant",
    "user_expertise": "technical user",
    "language": "English",
    "temperature": 0.7,
    "top_p": 0.9,
    "num_ctx": 8192,
    "num_predict": 800,
    "first_run": True
}

class Config:
    
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.config = self.load()
    
    def load(self):
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        return DEFAULT_CONFIG.copy()
    
    def save(self):
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def setup_wizard(self):
        print("\n" + "="*60)
        print("INITIAL SETUP - AI Assistant v7.82")
        print("="*60)
        print("\nWelcome! Let's customize your assistant.\n")
        
        nombre = input("What would you like to name your assistant? [Assistant]: ").strip()
        if nombre:
            self.config['assistant_name'] = nombre
        
        usuario = input("What is your name? [User]: ").strip()
        if usuario:
            self.config['user_name'] = usuario
        
        print("\nWhat role should your assistant have?")
        print("  1. Technical/Programming assistant")
        print("  2. General/Conversational assistant")
        print("  3. Educational tutor")
        print("  4. Custom")
        
        rol_choice = input("Select [1-4] or Enter for default: ").strip()
        if rol_choice == "1":
            self.config['assistant_role'] = "programming and technology expert"
        elif rol_choice == "2":
            self.config['assistant_role'] = "friendly conversational assistant"
        elif rol_choice == "3":
            self.config['assistant_role'] = "patient educational tutor"
        elif rol_choice == "4":
            custom_rol = input("Describe your assistant's role: ").strip()
            if custom_rol:
                self.config['assistant_role'] = custom_rol
        
        print(f"\nCurrent logs directory: {self.config['logs_dir']}")
        cambiar = input("Change location? (y/n): ").strip().lower()
        if cambiar == 'y':
            nuevo_dir = input("New path: ").strip()
            if nuevo_dir:
                self.config['logs_dir'] = nuevo_dir
        
        intervalo = input(f"\nAuto-save every how many messages? [{self.config['auto_save_interval']}]: ").strip()
        if intervalo.isdigit():
            self.config['auto_save_interval'] = int(intervalo)
        
        self.config['first_run'] = False
        self.save()
        
        print("\n" + "="*60)
        print("Configuration saved!")
        print(f"File: {self.config_file}")
        print("="*60)
        print("\nYou can manually edit the JSON file for more options.\n")
        input("Press Enter to continue...")

def obtener_modelos():
    try:
        models = ollama.list()
        if not models or 'models' not in models:
            return []
        
        model_list = []
        for model in models['models']:
            name = model.model if hasattr(model, 'model') else 'unknown'
            size = model.size if hasattr(model, 'size') else 0
            size_gb = size / (1024**3) if size > 0 else 0
            model_list.append({'name': name, 'size_gb': size_gb})
        
        return model_list
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []

def mostrar_modelos(modelos, modelo_actual=None):
    print("\nAvailable models:")
    print("-" * 60)
    
    for idx, model in enumerate(modelos, 1):
        marca = "> " if modelo_actual and model['name'] == modelo_actual else "  "
        print(f"{marca}{idx}. {model['name']:<40} ({model['size_gb']:.2f} GB)")
    
    print("-" * 60)

def seleccionar_modelo():
    print("\nFetching available Ollama models...")
    
    modelos = obtener_modelos()
    
    if not modelos:
        print("No models found installed.")
        print("Install a model with: ollama pull <model-name>")
        print("\nRecommended models:")
        print("  - ollama pull llama3.2:latest")
        print("  - ollama pull mistral:latest")
        sys.exit(1)
    
    mostrar_modelos(modelos)
    
    while True:
        try:
            choice = input(f"\nSelect a model [1-{len(modelos)}]: ").strip()
            
            if not choice:
                continue
            
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(modelos):
                selected = modelos[choice_idx]['name']
                print(f"Selected model: {selected}")
                return selected
            else:
                print(f"Invalid number. Choose between 1 and {len(modelos)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nCanceled by user")
            sys.exit(0)

def cambiar_modelo(modelo_actual):
    print(f"\nCurrent model: {modelo_actual}")
    
    modelos = obtener_modelos()
    if not modelos:
        print("Error: Could not fetch models")
        return modelo_actual
    
    mostrar_modelos(modelos, modelo_actual)
    
    while True:
        try:
            choice = input(f"\nSelect new model [1-{len(modelos)}] or Enter to cancel: ").strip()
            
            if not choice:
                print("Model change canceled")
                return modelo_actual
            
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(modelos):
                nuevo_modelo = modelos[choice_idx]['name']
                if nuevo_modelo == modelo_actual:
                    print("You're already using that model")
                    return modelo_actual
                
                print(f"\nChanging model...")
                print(f"  Previous: {modelo_actual}")
                print(f"  New: {nuevo_modelo}")
                print("  Conversation history preserved")
                return nuevo_modelo
            else:
                print(f"Invalid number. Choose between 1 and {len(modelos)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nChange canceled")
            return modelo_actual

def extraer_contexto_conversacional(messages, num_intercambios=3):
    if len(messages) <= 1:
        return ""
    
    num_mensajes = num_intercambios * 2
    recent_msgs = messages[-num_mensajes:] if len(messages) > num_mensajes else messages[1:]
    
    if not recent_msgs:
        return ""
    
    context_parts = []
    for msg in recent_msgs:
        if msg['role'] == 'user':
            content = msg['content']
            if '=== WEB SEARCH DATA' in content or '=== SEARCH RESULTS' in content:
                lines = content.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('===') and not line.startswith('IMPORTANT') and not line.startswith('CONTEXT'):
                        content = line[:100]
                        break
            else:
                content = content[:100].replace('\n', ' ')
            context_parts.append(f"User: {content}...")
        elif msg['role'] == 'assistant':
            content = msg['content'][:100].replace('\n', ' ')
            context_parts.append(f"Assistant: {content}...")
    
    if context_parts:
        return "\n".join(context_parts)
    return ""

def buscar_web(query, messages=None):
    
    queries_vagas = ['improve it', 'how to do it', 'how effective', 'more information', 'explain it', 'give examples', 'how to do']
    query_original = query
    query_es_vaga = any(vaga in query.lower() for vaga in queries_vagas)
    
    contexto = ""
    query_enriquecida = query
    
    if messages and len(messages) > 1:
        contexto = extraer_contexto_conversacional(messages)
        
        if query_es_vaga:
            for msg in reversed(messages):
                if msg['role'] == 'user' and '===' not in msg['content']:
                    keywords = msg['content'][:50].replace('\n', ' ').strip()
                    if 'improve' in query.lower():
                        query_enriquecida = f"how to improve {keywords}"
                    elif 'effective' in query.lower():
                        query_enriquecida = f"how effective is {keywords}"
                    elif 'do it' in query.lower():
                        query_enriquecida = f"how to do {keywords}"
                    else:
                        query_enriquecida = f"{keywords} {query}"
                    break
    
    if query_enriquecida != query_original:
        print(f"🌐 Searching: '{query_original}'...")
        print(f"   Enhanced query: '{query_enriquecida}'")
    else:
        print(f"🌐 Searching: '{query_enriquecida}'...")
    
    if contexto:
        print(f"   With conversational context")
    
    try:
        time.sleep(0.5)
        
        with DDGS() as ddgs:
            results = []
            try:
                for r in ddgs.text(query_enriquecida, region='en-us', safesearch='off', max_results=10):
                    results.append(r)
                    if len(results) >= 10:
                        break
            except StopIteration:
                pass
            
            if not results:
                print("   No results found")
                return (None, None) if messages else None
            
            print(f"   Found {len(results)} results")
            
            formatted = []
            for i, r in enumerate(results[:5], 1):
                title = r.get('title', 'No title')
                body = r.get('body', r.get('description', ''))
                url = r.get('href', '')
                
                formatted.append(f"{i}. **{title}**\n   {body}\n   Source: {url}")
            
            resultados = "\n\n".join(formatted)
            
            if contexto:
                return (contexto, resultados)
            else:
                return (None, resultados)
    
    except Exception as e:
        print(f"   Search error: {type(e).__name__}: {e}")
        return (None, None) if messages else None

def aplicar_sliding_window(messages, max_messages=20):
    if len(messages) <= max_messages + 1:
        return messages
    
    system_msg = messages[0]
    recent_messages = messages[-(max_messages):]
    
    print(f"[Sliding Window] Reducing context: {len(messages)} -> {len(recent_messages) + 1} messages")
    
    return [system_msg] + recent_messages

def guardar_sesion(messages, modelo, mensaje_count, cambios_modelo, config):
    try:
        log_dir = config['logs_dir']
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_{timestamp}.md"
        filepath = os.path.join(log_dir, filename)
        
        content = f"""# {config['assistant_name']} Session - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**User**: {config['user_name']}  
**Model**: {modelo}  
**Messages**: {mensaje_count}  
**Model changes**: {cambios_modelo}

---

## Conversation

"""
        
        for i, msg in enumerate(messages[1:], 1):
            role = msg['role']
            content_text = msg['content']
            
            if role == "user":
                content += f"\n### > {config['user_name']} (Message #{i//2 + 1})\n\n{content_text}\n"
            elif role == "assistant":
                content += f"\n### [{config['assistant_name']}] Response #{i//2 + 1}\n\n{content_text}\n"
        
        content += f"\n---\n\n*Session auto-saved by AI Assistant v7.82*\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\nSession saved: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"\nError saving session: {e}")
        return None

def asistente(modelo, config):
    assistant_name = config['assistant_name']
    user_name = config['user_name']
    
    print(f"\n{assistant_name} v7.82 | Customizable AI Assistant")
    print(f"User: {user_name}")
    print(f"Model: {modelo}")
    print("-" * 60)
    print("Commands:")
    print("  - 'exit' / 'quit': Terminate (auto-saves session)")
    print("  - 'clear': Clear conversation memory")
    print("  - 'save': Manually save session")
    print("  - 'model': Change model (preserves history)")
    print("  - 'models': View available models")
    print("  - 'search <query>': Force manual web search")
    print("  - '```': Start multi-line mode (end with ```)")
    print("  - 'config': Reconfigure assistant")
    print(f"{assistant_name} has contextual and intelligent web search\n")
    
    ahora = datetime.now()
    ayer = ahora - timedelta(days=1)
    manana = ahora + timedelta(days=1)
    
    fecha_hoy = ahora.strftime("%A, %B %d, %Y")
    fecha_ayer = ayer.strftime("%A, %B %d, %Y")
    fecha_manana = manana.strftime("%A, %B %d, %Y")
    
    dia_hoy = ahora.strftime("%d")
    mes_hoy = ahora.strftime("%B")
    ano_hoy = ahora.strftime("%Y")
    
    system_prompt = f"""You are {assistant_name}, the {config['assistant_role']} for {user_name}.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CURRENT TEMPORAL CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TODAY is:     {fecha_hoy}  (Day {dia_hoy} of {mes_hoy}, {ano_hoy})
YESTERDAY was:   {fecha_ayer}
TOMORROW will be: {fecha_manana}

TEMPORAL AWARENESS:
- We are in the year {ano_hoy}
- If asked about "yesterday", refer to {fecha_ayer}
- If asked about "tomorrow", refer to {fecha_manana}
- ALWAYS prioritize {ano_hoy} information over previous years
- If you don't have current data, request web search
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEHAVIOR RULES:
1. You are helpful, direct and clear in your responses
2. You speak {config['language']} with {user_name}
3. Your expertise level adapts to: {config['user_expertise']}
4. YOU HAVE MEMORY: You remember this entire conversation

WEB SEARCH CAPABILITY:
If you DON'T know specific information, new terms, updated data, recent events or anything outside your training data, you can request a web search.

To request search, respond ONLY:
SEARCH: <your query>

WEB SEARCH RULES (v7.82 - DIRECT ACTION):
1. If you receive WEB SEARCH DATA, use it as primary source
2. When search data has code/examples, IMPLEMENT the solution directly
3. DO NOT be passive saying "check the resources" - GENERATE the improved code YOURSELF
4. If search has code examples, USE THEM to create a complete implementation
5. Combine multiple search resources to create the best solution

RESPONSE FORMAT:
- Always in {config['language']}
- Be concise and technical
- Provide code when relevant
- GENERATE code based on searches, not just summaries
- If search data has code, IMPLEMENT it directly
"""
    
    messages = [{"role": "system", "content": system_prompt}]
    mensaje_count = 0
    cambios_modelo = 0
    max_messages = config['max_messages_context']
    auto_save_interval = config['auto_save_interval']
    
    while True:
        try:
            user_input = input(f"\n{user_name}> ").strip()
            
            if user_input.startswith("```"):
                print("Multi-line mode activated. End with ``` on separate line.")
                lines = []
                first_line = user_input[3:].strip()
                if first_line:
                    lines.append(first_line)
                
                while True:
                    try:
                        line = input()
                        if line.strip() == "```":
                            break
                        lines.append(line)
                    except EOFError:
                        print("\nIncomplete block (missing ```)")
                        break
                
                user_input = "\n".join(lines)
                print(f"Code captured ({len(lines)} lines)\n")
            
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                print(f"\nSaving session...")
                guardar_sesion(messages, modelo, mensaje_count, cambios_modelo, config)
                print(f"Goodbye, {user_name}! ({mensaje_count} messages)")
                break
            
            if user_input.lower() in ["clear", "reset"]:
                messages = [{"role": "system", "content": system_prompt}]
                mensaje_count = 0
                print("Memory cleared")
                continue
            
            if user_input.lower() == "save":
                guardar_sesion(messages, modelo, mensaje_count, cambios_modelo, config)
                continue
            
            if user_input.lower() in ["model", "switch"]:
                nuevo_modelo = cambiar_modelo(modelo)
                if nuevo_modelo != modelo:
                    modelo = nuevo_modelo
                    cambios_modelo += 1
                continue
            
            if user_input.lower() == "models":
                modelos = obtener_modelos()
                mostrar_modelos(modelos, modelo)
                continue
            
            if user_input.lower() == "config":
                print("\nReconfiguring assistant...")
                cfg = Config()
                cfg.setup_wizard()
                config = cfg.config
                print("Restart assistant to apply changes")
                continue
            
            if user_input.lower().startswith("search "):
                query = user_input[7:].strip()
                if query:
                    result = buscar_web(query, messages)
                    
                    if result and result[1]:
                        contexto_prev, resultados = result
                        
                        web_context = f"""=== WEB SEARCH DATA ===
Query: {query}
"""
                        if contexto_prev:
                            web_context += f"\nCONTEXT:\n{contexto_prev}\n"
                        
                        web_context += f"""
Results:
{resultados}
=== END DATA ===

IMPORTANT: Use context and data to respond.
"""
                        user_message = web_context
                        messages.append({"role": "user", "content": user_message})
                        messages = aplicar_sliding_window(messages, max_messages)
                        
                        print(f"[{assistant_name}] processing...")
                        
                        try:
                            response = ollama.chat(
                                model=modelo,
                                messages=messages,
                                stream=True,
                                options={
                                    'temperature': config['temperature'],
                                    'top_p': config['top_p'],
                                    'num_ctx': config['num_ctx'],
                                    'num_predict': config['num_predict'],
                                }
                            )
                            
                            print(f"\n[{assistant_name}] (#{mensaje_count + 1}): ", end="", flush=True)
                            assistant_message = ""
                            
                            for chunk in response:
                                if 'message' in chunk and 'content' in chunk['message']:
                                    content = chunk['message']['content']
                                    print(content, end="", flush=True)
                                    assistant_message += content
                            
                            print("\n")
                            messages.append({"role": "assistant", "content": assistant_message})
                            mensaje_count += 1
                        except Exception as e:
                            print(f"\nError: {e}")
                            if messages[-1]["role"] == "user":
                                messages.pop()
                    else:
                        print("Could not perform search")
                continue
            
            search_keywords = ["search", "look up", "find", "explain what is", "tell me what is"]
            needs_search = any(kw in user_input.lower() for kw in search_keywords)
            
            web_context = ""
            if needs_search:
                result = buscar_web(user_input, messages)
                if result and result[1]:
                    contexto_prev, resultados = result
                    web_context = f"""=== WEB SEARCH DATA ===
Query: {user_input}
"""
                    if contexto_prev:
                        web_context += f"\nCONTEXT:\n{contexto_prev}\n"
                    
                    web_context += f"""
Results:
{resultados}
=== END ===

IMPORTANT: Based on context and search, provide clear response.
"""
            
            user_message = f"{web_context}\n\n{user_input}" if web_context else user_input
            messages.append({"role": "user", "content": user_message})
            messages = aplicar_sliding_window(messages, max_messages)
            
            print(f"[{assistant_name}] processing...")
            
            try:
                response = ollama.chat(
                    model=modelo,
                    messages=messages,
                    stream=True,
                    options={
                        'temperature': config['temperature'],
                        'top_p': config['top_p'],
                        'num_ctx': config['num_ctx'],
                        'num_predict': config['num_predict'],
                    }
                )
                
                print(f"\n[{assistant_name}] (#{mensaje_count + 1}): ", end="", flush=True)
                assistant_message = ""
                
                for chunk in response:
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        print(content, end="", flush=True)
                        assistant_message += content
                
                print("\n")
                
                if assistant_message.strip().startswith("SEARCH:"):
                    search_query = assistant_message.replace("SEARCH:", "").strip()
                    print(f"[Auto-Search] Requested: '{search_query}'")
                    
                    result = buscar_web(search_query, messages)
                    
                    if result and result[1]:
                        contexto_prev, resultados = result
                        messages.pop()
                        
                        search_context = f"""=== AUTO-SEARCH DATA ===
Original query: {user_input}
Search: {search_query}
"""
                        if contexto_prev:
                            search_context += f"\nCONTEXT:\n{contexto_prev}\n"
                        
                        search_context += f"""
Results:
{resultados}
=== END ===

NOW respond using this data.
"""
                        messages.append({"role": "user", "content": search_context})
                        
                        print(f"\n[Reprocessing with web data...]")
                        print(f"[{assistant_name}] processing...")
                        
                        try:
                            retry_response = ollama.chat(
                                model=modelo,
                                messages=messages,
                                stream=True,
                                options={
                                    'temperature': config['temperature'],
                                    'top_p': config['top_p'],
                                    'num_ctx': config['num_ctx'],
                                    'num_predict': config['num_predict'],
                                }
                            )
                            
                            print(f"\n[{assistant_name}] (#{mensaje_count + 1}): ", end="", flush=True)
                            final_message = ""
                            
                            for chunk in retry_response:
                                if 'message' in chunk and 'content' in chunk['message']:
                                    content = chunk['message']['content']
                                    print(content, end="", flush=True)
                                    final_message += content
                            
                            print("\n")
                            
                            messages.pop()
                            messages.append({"role": "assistant", "content": final_message})
                            mensaje_count += 1
                            
                        except Exception as e:
                            print(f"\nError reprocessing: {e}")
                            messages.pop()
                    else:
                        mensaje_count += 1
                else:
                    messages.append({"role": "assistant", "content": assistant_message})
                    mensaje_count += 1
                    
                    if mensaje_count % auto_save_interval == 0:
                        print(f"\n[Auto-save] Saving session (message #{mensaje_count})...")
                        guardar_sesion(messages, modelo, mensaje_count, cambios_modelo, config)
                
            except Exception as e:
                print(f"\nModel error: {e}")
                print("Is Ollama running? Check with: ollama list")
                if messages[-1]["role"] == "user":
                    messages.pop()
            
        except KeyboardInterrupt:
            print(f"\n\nInterrupted.")
            print("Saving session...")
            guardar_sesion(messages, modelo, mensaje_count, cambios_modelo, config)
            break
        except EOFError:
            print(f"\n\nSaving session...")
            guardar_sesion(messages, modelo, mensaje_count, cambios_modelo, config)
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    print("AI Assistant v7.82 - Customizable")
    print("="*60)
    
    cfg = Config()
    
    if cfg.config.get('first_run', True):
        cfg.setup_wizard()
    
    modelo_seleccionado = seleccionar_modelo()
    asistente(modelo_seleccionado, cfg.config)
