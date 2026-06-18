"""
Integrazione AgentTracker con CrewAI
====================================

Questo file dimostra come integrare l'AgentTracker con CrewAI
per monitorare le interazioni tra agenti.

NOTA: Questo è un file di ESEMPIO. Richiede CrewAI installato:
    pip install crewai
"""

from agent_tracker import AgentTracker, LoopDetectionException
from typing import Optional, Callable
import json
from datetime import datetime


class TrackedCrewAIIntegration:
    """
    Wrapper per integrare AgentTracker con CrewAI.
    
    Questo modulo fornisce decoratori e hook per loggare automaticamente
    le comunicazioni tra agenti CrewAI.
    """
    
    def __init__(self, tracker: Optional[AgentTracker] = None,
                 auto_save: bool = False, save_interval: int = 5):
        """
        Inizializza l'integrazione.
        
        Args:
            tracker: AgentTracker da utilizzare (crea uno nuovo se None)
            auto_save: Se True, salva automaticamente il log ogni N messaggi
            save_interval: Numero di messaggi prima di auto-save
        """
        self.tracker = tracker or AgentTracker()
        self.auto_save = auto_save
        self.save_interval = save_interval
        self.message_count = 0
        self.log_buffer = []
        
    def log_interaction(self, sender: str, recipient: str, message: str, 
                       tokens: int = 0, metadata: dict = None) -> dict:
        """
        Logga un'interazione tra agenti.
        
        Args:
            sender: Nome dell'agente mittente
            recipient: Nome dell'agente destinatario
            message: Contenuto del messaggio
            tokens: Token consumati
            metadata: Metadati aggiuntivi (opzionali)
        
        Returns:
            Dict con lo stato del logging
        """
        try:
            result = self.tracker.add_message(
                sender=sender,
                recipient=recipient,
                content=message,
                tokens_used=tokens,
                raise_on_loop=False
            )
            
            self.message_count += 1
            
            # Aggiungi ai log buffer
            log_entry = {
                "sender": sender,
                "recipient": recipient,
                "message": message,
                "tokens": tokens,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat(),
                "loop_detected": result["loop_detected"]
            }
            self.log_buffer.append(log_entry)
            
            # Auto-save se necessario
            if self.auto_save and self.message_count % self.save_interval == 0:
                self.save_logs()
            
            return {
                "status": "success",
                "loop_detected": result["loop_detected"],
                "message_count": self.message_count
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message_count": self.message_count
            }
    
    def save_logs(self, filename: str = "crewai_logs.json") -> str:
        """
        Salva i log in un file JSON.
        
        Args:
            filename: Nome del file di output
        
        Returns:
            Percorso del file creato
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "messages": self.log_buffer,
                "summary": self.tracker.get_conversation_summary(),
                "export_time": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def get_status(self) -> dict:
        """Ottiene lo stato corrente del tracking."""
        return {
            "message_count": self.message_count,
            "agents": list(self.tracker._agents_involved),
            "loop_detected": self.tracker._loop_detected,
            "total_tokens": sum(m.tokens_used for m in self.tracker.messages),
            "estimated_cost": self.tracker.estimate_session_cost()
        }
    
    def reset(self):
        """Resetta il tracker e il buffer."""
        self.tracker.reset_session()
        self.log_buffer.clear()
        self.message_count = 0


# ============================================================================
# DECORATORE PER HOOK AUTOMATICO
# ============================================================================

def track_agent_interaction(integration: TrackedCrewAIIntegration):
    """
    Decoratore per tracciare automaticamente le interazioni.
    
    Uso:
        @track_agent_interaction(integration)
        def agent_method(self, ...):
            ...
    """
    def decorator(func: Callable):
        def wrapper(agent_self, *args, **kwargs):
            # Esegui il metodo
            result = func(agent_self, *args, **kwargs)
            
            # Log automatico (se il risultato contiene i dati necessari)
            if isinstance(result, dict) and "sender" in result:
                integration.log_interaction(
                    sender=result.get("sender", "Unknown"),
                    recipient=result.get("recipient", "Unknown"),
                    message=result.get("message", str(result)),
                    tokens=result.get("tokens", 0),
                    metadata=result.get("metadata", {})
                )
            
            return result
        
        return wrapper
    
    return decorator


# ============================================================================
# ESEMPIO DI UTILIZZO CON MOCK AGENTS
# ============================================================================

class MockCrewAIAgent:
    """
    Agente mock per demonstrare l'integrazione.
    
    In una situazione reale, questo sarebbe un vero agente CrewAI.
    """
    
    def __init__(self, name: str, role: str, tracked_integration: Optional[TrackedCrewAIIntegration] = None):
        self.name = name
        self.role = role
        self.integration = tracked_integration
    
    def execute_task(self, task_description: str, tokens: int = 100) -> dict:
        """Simula l'esecuzione di un task."""
        return {
            "agent": self.name,
            "task": task_description,
            "result": f"Task completato: {task_description}",
            "tokens": tokens
        }
    
    def send_message(self, recipient_name: str, message: str, tokens: int = 50):
        """Simula l'invio di un messaggio ad un altro agente."""
        if self.integration:
            self.integration.log_interaction(
                sender=self.name,
                recipient=recipient_name,
                message=message,
                tokens=tokens,
                metadata={
                    "role": self.role,
                    "message_type": "direct_communication"
                }
            )
        return {"status": "sent", "recipient": recipient_name}


# ============================================================================
# SCENARIO DI ESEMPIO
# ============================================================================

def example_crewai_workflow():
    """
    Esempio di workflow CrewAI con tracking integrato.
    
    Questo simula un crew di agenti che lavorano insieme su un progetto.
    """
    
    print("\n" + "="*80)
    print("ESEMPIO: Integrazione AgentTracker con CrewAI")
    print("="*80)
    
    # Crea l'integrazione
    integration = TrackedCrewAIIntegration(
        auto_save=False,  # Salva manualmente
        save_interval=10
    )
    
    print("\n🤖 Creazione del crew:\n")
    
    # Crea gli agenti (mock)
    researcher = MockCrewAIAgent("researcher", "Research Specialist", integration)
    writer = MockCrewAIAgent("writer", "Content Writer", integration)
    editor = MockCrewAIAgent("editor", "Editor", integration)
    
    agents = [researcher, writer, editor]
    print(f"✓ {len(agents)} agenti creati")
    
    print("\n📝 Simulazione del workflow:\n")
    
    # Simula il flusso di lavoro
    
    # Step 1: Ricerca
    print("[1] Ricerca avviata...")
    researcher.send_message(
        "writer",
        "Ho completato la ricerca su AI. Trovati 15 articoli rilevanti.",
        tokens=200
    )
    
    # Step 2: Scrittura
    print("[2] Scrittura avviata...")
    writer.send_message(
        "researcher",
        "Grazie! Sto scrivendo l'articolo basato sui tuoi risultati.",
        tokens=150
    )
    
    # Step 3: Più messaggi
    print("[3] Iterazione:")
    for i in range(3):
        writer.send_message(
            "editor",
            f"Ho terminato la sezione {i+1}. Puoi rivedere?",
            tokens=100
        )
        editor.send_message(
            "writer",
            f"Sezione {i+1} revisionata. Buona qualità, continua così.",
            tokens=80
        )
    
    print("\n✓ Workflow completato!\n")
    
    # Mostra le statistiche
    print("="*80)
    print("📊 STATISTICHE DI TRACKING")
    print("="*80)
    
    status = integration.get_status()
    print(f"\n✓ Messaggi loggati: {status['message_count']}")
    print(f"✓ Agenti coinvolti: {', '.join(status['agents'])}")
    print(f"✓ Token totali: {status['total_tokens']}")
    print(f"✓ Costo stimato (GPT-3.5): ${status['estimated_cost']['total_cost']:.6f}")
    print(f"✓ Loop rilevati: {'Sì ⚠️' if status['loop_detected'] else 'No ✓'}")
    
    # Salva i logs
    print("\n" + "="*80)
    print("💾 ESPORTAZIONE")
    print("="*80)
    
    # Esporta il log JSON
    json_file = integration.save_logs("example_crewai_logs.json")
    print(f"\n✓ Log JSON esportato: {json_file}")
    
    # Esporta il log di conversazione
    txt_file = integration.tracker.export_conversation("example_crewai_conversation.txt")
    print(f"✓ Log di conversazione esportato: {txt_file}")
    
    # Mostra l'anteprima del riepilogo
    print("\n" + "="*80)
    print("📋 RIEPILOGO CONVERSAZIONE")
    print("="*80)
    
    summary = integration.tracker.get_conversation_summary()
    for key, value in summary.items():
        if key != "estimated_cost":
            print(f"  {key}: {value}")
    
    return integration


# ============================================================================
# SCENARIO CON LOOP DETECTION
# ============================================================================

def example_with_loop_detection():
    """Esempio che mostra il rilevamento di loop."""
    
    print("\n" + "="*80)
    print("ESEMPIO: Rilevamento di Loop in Conversazione CrewAI")
    print("="*80)
    
    integration = TrackedCrewAIIntegration()
    
    # Crea agenti
    agent_a = MockCrewAIAgent("agent_a", "Analyzer", integration)
    agent_b = MockCrewAIAgent("agent_b", "Debugger", integration)
    
    print("\n🔄 Simulazione di conversazione con loop:\n")
    
    # Simula una conversazione che crea un loop
    
    for i in range(6):
        if i % 2 == 0:
            agent_a.send_message(
                "agent_b",
                "C'è un errore nel codice. Puoi debuggare?",
                tokens=100
            )
        else:
            agent_b.send_message(
                "agent_a",
                "Non riesco a trovare l'errore. Puoi spiegare meglio?",
                tokens=90
            )
        
        status = integration.get_status()
        if status['loop_detected']:
            print(f"  Messaggio {i+1}: 🚨 LOOP RILEVATO!")
        else:
            print(f"  Messaggio {i+1}: ✓ Continuando...")
    
    print(f"\n⚠️ Sessione contiene loop: {status['loop_detected']}")


# ============================================================================
# BEST PRACTICES
# ============================================================================

"""
BEST PRACTICES PER L'INTEGRAZIONE CON CREWAI
=============================================

1. INIZIALIZZAZIONE
   - Crea l'integrazione una volta all'inizio del workflow
   - Riusa lo stesso tracker per tutta la sessione
   
2. LOGGING
   - Log immediatamente dopo ogni comunicazione
   - Includi metadati utili (role, tipo di messaggio, ecc.)
   
3. MONITORAGGIO DEI LOOP
   - Configura soglie appropriate per il tuo use case
   - Usa raise_on_loop=True per fermare la sessione subito
   - Usa raise_on_loop=False per continuare con avvertimenti
   
4. ANALISI COSTI
   - Estrai i token reali dagli agenti CrewAI
   - Usa il modello corretto per calcoli accurati
   
5. SALVATAGGIO
   - Salva i logs regolarmente durante l'esecuzione
   - Usa auto_save=True per sessioni lunghe
   
6. SICUREZZA
   - Non loggare informazioni sensibili nel messaggio
   - Usa i metadati per info private
   - Crittografa i file di log se necessario

INTEGRAZIONE CON CREWAI REALE
=============================

Per integrare con CrewAI reale, aggiungi hook nel metodo execute():

    class MyCrewAI(Crew):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tracker = TrackedCrewAIIntegration()
        
        def execute(self, ...):
            # Hook nel metodo che gestisce la comunicazione
            original_send = Agent.send_message
            
            def tracked_send(self, to_agent, message, ...):
                self.crew.tracker.log_interaction(
                    self.name, to_agent.name, message, tokens
                )
                return original_send(self, to_agent, message, ...)
            
            Agent.send_message = tracked_send
            return super().execute(...)
"""


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  INTEGRAZIONE AGENT TRACKER CON CREWAI".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    # Esegui gli esempi
    example_crewai_workflow()
    example_with_loop_detection()
    
    # Conclusione
    print("\n" + "="*80)
    print("✅ INTEGRAZIONE COMPLETATA!")
    print("="*80)
    print("\n📚 Note:")
    print("  • Questo è un esempio con agenti MOCK")
    print("  • Per CrewAI reale, integra i hook nel metodo execute()")
    print("  • Vedi le BEST PRACTICES sopra per i dettagli")
    print("  • Controlla il README.md per la documentazione completa\n")
