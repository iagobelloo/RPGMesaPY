import unittest
import os
from unittest.mock import MagicMock
from ai_master.ai_client import AIGameMaster

class TestAIAgent(unittest.TestCase):
    """
    Testes de validação da IA (AIGameMaster / Maelor / Taverna):
    - Eliminação de duplicidade de mensagens narrativas no turno e no histórico de log.
    - Detecção rica e viva de intenções do jogador na Taverna (estrada, missões, taverneiro, Maelor).
    - Enriquecimento dos fallbacks offline específicos e contextuais.
    - Refinamento do prólogo e concordância estrita de gênero (masculino/feminino).
    """

    def setUp(self):
        self.ai = AIGameMaster()
        self.ai.client = MagicMock()
        self.ai.client.chats.create = MagicMock(side_effect=Exception("Offline"))

    # 1. Eliminação de duplicidade no log / fila
    def test_01_no_duplicate_narrative_in_chat_history(self):
        """Valida que chamadas repetidas ou idempotentes não duplicam no histórico recente."""
        self.ai.chat_history.clear()
        self.ai._generate_text_with_retry = MagicMock(return_value='{"texto": "O taverneiro limpa a caneca em silêncio.", "npc_falando": "Taverneiro"}')

        # Primeira inserção
        res1 = self.ai.generate_narrative_from_log("[LOG] Entrada", {"race": "Humano", "class": "Guerreiro"}, {}, "olhar taverna")
        self.assertEqual(len(self.ai.chat_history), 1)
        self.assertEqual(self.ai.chat_history[0]["dm"], "O taverneiro limpa a caneca em silêncio.")

        # Tentativa de inserção duplicada do mesmo turno/texto
        res2 = self.ai.generate_narrative_from_log("[LOG] Entrada", {"race": "Humano", "class": "Guerreiro"}, {}, "olhar taverna")
        self.assertEqual(len(self.ai.chat_history), 1, "Histórico recente não deve conter entradas duplicadas idênticas consecutivas.")

    def test_02_generate_narrative_from_math_optional_ui_queue(self):
        """Valida que generate_narrative_from_math respeita a fila ui_queue sem duplicar mensagens."""
        class MockQueue:
            def __init__(self):
                self.items = []
            def put(self, item):
                self.items.append(item)

        q = MockQueue()
        res = self.ai.generate_narrative_from_math("Dano sofrido.", "golpe de adaga", ui_queue=q)
        self.assertIsInstance(res, str)
        self.assertEqual(len(q.items), 1)
        self.assertEqual(q.items[0]["type"], "narrative")
        self.assertEqual(q.items[0]["content"], res)

    # 2. Detecção de intenções do jogador na Taverna (Offline / Heurística)
    def test_03_detect_road_perils_and_hanging_tree_trail(self):
        """Valida detecção de perguntas sobre o que espera lá fora e a Trilha dos Enforcados."""
        self.ai.client.models.generate_content = MagicMock(side_effect=Exception("Offline"))

        queries = [
            "o que me espera lá fora?",
            "o que tem la fora?",
            "quais os perigos da estrada?",
            "falar sobre a trilha dos enforcados",
            "o que me aguarda la fora na trilha?"
        ]
        for q in queries:
            res = self.ai.parse_player_intent(q, {})
            self.assertEqual(res["tipo_acao"], "DIALOGAR", f"Query '{q}' deveria ser DIALOGAR.")
            self.assertNotEqual(res["tipo_acao"], "AVANCAR_HISTORIA", f"Query '{q}' não pode avançar a história.")
            self.assertTrue(
                "estrada" in res["intencao_cena"] or "perigos" in res["intencao_cena"] or "enforcados" in res["intencao_cena"],
                f"Intenção contextual não encontrada para '{q}'."
            )

    def test_04_detect_missions_and_contracts_acceptance(self):
        """Valida detecção de perguntas sobre como aceitar contratos e trabalhos disponíveis."""
        self.ai.client.models.generate_content = MagicMock(side_effect=Exception("Offline"))

        queries = [
            "como aceitar missões?",
            "como aceitar um contrato no mural?",
            "onde pego trabalho?",
            "quais os contratos disponíveis?",
            "como funciona o quadro de avisos?"
        ]
        for q in queries:
            res = self.ai.parse_player_intent(q, {})
            self.assertEqual(res["tipo_acao"], "DIALOGAR")
            self.assertNotEqual(res["tipo_acao"], "AVANCAR_HISTORIA")
            self.assertTrue("missões" in res["intencao_cena"] or "trabalhos" in res["intencao_cena"])

    def test_05_detect_everyday_barkeep_conversations(self):
        """Valida conversas cotidianas: pagar conta, falar do clima, falar do reino e pedir bebida."""
        self.ai.client.models.generate_content = MagicMock(side_effect=Exception("Offline"))

        # Pagar conta
        res_bill = self.ai.parse_player_intent("pagar a conta da cerveja", {})
        self.assertEqual(res_bill["tipo_acao"], "DIALOGAR")
        self.assertIn("paga o taverneiro", res_bill["intencao_cena"])

        # Clima
        res_weather = self.ai.parse_player_intent("falar sobre o clima lá fora", {})
        self.assertEqual(res_weather["tipo_acao"], "DIALOGAR")
        self.assertIn("clima", res_weather["intencao_cena"])

        # Reino
        res_realm = self.ai.parse_player_intent("o que aconteceu com o reino?", {})
        self.assertEqual(res_realm["tipo_acao"], "DIALOGAR")
        self.assertIn("reino", res_realm["intencao_cena"])

        # Bebida
        res_drink = self.ai.parse_player_intent("pedir uma caneca de hidromel", {})
        self.assertEqual(res_drink["tipo_acao"], "DIALOGAR")
        self.assertIn("bebida", res_drink["intencao_cena"])

    def test_06_detect_menestrel_maelor_dialogues(self):
        """Valida diálogos com Maelor: pedir canção, falar do Tirano das Cinzas e do Orbe."""
        self.ai.client.models.generate_content = MagicMock(side_effect=Exception("Offline"))

        # Canção
        res_song = self.ai.parse_player_intent("pedir uma canção a maelor", {})
        self.assertEqual(res_song["tipo_acao"], "DIALOGAR")
        self.assertIn("canção", res_song["intencao_cena"])
        self.assertEqual(res_song["alvo"], ["Maelor"])

        # Tirano das Cinzas
        res_tyrant = self.ai.parse_player_intent("quem é o tirano das cinzas?", {})
        self.assertEqual(res_tyrant["tipo_acao"], "DIALOGAR")
        self.assertIn("tirano", res_tyrant["intencao_cena"].lower())

        # Orbe Quebra-Chamas
        res_orb = self.ai.parse_player_intent("perguntar sobre o orbe quebra-chamas", {})
        self.assertEqual(res_orb["tipo_acao"], "DIALOGAR")
        self.assertIn("orbe", res_orb["intencao_cena"].lower())

    # 3. Respostas vivas e contextuais no Fallback Visceral
    def test_07_visceral_fallback_specific_responses(self):
        """Valida respostas detalhadas do fallback sem dedilhar melancólico repetitivo."""
        # 1. Trilha dos Enforcados / perigos lá fora
        fb_trail = self.ai._create_visceral_fallback("", "perguntar sobre a trilha dos enforcados")
        self.assertNotIn("dedilhar melancólico", fb_trail.lower())
        self.assertTrue("enforcados" in fb_trail.lower() or "saqueadores" in fb_trail.lower() or "estrada" in fb_trail.lower())

        fb_outside = self.ai._create_visceral_fallback("", "o que me espera lá fora?")
        self.assertNotIn("dedilhar melancólico", fb_outside.lower())
        self.assertTrue("cinzas" in fb_outside.lower() or "frio" in fb_outside.lower() or "portas" in fb_outside.lower() or "taverneiro" in fb_outside.lower())

        # 2. Como aceitar missões
        fb_accept = self.ai._create_visceral_fallback("", "como aceitar missões no mural?")
        self.assertNotIn("dedilhar melancólico", fb_accept.lower())
        self.assertTrue("grimório" in fb_accept.lower() or "mural" in fb_accept.lower() or "contrato" in fb_accept.lower())

        # 3. Pagar conta
        fb_bill = self.ai._create_visceral_fallback("", "pagar a conta ao taverneiro")
        self.assertNotIn("dedilhar melancólico", fb_bill.lower())
        self.assertTrue("cobre" in fb_bill.lower() or "moeda" in fb_bill.lower() or "quites" in fb_bill.lower())

        # 4. Falar sobre o clima
        fb_weather = self.ai._create_visceral_fallback("", "falar sobre o clima lá fora com o taverneiro")
        self.assertNotIn("dedilhar melancólico", fb_weather.lower())
        self.assertTrue("fuligem" in fb_weather.lower() or "vento" in fb_weather.lower() or "cinzas" in fb_weather.lower())

        # 5. Falar sobre o reino
        fb_realm = self.ai._create_visceral_fallback("", "perguntar ao taverneiro sobre o reino e a corte")
        self.assertNotIn("dedilhar melancólico", fb_realm.lower())
        self.assertTrue("reino" in fb_realm.lower() or "corte" in fb_realm.lower() or "vanguarda" in fb_realm.lower() or "nobres" in fb_realm.lower())

        # 6. Maelor: pedir canção
        fb_song = self.ai._create_visceral_fallback("", "pedir uma canção a maelor")
        self.assertNotIn("dedilhar melancólico", fb_song.lower())
        self.assertTrue("balada dos caídos" in fb_song.lower() or "canção" in fb_song.lower() or "alaúde" in fb_song.lower())

        # 7. Maelor: lenda do Tirano das Cinzas
        fb_tyrant = self.ai._create_visceral_fallback("", "perguntar sobre o tirano das cinzas")
        self.assertNotIn("dedilhar melancólico", fb_tyrant.lower())
        self.assertTrue("obsidiana" in fb_tyrant.lower() or "tirano" in fb_tyrant.lower() or "beat 15" in fb_tyrant.lower() or "caldeira" in fb_tyrant.lower())

        # 8. Maelor: lenda do Orbe Quebra-Chamas
        fb_orb = self.ai._create_visceral_fallback("", "perguntar a maelor sobre o orbe quebra-chamas")
        self.assertNotIn("dedilhar melancólico", fb_orb.lower())
        self.assertTrue("orbe" in fb_orb.lower() or "relíquia" in fb_orb.lower() or "muralha de fogo" in fb_orb.lower())

    # 4. Prólogo com concordância de gênero
    def test_08_gender_concordance_in_prologue(self):
        """Valida concordância gramatical estrita entre masculino e feminino."""
        # Personagem Feminina
        char_fem = {
            "name": "Valéria",
            "race": "Humano",
            "class": "Guerreiro",
            "background": "Forasteiro",
            "alignment": "Neutro e Bom",
            "gender": "female"
        }
        prologue_f = self.ai.get_personalized_prologue(char_fem)
        self.assertIn("Valéria", prologue_f)
        self.assertIn("Humana", prologue_f)
        self.assertIn("Guerreira", prologue_f)
        self.assertIn("Forasteira", prologue_f)

        # Personagem Masculino
        char_masc = {
            "name": "Valerius",
            "race": "Humano",
            "class": "Guerreiro",
            "background": "Forasteiro",
            "alignment": "Neutro e Bom",
            "gender": "male"
        }
        prologue_m = self.ai.get_personalized_prologue(char_masc)
        self.assertIn("Valerius", prologue_m)
        self.assertIn("Humano", prologue_m)
        self.assertIn("Guerreiro", prologue_m)
        self.assertIn("Forasteiro", prologue_m)

    def test_09_gender_helpers_and_prologue_fallbacks(self):
        """Valida métodos utilitários de gênero e fallbacks de geração de prólogo."""
        # Helpers
        self.assertEqual(self.ai._format_gender_race("Elfo da Floresta", True), "Elfa da Floresta")
        self.assertEqual(self.ai._format_gender_race("Anão da Colina", True), "Anã da Colina")
        self.assertEqual(self.ai._format_gender_class("Ladino", True), "Ladina")
        self.assertEqual(self.ai._format_gender_class("Mago", True), "Maga")
        self.assertEqual(self.ai._format_gender_background("Soldado", True), "Soldada")

        # Fallback de geração de perguntas do prólogo
        self.ai._generate_text_with_retry = MagicMock(side_effect=Exception("Offline"))
        char_f = {"gender": "female", "class": "Clérigo", "background": "Acólito"}
        questions = self.ai.generate_prologue_questions(char_f)
        self.assertEqual(len(questions), 3)
        self.assertIn("Acólita", questions[0])
        self.assertIn("Clériga", questions[1])
        self.assertIn(" a trouxe ", questions[2])

        # Fallback de geração do prólogo dinâmico
        dyn_prologue_f = self.ai.generate_prologue({"name": "Aria", "race": "Elfo", "class": "Mago", "gender": "female"}, [])
        self.assertIn("Como uma Elfa Maga", dyn_prologue_f)

    # 5. Correção de Fallback de Contrato vs Diálogo/Observação e Cascata de Modelos
    def test_10_beat_1_mural_does_not_trigger_contract_completed_fallback(self):
        """
        Valida que menção a 'contratos de caçada no mural' no log do Beat 1
        NUNCA dispara o fallback de contrato concluído em diálogos ou observação.
        """
        beat_1_log = "Na Taverna do Dragão Acordado há lareira crepitante e contratos de caçada no mural de avisos."

        # 1. Falar com taverneiro
        fb_tav = self.ai._create_visceral_fallback(beat_1_log, "falar com taverneiro")
        self.assertNotIn("contrato sangrento chega ao fim", fb_tav.lower())
        self.assertIn("taverneiro", fb_tav.lower())

        # 2. Conversar com balconista
        fb_balc = self.ai._create_visceral_fallback(beat_1_log, "conversar com balconista")
        self.assertNotIn("contrato sangrento chega ao fim", fb_balc.lower())
        self.assertIn("taverneiro", fb_balc.lower())

        # 3. Observar
        fb_obs = self.ai._create_visceral_fallback(beat_1_log, "observar")
        self.assertNotIn("contrato sangrento chega ao fim", fb_obs.lower())
        self.assertTrue("taverna" in fb_obs.lower() or "olhos" in fb_obs.lower() or "mercenários" in fb_obs.lower())

        # 4. Dialogar genérico
        fb_dial = self.ai._create_visceral_fallback(beat_1_log, "dialogar")
        self.assertNotIn("contrato sangrento chega ao fim", fb_dial.lower())
        self.assertIn("taverneiro", fb_dial.lower())

        # 5. Conclusão real de contrato DEVE disparar o texto de contrato finalizado
        fb_real_contract = self.ai._create_visceral_fallback("Contrato de caçada concluído com sucesso. Recompensa recebida.", "concluir contrato")
        self.assertIn("contrato sangrento chega ao fim", fb_real_contract.lower())

    def test_11_model_cascade_fallback(self):
        """Valida que a cascata de modelos tenta os modelos ativos e atualiza para o modelo estável."""
        cascade = self.ai._get_models_cascade()
        self.assertEqual(cascade[0], "gemini-3.5-flash-lite")
        self.assertIn("gemini-flash-lite-latest", cascade)
        self.assertIn("gemini-flash-latest", cascade)

        # Simula falha 404 no primeiro modelo e sucesso no segundo (via chats.create)
        call_models = []
        def mock_chats_create(model, config=None, **kwargs):
            call_models.append(model)
            if model == "gemini-3.5-flash-lite":
                raise Exception("404 NOT_FOUND: Model not found")
            mock_chat = MagicMock()
            mock_res = MagicMock()
            mock_res.text = '{"tipo_acao": "DIALOGAR", "alvo": ["Taverneiro"], "recurso_utilizado": null, "intencao_cena": "Diálogo com taverneiro."}'
            mock_chat.send_message.return_value = mock_res
            return mock_chat

        self.ai.client.chats.create = MagicMock(side_effect=mock_chats_create)
        res = self.ai.parse_player_intent("conversar com o taverneiro", {})
        self.assertEqual(res["tipo_acao"], "DIALOGAR")
        self.assertEqual(call_models[0], "gemini-3.5-flash-lite")
        self.assertEqual(call_models[1], "gemini-2.5-flash")
        self.assertEqual(self.ai.model_name, "gemini-2.5-flash")


if __name__ == "__main__":
    unittest.main()
