"""
AgentTracker Integration with CrewAI
====================================

This file demonstrates how to integrate the AgentTracker with CrewAI
to monitor interactions between agents.

NOTE: This is an EXAMPLE file. Requires CrewAI installed:
    pip install crewai
"""

from agent_tracker_en import AgentTracker, LoopDetectionException
from typing import Optional, Callable
import json
from datetime import datetime


class TrackedCrewAIIntegration:
    """
    Wrapper to integrate AgentTracker with CrewAI.
    
    This module provides decorators and hooks to automatically log
    communications between CrewAI agents.
    """
    
    def __init__(self, tracker: Optional[AgentTracker] = None,
                 auto_save: bool = False, save_interval: int = 5):
        """
        Initializes the integration.
        
        Args:
            tracker: AgentTracker to use (creates new one if None)
            auto_save: If True, automatically saves log every N messages
            save_interval: Number of messages before auto-save
        """
        self.tracker = tracker or AgentTracker()
        self.auto_save = auto_save
        self.save_interval = save_interval
        self.message_count = 0
        self.log_buffer = []
        
    def log_interaction(self, sender: str, recipient: str, message: str, 
                       tokens: int = 0, metadata: dict = None) -> dict:
        """
        Logs an interaction between agents.
        
        Args:
            sender: Sending agent name
            recipient: Receiving agent name
            message: Message content
            tokens: Tokens consumed
            metadata: Additional metadata (optional)
        
        Returns:
            Dict with logging status
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
            
            # Add to log buffer
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
            
            # Auto-save if needed
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
        Saves logs to a JSON file.
        
        Args:
            filename: Output file name
        
        Returns:
            Path of created file
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "messages": self.log_buffer,
                "summary": self.tracker.get_conversation_summary(),
                "export_time": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def get_status(self) -> dict:
        """Gets current tracking status."""
        return {
            "message_count": self.message_count,
            "agents": list(self.tracker._agents_involved),
            "loop_detected": self.tracker._loop_detected,
            "total_tokens": sum(m.tokens_used for m in self.tracker.messages),
            "estimated_cost": self.tracker.estimate_session_cost()
        }
    
    def reset(self):
        """Resets tracker and buffer."""
        self.tracker.reset_session()
        self.log_buffer.clear()
        self.message_count = 0


# ============================================================================
# MOCK CREWAI AGENT FOR DEMONSTRATION
# ============================================================================

class MockCrewAIAgent:
    """
    Mock agent for demonstrating integration.
    
    In a real situation, this would be an actual CrewAI agent.
    """
    
    def __init__(self, name: str, role: str, tracked_integration: Optional[TrackedCrewAIIntegration] = None):
        self.name = name
        self.role = role
        self.integration = tracked_integration
    
    def execute_task(self, task_description: str, tokens: int = 100) -> dict:
        """Simulates task execution."""
        return {
            "agent": self.name,
            "task": task_description,
            "result": f"Task completed: {task_description}",
            "tokens": tokens
        }
    
    def send_message(self, recipient_name: str, message: str, tokens: int = 50):
        """Simulates sending a message to another agent."""
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
# EXAMPLE SCENARIO
# ============================================================================

def example_crewai_workflow():
    """
    Example of CrewAI workflow with integrated tracking.
    
    This simulates a crew of agents working together on a project.
    """
    
    print("\n" + "="*80)
    print("EXAMPLE: AgentTracker Integration with CrewAI")
    print("="*80)
    
    # Create integration
    integration = TrackedCrewAIIntegration(
        auto_save=False,
        save_interval=10
    )
    
    print("\n🤖 Creating crew:\n")
    
    # Create agents (mock)
    researcher = MockCrewAIAgent("researcher", "Research Specialist", integration)
    writer = MockCrewAIAgent("writer", "Content Writer", integration)
    editor = MockCrewAIAgent("editor", "Editor", integration)
    
    agents = [researcher, writer, editor]
    print(f"✓ {len(agents)} agents created")
    
    print("\n📝 Simulating workflow:\n")
    
    # Simulate workflow
    
    # Step 1: Research
    print("[1] Starting research...")
    researcher.send_message(
        "writer",
        "Completed research on AI. Found 15 relevant articles.",
        tokens=200
    )
    
    # Step 2: Writing
    print("[2] Starting writing...")
    writer.send_message(
        "researcher",
        "Thanks! Writing article based on your results.",
        tokens=150
    )
    
    # Step 3: More messages
    print("[3] Iteration:")
    for i in range(3):
        writer.send_message(
            "editor",
            f"Finished section {i+1}. Can you review?",
            tokens=100
        )
        editor.send_message(
            "writer",
            f"Section {i+1} reviewed. Good quality, continue.",
            tokens=80
        )
    
    print("\n✓ Workflow completed!\n")
    
    # Show statistics
    print("="*80)
    print("📊 TRACKING STATISTICS")
    print("="*80)
    
    status = integration.get_status()
    print(f"\n✓ Messages logged: {status['message_count']}")
    print(f"✓ Agents involved: {', '.join(status['agents'])}")
    print(f"✓ Total tokens: {status['total_tokens']}")
    print(f"✓ Estimated cost (GPT-3.5): ${status['estimated_cost']['total_cost']:.6f}")
    print(f"✓ Loops detected: {'Yes ⚠️' if status['loop_detected'] else 'No ✓'}")
    
    # Save logs
    print("\n" + "="*80)
    print("💾 EXPORT")
    print("="*80)
    
    # Export JSON log
    json_file = integration.save_logs("example_crewai_logs_en.json")
    print(f"\n✓ JSON log exported: {json_file}")
    
    # Export conversation
    txt_file = integration.tracker.export_conversation("example_crewai_conversation_en.txt")
    print(f"✓ Conversation log exported: {txt_file}")
    
    # Show summary preview
    print("\n" + "="*80)
    print("📋 CONVERSATION SUMMARY")
    print("="*80)
    
    summary = integration.tracker.get_conversation_summary()
    for key, value in summary.items():
        if key != "estimated_cost":
            print(f"  {key}: {value}")
    
    return integration


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  AGENTTRACKER + CREWAI INTEGRATION".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    example_crewai_workflow()
    
    # Conclusion
    print("\n" + "="*80)
    print("✅ INTEGRATION COMPLETED!")
    print("="*80)
    print("\n📚 Notes:")
    print("  • This example uses MOCK agents")
    print("  • For real CrewAI, integrate hooks in execute() method")
    print("  • See README_EN.md for complete details")
    print("  • Check crewai_integration_en.py for source code\n")
