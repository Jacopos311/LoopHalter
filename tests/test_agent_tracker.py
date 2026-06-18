"""
Test Suite per AgentTracker

Questo modulo contiene test completi per validare le funzionalità del tracker,
includendo rilevamento di loop, calcolo dei costi e gestione dei messaggi.
"""

import unittest
from agent_tracker import AgentTracker, LoopDetectionException, Message
from datetime import datetime


class TestMessage(unittest.TestCase):
    """Test della classe Message."""

    def test_message_creation(self):
        """Verifica la creazione di un messaggio."""
        msg = Message(
            sender="Agent_A",
            recipient="Agent_B",
            content="Test message",
            tokens_used=100
        )
        self.assertEqual(msg.sender, "Agent_A")
        self.assertEqual(msg.recipient, "Agent_B")
        self.assertEqual(msg.content, "Test message")
        self.assertEqual(msg.tokens_used, 100)

    def test_message_default_timestamp(self):
        """Verifica che il timestamp sia automaticamente impostato."""
        msg = Message(sender="A", recipient="B", content="Test")
        self.assertIsInstance(msg.timestamp, datetime)


class TestAgentTrackerBasics(unittest.TestCase):
    """Test delle funzionalità di base di AgentTracker."""

    def setUp(self):
        """Prepara un tracker per ogni test."""
        self.tracker = AgentTracker()

    def test_initialization(self):
        """Verifica l'inizializzazione corretta."""
        self.assertEqual(len(self.tracker.messages), 0)
        self.assertEqual(self.tracker.max_loop_repetitions, 3)
        self.assertEqual(self.tracker.similarity_threshold, 0.85)

    def test_add_single_message(self):
        """Verifica l'aggiunta di un singolo messaggio."""
        result = self.tracker.add_message(
            sender="Agent_A",
            recipient="Agent_B",
            content="Hello",
            tokens_used=50
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(self.tracker.messages), 1)
        self.assertFalse(result["loop_detected"])

    def test_add_multiple_messages(self):
        """Verifica l'aggiunta di più messaggi."""
        for i in range(5):
            self.tracker.add_message(
                sender="Agent_A",
                recipient="Agent_B",
                content=f"Message {i}",
                tokens_used=50,
                raise_on_loop=False
            )
        self.assertEqual(len(self.tracker.messages), 5)

    def test_agents_involved_tracking(self):
        """Verifica il tracking degli agenti coinvolti."""
        self.tracker.add_message("Agent_A", "Agent_B", "Test", 50)
        self.tracker.add_message("Agent_C", "Agent_D", "Test", 50)
        
        agents = self.tracker._agents_involved
        self.assertIn("Agent_A", agents)
        self.assertIn("Agent_B", agents)
        self.assertIn("Agent_C", agents)
        self.assertIn("Agent_D", agents)


class TestLoopDetection(unittest.TestCase):
    """Test del rilevamento di loop."""

    def setUp(self):
        """Prepara un tracker per ogni test."""
        self.tracker = AgentTracker(max_loop_repetitions=3, 
                                   similarity_threshold=0.85)

    def test_no_loop_with_different_messages(self):
        """Verifica che messaggi diversi non attivino il loop detector."""
        messages = [
            "Come stai?",
            "Mi piace il calcio",
            "Qual è il tuo colore preferito?",
            "Parla di Python"
        ]
        for msg in messages:
            result = self.tracker.add_message(
                sender="Agent_A",
                recipient="Agent_B",
                content=msg,
                tokens_used=50
            )
            self.assertFalse(result["loop_detected"])

    def test_loop_detection_with_identical_messages(self):
        """Verifica il rilevamento di loop con messaggi identici."""
        identical_msg = "Ripeti questa frase!"
        
        for i in range(4):
            result = self.tracker.add_message(
                sender="Agent_A",
                recipient="Agent_B",
                content=identical_msg,
                tokens_used=50,
                raise_on_loop=False
            )
            
            if i >= 3:  # Dopo 4 messaggi identici (3 ripetizioni)
                self.assertTrue(result["loop_detected"])
                self.assertGreaterEqual(result["loop_info"]["repetitions"], 3)

    def test_loop_detection_with_similar_messages(self):
        """Verifica il rilevamento di loop con messaggi molto simili."""
        messages = [
            "Puoi ripetere la domanda?",
            "Puoi ripetere la domanda?",
            "Puoi ripetere la domanda?",
            "Puoi ripetere la domanda?"
        ]
        
        for i, msg in enumerate(messages):
            result = self.tracker.add_message(
                sender="Agent_A",
                recipient="Agent_B",
                content=msg,
                tokens_used=50,
                raise_on_loop=False
            )
            
            if i >= 3:
                self.assertTrue(result["loop_detected"])

    def test_loop_exception_raising(self):
        """Verifica che l'eccezione venga sollevata quando raise_on_loop=True."""
        for i in range(4):
            if i < 3:
                self.tracker.add_message(
                    sender="Agent_A",
                    recipient="Agent_B",
                    content="Stesso messaggio",
                    tokens_used=50,
                    raise_on_loop=False
                )
            else:
                # Al 4° messaggio dovrebbe sollevare eccezione
                with self.assertRaises(LoopDetectionException):
                    self.tracker.add_message(
                        sender="Agent_A",
                        recipient="Agent_B",
                        content="Stesso messaggio",
                        tokens_used=50,
                        raise_on_loop=True
                    )

    def test_loop_detection_bidirectional(self):
        """Verifica il rilevamento di loop in conversazioni bidirezionali."""
        # A -> B
        self.tracker.add_message("Agent_A", "Agent_B", "Ciao", 50, False)
        # B -> A
        self.tracker.add_message("Agent_B", "Agent_A", "Ciao", 50, False)
        # A -> B
        self.tracker.add_message("Agent_A", "Agent_B", "Ciao", 50, False)
        # B -> A
        result = self.tracker.add_message(
            "Agent_B", "Agent_A", "Ciao", 50, 
            raise_on_loop=False
        )
        
        self.assertTrue(result["loop_detected"])

    def test_custom_similarity_threshold(self):
        """Verifica l'uso di una soglia di similarità personalizzata."""
        tracker = AgentTracker(max_loop_repetitions=3, 
                              similarity_threshold=0.95)  # Soglia alta
        
        # Messaggi molto diversi tra loro
        tracker.add_message("Agent_A", "Agent_B", "Ciao, come stai?", 50, False)
        tracker.add_message("Agent_A", "Agent_B", "Mi piace il calcio", 50, False)
        result = tracker.add_message(
            "Agent_A", "Agent_B", "Python è fantastico", 50, 
            raise_on_loop=False
        )
        
        # Con messaggi diversi e soglia alta, non dovrebbe rilevare loop
        self.assertFalse(result["loop_detected"])


class TestCostCalculation(unittest.TestCase):
    """Test del calcolo dei costi."""

    def setUp(self):
        """Prepara un tracker per ogni test."""
        self.tracker = AgentTracker()

    def test_cost_calculation_empty_session(self):
        """Verifica il costo di una sessione vuota."""
        cost = self.tracker.estimate_session_cost()
        self.assertEqual(cost["total_cost"], 0)
        self.assertEqual(cost["total_tokens"], 0)

    def test_cost_calculation_with_tokens(self):
        """Verifica il calcolo del costo con token."""
        self.tracker.add_message("Agent_A", "Agent_B", "Test", tokens_used=1000)
        cost = self.tracker.estimate_session_cost(model="gpt-3.5-turbo")
        
        self.assertEqual(cost["total_tokens"], 1000)
        self.assertGreater(cost["total_cost"], 0)
        self.assertGreater(cost["input_cost"], 0)
        self.assertGreater(cost["output_cost"], 0)

    def test_cost_calculation_different_models(self):
        """Verifica il calcolo con diversi modelli."""
        self.tracker.add_message("Agent_A", "Agent_B", "Test", tokens_used=1000)
        
        cost_gpt4 = self.tracker.estimate_session_cost(model="gpt-4")
        cost_gpt35 = self.tracker.estimate_session_cost(model="gpt-3.5-turbo")
        cost_default = self.tracker.estimate_session_cost(model="default")
        
        # I costi dovrebbero essere diversi per modelli diversi
        self.assertNotEqual(cost_gpt4["total_cost"], cost_gpt35["total_cost"])
        self.assertLess(cost_default["total_cost"], cost_gpt4["total_cost"])

    def test_cost_proportional_to_tokens(self):
        """Verifica che il costo sia proporzionale ai token."""
        self.tracker.add_message("Agent_A", "Agent_B", "Test", tokens_used=500)
        cost1 = self.tracker.estimate_session_cost()["total_cost"]
        
        self.tracker.reset_session()
        self.tracker.add_message("Agent_A", "Agent_B", "Test", tokens_used=1000)
        cost2 = self.tracker.estimate_session_cost()["total_cost"]
        
        # Il costo con il doppio dei token dovrebbe essere approssimativamente 
        # il doppio
        self.assertAlmostEqual(cost2 / cost1, 2.0, places=1)


class TestMessageFiltering(unittest.TestCase):
    """Test del filtering dei messaggi."""

    def setUp(self):
        """Prepara un tracker con alcuni messaggi."""
        self.tracker = AgentTracker()
        self.tracker.add_message("Agent_A", "Agent_B", "Msg 1", 50)
        self.tracker.add_message("Agent_B", "Agent_A", "Msg 2", 60)
        self.tracker.add_message("Agent_A", "Agent_C", "Msg 3", 70)

    def test_get_all_messages(self):
        """Verifica il recupero di tutti i messaggi."""
        messages = self.tracker.get_message_history()
        self.assertEqual(len(messages), 3)

    def test_filter_by_sender(self):
        """Verifica il filtraggio per mittente."""
        messages = self.tracker.get_message_history(sender="Agent_A")
        self.assertEqual(len(messages), 2)
        for msg in messages:
            self.assertEqual(msg.sender, "Agent_A")

    def test_filter_by_recipient(self):
        """Verifica il filtraggio per destinatario."""
        messages = self.tracker.get_message_history(recipient="Agent_B")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, "Msg 1")

    def test_filter_by_both(self):
        """Verifica il filtraggio per mittente e destinatario."""
        messages = self.tracker.get_message_history(
            sender="Agent_A",
            recipient="Agent_B"
        )
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, "Msg 1")


class TestSessionSummary(unittest.TestCase):
    """Test del riepilogo della sessione."""

    def setUp(self):
        """Prepara un tracker con alcuni messaggi."""
        self.tracker = AgentTracker()
        self.tracker.add_message("Agent_A", "Agent_B", "Test 1", 100)
        self.tracker.add_message("Agent_B", "Agent_C", "Test 2", 150)

    def test_conversation_summary_structure(self):
        """Verifica la struttura del riepilogo."""
        summary = self.tracker.get_conversation_summary()
        
        required_keys = [
            "total_messages", "agents_involved", "session_duration_seconds",
            "loop_detected", "total_tokens", "estimated_cost",
            "message_count_by_agent", "start_time", "end_time"
        ]
        
        for key in required_keys:
            self.assertIn(key, summary)

    def test_conversation_summary_values(self):
        """Verifica i valori del riepilogo."""
        summary = self.tracker.get_conversation_summary()
        
        self.assertEqual(summary["total_messages"], 2)
        self.assertEqual(len(summary["agents_involved"]), 3)
        self.assertEqual(summary["total_tokens"], 250)
        self.assertFalse(summary["loop_detected"])


class TestResetAndExport(unittest.TestCase):
    """Test del reset e dell'esportazione."""

    def setUp(self):
        """Prepara un tracker."""
        self.tracker = AgentTracker()

    def test_reset_session(self):
        """Verifica il reset della sessione."""
        self.tracker.add_message("Agent_A", "Agent_B", "Test", 100)
        self.assertEqual(len(self.tracker.messages), 1)
        
        self.tracker.reset_session()
        
        self.assertEqual(len(self.tracker.messages), 0)
        self.assertEqual(len(self.tracker._agents_involved), 0)
        self.assertFalse(self.tracker._loop_detected)

    def test_export_conversation(self):
        """Verifica l'esportazione della conversazione."""
        self.tracker.add_message("Agent_A", "Agent_B", "Test message", 100)
        
        filename = self.tracker.export_conversation("test_export.txt")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Test message", content)
            self.assertIn("Agent_A", content)
            self.assertIn("Agent_B", content)
        
        # Cleanup
        import os
        os.remove(filename)


class TestSimilarityCalculation(unittest.TestCase):
    """Test del calcolo della similarità."""

    def setUp(self):
        """Prepara un tracker."""
        self.tracker = AgentTracker()

    def test_identical_texts_similarity(self):
        """Verifica la similarità di testi identici."""
        sim = self.tracker._calculate_similarity("Hello", "Hello")
        self.assertEqual(sim, 1.0)

    def test_completely_different_texts(self):
        """Verifica la similarità di testi completamente diversi."""
        sim = self.tracker._calculate_similarity("Hello", "XYZ123")
        self.assertLess(sim, 0.5)

    def test_similar_texts(self):
        """Verifica la similarità di testi simili."""
        sim = self.tracker._calculate_similarity(
            "Puoi ripetere la domanda?",
            "Puoi ripetere la domanda?"
        )
        self.assertGreater(sim, 0.95)

    def test_case_insensitive_similarity(self):
        """Verifica che il calcolo sia case-insensitive."""
        sim1 = self.tracker._calculate_similarity("HELLO", "hello")
        sim2 = self.tracker._calculate_similarity("Hello", "hello")
        
        self.assertEqual(sim1, 1.0)
        self.assertEqual(sim2, 1.0)


def run_all_tests():
    """Esegue tutti i test e fornisce un report."""
    # Crea una test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Aggiungi tutti i test
    suite.addTests(loader.loadTestsFromTestCase(TestMessage))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentTrackerBasics))
    suite.addTests(loader.loadTestsFromTestCase(TestLoopDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestCostCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestMessageFiltering))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionSummary))
    suite.addTests(loader.loadTestsFromTestCase(TestResetAndExport))
    suite.addTests(loader.loadTestsFromTestCase(TestSimilarityCalculation))
    
    # Esegui i test
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    run_all_tests()
