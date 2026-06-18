"""
Agent Interaction Tracker and Loop Detection Middleware

This module provides a tracking system to monitor interactions between AI agents,
calculate session costs, and detect repetitive communication loops.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import difflib
import warnings


@dataclass
class Message:
    """Represents a single message exchanged between agents."""
    sender: str
    recipient: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    tokens_used: int = 0

    def __repr__(self) -> str:
        return (f"Message(sender={self.sender}, recipient={self.recipient}, "
                f"tokens={self.tokens_used}, time={self.timestamp.strftime('%H:%M:%S')})")


class LoopDetectionException(Exception):
    """Exception raised when a communication loop is detected."""
    pass


class AgentTracker:
    """
    Middleware for tracking interactions between AI agents.
    
    Main features:
    - Chronological storage of exchanged messages
    - Cost calculation based on consumed tokens
    - Automatic detection of communication loops
    - Query capabilities on message history
    """

    # Cost per token (based on OpenAI GPT-4 models)
    TOKEN_COSTS = {
        "gpt-4": {"input": 0.00003, "output": 0.00006},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "default": {"input": 0.00001, "output": 0.00002}
    }

    def __init__(self, max_loop_repetitions: int = 3, 
                 similarity_threshold: float = 0.85):
        """
        Initializes the AgentTracker.
        
        Args:
            max_loop_repetitions: Maximum number of identical messages before 
                                 detecting a loop (default: 3)
            similarity_threshold: Similarity threshold (0-1) to detect repetitive
                                 patterns (default: 0.85)
        """
        self.messages: List[Message] = []
        self.max_loop_repetitions = max_loop_repetitions
        self.similarity_threshold = similarity_threshold
        self.session_start = datetime.now()
        self._loop_detected = False
        self._agents_involved: set = set()

    def add_message(self, sender: str, recipient: str, content: str, 
                   tokens_used: int = 0, raise_on_loop: bool = True) -> Dict[str, any]:
        """
        Adds a message to the history and checks for loops.
        
        Args:
            sender: Sending agent ID
            recipient: Receiving agent ID
            content: Message content
            tokens_used: Tokens consumed for this message
            raise_on_loop: If True, raises exception when loop is detected
        
        Returns:
            Dict with 'status', 'loop_detected', 'warning_message' and 'loop_info'
        
        Raises:
            LoopDetectionException: If raise_on_loop=True and loop is detected
        """
        # Create new message
        message = Message(
            sender=sender,
            recipient=recipient,
            content=content,
            tokens_used=tokens_used
        )

        # Update involved agents
        self._agents_involved.add(sender)
        self._agents_involved.add(recipient)

        # Add message to history
        self.messages.append(message)

        # Check for loops
        loop_info = self._check_for_loops(sender, recipient)

        response = {
            "status": "success",
            "message_count": len(self.messages),
            "loop_detected": loop_info["detected"],
            "warning_message": loop_info["message"],
            "loop_info": loop_info
        }

        # Gestisci il loop se rilevato
        if loop_info["detected"]:
            self._loop_detected = True
            if raise_on_loop:
                raise LoopDetectionException(loop_info["message"])
            else:
                warnings.warn(loop_info["message"], UserWarning)

        return response

    def _check_for_loops(self, sender: str, recipient: str) -> Dict[str, any]:
        """
        Verifica la presenza di loop di comunicazione tra due agenti.
        
        Algoritmo:
        1. Estrae gli ultimi N messaggi tra i due agenti (bidiezionale)
        2. Calcola la similarità tra messaggi consecutivi
        3. Rileva pattern ripetitivi (messaggi identici o molto simili)
        4. Se trovati più di max_loop_repetitions repetizioni, segnala loop
        
        Args:
            sender: ID dell'agente mittente
            recipient: ID dell'agente destinatario
        
        Returns:
            Dict con 'detected', 'message', 'repetitions', 'similar_messages'
        """
        # Estrai i messaggi tra i due agenti
        conversation = self._get_conversation_between(sender, recipient)

        if len(conversation) < self.max_loop_repetitions:
            return {
                "detected": False,
                "message": "Non sono disponibili sufficienti messaggi per il rilevamento",
                "repetitions": 0,
                "similar_messages": []
            }

        # Analizza gli ultimi messaggi per rilevare pattern
        loop_info = self._analyze_message_patterns(conversation)

        return loop_info

    def _get_conversation_between(self, agent1: str, agent2: str) -> List[Message]:
        """
        Estrae la conversazione bidirezionale tra due agenti.
        
        Args:
            agent1: Primo agente
            agent2: Secondo agente
        
        Returns:
            Lista di messaggi scambiati tra i due agenti (in ordine cronologico)
        """
        conversation = [
            msg for msg in self.messages
            if (msg.sender == agent1 and msg.recipient == agent2) or
               (msg.sender == agent2 and msg.recipient == agent1)
        ]
        return conversation

    def _analyze_message_patterns(self, messages: List[Message]) -> Dict[str, any]:
        """
        Analizza i pattern nei messaggi per rilevare loop e ripetizioni.
        
        Args:
            messages: Lista di messaggi da analizzare
        
        Returns:
            Dict con informazioni sul loop rilevato
        """
        if len(messages) < 2:
            return {
                "detected": False,
                "message": "Non sono disponibili abbastanza messaggi per l'analisi",
                "repetitions": 0,
                "similar_messages": []
            }

        # Estrai solo i contenuti
        contents = [msg.content for msg in messages]

        # Cerca pattern ripetitivi negli ultimi messaggi
        repetition_count = 0
        max_repetitions = 0
        repeated_message_group = []

        # Analizza da dietro (ultimi messaggi)
        for i in range(len(contents) - 1, 0, -1):
            similarity = self._calculate_similarity(contents[i], contents[i-1])

            if similarity >= self.similarity_threshold:
                repetition_count += 1
                repeated_message_group.append({
                    "message": contents[i],
                    "similarity": similarity,
                    "index": i
                })
                max_repetitions = max(max_repetitions, repetition_count)
            else:
                repetition_count = 0
                if max_repetitions >= self.max_loop_repetitions:
                    break

        # Se trovato un loop
        detected = max_repetitions >= self.max_loop_repetitions

        if detected:
            loop_message = (
                f"⚠️ LOOP RILEVATO: {max_repetitions} messaggi ripetitivi con "
                f"similarità >= {self.similarity_threshold*100:.0f}% "
                f"tra gli ultimi {len(repeated_message_group)} messaggi"
            )
        else:
            loop_message = (
                f"No loop detected. Ripetizioni massime trovate: {max_repetitions}"
            )

        return {
            "detected": detected,
            "message": loop_message,
            "repetitions": max_repetitions,
            "similar_messages": repeated_message_group,
            "threshold": self.similarity_threshold
        }

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcola la similarità tra due testi usando SequenceMatcher.
        
        Args:
            text1: Primo testo
            text2: Secondo testo
        
        Returns:
            Valore di similarità tra 0 e 1
        """
        matcher = difflib.SequenceMatcher(None, text1.lower(), text2.lower())
        return matcher.ratio()

    def estimate_session_cost(self, model: str = "default") -> Dict[str, float]:
        """
        Calculates estimated session cost based on consumed tokens.
        
        Args:
            model: Model used for cost calculation
                  ('gpt-4', 'gpt-3.5-turbo', 'default')
        
        Returns:
            Dict with 'total_cost', 'input_cost', 'output_cost', 'total_tokens'
        """
        if model not in self.TOKEN_COSTS:
            model = "default"

        costs = self.TOKEN_COSTS[model]
        total_tokens = sum(msg.tokens_used for msg in self.messages)

        # Assume 80% input tokens e 20% output tokens (rapporto comune)
        input_tokens = int(total_tokens * 0.8)
        output_tokens = int(total_tokens * 0.2)

        input_cost = input_tokens * costs["input"]
        output_cost = output_tokens * costs["output"]
        total_cost = input_cost + output_cost

        return {
            "total_cost": round(total_cost, 6),
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_tokens": total_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "model": model
        }

    def get_message_history(self, sender: Optional[str] = None, 
                           recipient: Optional[str] = None) -> List[Message]:
        """
        Retrieves message history with optional filters.
        
        Args:
            sender: Filter by sender (optional)
            recipient: Filter by recipient (optional)
        
        Returns:
            List of messages matching the criteria
        """
        filtered_messages = self.messages

        if sender:
            filtered_messages = [m for m in filtered_messages if m.sender == sender]
        
        if recipient:
            filtered_messages = [m for m in filtered_messages 
                               if m.recipient == recipient]

        return filtered_messages

    def get_conversation_summary(self) -> Dict[str, any]:
        """
        Provides a complete summary of the monitoring session.
        
        Returns:
            Dict with session statistics
        """
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        return {
            "total_messages": len(self.messages),
            "agents_involved": sorted(list(self._agents_involved)),
            "session_duration_seconds": round(session_duration, 2),
            "loop_detected": self._loop_detected,
            "total_tokens": sum(msg.tokens_used for msg in self.messages),
            "estimated_cost": self.estimate_session_cost(),
            "message_count_by_agent": self._count_messages_by_agent(),
            "start_time": self.session_start.isoformat(),
            "end_time": datetime.now().isoformat()
        }

    def _count_messages_by_agent(self) -> Dict[str, int]:
        """Conteggia i messaggi per agente."""
        count = defaultdict(int)
        for msg in self.messages:
            count[msg.sender] += 1
        return dict(count)

    def reset_session(self) -> None:
        """Resets the session state and clears the history."""
        self.messages.clear()
        self._agents_involved.clear()
        self._loop_detected = False
        self.session_start = datetime.now()

    def export_conversation(self, filename: str = "conversation_log.txt") -> str:
        """
        Exports the conversation to a text file.
        
        Args:
            filename: Output file name
        
        Returns:
            Path of created file
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("AGENT INTERACTION LOG\n")
            f.write("=" * 80 + "\n\n")

            for i, msg in enumerate(self.messages, 1):
                f.write(f"[{i}] {msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"    From: {msg.sender}\n")
                f.write(f"    To: {msg.recipient}\n")
                f.write(f"    Tokens: {msg.tokens_used}\n")
                f.write(f"    Content: {msg.content[:100]}...\n" 
                        if len(msg.content) > 100 
                        else f"    Content: {msg.content}\n")
                f.write("-" * 80 + "\n\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("SESSION SUMMARY\n")
            f.write("=" * 80 + "\n")
            summary = self.get_conversation_summary()
            for key, value in summary.items():
                f.write(f"{key}: {value}\n")

        return filename


# ============================================================================
# ESEMPIO DI UTILIZZO E TEST
# ============================================================================

if __name__ == "__main__":
    print("🚀 Agent Tracker - Esempio di utilizzo\n")
    print("=" * 80)

    # Crea un'istanza di AgentTracker
    tracker = AgentTracker(max_loop_repetitions=3, similarity_threshold=0.85)

    print("\n📝 Test 1: Adding normal messages\n")
    try:
        result = tracker.add_message(
            sender="Agent_A",
            recipient="Agent_B",
            content="Qual è il significato della vita?",
            tokens_used=150
        )
        print(f"✓ Messaggio 1 aggiunto: {result['status']}")

        result = tracker.add_message(
            sender="Agent_B",
            recipient="Agent_A",
            content="La risposta è 42, secondo Douglas Adams.",
            tokens_used=120
        )
        print(f"✓ Messaggio 2 aggiunto: {result['status']}")

    except LoopDetectionException as e:
        print(f"❌ Loop rilevato: {e}")

    print("\n📝 Test 2: Loop detection (repetitive messages)\n")
    try:
        # Aggiungi messaggi ripetitivi
        for i in range(4):
            result = tracker.add_message(
                sender="Agent_A",
                recipient="Agent_B",
                content="Puoi ripetere la domanda?",  # Messaggio quasi identico
                tokens_used=100,
                raise_on_loop=False  # Non sollevare eccezione, solo avvertimento
            )
            print(f"Messaggio {i+3}: {result['warning_message']}")
            if result['loop_detected']:
                print(f"   ⚠️ Loop info: {result['loop_info']}")

    except LoopDetectionException as e:
        print(f"❌ Loop rilevato: {e}")

    print("\n💰 Test 3: Cost calculation\n")
    cost_summary = tracker.estimate_session_cost(model="gpt-3.5-turbo")
    print(f"Estimated cost (GPT-3.5-Turbo):")
    print(f"  - Total tokens: {cost_summary['total_tokens']}")
    print(f"  - Input cost: ${cost_summary['input_cost']:.6f}")
    print(f"  - Output cost: ${cost_summary['output_cost']:.6f}")
    print(f"  - Total cost: ${cost_summary['total_cost']:.6f}")

    print("\n📊 Test 4: Session summary\n")
    summary = tracker.get_conversation_summary()
    for key, value in summary.items():
        if key != "estimated_cost":
            print(f"  {key}: {value}")

    print("\n📄 Test 5: Exporting conversation\n")
    export_file = tracker.export_conversation("test_conversation_log.txt")
    print(f"✓ Conversation exported to: {export_file}")

    print("\n" + "=" * 80)
    print("✅ All tests completed!")
