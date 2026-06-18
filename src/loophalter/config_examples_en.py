"""
Configuration Examples for AgentTracker
========================================

This file contains preset configurations for different scenarios.
"""

from agent_tracker_en import AgentTracker


# ============================================================================
# PREDEFINED CONFIGURATIONS
# ============================================================================

class TrackerConfigs:
    """Collection of recommended configurations."""
    
    # ---- STRICT MODE ----
    # Use for critical applications where you want to block
    # any repetitive communication immediately
    @staticmethod
    def strict():
        """
        STRICT Mode: Detects loops very quickly
        - max_loop_repetitions=2 (only 2 repetitions)
        - similarity_threshold=0.80 (sensitive)
        """
        return AgentTracker(
            max_loop_repetitions=2,
            similarity_threshold=0.80
        )
    
    # ---- STANDARD MODE ----
    # Balanced configuration (DEFAULT)
    # Good compromise between sensitivity and false positives
    @staticmethod
    def standard():
        """
        STANDARD Mode: Balanced (DEFAULT)
        - max_loop_repetitions=3
        - similarity_threshold=0.85
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.85
        )
    
    # ---- LENIENT MODE ----
    # Use for natural conversations with agents
    # that tend to repeat similar messages
    @staticmethod
    def lenient():
        """
        LENIENT Mode: Less sensitive
        - max_loop_repetitions=5
        - similarity_threshold=0.95 (very similar)
        """
        return AgentTracker(
            max_loop_repetitions=5,
            similarity_threshold=0.95
        )
    
    # ---- DEVELOPMENT MODE ----
    # Use during development to debug your agents
    @staticmethod
    def development():
        """
        DEVELOPMENT Mode: Very permissive
        - max_loop_repetitions=10
        - similarity_threshold=0.98 (almost identical)
        """
        return AgentTracker(
            max_loop_repetitions=10,
            similarity_threshold=0.98
        )
    
    # ---- RESEARCH MODE ----
    # For experiments and research
    @staticmethod
    def research():
        """
        RESEARCH Mode: Observational
        - max_loop_repetitions=20
        - similarity_threshold=0.99 (identical)
        """
        return AgentTracker(
            max_loop_repetitions=20,
            similarity_threshold=0.99
        )
    
    # ---- PRODUCTION MODE ----
    # For critical production environments
    @staticmethod
    def production():
        """
        PRODUCTION Mode: Rigorous
        - max_loop_repetitions=1 (even one repetition!)
        - similarity_threshold=0.75 (sensitive)
        """
        return AgentTracker(
            max_loop_repetitions=1,
            similarity_threshold=0.75
        )


# ============================================================================
# CONFIGURATIONS FOR SPECIFIC FRAMEWORKS
# ============================================================================

class FrameworkConfigs:
    """Configurations optimized for specific frameworks."""
    
    @staticmethod
    def crewai():
        """
        Configuration optimized for CrewAI
        CrewAI tends to have long iterations, so it's permissive
        """
        return AgentTracker(
            max_loop_repetitions=4,
            similarity_threshold=0.88
        )
    
    @staticmethod
    def autogen():
        """
        Configuration optimized for AutoGen
        AutoGen has very structured conversations
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.85
        )
    
    @staticmethod
    def langchain():
        """
        Configuration optimized for LangChain
        LangChain tends to have precise communications
        """
        return AgentTracker(
            max_loop_repetitions=2,
            similarity_threshold=0.80
        )
    
    @staticmethod
    def custom_agent_framework():
        """
        Configuration for custom frameworks
        Balanced and flexible
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.85
        )


# ============================================================================
# CONFIGURATIONS FOR USE CASES
# ============================================================================

class UseCaseConfigs:
    """Configurations for different use cases."""
    
    @staticmethod
    def qa_testing():
        """
        For QA testing between agents
        Very strict to catch bugs
        """
        return AgentTracker(
            max_loop_repetitions=2,
            similarity_threshold=0.80
        )
    
    @staticmethod
    def data_processing():
        """
        For data processing between agents
        Moderate because data can be similar
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.87
        )
    
    @staticmethod
    def content_creation():
        """
        For content creation (articles, code, etc.)
        Permissive because iterations are normal
        """
        return AgentTracker(
            max_loop_repetitions=5,
            similarity_threshold=0.90
        )
    
    @staticmethod
    def customer_support():
        """
        For customer support
        Moderate to avoid response loops
        """
        return AgentTracker(
            max_loop_repetitions=3,
            similarity_threshold=0.82
        )
    
    @staticmethod
    def decision_making():
        """
        For complex decision-making processes
        Permissive because iterative discussions are normal
        """
        return AgentTracker(
            max_loop_repetitions=6,
            similarity_threshold=0.92
        )
    
    @staticmethod
    def debug_scenario():
        """
        For debugging and troubleshooting
        Very strict because debug loops are bad
        """
        return AgentTracker(
            max_loop_repetitions=1,
            similarity_threshold=0.75
        )


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
    Factory function to create tracker with flexible configuration.
    
    Args:
        mode: 'strict', 'standard', 'lenient', 'development', 'research', 'production'
        framework: 'crewai', 'autogen', 'langchain', etc.
        use_case: 'qa_testing', 'data_processing', 'content_creation', etc.
        custom_params: Dict with custom parameters to apply
    
    Returns:
        Configured AgentTracker
    
    Example:
        tracker = create_tracker(mode='strict')
        tracker = create_tracker(framework='crewai')
        tracker = create_tracker(use_case='content_creation')
    """
    
    # Select base configuration
    if use_case:
        config = getattr(UseCaseConfigs, use_case, None)
        if config:
            tracker = config()
            print(f"✓ Tracker created with use_case='{use_case}'")
            return tracker
    
    if framework:
        config = getattr(FrameworkConfigs, framework, None)
        if config:
            tracker = config()
            print(f"✓ Tracker created with framework='{framework}'")
            return tracker
    
    if mode:
        config = getattr(TrackerConfigs, mode, None)
        if config:
            tracker = config()
            print(f"✓ Tracker created with mode='{mode}'")
            # Apply custom parameters if provided
            if custom_params:
                for key, value in custom_params.items():
                    if hasattr(tracker, key):
                        setattr(tracker, key, value)
                        print(f"  - Override: {key}={value}")
            return tracker
    
    # Default: standard mode
    tracker = TrackerConfigs.standard()
    print(f"✓ Tracker created with mode='standard' (default)")
    return tracker


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  CONFIGURATION EXAMPLES - AgentTracker".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    print("\n" + "="*80)
    print("CONFIGURATION SUMMARY TABLE")
    print("="*80)
    
    configs = [
        ("STRICT", 2, 0.80, "Critical production"),
        ("STANDARD", 3, 0.85, "Default / Generic"),
        ("LENIENT", 5, 0.95, "Conversations"),
        ("DEVELOPMENT", 10, 0.98, "Debug"),
        ("RESEARCH", 20, 0.99, "Analysis"),
        ("PRODUCTION", 1, 0.75, "Maximum production"),
    ]
    
    for name, reps, sim, use in configs:
        print(f"  {name:15s} | Reps: {reps:2d} | Sim: {sim:.2f} | {use}")
    
    print("\n" + "="*80)
    print("USING create_tracker() FACTORY FUNCTION")
    print("="*80)
    
    print("\n✓ Creating tracker with factory function:")
    tracker1 = create_tracker(mode='strict')
    tracker2 = create_tracker(framework='crewai')
    tracker3 = create_tracker(use_case='content_creation')
    
    print("\n✅ CONFIGURATIONS LOADED!")
    print("📚 Use create_tracker() to create tracker with the right configuration")
