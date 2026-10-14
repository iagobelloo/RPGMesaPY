import os
import json
import warnings
import time
from typing import List, Dict, Any, Optional
from google import genai

# Silencia o aviso inofensivo de AFC do SDK para deixar o console limpo
warnings.filterwarnings("ignore", message="Direct use of automatic function calling")

class AIGameMaster:
    """
    O Cérebro do Jogo (Integração com a LLM).
    Atua como o Game Master de uma campanha de D&D 5e.
    """
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        # Carrega variáveis de ambiente de .env local se existir
        if os.path.exists(".env"):
            try:
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            os.environ.setdefault(k.strip(), v.strip())
            except Exception:
                pass

        resolved_key = api_key or os.environ.get("GEMINI_API_KEY")
        if resolved_key:
            self.client = genai.Client(api_key=resolved_key)
        else:
            self.client = genai.Client(api_key="AIzaSyDummyKeyForMockingTestingEnvironment")

        self.model_name = os.environ.get("GEMINI_MODEL", model_name if model_name != "gemini-3.5-flash-lite" else "gemini-2.5-flash")
        self.chat_history: List[Dict[str, str]] = []
        try:
            with open("docs/dm_guidelines.md", "r", encoding="utf-8") as f:
                guidelines = f.read()
        except FileNotFoundError:
            guidelines = (
                "Você é Maelor das Cordas de Cinza, o Menestrel, cronista e AI Game Master de uma campanha de Grounded Dark Fantasy (RPGMesaPY - D&D 5e).\n"
                "Você narra com voz taciturna e poética, rica nos 5 sentidos. O herói caminha e luta sozinho do Beat 1 ao Beat 14; aliados juram honra e só se unem no Beat 15.\n"
            )

        self.system_instruction = (
            f"{guidelines}\n\n"
            "INSTRUÇÕES TÉCNICAS E DE COMBATE DE MAELOR:\n"
            "- MATEMÁTICA DE COMBATE E TESTES: Para ataques, compare o 'dice_roll_result' do jogador com a CA (Armor Class) do monstro/inimigo. Se o resultado >= CA, o jogador acerta (aplique dano ao inimigo via 'damage_applied'). Se o resultado < CA, a ação falha e você deve engatilhar um contra-ataque ou consequência (Fail Forward). Para testes de perícia, defina uma CD silenciosa na sua mente (ex: CD 15) e julgue o sucesso/falha.\n"
            "- REGRA DE OURO DOS ALIADOS: Nos Beats 1 a 14, o protagonista viaja e luta sozinho. Aliados encontrados selam juramentos e partem para se preparar; eles só lutam juntos no Beat 15 (Covil do Tirano).\n"
            "- MEMÓRIA: Introduza NPCs com 'register_npc' na primeira aparição.\n"
            "- FILTRO ANTI-LIXO: Inputs sem sentido ('aaa', '123') resultam em hesitação traumática do herói, SEM iniciar combates precipitados.\n\n"
            "Sua resposta DEVE ser estritamente em formato JSON válido, sem NENHUMA marcação markdown externa.\n"
            "Estrutura JSON obrigatória (exata):\n"
            "{\n"
            "    \"narrative\": \"Sua narrativa contendo Resolução, Reação e Gatilho com 2 a 3 opções de ação, e no final desta string adicione o Bloco [STATUS] OBRIGATÓRIO...\",\n"
            "    \"dialogue\": {\"npc_name\": \"Fala do NPC caso exista\"},\n"
            "    \"environment_tag\": \"Palavra curta em inglês para gerar fundo. Ex: tavern, dungeon, forest, cave, snow\",\n"
            "    \"system_commands\": {\n"
            "        \"damage_applied\": [{\"char_name\": \"string\", \"amount\": 0}],\n"
            "        \"healing_applied\": [],\n"
            "        \"spawn_enemy\": [{\"name\": \"string\", \"race\": \"string\", \"hp\": 0, \"ac\": 0}],\n"
            "        \"register_npc\": [{\"name\": \"string\", \"desc\": \"string\"}],\n"
            "        \"give_item\": [],\n"
            "        \"give_exp\": 0,\n"
            "        \"time_passed_hours\": 0\n"
            "    }\n"
            "}"
        )

    def _extract_and_parse_json(self, raw_text: str, is_narrative: bool = False) -> Dict[str, Any]:
        """
        Extrator Universal de JSON (Anti-Crash e Fallback Silencioso).
        """
        try:
            start_idx = raw_text.find('{')
            end_idx = raw_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
                json_str = raw_text[start_idx:end_idx+1]
                return json.loads(json_str)
            else:
                raise ValueError("Bloco JSON não encontrado na resposta da IA.")
        except (json.JSONDecodeError, Exception) as e:
            print(f"[ERRO] Falha ao extrair/decodificar JSON da IA: {e}\nTexto bruto recebido:\n{raw_text}")
            if is_narrative:
                return {"texto": "A poeira levanta enquanto a ação se desenrola em silêncio...", "npc_falando": "nenhum"}
            else:
                return {"tipo_acao": "narrativa", "arma_usada": None, "intencao_cena": "avançar"}

    def _generate_text_with_retry(self, prompt: str, system_instr: str, max_retries: int = 2, temperature: float = 0.8) -> str:
        """Função genérica para invocar o LLM usando Chat session (evita avisos AFC) e Retries."""
        for attempt in range(max_retries + 1):
            try:
                # Usamos um chat one-shot em vez de generate_content() direto para evitar o aviso
                # "Direct use of automatic function calling..."
                chat = self.client.chats.create(
                    model=self.model_name,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_instr,
                        temperature=temperature
                    )
                )
                response = chat.send_message(prompt)
                return response.text or ""
            except Exception as e:
                print(f"[Aviso] Falha na API Gemini (Tentativa {attempt+1}/{max_retries+1}): {e}")
                if attempt < max_retries:
                    time.sleep(3)
                else:
                    raise e
        return ""

    def generate_prologue_questions(self, char_data: Dict[str, Any]) -> List[str]:
        """Gera 3 perguntas de background em lote com base no perfil do herói."""
        sys_instr = (
            "Você é o Dungeon Master de um VTT de D&D 5e de Grounded Dark Fantasy.\n"
            "Sua tarefa é elaborar 3 perguntas curtas em primeira pessoa para o jogador, focadas na história dele.\n"
            "ESTRUTURA OBRIGATÓRIA:\n"
            "Pergunta 1: Focada na vivência do Antecedente.\n"
            "Pergunta 2: Focada no treinamento ou natureza da Classe.\n"
            "Pergunta 3: O motivo de ele estar entrando na taverna escura nesta mesma noite.\n"
            "REGRA ABSOLUTA CONTRA ALUCINAÇÃO: Não assuma que a família dele morreu, que ele foi traído ou que é amaldiçoado a menos que o Antecedente exija isso. "
            "Seja evocativo e focado no mundo físico e sombrio (ferrugem, frio, fome, perigo), mas deixe O JOGADOR decidir se o passado foi heroico, neutro ou trágico.\n"
            "FORMATO DE SAÍDA ESTRITO: Retorne APENAS um JSON array contendo 3 strings. Nada mais. Exemplo:\n"
            "[\"Pergunta 1...\", \"Pergunta 2...\", \"Pergunta 3...\"]"
        )
        
        equipments = ", ".join(char_data.get('inventory', []))
        abilities = ", ".join(char_data.get('abilities', []))
        proficiencies = ", ".join(char_data.get('proficiencies', []))
        
        prompt = (f"Baseado nesta exata combinação de:\n"
                  f"- Raça: {char_data['race']}\n"
                  f"- Classe: {char_data['class']} (Habilidades: {abilities}, Proficiências: {proficiencies})\n"
                  f"- Antecedente: {char_data.get('background')} (Inventário: {equipments})\n"
                  f"- Tendência: {char_data.get('alignment')}\n\n"
                  f"Elabore as 3 perguntas em formato JSON estrito.")
                  
        fallback = [
            f"Como sua vivência como {char_data.get('background')} te preparou para a crueldade do mundo lá fora?",
            f"O que foi mais difícil no seu treinamento para se tornar um {char_data['class']} em um reino implacável?",
            "O vento corta lá fora. O que exatamente o trouxe a esta taverna imunda nesta noite?"
        ]
        
        try:
            raw_text = self._generate_text_with_retry(prompt, sys_instr)
            # Reaproveita a lógica de extração genérica para array
            start_idx = raw_text.find('[')
            end_idx = raw_text.rfind(']')
            if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
                questions = json.loads(raw_text[start_idx:end_idx+1])
                if isinstance(questions, list) and len(questions) >= 3:
                    return [str(q) for q in questions[:3]]
            return fallback
        except Exception as e:
            print(f"[ERRO] Falha ao gerar/decodificar perguntas JSON: {e}")
            return fallback

    def generate_prologue(self, char_data: Dict[str, Any], qa_history: List[Dict[str, str]]) -> str:
        """Gera o Prólogo do mundo amarrando visceralmente as respostas da Sessão Zero."""
        sys_instr = (
            "[Regras de Persona Base]\n"
            "Você é o Narrador de uma aventura Grounded Dark Fantasy brutal.\n"
            "[Instrução de Visceralidade]\n"
            "REGRA DE COMPOSIÇÃO ATÔMICA: É ESTRITAMENTE PROIBIDO usar templates descritivos ou clichês literários (ex: 'penumbra fétida', 'cicatrizes de batalhas antigas', ou chamar o personagem de 'aventureiro'/'herói').\n"
            "Você DEVE construir a narrativa unicamente a partir da síntese visceral dos dados do personagem e das respostas dele, usando os 5 sentidos (ex: cheiro de ferrugem, som do assoalho rangendo, frio do metal).\n"
            "DIRETRIZES ABSOLUTAS:\n"
            "1. FILTRO DE IMERSÃO: Proibido inventar lore ou histórias novas não citadas. Foque nos fatos crus fornecidos.\n"
            "2. FORMATO: Exatamente 1 parágrafo denso (máximo 5 linhas).\n"
            "3. CENA FINAL OBRIGATÓRIA: O texto TEM QUE terminar no PRESENTE. O herói está sentado na Taverna manuseando algum equipamento específico de sua ficha, quando a pesada porta de carvalho é estilhaçada revelando uma ameaça iminente.\n"
            "GOLDEN RULE: NEVER end your response with questions to the player (e.g., 'What do you do?'). Always end with a descriptive statement and passively wait for the user's action."
        )
        
        equipments = ", ".join(char_data.get('inventory', []))
        abilities = ", ".join(char_data.get('abilities', []))
        proficiencies = ", ".join(char_data.get('proficiencies', []))
        
        prompt = (
            f"[Contexto da Cena Atual (Raw Data)]\n"
            f"Fatos Crus do Herói: {char_data['name']}, {char_data['race']} {char_data['class']}.\n"
            f"Inventário Físico: {equipments}. Habilidades: {abilities}. Proficiências: {proficiencies}.\n\n"
            f"[Quest Log/Diário de Campanha (Layer 3 - Fatos Crus)]\n"
            f"Histórico e Passado (Respostas do Jogador):\n"
        )
        for qa in qa_history:
            prompt += f"- {qa['a']}\n"
            
        prompt += "\nCom base no histórico recente e PRIORIZANDO ABSOLUTAMENTE A ÚLTIMA RESPOSTA DO USUÁRIO, elabore uma narração/pergunta VISCERAL baseada nos fatos crus. Use os 5 sentidos e engatilhe a ameaça na porta:"
        
        try:
            return self._generate_text_with_retry(prompt, sys_instr)
        except Exception:
            nome = char_data.get('name', 'Viajante')
            raca = char_data.get('race', 'Humano')
            classe = char_data.get('class', 'Guerreiro')
            return f"O cheiro de suor e cinzas domina o ar. Como um {raca} {classe}, você, {nome}, aperta o cabo da arma enquanto a porta de carvalho é arrancada, revelando o perigo imediato."

    def parse_player_action(self, player_input: str, available_backgrounds: list, lista_bestiario: list = None, context: dict = None, **kwargs) -> dict:
        """
        Recebe o input bruto do jogador e atua como um Classificador Lógico JSON
        para fornecer parâmetros matemáticos ao motor de regras (Fase 0).
        """
        sys_instr = (
            "Você é um classificador de regras de D&D 5e e também atua como Diretor Visual.\n"
            f"Cenários visuais disponíveis no motor: {available_backgrounds}.\n"
            f"Bestiário Oficial do Motor: {lista_bestiario}\n"
            "Instrução Crucial para a IA: Quando inimigos aparecerem, você deve instanciá-los ESTRITAMENTE a partir da lista do Bestiário. O 'id_narrativo' DEVE ser único para cada monstro (ex: se houver dois goblins, chame de 'Lacaio Goblin 1' e 'Lacaio Goblin 2').\n"
            "Após classificar a ação do jogador, você DEVE determinar a intenção tática de resposta de cada inimigo na cena, caso eles sobrevivam ao ataque do jogador.\n"
            "Magias forçam o alvo a fazer um Teste de Resistência.\n"
            "Identifique o posicionamento relativo do jogador na narrativa (Teatro da Mente).\n"
            "Chaves Exigidas no JSON:\n"
            '"npc_falando": (Se algum personagem ou inimigo falar diretamente com o jogador, coloque o nome exato dele aqui. Se ninguém falar, "nenhum")\n'
            '"arma_usada": (Se tipo_acao for "ataque", você DEVE especificar a arma usada baseada no inventário do jogador ou no texto. Ex: "espada longa", "arco curto". Se não for ataque, "nenhum")\n'
            '"intencao_cena": (Restrito a: "manter", "iniciar_combate" ou "fugir". SE O JOGADOR ATACAR, SACAR ARMA OU USAR MAGIA OFENSIVA, VOCÊ DEVE OBRIGATORIAMENTE RETORNAR "iniciar_combate". Se ele tentar correr da luta, mande "fugir")\n'
            '"tipo_acao": (Restrito a: "ataque", "magia", "teste_pericia", "uso_item", "movimento", "dialogo")\n'
            '"pericia_sugerida": (SE for um teste_pericia, use a grafia exata: Atletismo, Acrobacia, Furtividade, Prestidigitação, Arcanismo, História, Investigação, Natureza, Religião, Adestrar Animais, Intuição, Medicina, Percepção, Sobrevivência, Atuação, Enganação, Intimidação, Persuasão. Caso contrário, "nenhum")\n'
            '"cd_sugerida": (Inteiro entre 5 e 25 avaliando a dificuldade narrativa da ação. 10 é médio, 15 difícil, 20 heroico)\n'
            '"estado_tatico": (Restrito a: "normal", "vantagem", "desvantagem". Baseie-se na inteligência tática descrita pelo jogador)\n'
            '"alvo": (Lista de strings com os IDs dos inimigos/NPCs. Ex: ["Lacaio Goblin 1", "Lacaio Goblin 2"]. Se não houver alvo, ["nenhum"])\n'
            '"exige_resistencia": (Atributo exigido para resistir à magia, ex: "DES", "CON", "SAB". Se for ataque físico normal, retorne "nenhum")\n'
            '"recurso_utilizado": (A arma, magia ou item declarado. Se nenhum, "nenhum")\n'
            '"movimentacao": (Restrito a: "corpo_a_corpo", "curto_alcance", "longo_alcance", ou "cobertura". Ex: "Eu corro para trás do balcão" = "cobertura")\n'
            '"mudanca_cenario": (Se a ação ditar uma viagem/fuga para um novo local, escolha o nome EXATO do cenário da lista. Se a cena continuar no mesmo lugar, retorne estritamente "manter").\n'
            '"flavor_text": (Resumo de 1 linha da ação narrativa para uso futuro).\n'
            '"novos_inimigos": [{"id_narrativo": "String Única", "tipo_bestiario": "String Exata da Lista"}] (Retorne dados AQUI APENAS se novos inimigos entrarem na cena. Do contrário, retorne [] vazio).\n'
            '"reacao_inimigos": Lista de objetos ditando o contra-ataque. Ex: [{"id_narrativo": "Lacaio Goblin 1", "tipo_acao": "ataque", "alvo": ["Jogador"]}]. (O tipo deve ser "ataque" ou "magia").'
        )
        
        fallback = {
            "npc_falando": "nenhum",
            "arma_usada": "nenhum",
            "intencao_cena": "manter",
            "tipo_acao": "narrativa",
            "pericia_sugerida": "nenhum",
            "cd_sugerida": 0,
            "estado_tatico": "normal",
            "alvo": ["nenhum"],
            "exige_resistencia": "nenhum",
            "recurso_utilizado": "nenhum",
            "movimentacao": "curto_alcance",
            "mudanca_cenario": "manter",
            "flavor_text": player_input,
            "novos_inimigos": [],
            "reacao_inimigos": []
        }
        
        try:
            # Temperatura 0.0 para precisão matemática máxima e previsibilidade
            raw_text = self._generate_text_with_retry(player_input, sys_instr, temperature=0.0)
            parsed = self._extract_and_parse_json(raw_text, is_narrative=False)
            
            # Validação defensiva de chaves
            for k in fallback.keys():
                if k not in parsed:
                    parsed[k] = fallback[k]
                    
            # Trava Implacável de Combate
            if parsed.get("tipo_acao") in ["ataque", "magia"] and parsed.get("alvo", ["nenhum"]) != ["nenhum"]:
                parsed["intencao_cena"] = "iniciar_combate"
            
            print("\n[AI_MASTER PARSER] JSON Classificado com Sucesso:")
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
            
            return parsed
        except Exception as e:
            print(f"[ERRO] Parser JSON do LLM falhou: {e}")
            return fallback

    def parse_player_intent(self, player_input: str, game_state: dict) -> dict:
        """
        Fase 0 - O Extrator JSON Silencioso (Bloco 28).
        Atua estritamente como um Classificador de Dados NLP sem tomar decisões mecânicas.
        """
        modo_atual = game_state.get("game_mode", "EXPLORACAO")
        entidades_ativas = list(game_state.get("active_combat_targets", {}).keys())
        
        sys_instr = (
            "Você é um Classificador de Dados NLP especializado em extrair intenções de jogadores em RPG de Mesa.\n"
            "Sua única função é ler o INPUT DO JOGADOR e converter a intenção em um JSON estrito.\n"
            "REGRA DE OURO: NÃO valide se o jogador pode ou não fazer a ação. NÃO verifique regras, nível ou itens. Apenas extraia a intenção fielmente.\n"
            "O Schema JSON OBRIGATÓRIO deve conter as exatas seguintes chaves:\n"
            "- \"tipo_acao\": String ESTRITA dentre: [ATACAR, CONJURAR_MAGIA, USAR_HABILIDADE, USAR_ITEM, EQUIPAR_ITEM, MOVER, ACAO_TATICA_5E, DIALOGAR, INTERAGIR_AMBIENTE, DESCANSAR, INTERAGIR_CENARIO, AVANCAR_HISTORIA, SUBIR_NIVEL].\n"
            "  * DICA: Se o jogador estiver conversando, perguntando por missões, procurando trabalho/contratos, pedindo bebidas, ouvindo rumores ou falando com NPCs (ex: 'estava a procura de uma missão', 'procuro trabalho', 'quero um contrato', 'conversar com o taverneiro', 'pedir cerveja'), use 'DIALOGAR' ou 'INTERAGIR_CENARIO', NUNCA 'AVANCAR_HISTORIA'.\n"
            "  * DICA: Se o jogador quiser usar ou ativar uma habilidade de classe (ex: 'retomar o fôlego', 'second wind', 'surto de ação', 'action surge', 'cura pelas mãos', 'lay on hands', 'destruição divina', 'smite', 'marca do caçador', 'hunter\\'s mark', 'ataque furtivo', 'sneak attack', 'ação ardilosa', 'escudo arcano', 'preservar a vida', 'esquiva sobrenatural'), use 'USAR_HABILIDADE' e extraia o nome da habilidade em 'recurso_utilizado'.\n"
            "  * DICA: Se o jogador quiser equipar, empunhar, desembainhar, sacar ou trocar de arma/escudo (ex: 'equipar espada longa', 'empunhar arco curto', 'trocar para adaga', 'usar escudo'), use 'EQUIPAR_ITEM' e extraia o nome do equipamento em 'recurso_utilizado'.\n"
            "  * DICA: Se o jogador quiser subir de nível, upar ou evoluir atributos, use 'SUBIR_NIVEL'. Se o jogador quiser SAIR do local atual para a estrada, VIAJAR ou AVANCAR a campanha para o próximo Beat (ex: 'viajar pela estrada', 'partir da taverna', 'proximo beat', 'avançar na jornada'), extraia como 'AVANCAR_HISTORIA'. NÃO use AVANCAR_HISTORIA se ele estiver apenas procurando missões, pedindo contratos ou conversando na taverna.\n"
            "- \"recurso_utilizado\": String com o nome da arma, magia, habilidade ou item extraído. Se não houver, retorne null.\n"
            "- \"alvo\": Array de strings [] com os nomes/IDs dos alvos desejados. Cruze com as ENTIDADES NO CAMPO se possível. Se não houver alvo, retorne [].\n"
            "- \"intencao_cena\": String resumindo de forma visual e direta o que o jogador quer fazer na narrativa.\n"
        )
        
        prompt = (
            f"MODO ATUAL: {modo_atual}\n"
            f"ENTIDADES NO CAMPO: {entidades_ativas}\n"
            f"INPUT DO JOGADOR: {player_input}\n"
        )
        
        # Heurística inteligente para fallback resiliente (offline / rate limit)
        p_low = player_input.lower().strip()
        local_tipo = "INTERAGIR_AMBIENTE"
        local_recurso = None
        local_alvo = []
        local_intencao = f"O jogador decide {player_input}."
        
        # 1. Procura de Missões / Contratos / Trabalho na Taverna
        if any(w in p_low for w in [
            "procura de uma missao", "procura de uma missão", "procurando missao", "procurando missão",
            "procuro missao", "procuro missão", "quero missao", "quero missão", "buscar missao", "buscar missão",
            "procura de missao", "procura de missão", "procura de trabalho", "procurando trabalho",
            "procuro trabalho", "quero trabalho", "procura de contrato", "procurando contrato",
            "procuro contrato", "quero um contrato", "quero contrato", "quadro de avisos", "mural de contratos",
            "trabalho na taverna", "missao na taverna", "missão na taverna", "tem alguma missao", "tem alguma missão",
            "algum trabalho", "algum contrato", "missões disponíveis", "missoes disponiveis"
        ]) or (any(w in p_low for w in ["missao", "missão", "trabalho", "contrato"]) and any(w in p_low for w in ["procura", "procuro", "busco", "buscar", "quero", "queria", "disponivel", "disponível", "tem", "ha", "há"])):
            local_tipo = "DIALOGAR"
            local_intencao = "O herói procura informações sobre trabalhos e missões disponíveis na taverna."

        # 2. Conversas / Diálogos com NPCs / Pedidos de Bebida / Rumores na Taverna
        elif any(w in p_low for w in [
            "conversar com", "falar com", "perguntar ao", "perguntar para", "chamar o", "dialogar",
            "taverneiro", "bardo", "maelor", "garcom", "garçom", "balconista",
            "pedir uma cerveja", "pedir cerveja", "pedir bebida", "pedir vinho", "pedir guisado", "pedir comida",
            "comprar cerveja", "pagar uma caneca", "uma caneca de", "caneca de cerveja",
            "ouvir rumores", "escutar rumores", "ouvir boatos", "escutar boatos", "ouvir conversas",
            "conversar na taverna", "puxar conversa"
        ]):
            local_tipo = "DIALOGAR"
            if any(w in p_low for w in ["cerveja", "bebida", "vinho", "caneca", "guisado", "comida"]):
                local_intencao = "O herói pede uma bebida e comida no balcão da taverna enquanto observa o ambiente."
            elif any(w in p_low for w in ["rumor", "rumores", "boato", "boatos"]):
                local_intencao = "O herói apura os ouvidos para ouvir rumores e conversas na taverna."
            elif any(w in p_low for w in ["maelor", "bardo", "menestrel"]):
                local_intencao = "O herói se aproxima do menestrel Maelor para conversar sobre canções e histórias da terra."
            elif any(w in p_low for w in ["taverneiro", "balconista"]):
                local_intencao = "O herói se aproxima do taverneiro de um olho só para conversar."
            else:
                local_intencao = f"O herói inicia um diálogo: {player_input}."

        # 3. Observação do Cenário
        elif any(w in p_low for w in ["olhar ao redor", "observar taverna", "olhar taverna", "examinar taverna", "observar o local", "examinar o local", "vasculhar taverna"]):
            local_tipo = "INTERAGIR_CENARIO"
            local_intencao = "O herói observa atentamente o movimento e as figuras presentes na taverna."

        # 4. Descanso
        elif any(w in p_low for w in ["descansar", "dormir", "repousar", "descanso"]):
            local_tipo = "DESCANSAR"
            local_intencao = "O jogador procura um lugar para descansar e recuperar forças."

        # 5. Subir Nível
        elif any(w in p_low for w in ["subir nivel", "subir de nivel", "level up", "upar", "evoluir"]):
            local_tipo = "SUBIR_NIVEL"
            local_intencao = "O herói canaliza sua experiência acumulada para subir de nível."

        # 6. Avançar História (com proteção contra falsos positivos)
        elif (
            any(w in p_low for w in ["proximo beat", "próximo beat", "avancar na estrada", "avançar na estrada", "seguir viagem", "pegar a estrada", "partir para a estrada", "viajar para a estrada", "avancar historia", "avançar história", "avancar campanha", "avançar campanha", "ir para o vulcao", "ir para o vulcão", "partir da taverna", "sair da taverna"])
            or (
                any(w in p_low for w in ["sair", "viajar", "partir", "avancar", "avançar"])
                and not any(w in p_low for w in ["mesa", "canto", "balcao", "balcão", "missao", "missão", "trabalho", "contrato", "falar", "conversar", "taverneiro", "cerveja", "pedir"])
            )
        ):
            local_tipo = "AVANCAR_HISTORIA"
            local_intencao = "O herói decide partir e avançar pela estrada."
        elif any(w in p_low for w in [
            "retomar o folego", "retomar o fôlego", "second wind",
            "surto de acao", "surto de ação", "action surge",
            "smite", "destruicao divina", "destruição divina", "divine smite",
            "curar pelas maos", "curar pelas mãos", "cura pelas maos", "cura pelas mãos", "lay on hands",
            "marca do cacador", "marca do caçador", "hunter's mark", "hunters mark",
            "ataque furtivo", "sneak attack",
            "acao ardilosa", "ação ardilosa", "cunning action",
            "escudo arcano", "shield spell",
            "preservar a vida", "canalizar divindade",
            "esquiva sobrenatural", "uncanny dodge",
            "usar habilidade", "ativar habilidade"
        ]):
            local_tipo = "USAR_HABILIDADE"
            habilidades_map = {
                "retomar o fôlego": ["retomar o folego", "retomar o fôlego", "second wind"],
                "surto de ação": ["surto de acao", "surto de ação", "action surge"],
                "destruição divina": ["destruicao divina", "destruição divina", "divine smite", "smite"],
                "cura pelas mãos": ["curar pelas maos", "curar pelas mãos", "cura pelas maos", "cura pelas mãos", "lay on hands"],
                "marca do caçador": ["marca do cacador", "marca do caçador", "hunter's mark", "hunters mark"],
                "ataque furtivo": ["ataque furtivo", "sneak attack"],
                "ação ardilosa": ["acao ardilosa", "ação ardilosa", "cunning action"],
                "escudo arcano": ["escudo arcano", "shield spell"],
                "preservar a vida": ["preservar a vida", "canalizar divindade"],
                "esquiva sobrenatural": ["esquiva sobrenatural", "uncanny dodge"]
            }
            for hab_nome, triggers in habilidades_map.items():
                if any(t in p_low for t in triggers):
                    local_recurso = hab_nome
                    break
            if not local_recurso:
                local_recurso = "habilidade de classe"
            for ent in entidades_ativas:
                if ent.lower() in p_low:
                    local_alvo = [ent]
                    break
            if not local_alvo and entidades_ativas and local_recurso in ["destruição divina", "marca do caçador", "ataque furtivo"]:
                local_alvo = [entidades_ativas[0]]
            local_intencao = f"O herói ativa a habilidade {local_recurso}."
        elif any(w in p_low for w in ["equipar", "empunhar", "desembainhar", "trocar de arma", "trocar para", "usar arma", "sacar"]):
            local_tipo = "EQUIPAR_ITEM"
            palavras_chave_troca = ["equipar", "empunhar", "desembainhar", "trocar para", "trocar de arma para", "trocar de arma", "usar arma", "sacar"]
            for pk in palavras_chave_troca:
                if pk in p_low:
                    partes = p_low.split(pk, 1)
                    if len(partes) > 1 and partes[1].strip():
                        # Remove preposições comuns no início
                        sub = partes[1].strip()
                        for prep in ["minha ", "meu ", "a ", "o ", "um ", "uma ", "para ", "de "]:
                            if sub.startswith(prep):
                                sub = sub[len(prep):].strip()
                        if sub:
                            local_recurso = sub
                            break
            if not local_recurso:
                for arma_padrao in ["espada longa", "espada curta", "espada bastarda", "montante", "arco longo", "arco curto", "besta", "adaga", "machado", "maça", "maca", "lança", "lanca", "escudo"]:
                    if arma_padrao in p_low:
                        local_recurso = arma_padrao
                        break
            local_intencao = f"O herói desembainha e equipa {local_recurso if local_recurso else 'sua arma'} para combate."
        elif any(w in p_low for w in ["atacar", "golpear", "bater", "investir", "flechar"]):
            local_tipo = "ATACAR"
            for ent in entidades_ativas:
                if ent.lower() in p_low:
                    local_alvo = [ent]
                    break
            if not local_alvo and entidades_ativas:
                local_alvo = [entidades_ativas[0]]
            local_intencao = f"O jogador ataca {local_alvo[0] if local_alvo else 'o inimigo'}."
        elif any(w in p_low for w in ["pocao", "poção", "usar item", "antidoto", "antídoto"]):
            local_tipo = "USAR_ITEM"
            local_intencao = "O herói usa um item de seu inventário."

        fallback = {
            "tipo_acao": local_tipo, 
            "alvo": local_alvo, 
            "recurso_utilizado": local_recurso, 
            "intencao_cena": local_intencao
        }
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=sys_instr,
                    response_mime_type="application/json",
                    temperature=0.0
                )
            )
            raw_text = response.text or "{}"
            parsed = self._extract_and_parse_json(raw_text, is_narrative=False)
            if not isinstance(parsed, dict):
                parsed = fallback.copy()
            
            # Validação rápida para garantir chaves do fallback
            for k in fallback.keys():
                if k not in parsed or parsed[k] is None and k == "tipo_acao":
                    parsed[k] = fallback[k]
                    
            print("\n[AI_MASTER NLP] Intenção Extraída com Sucesso:")
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
            return parsed
            
        except Exception as e:
            print(f"[ERRO NLP] Falha ao extrair intenção via JSON nativo: {e}")
            return fallback.copy()

    def generate_narrative_from_log(
        self, 
        system_log: str, 
        player_identity: Dict[str, Any], 
        scene_state: Dict[str, Any], 
        player_action: str,
        campaign_lore: str = "",
        scene_context: str = ""
    ) -> Dict[str, Any]:
        """
        Recebe o Log de Máquina matemático (Fase 1) e atua como o Tradutor Narrativo (Fase 2).
        Retorna um dicionário JSON com a prosa final e identificação de NPC falante.
        Implementa a Memória Híbrida de 3 Camadas.
        """
        sys_instr_base = (
            "[O Código de Maelor das Cordas de Cinza - Menestrel e AI Game Master]\n"
            "Você é Maelor das Cordas de Cinza, o cronista e bardo taciturno, cínico e poético do cataclismo de cinzas.\n"
            "Dedilhando seu alaúde de cordas de cinza e tendões de wyrm ao canto da lareira ou na beira da estrada fustigada pelo vento, você narra os feitos com solenidade poética, realismo sombrio e rica evocação dos 5 sentidos (cheiro acre de fuligem, gosto ferroso de sangue, frio cortante, tinir de ferro fundido).\n"
            "\nDIRETRIZES FUNDAMENTAIS DO MENESTREL:\n"
            "1. INCORPORAÇÃO DA AÇÃO: Pegue exatamente o que o jogador digitou ou falou e insira organicamente na narrativa, respeitando o contexto da cena.\n"
            "2. AMBIENTAÇÃO SENSORIAL DOS 5 SENTIDOS: Descreva o cenário com riqueza sensorial palpável (iluminação, sombras, texturas, cheiro de ferro/terra/fumaça, frio do vento, ruídos distantes) para que o jogador sinta onde pisa.\n"
            "3. REAÇÃO DO MUNDO E ENTIDADES: Descreva o que os monstros, NPCs e o ambiente ao redor estão fazendo ou como reagem à presença e ações do herói.\n"
            "4. A REGRA DE OURO DOS ALIADOS E DA JORNADA SOLITÁRIA: O protagonista viaja e combate ABSOLUTAMENTE SOZINHO do Beat 1 ao Beat 14. Quando um Herói Aliado (HERO-01 a HERO-42) for resgatado ou recrutado, narre a solenidade do juramento de sangue/honra selado para a batalha final na caldeira, e a partida imediata do aliado para reunir forças ou cuidar de sobreviventes. NUNCA narre aliados marchando ou lutando ao lado do herói nos Beats 1 a 14. Todos os aliados jurados só se reúnem na arena final do Beat 15 (Covil do Tirano).\n"
            "5. FIDELIDADE MECÂNICA VISCERAL: Espelhe as consequências físicas exatas do Log de Máquina (acertos, erros, defesas, ferimentos). É ESTRITAMENTE PROIBIDO citar números ou dados na narrativa ('1d20', 'CA 15', '4 de dano'); traduza tudo em peso da lâmina, dor, estilhaços e sangue. Se o log contiver '[SISTEMA FATAL]', narre a queda definitiva.\n"
            "6. ALTERNÂNCIA E REFLEXO DE EQUIPAMENTO: Sempre que o jogador equipar, empunhar ou trocar de arma (ou realizar um ataque após troca), reflita a arma equipada atual com peso sensorial palpável na prosa (o peso do aço forjado, a tensão da corda do arco, o estalar das flechas ou o equilíbrio da lâmina em guarda).\n"
            "7. RESSONÂNCIA SENSORIAL DAS HABILIDADES DE CLASSE: Quando o log do sistema ou a ação do jogador indicar a ativação ou aquisição de habilidades icônicas (ex: o clarão ofuscante de um Smite divino consumindo a lâmina, o fôlego recuperado com dentes cerrados no Retomar o Fôlego/Second Wind, a flecha marcada sibilando nas sombras com a Marca do Caçador, o golpe furtivo abrindo a jugular no Ataque Furtivo, ou o hexágono cintilante de um Escudo Arcano), narre a manifestação física visceral dessa proeza sem metajogo de números.\n"
            "8. ENQUADRAMENTO ESPACIAL E GANCHOS DE AÇÃO: Ao final da narração, sempre situe onde o herói se encontra e apresente de 2 a 3 possibilidades naturais de ação ou investigação para devolver a agência ao jogador.\n"
            "9. VOCÊ DEVE RETORNAR ESTRITAMENTE UM JSON NO SEGUINTE FORMATO:\n"
            "{\"texto\": \"Sua narrativa imersiva aqui\", \"npc_falando\": \"Nome do NPC ou null\"}\n"
        )
        
        # Tratamento da injeção do Lore caso venha vazio nas primeiras rodadas
        if not campaign_lore:
            campaign_lore = "O mundo é hostil. O perigo é constante e impiedoso."
        if not scene_context:
            scene_context = "Uma área desconhecida e brutal."

        # Construção do Índice 0 (Imutável e Protegido)
        mensagem_sistema = f"{sys_instr_base}\n\n[Contexto da Cena Atual (Raw Data)]\n{scene_context}\n\n[Quest Log/Diário de Campanha (Layer 3 - Fatos Crus)]\n{campaign_lore}"
        
        # Monta a ficha resumida do jogador
        equipments = ", ".join(player_identity.get('inventory', []))
        identity_str = f"Raça: {player_identity.get('race', 'Aventureiro')}. Classe: {player_identity.get('class', 'Desconhecida')}. Equipamentos: {equipments}."
        scene_str = f"Ambiente atual: {scene_state.get('environment', 'Desconhecido')}. Inimigos Vivos: {scene_state.get('living_enemies', 'Nenhum visível')}."
        if "combat_alert" in scene_state:
            scene_str += f" | {scene_state['combat_alert']}"
            
        # Camada 1 (Sliding Window): Fatiar histórico recente para as últimas 5 interações
        historico_recente = self.chat_history[-5:]
        history_str = "Histórico Recente:\n"
        for turn in historico_recente:
            history_str += f"- Jogador: {turn.get('user', '')}\n- DM: {turn.get('dm', '')}\n"
            
        prompt = (
            f"[FATOS CRUS - IDENTIDADE]: {identity_str}\n"
            f"[FATOS CRUS - ESTADO ATUAL]: {scene_str}\n"
            f"[HISTÓRICO]:\n{history_str}\n"
            f"[LOG DE MÁQUINA - A LEI ABSOLUTA]: {system_log}\n"
            f"[AÇÃO DO JOGADOR NESTE TURNO]: {player_action}\n\n"
            f"Com base no histórico recente e PRIORIZANDO ABSOLUTAMENTE A ÚLTIMA RESPOSTA DO USUÁRIO, elabore uma narração/pergunta VISCERAL baseada nos fatos crus. Use os 5 sentidos e retorne o JSON estrito:"
        )
        
        try:
            # Temperatura 0.7 para permitir a prosa descritiva sem quebrar regras lógicas
            raw_text = self._generate_text_with_retry(prompt, mensagem_sistema, temperature=0.7)
            
            parsed_json = self._extract_and_parse_json(raw_text, is_narrative=True)
            texto_narrativa = parsed_json.get("texto", "")
            
            # Adiciona ao histórico (Sliding Window)
            self.chat_history.append({"user": player_action, "dm": texto_narrativa})
            # Mantém apenas as últimas 5 interações
            if len(self.chat_history) > 5:
                self.chat_history.pop(0)
                
            return parsed_json
        except Exception as e:
            print(f"[ERRO] Falha ao gerar narrativa na Fase 2: {e}")
            return self._extract_and_parse_json("ERRO", is_narrative=True)

    def generate_narrative_from_math(self, combat_log: str, intencao_cena: str) -> str:
        """
        Fase 2 - The Visceral Narrator (Bloco 30).
        Traduz o log matemático em narrativa visceral Dark Fantasy na voz de Maelor das Cordas de Cinza.
        """
        sys_instr = (
            "[O Código de Maelor das Cordas de Cinza - Menestrel e AI Game Master]\n"
            "Você é Maelor das Cordas de Cinza, o cronista e bardo taciturno, cínico e poético do cataclismo de cinzas.\n"
            "Dedilhando seu alaúde de cordas de cinzas e tendões ao canto da lareira ou na beira da estrada, você traduz o LOG MECÂNICO ou CENÁRIO em uma narrativa visceral, sensorial e cinematográfica (1 a 2 parágrafos).\n"
            "\nDIRETRIZES FUNDAMENTAIS DO MENESTREL:\n"
            "1. INCORPORAÇÃO DA AÇÃO DO JOGADOR: Pegue exatamente o que o jogador tentou fazer ou falar (da INTENÇÃO DO JOGADOR) e teça isso diretamente na narrativa dentro do contexto atual.\n"
            "2. ENQUADRAMENTO SENSORIAL DOS 5 SENTIDOS: Introduza e descreva o ambiente para que o jogador 'enxergue' e 'sinta' tudo ao redor — texturas de aço e pedra, cheiro acre de fuligem e sangue, frio do vento, eco de lâminas e a reação dos inimigos e NPCs no local.\n"
            "3. FIDELIDADE AOS FATOS E À MECÂNICA: Espelhe a matemática e o estado do jogo. Se o ataque acertou ou errou, se curou ou se moveu, reflita com impacto físico real. É ESTRITAMENTE PROIBIDO citar números ou fórmulas de dados (ex: '1d20', 'CA 15', '12 de dano'); traduza tudo em peso da lâmina, dor, estilhaços e sangue.\n"
            "4. A REGRA DE OURO DOS ALIADOS E DA JORNADA SOLITÁRIA: O protagonista viaja e combate ABSOLUTAMENTE SOZINHO do Beat 1 ao Beat 14. Quando um Herói Aliado (HERO-01 a HERO-42) for resgatado ou recrutado, narre a solenidade do juramento de sangue/honra selado para a batalha final na caldeira, e a partida imediata do aliado para reunir forças ou cuidar de sobreviventes. NUNCA narre aliados marchando ou lutando ao lado do herói nos Beats 1 a 14. Todos os aliados jurados só se reúnem na arena final do Beat 15 (Covil do Tirano).\n"
            "5. ALTERNÂNCIA E REFLEXO DE EQUIPAMENTO: Reflita com exatidão a arma ou equipamento atualmente em punho nos ataques e ações (o equilíbrio da espada longa, a empunhadura gasta da adaga, a vibração do arco), dando textura física a cada golpe ou troca de postura.\n"
            "6. RESSONÂNCIA SENSORIAL DAS HABILIDADES DE CLASSE: Quando o log do sistema ou a intenção indicar ativação ou aprendizado de habilidades de classe icônicas (o clarão ofuscante de um Smite divino, o fôlego recuperado com dentes cerrados no Retomar o Fôlego/Second Wind, a flecha marcada sibilando nas sombras com a Marca do Caçador, o golpe furtivo abrindo a jugular no Ataque Furtivo, ou o escudo arcano desviando o aço), traduza em impacto sensorial potente e épico.\n"
            "7. ENQUADRAMENTO ESPACIAL E GANCHOS SITUACIONAIS: Conclua a narração situando o herói na cena e apresentando sutilmente de 2 a 3 possibilidades naturais de ação ou ganchos para onde ele pode olhar, interagir ou se mover (ex: 'Diante de você, o taverneiro limpa o balcão desconfiado, enquanto risadas ecoam ao fundo. Você pode puxar conversa, observar as redondezas ou pedir uma caneca.'). Dê agência ao jogador!\n"
            "\nREGRAS DE CONTEXTO ESPECÍFICO:\n"
            "- Interação/Exploração/Hub: Aja como Maelor observando a cena. Incorpore falas de NPCs, rumores da taverna ou perigos do ambiente.\n"
            "- Itens e Cura: Narre o frasco se partindo, o líquido amargo queimando na garganta e o fechamento doloroso da carne ferida.\n"
            "- Magia e Habilidades: Descreva energia ancestral, cheiro de ozônio, calor sagrado ou precisão marcial brutal, sem clichês infantis.\n"
            "- Descanso: No refúgio da taverna, descreva o alívio temporário do calor da lareira; no acampamento selvagem, o descanso tenso sob vigília solitária.\n"
            "- Clímax e Déjà Vu (Beat 15): Se o herói sucumbir ao fogo do Dragão Supremo, narre a torrente colossal e o retorno súbito do tempo para a taverna (Loop 1), mantendo a memória indelével da dor e da experiência.\n"
            "- Morte: Descreva a queda definitiva na lama e o frio da escuridão eterna.\n"
        )
        
        prompt = (
            f"INTENÇÃO DO JOGADOR: {intencao_cena}\n"
            f"LOG MATEMÁTICO OU CENÁRIO: {combat_log}\n\n"
            "Narre o resultado como Mestre de RPG situando o herói e sugerindo opções de ação (APENAS O TEXTO DA NARRAÇÃO, SEM JSON E SEM MARKDOWN):"
        )
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=sys_instr,
                    temperature=0.6,
                )
            )
            return response.text.strip() if response.text else self._create_visceral_fallback(combat_log, intencao_cena)
        except Exception as e:
            print(f"[ERRO] Falha ao gerar narrativa visceral (ativando fallback seguro): {e}")
            return self._create_visceral_fallback(combat_log, intencao_cena)

    def _create_visceral_fallback(self, combat_log: str, intencao_cena: str) -> str:
        """Fallback narrativo imersivo na voz de Maelor das Cordas de Cinza."""
        log_lower = (combat_log or "").lower()
        intencao_lower = (intencao_cena or "").lower()

        # 1. Déjà Vu / Loop Temporal do Clímax (Prioridade sobre morte simples, pois sopro fatal aciona Déjà Vu)
        if any(w in intencao_lower or w in log_lower for w in ["deja vu", "déjà vu", "loop", "deja_vu"]):
            return "Uma vertigem de chamas brancas estilhaça a realidade. O som do trovão ecoa como uma lembrança já vivida — o ciclo de déjà vu recomeça na taverna e a lembrança do fogo do dragão queima na mente."

        # 2. Morte Definitiva / 0 HP (quando não é loop)
        if "morreu" in log_lower or "fatal" in log_lower or "game over" in log_lower or "morte" in intencao_lower or "letal" in log_lower or "0 hp" in log_lower:
            return "O golpe final silencia a respiração e estilhaça a guarda. O corpo cede sob o peso inevitável da terra fria e a escuridão da morte o consome por inteiro."

        # 3. Premonição / Despertar / Ressurreição
        if any(w in intencao_lower or w in log_lower for w in ["acordar", "despertar", "premoni", "ressurrei"]):
            return "Você desperta com o coração disparado e o suor frio escorrendo pela pele. O ar entra cortando os pulmões como vidro moído enquanto a memória do fogo do dragão queima a mente."

        # 4. Habilidades de Classe Icônicas (Smite, Second Wind, Marca do Caçador, Sneak Attack, etc.)
        if any(w in intencao_lower or w in log_lower for w in ["smite", "destruicao divina", "destruição divina", "divine smite"]):
            return "Um clarão ofuscante de chamas celestes irrompe ao longo da lâmina no instante do impacto. O estrondo radiante estilhaça a penumbra com calor sagrado, purificando a carne corrompida em fúria divina!"

        if any(w in intencao_lower or w in log_lower for w in ["retomar o folego", "retomar o fôlego", "second wind"]):
            return "Com dentes cerrados e respiração entrecortada, seus pulmões puxam o ar cortante das cinzas. A dor latejante recua sob pura disciplina marcial enquanto o vigor retorna aos músculos retesados."

        if any(w in intencao_lower or w in log_lower for w in ["marca do cacador", "marca do caçador", "hunter's mark", "hunters mark"]):
            return "Seus olhos estreitam na penumbra enquanto uma runa espectral esmeralda fixa a presa. A flecha marcada sibila nas sombras, atraída inexoravelmente pelo ponto vital da criatura."

        if any(w in intencao_lower or w in log_lower for w in ["ataque furtivo", "sneak attack", "emboscada mortal"]):
            return "Movendo-se como fumaça gélida pelo ângulo morto do inimigo, o golpe furtivo encontra a brecha da armadura e abre a jugular com precisão cirúrgica antes que qualquer grito ecoe."

        if any(w in intencao_lower or w in log_lower for w in ["surto de acao", "surto de ação", "action surge"]):
            return "Um estalo violento de adrenalina rompe os limites da carne. O tempo parece desacelerar na bruma enquanto seus braços ignoram o cansaço, desferindo uma nova sequência fulminante de aço!"

        if any(w in intencao_lower or w in log_lower for w in ["cura pelas maos", "cura pelas mãos", "lay on hands", "preservar a vida", "bencao da cura", "bênção da cura"]):
            return "A mão repousa sobre as feridas abertas irradiando um calor dourado e solene. O sangue estanca sob a graça divina e a carne dilacerada se fecha, afastando a sombra da morte."

        if any(w in intencao_lower or w in log_lower for w in ["escudo arcano", "shield spell", "recuperacao arcana", "recuperação arcana", "evocacao potente", "evocação potente"]):
            return "Runas em ciano etéreo cintilam no ar com estalo de ozônio. A barreira geométrica de força arcana se ergue no milissegundo exato, desviando o impacto letal em uma chuva de fagulhas místicas!"

        if any(w in intencao_lower or w in log_lower for w in ["acao ardilosa", "ação ardilosa", "cunning action", "esquiva sobrenatural", "uncanny dodge"]):
            return "Com reflexos felinos forjados nos becos escuros, seu corpo se esgueira como vapor no último instante. A lâmina inimiga corta apenas o vazio e farrapos de capa enquanto você se reposiciona nas sombras."

        if any(w in intencao_lower or w in log_lower for w in ["desbloqueou habilidade", "nova habilidade", "habilidade adquirida", "arvore de habilidades", "árvore de habilidades"]):
            return "O sangue ferve com a sabedoria forjada no aço e nas cinzas. Uma nova técnica ancestral desperta em sua memória muscular, gravada no Grimório como trunfo para a provação vindoura."

        # 5. Alternância e Equipamento de Arma (Item 4.2)
        if any(w in intencao_lower or w in log_lower for w in ["equipar", "empunhar", "desembainhar", "trocar de arma", "trocar para", "troca de arma", "usar arma", "sacar"]):
            recurso_citado = "do aço"
            for arma in ["espada longa", "espada curta", "espada bastarda", "montante", "arco longo", "arco curto", "besta", "adaga", "machado", "maça", "maca", "lança", "lanca", "escudo"]:
                if arma in intencao_lower or arma in log_lower:
                    recurso_citado = f"da {arma}" if arma.endswith("a") else f"do {arma}"
                    break
            return f"O aço ressoa ao ser desembainhado na névoa; seus dedos ajustam o aperto firme no cabo {recurso_citado}, sentindo o peso e o equilíbrio mortal do equipamento sob as cinzas."

        # 5. Juramento de Herói Aliado
        if any(w in intencao_lower or w in log_lower for w in ["juramento", "aliado", "recrut", "pacto", "honra", "jurou"]):
            return "O aço toca o peito em solene promessa. O aliado sela o juramento de honra e sangue: ele recolhe seus pertences e parte para aguardar o chamado da marcha para a batalha final contra o Tirano."

        # 6. Viagem para Side Quest / Covil / Altar
        if any(w in intencao_lower or w in log_lower for w in ["covil", "altar"]) or (any(w in intencao_lower or w in log_lower for w in ["viagem", "partindo", "trilha"]) and any(w in intencao_lower or w in log_lower for w in ["side_quest", "side quest", "missao", "missão"])):
            return "A trilha cinzenta se estende sob um céu sufocado por fuligem. Seus passos solitários quebram o silêncio da terra desolada enquanto a aproximação cautelosa revela os perigos e provisões do covil."

        # 7. Conclusão de Side Quest / Contrato
        if any(w in intencao_lower or w in log_lower for w in ["side_quest", "side quest", "contrato", "resgate"]):
            return "O contrato sangrento chega ao fim. As cinzas assentam e a justa recompensa é tomada, enquanto os ecos da missão se dissipam na bruma da terra desolada."

        # 7. Reatividade de Aliados e Rumores no Hub da Taverna (Item 4.1)
        if "[rumores da taverna]" in log_lower or "[rumor" in log_lower or (any(w in intencao_lower or w in log_lower for w in ["taverna", "rumor", "conversa", "balcão"]) and any(w in log_lower for w in ["juramento", "aliado", "guerreiro", "leal"])):
            return "Maelor das Cordas de Cinza dedilha uma melodia solene no alaúde carcomido ao canto da lareira. Entre goles de cerveja amarga, sussurros confirmam a vigília leal dos guerreiros juramentados nos contrafortes da montanha e passos escuros, aguardando em silêncio o seu chamado para a batalha final do Clímax contra o Tirano."

        # 8. Procura de Missões / Contratos / Trabalho na Taverna
        if any(w in intencao_lower or w in log_lower for w in [
            "procura de missao", "procura de missão", "procurando missao", "procurando missão",
            "procuro missao", "procuro missão", "quero missao", "quero missão", "buscar missao", "buscar missão",
            "procura de trabalho", "procurando trabalho", "procuro trabalho", "quero trabalho",
            "procura de contrato", "procurando contrato", "procuro contrato", "quero um contrato", "quero contrato",
            "quadro de avisos", "mural de contratos", "pedir missao", "pedir missão", "trabalhos e missões",
            "trabalhos e missoes"
        ]) or (any(w in intencao_lower or w in log_lower for w in ["missao", "missão", "trabalho", "contrato"]) and any(w in intencao_lower or w in log_lower for w in ["taverna", "balcao", "balcão", "taverneiro", "procura", "procurando", "busco", "quero", "disponivel", "disponível"]) and not any(w in intencao_lower or w in log_lower for w in ["conclu", "cumprid", "fim", "recompensa"])):
            return "O taverneiro aponta uma caneca úmida em direção ao canto do balcão onde pergaminhos amarelados estão afixados: 'Se procura trabalho com recompensa em ouro, a Trilha dos Enforcados está infestada de feras e mercenários saqueadores. Você pode inspecionar os contratos no seu Diário ou perguntar aos mercenários ao redor.'"

        # 9. Conversas com o Menestrel Maelor
        if any(w in intencao_lower or w in log_lower for w in ["falar com maelor", "conversar com maelor", "ouvir maelor", "perguntar ao bardo", "falar com o bardo", "conversar com o menestrel", "ouvir bardo", "falar com bardo"]):
            return "Maelor dedilha um acorde sombrio no alaúde de cordas de cinzas e ergue o olhar cansado: 'Cada canção que entoo é o epitáfio de quem ousou desafiar o Tirano sem aliados. Se quer sobreviver ao clímax, procure os guerreiros perdidos nas terras baixas.'"

        # 8. Descanso / Repouso (Precedência sobre diálogos casuais de comida/bebida)
        if any(w in intencao_lower or w in log_lower for w in ["descanso", "repouso", "descansar", "dormir"]):
            if any(w in log_lower for w in ["[rumores da taverna]", "aliado jurado", "juramento", "vigília leal", "vigilia leal"]):
                return "Maelor das Cordas de Cinza dedilha uma melodia suave ao canto do fogo. O calor crepitante da lareira restaura suas forças enquanto ecos na taverna lembram da vigília leal de seus aliados juramentados nos contrafortes, aguardando o chamado para o Clímax."
            return "O calor crepitante da lareira e a caneca fumegante trazem um alívio temporário às dores do corpo. O descanso restaura as forças para a marcha solitária."

        if any(w in intencao_lower or w in log_lower for w in ["acampamento", "vigilia", "vigília"]):
            return "O vento sopra gélido entre as pedras calcinadas. Em vigília tensa e solitária, o repouso sob a capa puída é o suficiente para estancar as feridas da jornada."

        # 9. Conversas gerais com o Taverneiro / Pedido de Bebida / Comida
        if any(w in intencao_lower or w in log_lower for w in ["cerveja", "bebida", "vinho", "caneca", "taverneiro", "pedir bebida", "pedir cerveja", "comprar cerveja", "balconista", "garcom", "garçom", "guisado"]) and not any(w in intencao_lower or w in log_lower for w in ["combate", "atacar", "dano", "morte"]):
            return "O taverneiro enxuga a madeira carcomida com um trapo velho e serve uma caneca de cerveja escura e amarga: 'Beba enquanto há teto sobre sua cabeça, forasteiro. Lá fora, as cinzas não perdoam os descuidados.'"

        # 10. Observação do Cenário / Rumores e Boatos
        if any(w in intencao_lower or w in log_lower for w in ["rumores", "rumor", "boatos", "boato", "olhar ao redor", "observar taverna", "olhar taverna", "examinar taverna", "vasculhar taverna", "ouvir conversas"]):
            return "Seus olhos vasculham a taverna sombria. Mercenários cochicham sobre criaturas emboscando carroças na estrada norte e sussurros de um lobo atroz rondando as colinas."

        # 9. Recuo Tático e Fuga
        if any(w in intencao_lower or w in log_lower for w in ["recuo", "retorno ao hub", "retorno", "fuga", "fugir", "recuar"]):
            return "Com fôlego curto e passos firmes nas sombras, você recua em fuga pelas cinzas da estrada. O calor crepitante da lareira da Taverna do Dragão Acordado surge na bruma, oferecendo abrigo seguro para recompor o aço e o ânimo."

        if any(w in intencao_lower or w in log_lower for w in ["emboscada", "selvagem"]):
            return "Um estalo repentino quebra o silêncio da bruma. Vultos saltam das sombras com lâminas oxidadas em riste antes que qualquer palavra seja dita!"

        if "recuperou" in log_lower or "cura" in log_lower or "pocao" in intencao_lower or "poção" in intencao_lower or ("hp" in log_lower and ("+" in log_lower or "recupera" in log_lower)):
            return "A poção desce queimando amarga como fel pela garganta. O sangue estanca e as dores diminuem enquanto as feridas se fecham sob ardor pungente."

        if any(w in log_lower for w in ["dano", "sofreu", "acerto", "acertou"]) or any(w in intencao_lower for w in ["ataque", "atacar", "combate", "golpe"]):
            return "O choque das lâminas ressoa pelo ambiente com estalo brutal de ferro. O impacto arranca um chiado de esforço e sangue enquanto o combate avança sem hesitação."

        if "orbe" in intencao_lower or "relicario" in intencao_lower:
            return "A poeira dos séculos se desprende da pedra fria. Seus dedos encontram o artefato esculpido, cujo peso ressoa com energia ancestral na penumbra."

        if any(w in intencao_lower or w in log_lower for w in ["transi", "jornada", "avan", "viagem", "estrada", "partir"]):
            return "Os passos firmes ecoam pela terra desolada. O cenário cinzento fica para trás enquanto uma nova trilha solitária se abre diante de você."

        return "O dedilhar melancólico das cordas de cinza ecoa no ar. A tensão permanece suspensa na penumbra enquanto seus olhos buscam a próxima ameaça."

    def get_personalized_prologue(self, char_data: Dict[str, Any], cutscenes_path: str = "data/game_cutscenes.json") -> str:
        """
        Carrega o prólogo de cutscenes e injeta os dados reais da ficha
        ({nome}, {raca}, {classe}, {antecedente}, {tendencia}), valorizando
        também o gênero ("female" / "male") e a herança racial única do protagonista.
        """
        nome = char_data.get("name") or char_data.get("nome") or "Viajante"
        raca = char_data.get("race") or char_data.get("raca") or "Humano"
        classe = char_data.get("class") or char_data.get("classe") or "Guerreiro"
        antecedente = char_data.get("background") or char_data.get("antecedente") or "Forasteiro"
        tendencia = char_data.get("alignment") or char_data.get("tendencia") or "Neutro"
        genero_raw = str(char_data.get("gender") or char_data.get("genero") or "male").lower().strip()
        is_female = genero_raw in ["female", "feminino", "f", "mulher"]

        # Mapeamento canônico das 7 relíquias raciais
        raca_low = str(raca).lower()
        if "elf" in raca_low:
            reliquia_racial = "Manto de Folhas Cinzentas"
            detalhe_heranca = "envolvida pelo seu Manto de Folhas Cinzentas" if is_female else "envolvido pelo seu Manto de Folhas Cinzentas"
        elif "anão" in raca_low or "anao" in raca_low or "anã" in raca_low or "dwarf" in raca_low:
            reliquia_racial = "Runa da Pedra-Forja"
            detalhe_heranca = "portando o calor ancestral da Runa da Pedra-Forja"
        elif "halfling" in raca_low:
            reliquia_racial = "Moeda da Sorte Antiga"
            detalhe_heranca = "girando entre os dedos a Moeda da Sorte Antiga"
        elif "dracon" in raca_low or "dragon" in raca_low:
            reliquia_racial = "Escama Ancestral Incandescente"
            detalhe_heranca = "com a Escama Ancestral Incandescente pulsando junto ao peito"
        elif "orc" in raca_low:
            reliquia_racial = "Presa de Ferro Sangrento"
            detalhe_heranca = "ostentando a brutal Presa de Ferro Sangrento"
        elif "tiefling" in raca_low:
            reliquia_racial = "Selo de Brasas Abissais"
            detalhe_heranca = "sob o brilho sulfúrico do Selo de Brasas Abissais"
        else:
            reliquia_racial = "Sinete da Coroa Partida"
            detalhe_heranca = "trazendo consigo o Sinete da Coroa Partida"

        artigo = "uma" if is_female else "um"
        forjado_str = "forjada" if is_female else "forjado"

        prologue_lines = []
        for p in [cutscenes_path, "game_cutscenes.json", "data/game_cutscenes.json"]:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8", errors="replace") as f:
                        data = json.load(f)
                        if "beat_1_prologue" in data:
                            prologue_lines = data["beat_1_prologue"]
                            break
                except Exception as e:
                    print(f"[ERRO IA] Falha ao carregar cutscenes em '{p}': {e}")

        if not prologue_lines:
            return (
                f"O vento cinzento sopra uivos pela soleira quando {nome} empurra a pesada porta de carvalho da taverna.\n\n"
                f"Ao canto escuro da lareira, Maelor das Cordas de Cinza dedilha uma nota áspera em seu alaúde de tendões, "
                f"observando a silhueta de {artigo} {raca} {classe} {forjado_str} nas agruras de {antecedente}, {detalhe_heranca}.\n\n"
                f"Com postura {tendencia}, você sabe que neste vale devastado pela fumaça o aço fala mais alto que preces vãs. "
                f"O olhar cansado do taverneiro de um olho só se ergue na penumbra: a estrada para a montanha não perdoa os fracos, "
                f"e a canção do Tirano das Cinzas já começou a ser escrita."
            )

        raw_text = "\n\n".join(prologue_lines)
        formatted = (
            raw_text
            .replace("{nome}", str(nome))
            .replace("{raca}", str(raca))
            .replace("{classe}", str(classe))
            .replace("{antecedente}", str(antecedente))
            .replace("{tendencia}", str(tendencia))
            .replace("{reliquia}", str(reliquia_racial))
        )

        if is_female:
            formatted = (
                formatted
                .replace(f"Como um {raca} {classe} moldado", f"Como uma {raca} {classe} moldada")
                .replace("moldado pela dureza", "moldada pela dureza")
            )

        if reliquia_racial not in formatted:
            formatted += f"\n\nJunto ao seu equipamento de viagem, o peso ancestral de sua herança — {reliquia_racial} ({detalhe_heranca}) — lembra quem você é diante das cinzas."

        return formatted

    def process_player_action(self, game_state: dict, player_action: str, dice_roll_result: int) -> dict:
        payload = {
            "game_state": game_state,
            "player_action": player_action,
            "dice_roll_result": dice_roll_result
        }
        prompt = json.dumps(payload, ensure_ascii=False, indent=2)

        try:
            raw_text = self._generate_text_with_retry(prompt, self.system_instruction)
            return self._extract_and_parse_json(raw_text, is_narrative=False)
        except Exception as e:
            print(f"[ERRO FATAL] API indisponível após retries: {e}")
            return {"narrative": "Uma anomalia mágica impede suas ações no momento. O Mestre está temporariamente desconectado do véu astral."}