# AgentTracker: Middleware di Monitoraggio per Agenti AI

Un sistema completo per tracciare, monitorare e analizzare le interazioni tra agenti AI (come CrewAI, AutoGen, ecc.) con rilevamento automatico di loop di comunicazione e calcolo dei costi.

## 🎯 Caratteristiche Principali

### 1. **Tracciamento dei Messaggi**
- Memorizza cronologia completa dei messaggi scambiati
- Registra mittente, destinatario, contenuto, timestamp e token consumati
- Query flessibili sulla cronologia

### 2. **Rilevamento Intelligente di Loop**
- **Algoritmo avanzato** che analizza i pattern nei messaggi
- Rileva messaggi identici o molto simili (configurable similarity threshold)
- Segnala ripetizioni consecutive (default: 3+ ripetizioni)
- Eccezione o avvertimento configurabile

### 3. **Calcolo dei Costi**
- Stima del costo della sessione basata sui token consumati
- Supporto per multipli modelli (GPT-4, GPT-3.5-turbo, custom)
- Breakdown tra costi input/output

### 4. **Analisi e Reporting**
- Riepilogo completo della sessione
- Esportazione della conversazione in file
- Statistiche per agente

---

## 📦 Installazione

### Requisiti
- Python 3.8+
- Nessuna dipendenza esterna (libreria standard)

### Setup
```bash
# Clone o copia i file nel tuo progetto
git clone <repository>
cd LoopHalter

# (Opzionale) Crea un virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

---

## 🚀 Uso Rapido

### Esempio Base
```python
from agent_tracker import AgentTracker, LoopDetectionException

# Crea un tracker
tracker = AgentTracker()

# Aggiungi messaggi
try:
    tracker.add_message(
        sender="Agent_A",
        recipient="Agent_B",
        content="Qual è il significato della vita?",
        tokens_used=150
    )
    
    tracker.add_message(
        sender="Agent_B",
        recipient="Agent_A",
        content="La risposta è 42",
        tokens_used=120
    )
    
except LoopDetectionException as e:
    print(f"❌ Loop rilevato: {e}")

# Ottieni il costo stimato
cost = tracker.estimate_session_cost(model="gpt-3.5-turbo")
print(f"💰 Costo totale: ${cost['total_cost']:.6f}")

# Riepilogo della sessione
summary = tracker.get_conversation_summary()
print(f"📊 Messaggi totali: {summary['total_messages']}")
```

---

## 📚 API Dettagliata

### Classe: `AgentTracker`

#### Inizializzazione
```python
tracker = AgentTracker(
    max_loop_repetitions=3,      # Numero max di ripetizioni prima del loop
    similarity_threshold=0.85     # Soglia di similarità (0-1)
)
```

#### Metodo: `add_message()`
Aggiunge un messaggio e verifica la presenza di loop.

```python
result = tracker.add_message(
    sender: str,              # ID agente mittente
    recipient: str,           # ID agente destinatario
    content: str,             # Contenuto del messaggio
    tokens_used: int = 0,     # Token consumati (opzionale)
    raise_on_loop: bool = True # Sollevare eccezione se loop rilevato
)

# Ritorna:
# {
#     "status": "success",
#     "message_count": int,
#     "loop_detected": bool,
#     "warning_message": str,
#     "loop_info": {
#         "detected": bool,
#         "message": str,
#         "repetitions": int,
#         "similar_messages": list
#     }
# }
```

#### Metodo: `estimate_session_cost()`
Calcola il costo stimato della sessione.

```python
cost = tracker.estimate_session_cost(model="gpt-3.5-turbo")

# Ritorna:
# {
#     "total_cost": float,      # Costo totale in USD
#     "input_cost": float,      # Costo input
#     "output_cost": float,     # Costo output
#     "total_tokens": int,      # Token totali
#     "input_tokens": int,
#     "output_tokens": int,
#     "model": str
# }
```

**Modelli Supportati:**
- `"gpt-4"` - GPT-4 (più costoso, più potente)
- `"gpt-3.5-turbo"` - GPT-3.5 Turbo (standard)
- `"default"` - Modello generico

#### Metodo: `get_message_history()`
Recupera la cronologia dei messaggi con filtri opzionali.

```python
# Tutti i messaggi
all_messages = tracker.get_message_history()

# Filtrare per mittente
from_agent_a = tracker.get_message_history(sender="Agent_A")

# Filtrare per destinatario
to_agent_b = tracker.get_message_history(recipient="Agent_B")

# Filtrare per entrambi
conversation = tracker.get_message_history(
    sender="Agent_A",
    recipient="Agent_B"
)
```

#### Metodo: `get_conversation_summary()`
Fornisce un riepilogo completo della sessione.

```python
summary = tracker.get_conversation_summary()
print(summary)
# {
#     "total_messages": 5,
#     "agents_involved": ["Agent_A", "Agent_B", "Agent_C"],
#     "session_duration_seconds": 42.5,
#     "loop_detected": False,
#     "total_tokens": 750,
#     "estimated_cost": {...},
#     "message_count_by_agent": {"Agent_A": 3, "Agent_B": 2},
#     "start_time": "2024-06-18T10:30:00",
#     "end_time": "2024-06-18T10:30:42"
# }
```

#### Metodo: `export_conversation()`
Esporta la conversazione in un file di testo.

```python
filename = tracker.export_conversation("conversation_log.txt")
print(f"Esportato in: {filename}")
```

#### Metodo: `reset_session()`
Resetta lo stato della sessione e cancella la cronologia.

```python
tracker.reset_session()
# Ora il tracker è pulito e pronto per una nuova sessione
```

---

## 🔍 Algoritmo di Rilevamento Loop

### Come Funziona
1. **Estrazione**: Estrae gli ultimi N messaggi tra due agenti (bidirezionale)
2. **Calcolo Similarità**: Usa `difflib.SequenceMatcher` per calcolare la similarità
3. **Pattern Analysis**: Rileva pattern ripetitivi
4. **Segnalazione**: Se trovati 3+ messaggi simili consecutivi (configurable):
   - ✅ Opzione 1: Solleva `LoopDetectionException`
   - ⚠️ Opzione 2: Emette avvertimento

### Parametri Configurabili
```python
tracker = AgentTracker(
    max_loop_repetitions=3,    # Numero di ripetizioni prima di avviso
    similarity_threshold=0.85   # Soglia similarità (0.0 = diversi, 1.0 = identici)
)
```

### Esempio di Rilevamento
```python
# Questi messaggi attiveranno il loop detector
messages = [
    "Puoi ripetere la domanda?",
    "Puoi ripetere la domanda?",
    "Puoi ripetere la domanda?",  # ⚠️ Loop rilevato!
]

for msg in messages:
    result = tracker.add_message(
        sender="Agent_A",
        recipient="Agent_B",
        content=msg,
        raise_on_loop=False  # Non sollevare eccezione, solo avviso
    )
    
    if result["loop_detected"]:
        print(f"⚠️ {result['warning_message']}")
        print(f"   Ripetizioni: {result['loop_info']['repetitions']}")
```

---

## 💰 Sistema di Costo

### Modelli di Costo Predefiniti
| Modello | Input (per 1K token) | Output (per 1K token) |
|---------|----------------------|----------------------|
| GPT-4 | $0.03 | $0.06 |
| GPT-3.5-Turbo | $0.50 | $1.50 |
| Default | $0.01 | $0.02 |

### Personalizzazione
```python
# I costi sono calcolati come:
# - 80% input tokens (default)
# - 20% output tokens (default)

cost = tracker.estimate_session_cost(model="gpt-4")
print(f"Input cost: ${cost['input_cost']:.6f}")
print(f"Output cost: ${cost['output_cost']:.6f}")
print(f"Total: ${cost['total_cost']:.6f}")
```

---

## 🧪 Testing

### Eseguire i Test
```bash
# Esegui tutti i test
python -m unittest test_agent_tracker -v

# O
python test_agent_tracker.py

# Esegui test specifici
python -m unittest test_agent_tracker.TestLoopDetection -v
```

### Copertuta di Test
- ✅ 8 classi di test
- ✅ 30+ test unitari
- ✅ Copertuta completa delle funzionalità

### Argomenti Testati
- Creazione di messaggi
- Aggiunta di messaggi singoli e multipli
- Rilevamento di loop (identici e simili)
- Eccezioni
- Calcolo dei costi
- Filtraggio messaggi
- Riepilogo sessione
- Reset e esportazione

---

## 🔧 Integrazione con CrewAI

### Esempio di Integrazione
```python
from crewai import Agent, Task, Crew
from agent_tracker import AgentTracker

# Crea il tracker
tracker = AgentTracker()

# Crea agenti CrewAI normalmente
agent1 = Agent(name="Agent_A", role="Analyst", ...)
agent2 = Agent(name="Agent_B", role="Writer", ...)

# Crea un wrapper per intercettare i messaggi
class TrackedCrew(Crew):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracker = tracker
    
    def log_interaction(self, sender, recipient, message, tokens=0):
        try:
            self.tracker.add_message(
                sender=sender,
                recipient=recipient,
                content=message,
                tokens_used=tokens
            )
        except LoopDetectionException as e:
            print(f"❌ {e}")
            # Gestisci il loop (interrompi l'esecuzione, ecc.)

# Usa il tracker durante l'esecuzione
crew = TrackedCrew(agents=[agent1, agent2], tasks=[...])

# Log manuale (o integra con hooks CrewAI)
crew.log_interaction("Agent_A", "Agent_B", "Ciao!", tokens=50)
```

---

## 📊 Esempio Completo

```python
from agent_tracker import AgentTracker, LoopDetectionException

# Inizializza il tracker
tracker = AgentTracker(max_loop_repetitions=3, similarity_threshold=0.85)

print("🚀 Simulazione di interazione tra agenti\n")

# Simulazione di una conversazione
interactions = [
    ("Agent_Research", "Agent_Writing", 
     "Ho trovato questi articoli su Python", 100),
    ("Agent_Writing", "Agent_Research", 
     "Puoi trovare di più su async/await?", 80),
    ("Agent_Research", "Agent_Writing", 
     "Ecco 5 articoli su async/await in Python", 120),
    ("Agent_Writing", "Agent_Research", 
     "Ottimo, ora scrivo un articolo", 90),
    ("Agent_Research", "Agent_Writing", 
     "Perfetto, aspetto il tuo feedback", 70),
]

try:
    for sender, recipient, message, tokens in interactions:
        result = tracker.add_message(
            sender=sender,
            recipient=recipient,
            content=message,
            tokens_used=tokens
        )
        print(f"✓ {sender} → {recipient}: {message[:40]}...")

except LoopDetectionException as e:
    print(f"\n❌ ERRORE: {e}")

# Mostra il riepilogo
print("\n" + "="*80)
print("📊 RIEPILOGO SESSIONE")
print("="*80)

summary = tracker.get_conversation_summary()
for key, value in summary.items():
    if key != "estimated_cost":
        print(f"  {key}: {value}")

# Mostra il costo
print("\n💰 ANALISI COSTI")
print("="*80)
cost = tracker.estimate_session_cost(model="gpt-3.5-turbo")
print(f"  Modello: {cost['model']}")
print(f"  Token totali: {cost['total_tokens']}")
print(f"  Costo input: ${cost['input_cost']:.6f}")
print(f"  Costo output: ${cost['output_cost']:.6f}")
print(f"  COSTO TOTALE: ${cost['total_cost']:.6f}")

# Esporta il log
print("\n📄 ESPORTAZIONE")
print("="*80)
filename = tracker.export_conversation("session_log.txt")
print(f"  Log esportato in: {filename}")
```

---

## 📝 Note di Implementazione

### Architettura
```
AgentTracker (classe principale)
├── Message (dataclass per messaggi)
├── _check_for_loops() (rilevamento loop)
├── _analyze_message_patterns() (analisi pattern)
├── _calculate_similarity() (similarità testi)
├── estimate_session_cost() (calcolo costi)
├── get_message_history() (query messaggi)
├── get_conversation_summary() (riepilogo)
└── export_conversation() (esportazione)
```

### Complessità Computazionale
- **Aggiunta messaggio**: O(N) dove N = messaggi totali
- **Loop detection**: O(N × M) dove M = lunghezza media messaggi
- **Cost calculation**: O(N)
- **Query**: O(N)

### Limitazioni Attuali
- Non supporta media (immagini, audio)
- Similarità basata su testo (non semantica)
- Token usage deve essere fornito manualmente
- Cost estimation assume split 80/20 input/output

---

## 🛠️ Troubleshooting

### Q: Il loop detector è troppo sensibile
**A**: Aumenta `similarity_threshold` o `max_loop_repetitions`:
```python
tracker = AgentTracker(max_loop_repetitions=5, similarity_threshold=0.95)
```

### Q: I costi non sono accurati
**A**: Fornisci i token effettivi consumati:
```python
tracker.add_message(
    sender="Agent_A",
    recipient="Agent_B",
    content="Message",
    tokens_used=150  # Usa il token count dal modello
)
```

### Q: Come integro con il mio framework?
**A**: Intercetta le comunicazioni e log via `add_message()`:
```python
def log_agent_communication(sender, recipient, msg, tokens):
    tracker.add_message(sender, recipient, msg, tokens, raise_on_loop=False)
```

---

## 📄 Licenza
MIT License - vedi LICENSE file

## 👥 Contributi
Sono benvenuti pull requests e issue reports!

---

**Versione**: 1.0.0  
**Ultimo aggiornamento**: Giugno 2024  
**Autore**: AI Development Team
