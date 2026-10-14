import unittest
import json
import os
import sys
import copy
from typing import Dict, Any

# Assegura que o diretório raiz esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.story_engine import StoryManager
from core.game_engine import SessionManager
from core.combat_system import resolve_action
from core.dnd_rules import get_modifier
from ai_master.ai_client import AIGameMaster

class MockAI(AIGameMaster):
    def parse_player_intent(self, user_input: str, game_state: Dict[str, Any]) -> Dict[str, Any]:
        return {"tipo_acao": "ataque", "alvo": ["Inimigo"], "arma_usada": "espada longa"}

    def generate_narrative_from_math(self, sys_log: str, intent: str) -> str:
        return f"[MOCK NARRATIVA] {sys_log}"


class TestAlliesCompendium(unittest.TestCase):
    """
    Suíte de testes para a Fase C:
    - Validação de integridade matemática das 42 fichas D&D 5e em data/heroes_lore.json.
    - Carregamento dinâmico do pool em StoryManager.allies_pool.
    - Recrutamento dinâmico sem duplicações de classes ou raças.
    - Retrocompatibilidade total dos aliases legados ('fighter', 'cleric', etc.).
    - Preservação e participação em combate dos aliados.
    """

    def setUp(self):
        with open("data/heroes_lore.json", "r", encoding="utf-8") as f:
            self.heroes_data = json.load(f)

    def test_01_all_42_heroes_exist_and_have_valid_structure(self):
        """Valida que todas as 42 fichas (HERO-01 a HERO-42) estão presentes e estruturadas."""
        self.assertEqual(len(self.heroes_data), 42, f"Esperado 42 heróis, encontrado {len(self.heroes_data)}")
        
        expected_ids = [f"HERO-{i:02d}" for i in range(1, 43)]
        for hid in expected_ids:
            self.assertIn(hid, self.heroes_data, f"Herói {hid} ausente no compêndio!")
            h = self.heroes_data[hid]
            self.assertEqual(h["id"], hid)
            self.assertTrue(bool(h.get("name")), f"{hid} sem nome válido!")
            self.assertTrue(bool(h.get("race")), f"{hid} sem raça válida!")
            self.assertTrue(bool(h.get("class")), f"{hid} sem classe válida!")
            self.assertIn("lore", h)
            self.assertIn("personality", h)
            self.assertIn("recruitment_hook", h)

        # 7 Raças x 6 Classes = 42
        races = {h["race"] for h in self.heroes_data.values()}
        classes = {h["class"] for h in self.heroes_data.values()}
        expected_races = {"Humano", "Anão da Colina", "Draconato", "Elfo da Floresta", "Halfling", "Meio-Orc", "Tiefling"}
        expected_classes = {"Guerreiro", "Clérigo", "Paladino", "Mago", "Patrulheiro", "Ladino"}
        self.assertEqual(races, expected_races)
        self.assertEqual(classes, expected_classes)

    def test_02_mathematical_integrity_attributes_and_hp(self):
        """Valida a precisão matemática D&D 5e de atributos, PV e CA para cada um dos 42 heróis."""
        class_hit_die = {
            "Guerreiro": (10, "1d10"),
            "Paladino": (10, "1d10"),
            "Patrulheiro": (10, "1d10"),
            "Clérigo": (8, "1d8"),
            "Ladino": (8, "1d8"),
            "Mago": (6, "1d6")
        }

        speed_by_race = {
            "Humano": "9m",
            "Draconato": "9m",
            "Meio-Orc": "9m",
            "Tiefling": "9m",
            "Anão da Colina": "7.5m",
            "Halfling": "7.5m",
            "Elfo da Floresta": "10.5m"
        }

        for hid, h in self.heroes_data.items():
            # Atributos oficiais
            attrs = h.get("attributes", {})
            required_stats = {"STR", "DEX", "CON", "INT", "WIS", "CHA", "LUCK"}
            self.assertEqual(set(attrs.keys()), required_stats, f"{hid} possui chaves de atributos inválidas: {attrs.keys()}")
            
            for stat in required_stats:
                self.assertIsInstance(attrs[stat], int)
                self.assertGreaterEqual(attrs[stat], 8, f"{hid} possui {stat} abaixo do mínimo permitido!")
                self.assertLessEqual(attrs[stat], 20, f"{hid} possui {stat} acima do máximo nível 1!")

            # Modificador de CON e cálculo de HP
            con_val = attrs["CON"]
            con_mod = get_modifier(con_val)
            expected_hd_base, expected_hd_str = class_hit_die[h["class"]]
            self.assertEqual(h.get("hit_dice"), expected_hd_str, f"{hid} hit_dice inconsistente!")

            dwarven_bonus = 1 if h["race"] == "Anão da Colina" else 0
            expected_hp = max(1, expected_hd_base + con_mod + dwarven_bonus)
            
            self.assertEqual(h["hp_max"], expected_hp, f"{hid} hp_max inconsistente! Esperado {expected_hp}, obteve {h['hp_max']}")
            self.assertEqual(h["hp_current"], expected_hp, f"{hid} hp_current inconsistente!")
            self.assertEqual(h["pv_atual"], expected_hp, f"{hid} pv_atual inconsistente!")
            self.assertEqual(h["pv_max"], expected_hp, f"{hid} pv_max inconsistente!")

            # Classe de Armadura
            ac = h.get("ac")
            self.assertIsInstance(ac, int)
            self.assertGreaterEqual(ac, 11, f"{hid} CA muito baixa ({ac})!")
            self.assertLessEqual(ac, 20, f"{hid} CA excessiva ({ac})!")
            self.assertEqual(h["ca"], ac)

            # Deslocamento
            self.assertEqual(h.get("speed"), speed_by_race[h["race"]], f"{hid} velocidade inconsistente!")

            # Faction
            self.assertEqual(h.get("faction"), "ally")

    def test_03_combat_actions_abilities_and_spell_slots(self):
        """Valida que cada herói possui ações de combate reais, habilidades e spell slots se conjurador."""
        for hid, h in self.heroes_data.items():
            actions = h.get("actions", [])
            self.assertTrue(1 <= len(actions) <= 2, f"{hid} deve ter 1 a 2 ações de combate (tem {len(actions)})")
            for act in actions:
                self.assertIn("name", act)
                self.assertIn("hit_bonus", act)
                self.assertIn("damage_dice", act)
                self.assertIsInstance(act["hit_bonus"], int)
                self.assertTrue("d" in act["damage_dice"], f"{hid} dado de dano inválido: {act['damage_dice']}")

            abilities = h.get("abilities", [])
            self.assertGreaterEqual(len(abilities), 2, f"{hid} deve ter pelo menos 2 habilidades configuradas!")

            # Conjuradores
            if h["class"] in ["Clérigo", "Paladino", "Mago", "Patrulheiro"]:
                self.assertIn("spell_slots", h, f"{hid} é {h['class']} mas não possui spell_slots!")
                self.assertIn("1", h["spell_slots"])
                self.assertGreaterEqual(h["spell_slots"]["1"], 2)

            # Asset Keys
            self.assertTrue(bool(h.get("sprite_key")), f"{hid} sem sprite_key")
            self.assertTrue(bool(h.get("portrait_key")), f"{hid} sem portrait_key")

    def test_04_story_manager_allies_pool_dynamic_loading(self):
        """Valida que StoryManager carrega todos os 42 heróis dinamicamente e os aliases legados."""
        story = StoryManager()
        pool = story.allies_pool

        # Contém todos os 42 canônicos
        for i in range(1, 43):
            hid = f"HERO-{i:02d}"
            self.assertIn(hid, pool, f"{hid} não está em StoryManager.allies_pool!")
            self.assertIn("attributes", pool[hid])
            self.assertIn("hp_max", pool[hid])

        # Contém aliases legados
        legacy_keys = ["fighter", "cleric", "paladin", "mage", "ranger", "rogue", "guardian_human", "wizard"]
        for lk in legacy_keys:
            self.assertIn(lk, pool, f"Alias legado '{lk}' ausente no allies_pool!")

        # Flags inicializadas
        for k in pool:
            self.assertIn(f"ally_{k}_unlocked", story.flags)
            self.assertFalse(story.flags[f"ally_{k}_unlocked"])
        self.assertFalse(story.flags.get("ally_warlock_unlocked"))

    def test_05_legacy_aliases_backward_compatibility(self):
        """Valida 100% de compatibilidade retroativa com aliases legados e saves antigos."""
        story = StoryManager()
        
        # Desbloqueio de aliases legados
        self.assertTrue(story.unlock_ally("fighter"))
        self.assertTrue(story.unlock_ally("cleric"))
        self.assertTrue(story.unlock_ally("mage"))
        self.assertTrue(story.unlock_ally("wizard"))
        self.assertTrue(story.unlock_ally("warlock"))

        unlocked = story.get_unlocked_allies()
        self.assertIn("fighter", unlocked)
        self.assertEqual(unlocked["fighter"]["name"], "Thorgar, o Implacável")
        self.assertEqual(unlocked["cleric"]["name"], "Karg, o Devoto")
        self.assertEqual(unlocked["mage"]["name"], "Azaroth, o Arcanista")

        # Compatibilidade com get_hero_lore
        f_lore = story.get_hero_lore("fighter")
        self.assertIsNotNone(f_lore)
        self.assertEqual(f_lore["class"], "Guerreiro")

        c_lore = story.get_hero_lore("cleric")
        self.assertIsNotNone(c_lore)
        self.assertEqual(c_lore["class"], "Clérigo")

    def test_06_dynamic_recruitment_diversity_and_no_duplicates(self):
        """Valida recrutamento adaptativo de todo o pool dos 42 heróis sem duplicatas de classe e com diversidade racial."""
        story = StoryManager()
        
        # Jogador Clérigo Halfling
        player = {
            "name": "Bryn",
            "class": "Clérigo",
            "race": "Halfling",
            "hp_current": 10,
            "hp_max": 10
        }

        recrutados = []
        for _ in range(5):
            ally = story.recruit_next_ally(player)
            self.assertIsNotNone(ally, "Deveria conseguir recrutar um aliado!")
            recrutados.append(ally)

        self.assertEqual(len(recrutados), 5)

        # NENHUM Clérigo recrutado
        classes_recrutadas = [a["class"] for a in recrutados]
        self.assertNotIn("Clérigo", classes_recrutadas, "Não deve recrutar a classe do jogador!")

        # Todas as 5 classes recrutadas distintas
        self.assertEqual(len(set(classes_recrutadas)), 5, "Houve repetição de classe!")

        # Raça do jogador (Halfling) não deve se repetir entre os 5 recrutados se houver outras opções
        races_recrutadas = [a["race"] for a in recrutados]
        self.assertNotIn("Halfling", races_recrutadas, "Raça do jogador não deveria ser repetida quando há opções!")
        self.assertEqual(len(set(races_recrutadas)), 5, "Houve repetição desnecessária de raças!")

        # Nenhum aliado adicional pode ser recrutado (todas as 6 classes preenchidas na party)
        extra_ally = story.recruit_next_ally(player)
        self.assertIsNone(extra_ally, "Não deveria recrutar mais aliados quando todas as classes foram preenchidas!")

    def test_07_allies_participate_in_combat_system_and_survive_safe_travel(self):
        """Valida que aliados recrutados participam ativamente do sistema de combate e sobrevivem em viagens/hubs."""
        ai = MockAI()
        session = SessionManager(ai)
        session.game_state["player_character"] = {
            "name": "Herói Teste",
            "class": "Guerreiro",
            "race": "Humano",
            "level": 1,
            "hp_current": 12,
            "hp_max": 12,
            "ac": 16,
            "attributes": {"STR": 16, "DEX": 14, "CON": 15, "INT": 10, "WIS": 12, "CHA": 10, "FOR": 16, "DES": 14},
            "inventory": ["Espada Longa"]
        }
        
        # Recruta HERO-01 (Sir Alistair Valerius, Humano Guerreiro)
        story = session.story
        story.unlock_ally("HERO-01")
        
        unlocked = story.get_unlocked_allies()
        self.assertIn("HERO-01", unlocked)
        hero1 = unlocked["HERO-01"]
        
        # Injeta aliado em active_combat_targets
        session.active_combat_targets[hero1["name"]] = copy.deepcopy(hero1)
        session.active_combat_targets["Goblin Inimigo"] = {
            "name": "Goblin Inimigo",
            "pv_atual": 7,
            "pv_max": 7,
            "ca": 12,
            "tipo_bestiario": "goblin",
            "faction": "enemy",
            "actions": [{"name": "Cimitarra", "hit_bonus": 4, "damage_dice": "1d6+2"}]
        }

        # Executa turno de combate
        res = resolve_action(
            {"tipo_acao": "ataque", "alvo": ["Goblin Inimigo"], "arma_usada": "espada longa"},
            session.game_state["player_character"],
            [session.active_combat_targets["Goblin Inimigo"]],
            session.active_combat_targets,
            game_state=session.game_state
        )
        self.assertIn("sys_log", res)

        # Valida que aliado HERO-01 está na party e não foi descartado
        self.assertIn(hero1["name"], session.active_combat_targets)
        self.assertEqual(session.active_combat_targets[hero1["name"]]["faction"], "ally")

        # Simula viagem para side quest e confirma preservação de aliados (faction == 'ally')
        session.story.current_beat = 1
        session.game_state["story_beat"] = 1
        session.game_mode = "EXPLORACAO"
        session.accept_side_quest("sq_goblin_clearing")
        session.travel_to_side_quest("sq_goblin_clearing")
        self.assertIn(hero1["name"], session.active_combat_targets, "Aliado 'ally' deve ser preservado ao iniciar side quest!")

        # Simula vitória dos aliados e retorno ao hub seguro
        for t in session.active_combat_targets.values():
            if t.get("faction") != "ally":
                t["pv_atual"] = 0
                t["hp_current"] = 0
                t["status"] = "morto"

        session.check_combat_resolution()
        self.assertIn(hero1["name"], session.active_combat_targets, "Aliado 'ally' deve ser preservado ao retornar ao hub!")


if __name__ == "__main__":
    unittest.main()
