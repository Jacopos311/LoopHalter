"""
Quick Start Guide - AgentTracker
================================

This file demonstrates the most common use cases of the tracker.
Run this file to see the examples in action.
"""

from agent_tracker_en import AgentTracker, LoopDetectionException


# ============================================================================
# CASE 1: Basic Conversation Tracking
# ============================================================================

def case_1_basic_tracking():
    print("\n" + "="*80)
    print("CASE 1: Basic Conversation Tracking")
    print("="*80)
    
    tracker = AgentTracker()
    
    # Simulate conversation between 2 agents
    interactions = [
        ("Analyzer", "Writer", "Found 3 articles on Python", 150),
        ("Writer", "Analyzer", "Thanks! Writing a summary", 120),
        ("Analyzer", "Writer", "Perfect, waiting for your feedback", 100),
    ]
    
    for sender, recipient, message, tokens in interactions:
        tracker.add_message(sender, recipient, message, tokens)
        print(f"✓ {sender} -> {recipient}: {message[:40]}...")
    
    # Show summary
    summary = tracker.get_conversation_summary()
    print(f"\n📊 Total messages: {summary['total_messages']}")
    print(f"💰 Estimated cost: ${summary['estimated_cost']['total_cost']:.6f}")
    print(f"✓ Loop detected: {summary['loop_detected']}")


# ============================================================================
# CASE 2: Loop Detection
# ============================================================================

def case_2_loop_detection():
    print("\n" + "="*80)
    print("CASE 2: Automatic Loop Detection")
    print("="*80)
    
    tracker = AgentTracker(max_loop_repetitions=3, similarity_threshold=0.85)
    
    repetitive_msg = "Sorry, could you repeat the question?"
    
    print(f"\nAdding message '{repetitive_msg}' repeatedly...\n")
    
    for i in range(5):
        result = tracker.add_message(
            sender="Agent_A",
            recipient="Agent_B",
            content=repetitive_msg,
            tokens_used=80,
            raise_on_loop=False
        )
        
        print(f"Message #{i+1}: ", end="")
        
        if result["loop_detected"]:
            print(f"🚨 LOOP! {result['loop_info']['repetitions']} repetitions")
        else:
            print("✓ No loop (for now)")
    
    print(f"\n⚠️ Session contains loop: {tracker._loop_detected}")


# ============================================================================
# CASE 3: Exception Handling
# ============================================================================

def case_3_exception_handling():
    print("\n" + "="*80)
    print("CASE 3: Exception Handling")
    print("="*80)
    
    tracker = AgentTracker(max_loop_repetitions=2)
    
    try:
        for i in range(5):
            tracker.add_message(
                sender="Agent_X",
                recipient="Agent_Y",
                content="Repetitive message",
                tokens_used=50,
                raise_on_loop=True  # Raise exception
            )
            print(f"✓ Message {i+1} added")
    
    except LoopDetectionException as e:
        print(f"\n❌ Exception caught: {e}")
        print("🛑 Session terminated automatically!")


# ============================================================================
# CASE 4: Cost Analysis
# ============================================================================

def case_4_cost_analysis():
    print("\n" + "="*80)
    print("CASE 4: Cost Analysis and Comparison")
    print("="*80)
    
    tracker = AgentTracker()
    
    # Simulate a session with many tokens
    messages = [
        ("Agent_Research", "Agent_Writing", "Research completed", 500),
        ("Agent_Writing", "Agent_Review", "Article written", 800),
        ("Agent_Review", "Agent_Writing", "Reviewed", 300),
    ]
    
    for sender, recipient, msg, tokens in messages:
        tracker.add_message(sender, recipient, msg, tokens)
    
    # Compare costs across models
    print("\n📊 Costs for different models:\n")
    
    for model in ["gpt-4", "gpt-3.5-turbo", "default"]:
        cost = tracker.estimate_session_cost(model=model)
        print(f"  {model:20s}: ${cost['total_cost']:10.6f} " +
              f"({cost['total_tokens']:4d} tokens)")


# ============================================================================
# CASE 5: Filtering
# ============================================================================

def case_5_filtering():
    print("\n" + "="*80)
    print("CASE 5: Querying and Filtering Messages")
    print("="*80)
    
    tracker = AgentTracker()
    
    # Populate tracker with test messages
    messages = [
        ("Agent_A", "Agent_B", "Hi B", 100),
        ("Agent_B", "Agent_A", "Hi A", 100),
        ("Agent_A", "Agent_C", "Hi C", 100),
        ("Agent_C", "Agent_A", "Hi A", 100),
        ("Agent_B", "Agent_C", "Hi C", 100),
    ]
    
    for sender, recipient, msg, tokens in messages:
        tracker.add_message(sender, recipient, msg, tokens)
    
    # Run different queries
    print(f"\n✓ Total messages: {len(tracker.get_message_history())}")
    print(f"✓ Messages from Agent_A: {len(tracker.get_message_history(sender='Agent_A'))}")
    print(f"✓ Messages to/from Agent_B: {len(tracker.get_message_history(recipient='Agent_B'))}")
    
    # Specific conversation
    conv = tracker.get_message_history(sender="Agent_A", recipient="Agent_B")
    print(f"✓ Messages A->B: {len(conv)}")
    if conv:
        print(f"   First: '{conv[0].content}'")


# ============================================================================
# CASE 6: Export and Reporting
# ============================================================================

def case_6_export_and_reporting():
    print("\n" + "="*80)
    print("CASE 6: Export and Reporting")
    print("="*80)
    
    tracker = AgentTracker()
    
    # Create a conversation
    interactions = [
        ("DataAgent", "ModelAgent", "Data loaded", 200),
        ("ModelAgent", "DataAgent", "Training completed", 150),
        ("DataAgent", "ReportAgent", "Results available", 180),
        ("ReportAgent", "DataAgent", "Report generated", 220),
    ]
    
    for sender, recipient, msg, tokens in interactions:
        tracker.add_message(sender, recipient, msg, tokens)
    
    # Get summary
    summary = tracker.get_conversation_summary()
    
    print("\n📊 SESSION SUMMARY:")
    print(f"  • Duration: {summary['session_duration_seconds']:.2f}s")
    print(f"  • Agents: {', '.join(summary['agents_involved'])}")
    print(f"  • Messages: {summary['total_messages']}")
    print(f"  • Tokens: {summary['total_tokens']}")
    print(f"  • Cost: ${summary['estimated_cost']['total_cost']:.6f}")
    
    # Export log
    filename = tracker.export_conversation("quickstart_example_en.txt")
    print(f"\n📄 Session exported to: {filename}")


# ============================================================================
# CASE 7: Complex Multi-Agent Scenario
# ============================================================================

def case_7_complex_scenario():
    print("\n" + "="*80)
    print("CASE 7: Complex Multi-Agent Scenario")
    print("="*80)
    
    tracker = AgentTracker(max_loop_repetitions=3, similarity_threshold=0.8)
    
    print("\n🤖 Simulation: Crew of agents solving a problem\n")
    
    interactions = [
        ("Planner", "Researcher", "Find info on AI", 150, "planning"),
        ("Researcher", "Planner", "Found 5 articles", 200, "research"),
        ("Planner", "Coder", "Write a prototype", 180, "planning"),
        ("Coder", "Planner", "Prototype completed", 250, "coding"),
        ("Planner", "Reviewer", "Review the work", 140, "planning"),
        ("Reviewer", "Planner", "Quality OK", 120, "review"),
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
    
    # Final statistics
    summary = tracker.get_conversation_summary()
    print("\n📈 FINAL STATISTICS:")
    print(f"  • Messages per agent: {summary['message_count_by_agent']}")
    print(f"  • Total cost: ${summary['estimated_cost']['total_cost']:.6f}")
    print(f"  • Loops detected: {'Yes ⚠️' if summary['loop_detected'] else 'No ✓'}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  QUICK START GUIDE - AgentTracker".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    # Run all cases
    case_1_basic_tracking()
    case_2_loop_detection()
    case_3_exception_handling()
    case_4_cost_analysis()
    case_5_filtering()
    case_6_export_and_reporting()
    case_7_complex_scenario()
    
    # Conclusion
    print("\n" + "="*80)
    print("✅ QUICK START COMPLETED!")
    print("="*80)
    print("\n📚 For more details, see README_EN.md")
    print("🧪 To run tests: python -m unittest test_agent_tracker_en -v")
    print("📖 To view code: agent_tracker_en.py\n")
