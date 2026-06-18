"""
Quick Start Guide - AgentTracker
================================

Questo file dimostra i casi di utilizzo più comuni del tracker.
Esegui questo file per vedere gli esempi in azione.
"""

from agent_tracker import AgentTracker, LoopDetectionException


# ============================================================================
# CASO 1: Tracciamento Base di una Conversazione
# ============================================================================

def case_1_basic_tracking():
    print("\n" + "="*80)
    print("CASO 1: Tracciamento Base di una Conversazione")
    print("="*80)
    
    tracker = AgentTracker()
    
    # Simulazione di conversazione tra 2 agenti
    interactions = [
        ("Analyzer", "Writer", "Ho trovato 3 articoli su Python", 150),
        ("Writer", "Analyzer", "Grazie! Scrivo una sintesi", 120),
        ("Analyzer", "Writer", "Perfetto, aspetto il tuo feedback", 100),
    ]
    
    for sender, recipient, message, tokens in interactions:
        tracker.add_message(sender, recipient, message, tokens)
        print(f"✓ {sender} -> {recipient}: {message[:40]}...")
    
    # Mostra il riepilogo
    summary = tracker.get_conversation_summary()
    print(f"\n📊 Messaggi totali: {summary['total_messages']}")
    print(f"💰 Costo stimato: ${summary['estimated_cost']['total_cost']:.6f}")
    print(f"✓ Loop rilevato: {summary['loop_detected']}")


# ============================================================================
# CASO 2: Rilevamento di Loop
# ============================================================================

def case_2_loop_detection():
    print("\n" + "="*80)
    print("CASO 2: Rilevamento Automatico di Loop")
    print("="*80)
    
    tracker = AgentTracker(max_loop_repetitions=3, similarity_threshold=0.85)
    
    repetitive_msg = "Scusami, puoi ripetere la domanda?"
    
    print(f"\nAggiungendo il messaggio '{repetitive_msg}' ripetutamente...\n")
    
    for i in range(5):
        result = tracker.add_message(
            sender="Agent_A",
            recipient="Agent_B",
            content=repetitive_msg,
            tokens_used=80,
            raise_on_loop=False
        )
        
        print(f"Messaggio #{i+1}: ", end="")
        
        if result["loop_detected"]:
            print(f"🚨 LOOP! {result['loop_info']['repetitions']} ripetizioni")
        else:
            print("✓ Nessun loop (per ora)")
    
    print(f"\n⚠️ Sessione contiene loop: {tracker._loop_detected}")


# ============================================================================
# CASO 3: Gestione delle Eccezioni
# ============================================================================

def case_3_exception_handling():
    print("\n" + "="*80)
    print("CASO 3: Gestione delle Eccezioni")
    print("="*80)
    
    tracker = AgentTracker(max_loop_repetitions=2)
    
    try:
        for i in range(5):
            tracker.add_message(
                sender="Agent_X",
                recipient="Agent_Y",
                content="Messaggio ripetitivo",
                tokens_used=50,
                raise_on_loop=True  # Solleva eccezione
            )
            print(f"✓ Messaggio {i+1} aggiunto")
    
    except LoopDetectionException as e:
        print(f"\n❌ Eccezione catturata: {e}")
        print("🛑 La sessione è stata interrotta automaticamente!")


# ============================================================================
# CASO 4: Analisi dei Costi
# ============================================================================

def case_4_cost_analysis():
    print("\n" + "="*80)
    print("CASO 4: Analisi e Confronto dei Costi")
    print("="*80)
    
    tracker = AgentTracker()
    
    # Simula una sessione con molti token
    messages = [
        ("Agent_Research", "Agent_Writing", "Ricerca completata", 500),
        ("Agent_Writing", "Agent_Review", "Articolo scritto", 800),
        ("Agent_Review", "Agent_Writing", "Revisionato", 300),
    ]
    
    for sender, recipient, msg, tokens in messages:
        tracker.add_message(sender, recipient, msg, tokens)
    
    # Confronta i costi tra modelli
    print("\n📊 Costi per diversi modelli:\n")
    
    for model in ["gpt-4", "gpt-3.5-turbo", "default"]:
        cost = tracker.estimate_session_cost(model=model)
        print(f"  {model:20s}: ${cost['total_cost']:10.6f} " +
              f"({cost['total_tokens']:4d} token)")


# ============================================================================
# CASO 5: Query e Filtraggio
# ============================================================================

def case_5_filtering():
    print("\n" + "="*80)
    print("CASO 5: Query e Filtraggio dei Messaggi")
    print("="*80)
    
    tracker = AgentTracker()
    
    # Popola il tracker con messaggi di test
    messages = [
        ("Agent_A", "Agent_B", "Ciao B", 100),
        ("Agent_B", "Agent_A", "Ciao A", 100),
        ("Agent_A", "Agent_C", "Ciao C", 100),
        ("Agent_C", "Agent_A", "Ciao A", 100),
        ("Agent_B", "Agent_C", "Ciao C", 100),
    ]
    
    for sender, recipient, msg, tokens in messages:
        tracker.add_message(sender, recipient, msg, tokens)
    
    # Esegui diverse query
    print(f"\n✓ Messaggi totali: {len(tracker.get_message_history())}")
    print(f"✓ Messaggi di Agent_A: {len(tracker.get_message_history(sender='Agent_A'))}")
    print(f"✓ Messaggi da/a Agent_B: {len(tracker.get_message_history(recipient='Agent_B'))}")
    
    # Conversazione specifica
    conv = tracker.get_message_history(sender="Agent_A", recipient="Agent_B")
    print(f"✓ Messaggi A->B: {len(conv)}")
    if conv:
        print(f"   Primo: '{conv[0].content}'")


# ============================================================================
# CASO 6: Esportazione e Reporting
# ============================================================================

def case_6_export_and_reporting():
    print("\n" + "="*80)
    print("CASO 6: Esportazione e Reporting")
    print("="*80)
    
    tracker = AgentTracker()
    
    # Crea una conversazione
    interactions = [
        ("DataAgent", "ModelAgent", "Dati caricati", 200),
        ("ModelAgent", "DataAgent", "Training completato", 150),
        ("DataAgent", "ReportAgent", "Risultati disponibili", 180),
        ("ReportAgent", "DataAgent", "Rapport generato", 220),
    ]
    
    for sender, recipient, msg, tokens in interactions:
        tracker.add_message(sender, recipient, msg, tokens)
    
    # Ottieni il riepilogo
    summary = tracker.get_conversation_summary()
    
    print("\n📊 RIEPILOGO SESSIONE:")
    print(f"  • Durata: {summary['session_duration_seconds']:.2f}s")
    print(f"  • Agenti: {', '.join(summary['agents_involved'])}")
    print(f"  • Messaggi: {summary['total_messages']}")
    print(f"  • Token: {summary['total_tokens']}")
    print(f"  • Costo: ${summary['estimated_cost']['total_cost']:.6f}")
    
    # Esporta il log
    filename = tracker.export_conversation("quickstart_example.txt")
    print(f"\n📄 Sessione esportata in: {filename}")


# ============================================================================
# CASO 7: Multi-agent Complex Scenario
# ============================================================================

def case_7_complex_scenario():
    print("\n" + "="*80)
    print("CASO 7: Scenario Complesso Multi-Agent")
    print("="*80)
    
    tracker = AgentTracker(max_loop_repetitions=3, similarity_threshold=0.8)
    
    print("\n🤖 Simulazione: Crew di agenti che risolvono un problema\n")
    
    interactions = [
        ("Planner", "Researcher", "Ritrova info su AI", 150, "pianificazione"),
        ("Researcher", "Planner", "Ho trovato 5 articoli", 200, "ricerca"),
        ("Planner", "Coder", "Scrivi un prototipo", 180, "pianificazione"),
        ("Coder", "Planner", "Prototipo completato", 250, "codifica"),
        ("Planner", "Reviewer", "Rivedi il lavoro", 140, "pianificazione"),
        ("Reviewer", "Planner", "Qualità OK", 120, "review"),
    ]
    
    for sender, recipient, msg, tokens, role in interactions:
        result = tracker.add_message(
            sender=sender,
            recipient=recipient,
            content=msg,
            tokens_used=tokens,
            raise_on_loop=False
        )
        
        status = "✓" if not result["loop_detected"] else "⚠️"
        print(f"{status} {sender} -> {recipient}: {msg}")
    
    # Statistiche finali
    summary = tracker.get_conversation_summary()
    print("\n📈 STATISTICHE FINALI:")
    print(f"  • Messaggi per agente: {summary['message_count_by_agent']}")
    print(f"  • Costo totale: ${summary['estimated_cost']['total_cost']:.6f}")
    print(f"  • Loop rilevati: {'Sì ⚠️' if summary['loop_detected'] else 'No ✓'}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  QUICK START GUIDE - AgentTracker".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    # Esegui tutti i casi
    case_1_basic_tracking()
    case_2_loop_detection()
    case_3_exception_handling()
    case_4_cost_analysis()
    case_5_filtering()
    case_6_export_and_reporting()
    case_7_complex_scenario()
    
    # Conclusione
    print("\n" + "="*80)
    print("✅ QUICK START COMPLETATO!")
    print("="*80)
    print("\n📚 Per ulteriori dettagli, vedi README.md")
    print("🧪 Per eseguire i test: python -m unittest test_agent_tracker -v")
    print("📖 Per visualizzare il codice: agent_tracker.py\n")
