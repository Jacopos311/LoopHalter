"""
Configurazioni di Esempio per AgentTracker
==========================================

Questo file contiene configurazioni preimpostate per diversi scenari.
"""

from agent_tracker import AgentTracker


# ============================================================================
# CONFIGURAZIONI PREDEFINITE
# ============================================================================

class TrackerConfigs:
    """Collezione di configurazioni consigliate."""
    
    # ---- STRICT MODE ----
    # Usa questo per applicazioni critiche dove vuoi bloccare
    # immediatamente qualsiasi comunicazione ripetitiva
    @staticmethod
    def strict():
        """
        Modalità STRICT: Rileva loop molto rapidamente
        - max_loop_repetitions=2 (solo 2 ripetizioni)
        - similarity_threshold=0.80 (sensibile)
        """
        return AgentTracker(
            max_loop_repetitions=2,
            similarity_threshold=0.80
        )
    
    # ---- STANDARD MODE ----
    # Configurazione equilibrata (DEFAULT)
    # Buon compromesso tra sensibilità e false positive
    @staticmethod
    def standard():
        """
        Modalità STANDARD: Bilanciata (DEFAULT)
        - max_loop_repetitions=3
        - similarity_threshold=0.85
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.85
        )
    
    # ---- LENIENT MODE ----
    # Usa questo per conversazioni naturali con agenti
    # che tendono a ripetere messaggi simili
    @staticmethod
    def lenient():
        """
        Modalità LENIENT: Meno sensibile
        - max_loop_repetitions=5
        - similarity_threshold=0.95 (molto simili)
        """
        return AgentTracker(
            max_loop_repetitions=5,
            similarity_threshold=0.95
        )
    
    # ---- DEVELOPMENT MODE ----
    # Usa durante lo sviluppo per debuggare i tuoi agenti
    @staticmethod
    def development():
        """
        Modalità DEVELOPMENT: Molto permissiva
        - max_loop_repetitions=10
        - similarity_threshold=0.98 (quasi identici)
        """
        return AgentTracker(
            max_loop_repetitions=10,
            similarity_threshold=0.98
        )
    
    # ---- RESEARCH MODE ----
    # Per esperimenti e ricerca
    @staticmethod
    def research():
        """
        Modalità RESEARCH: Osservativa
        - max_loop_repetitions=20
        - similarity_threshold=0.99 (identici)
        """
        return AgentTracker(
            max_loop_repetitions=20,
            similarity_threshold=0.99
        )
    
    # ---- PRODUCTION MODE ----
    # Per ambienti di produzione critici
    @staticmethod
    def production():
        """
        Modalità PRODUCTION: Rigorosa
        - max_loop_repetitions=1 (anche una sola ripetizione!)
        - similarity_threshold=0.75 (sensibile)
        """
        return AgentTracker(
            max_loop_repetitions=1,
            similarity_threshold=0.75
        )


# ============================================================================
# CONFIGURAZIONI PER FRAMEWORK SPECIFICI
# ============================================================================

class FrameworkConfigs:
    """Configurazioni ottimizzate per framework specifici."""
    
    @staticmethod
    def crewai():
        """
        Configurazione ottimizzata per CrewAI
        CrewAI tende ad avere iterazioni lunghe, quindi è permissivo
        """
        return AgentTracker(
            max_loop_repetitions=4,
            similarity_threshold=0.88
        )
    
    @staticmethod
    def autogen():
        """
        Configurazione ottimizzata per AutoGen
        AutoGen ha conversazioni molto strutturate
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.85
        )
    
    @staticmethod
    def langchain():
        """
        Configurazione ottimizzata per LangChain
        LangChain tende a avere comunicazioni precise
        """
        return AgentTracker(
            max_loop_repetitions=2,
            similarity_threshold=0.80
        )
    
    @staticmethod
    def custom_agent_framework():
        """
        Configurazione per framework custom
        Bilanciata e flessibile
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.85
        )


# ============================================================================
# CONFIGURAZIONI PER CASE DI UTILIZZO
# ============================================================================

class UseCaseConfigs:
    """Configurazioni per diversi casi di utilizzo."""
    
    @staticmethod
    def qa_testing():
        """
        Per testing di QA tra agenti
        Molto rigido per catturare bug
        """
        return AgentTracker(
            max_loop_repetitions=2,
            similarity_threshold=0.80
        )
    
    @staticmethod
    def data_processing():
        """
        Per elaborazione dati tra agenti
        Moderato perché i dati possono essere simili
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.87
        )
    
    @staticmethod
    def content_creation():
        """
        Per creazione contenuti (articoli, codice, ecc.)
        Permissivo perché iterazioni sono normali
        """
        return AgentTracker(
            max_loop_repetitions=5,
            similarity_threshold=0.90
        )
    
    @staticmethod
    def customer_support():
        """
        Per supporto clienti
        Moderato per evitare loop di risposte
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.82
        )
    
    @staticmethod
    def decision_making():
        """
        Per processi decisionali complessi
        Permissivo perché discussioni iterative sono normali
        """
        return AgentTracker(
            max_loop_repetitions=6,
            similarity_threshold=0.92
        )
    
    @staticmethod
    def debug_scenario():
        """
        Per debugging e troubleshooting
        Molto rigido perché debug loop sono cattivi
        """
        return AgentTracker(
            max_loop_repetitions=1,
            similarity_threshold=0.75
        )


# ============================================================================
# ESEMPI DI UTILIZZO DELLE CONFIGURAZIONI
# ============================================================================

def example_using_configs():
    """Mostra come usare le configurazioni."""
    
    print("="*80)
    print("ESEMPI DI UTILIZZO DELLE CONFIGURAZIONI")
    print("="*80)
    
    # Esempio 1: Usa una configurazione predefinita
    print("\n1️⃣ USAR CONFIGURAZIONE PREDEFINITA:")
    print("-" * 80)
    tracker = TrackerConfigs.standard()
    print(f"✓ Tracker creato in modalità STANDARD")
    print(f"  - max_loop_repetitions: {tracker.max_loop_repetitions}")
    print(f"  - similarity_threshold: {tracker.similarity_threshold}")
    
    # Esempio 2: Cambia configurazione a seconda della necessità
    print("\n2️⃣ CAMBIARE CONFIGURAZIONE DINAMICAMENTE:")
    print("-" * 80)
    
    in_production = True
    
    if in_production:
        tracker = TrackerConfigs.production()
        print("✓ Ambiente PRODUCTION - Usando modalità PRODUCTION")
    else:
        tracker = TrackerConfigs.development()
        print("✓ Ambiente DEVELOPMENT - Usando modalità DEVELOPMENT")
    
    print(f"  - max_loop_repetitions: {tracker.max_loop_repetitions}")
    print(f"  - similarity_threshold: {tracker.similarity_threshold}")
    
    # Esempio 3: Usa configurazione per framework specifico
    print("\n3️⃣ CONFIGURAZIONE PER FRAMEWORK:")
    print("-" * 80)
    
    framework = "crewai"  # Potrebbe venire da env var o config file
    
    if framework == "crewai":
        tracker = FrameworkConfigs.crewai()
        print(f"✓ CrewAI - Configurazione ottimizzata caricata")
    elif framework == "autogen":
        tracker = FrameworkConfigs.autogen()
        print(f"✓ AutoGen - Configurazione ottimizzata caricata")
    
    print(f"  - max_loop_repetitions: {tracker.max_loop_repetitions}")
    print(f"  - similarity_threshold: {tracker.similarity_threshold}")
    
    # Esempio 4: Usa configurazione per case di utilizzo
    print("\n4️⃣ CONFIGURAZIONE PER CASE DI UTILIZZO:")
    print("-" * 80)
    
    use_case = "content_creation"
    
    if use_case == "content_creation":
        tracker = UseCaseConfigs.content_creation()
        print(f"✓ Content Creation - Configurazione caricata")
    elif use_case == "qa_testing":
        tracker = UseCaseConfigs.qa_testing()
        print(f"✓ QA Testing - Configurazione rigorosa caricata")
    
    print(f"  - max_loop_repetitions: {tracker.max_loop_repetitions}")
    print(f"  - similarity_threshold: {tracker.similarity_threshold}")
    
    # Esempio 5: Crea configurazione custom
    print("\n5️⃣ CONFIGURAZIONE CUSTOM:")
    print("-" * 80)
    
    tracker = AgentTracker(
        max_loop_repetitions=7,
        similarity_threshold=0.89
    )
    print(f"✓ Tracker custom creato")
    print(f"  - max_loop_repetitions: {tracker.max_loop_repetitions}")
    print(f"  - similarity_threshold: {tracker.similarity_threshold}")


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_tracker(
    mode: str = "standard",
    framework: str = None,
    use_case: str = None,
    custom_params: dict = None
) -> AgentTracker:
    """
    Funzione factory per creare tracker con configurazione flessibile.
    
    Args:
        mode: 'strict', 'standard', 'lenient', 'development', 'research', 'production'
        framework: 'crewai', 'autogen', 'langchain', etc.
        use_case: 'qa_testing', 'data_processing', 'content_creation', etc.
        custom_params: Dict con parametri custom da applicare
    
    Returns:
        AgentTracker configurato
    
    Example:
        tracker = create_tracker(mode='strict')
        tracker = create_tracker(framework='crewai')
        tracker = create_tracker(use_case='content_creation')
        tracker = create_tracker(custom_params={'max_loop_repetitions': 5})
    """
    
    # Seleziona configurazione base
    if use_case:
        config = getattr(UseCaseConfigs, use_case, None)
        if config:
            tracker = config()
            print(f"✓ Tracker creato con use_case='{use_case}'")
            return tracker
    
    if framework:
        config = getattr(FrameworkConfigs, framework, None)
        if config:
            tracker = config()
            print(f"✓ Tracker creato con framework='{framework}'")
            return tracker
    
    if mode:
        config = getattr(TrackerConfigs, mode, None)
        if config:
            tracker = config()
            print(f"✓ Tracker creato con mode='{mode}'")
            # Applica parametri custom se forniti
            if custom_params:
                for key, value in custom_params.items():
                    if hasattr(tracker, key):
                        setattr(tracker, key, value)
                        print(f"  - Override: {key}={value}")
            return tracker
    
    # Default: standard mode
    tracker = TrackerConfigs.standard()
    print(f"✓ Tracker creato con mode='standard' (default)")
    return tracker


# ============================================================================
# CONFIG FILE (JSON-style)
# ============================================================================

CONFIG_FILE_EXAMPLE = """
{
  "environments": {
    "development": {
      "mode": "development",
      "max_loop_repetitions": 10,
      "similarity_threshold": 0.98
    },
    "staging": {
      "mode": "standard",
      "max_loop_repetitions": 3,
      "similarity_threshold": 0.85
    },
    "production": {
      "mode": "production",
      "max_loop_repetitions": 1,
      "similarity_threshold": 0.75
    }
  },
  "frameworks": {
    "crewai": {
      "max_loop_repetitions": 4,
      "similarity_threshold": 0.88
    },
    "autogen": {
      "max_loop_repetitions": 3,
      "similarity_threshold": 0.85
    }
  },
  "use_cases": {
    "content_creation": {
      "max_loop_repetitions": 5,
      "similarity_threshold": 0.90
    },
    "qa_testing": {
      "max_loop_repetitions": 2,
      "similarity_threshold": 0.80
    }
  }
}
"""


# ============================================================================
# TABELLA DI CONFRONTO
# ============================================================================

COMPARISON_TABLE = """
┌─────────────────────────────────────────────────────────────────────────────┐
│ CONFIGURAZIONI DI RIEPILOGO                                                 │
├─────────────┬──────────────────────┬─────────────────┬──────────────────────┤
│ Mode        │ Loop Repetitions     │ Similarity      │ Use Case             │
├─────────────┼──────────────────────┼─────────────────┼──────────────────────┤
│ STRICT      │ 2 (rigido)           │ 0.80 (sensibile)│ Produzione critica   │
│ STANDARD    │ 3 (bilanciato)       │ 0.85 (standard) │ Default / Generico   │
│ LENIENT     │ 5 (permissivo)       │ 0.95 (poco)     │ Conversazioni        │
│ DEVELOPMENT │ 10 (molto)           │ 0.98 (minimal)  │ Debug                │
│ RESEARCH    │ 20 (osservativo)     │ 0.99 (molto)    │ Analisi              │
│ PRODUCTION  │ 1 (critico)          │ 0.75 (massima)  │ Produzione massima   │
└─────────────┴──────────────────────┴─────────────────┴──────────────────────┘
"""


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  CONFIGURAZIONI DI ESEMPIO - AgentTracker".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    # Mostra la tabella
    print(COMPARISON_TABLE)
    
    # Esegui gli esempi
    example_using_configs()
    
    # Mostra come usare la factory function
    print("\n" + "="*80)
    print("FACTORY FUNCTION - create_tracker()")
    print("="*80)
    
    print("\n✓ Creazione con factory function:")
    tracker1 = create_tracker(mode='strict')
    tracker2 = create_tracker(framework='crewai')
    tracker3 = create_tracker(use_case='content_creation')
    tracker4 = create_tracker(custom_params={'max_loop_repetitions': 15})
    
    # Mostra il file di config di esempio
    print("\n" + "="*80)
    print("CONFIG FILE EXAMPLE (JSON)")
    print("="*80)
    print(CONFIG_FILE_EXAMPLE)
    
    print("\n✅ CONFIGURAZIONI CARICATE!")
    print("📚 Usa create_tracker() per creare tracker con la configurazione giusta")
