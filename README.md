# ⚔️ RPGMesaPY — D&D 5e VTT com IA Game Master

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5%2B-green.svg?logo=python)](https://pyga.me/)
[![Google Gemini API](https://img.shields.io/badge/Google_Gemini-3.5_Flash--Lite-orange.svg?logo=google)](https://ai.google.dev/)
[![D&D 5e Ruleset](https://img.shields.io/badge/Ruleset-D%26D_5e_SRD-red.svg)](https://dnd.wizards.com/)
[![Development: AI-Coded](https://img.shields.io/badge/Development-AI--Coded%20%7C%20Human--Directed-blueviolet.svg)](https://github.com/iagobelloo/RPGMesaPY)
[![Tests](https://img.shields.io/badge/Tests-Pytest_Passing-brightgreen.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> [!IMPORTANT]
> **🤖 Nota de Autoria e Metodologia (Desenvolvimento Guiado por IA):**  
> Este projeto está sendo **100% desenvolvido e codificado por Inteligência Artificial**, sob a **direção criativa, comando e validação de [@iagobelloo](https://github.com/iagobelloo)**. O papel humano atua como *Director / Product Owner* (definindo escopo, regras D&D 5e, arte e arquitetura), enquanto toda a implementação do código, lógica matemática, interface gráfica e testes são gerados autonomamente via IA.

O **RPGMesaPY** é uma plataforma **VTT (Virtual Tabletop) 2D** desenvolvida em Python e Pygame, projetada para proporcionar uma experiência imersiva de RPG de mesa solo ou guiado, ambientada em um universo de **Grounded Dark Fantasy (Grimdark Tático)** em resolução nativa de **1280x720**.

O diferencial central do projeto é a integração profunda de um **Motor de Regras D&D 5e autêntico** com um **Game Master impulsionado por Inteligência Artificial (Google Gemini API — `gemini-3.5-flash-lite`)**, batizado de **Maelor das Cordas de Cinza**.

---

## 🎭 O Mestre da Masmorra: Maelor das Cordas de Cinza

> *"O aço não mente sob a chuva fria. O Tirano queima vilas, mas são as escolhas de um único viajante que decidem se as cinzas se levantarão ou se espalharão pelo vento."*

Maelor não é um assistente genérico: ele é um bardo e cronista taciturno sentado ao canto da fogueira, dedilhando um alaúde cujas cordas foram trançadas com tendões de wyrm.
* **Prosa dos Cinco Sentidos:** Descrições ricas em cheiro de fuligem, o tinir surdo do ferro, o gosto amargo do sangue e o vento cortante.
* **Respeito à Matemática do D&D:** Maelor nunca inventa números; ele recebe o resultado das rolagens do motor físico (D20 + Modificadores vs CA/CD) e traduz o resultado em narrativa tática (*Fail Forward*).
* **Narrativa Consequente:** Suas escolhas, descanso, inventário e ferimentos impactam diretamente a atitude dos NPCs e o rumo dos capítulos (*Beats 1 a 15*).
* **Respawn Narrativo:** Em caso de derrota fatal, Maelor intervém com uma melodia serena nas brasas da Taverna do Dragão Acordado, acolhendo o aventureiro para um novo fôlego sem quebra de imersão.

---

## ✨ Funcionalidades Principais

* **⚔️ Motor de Regras D&D 5e Completo:**
  * Criação de personagem com raças canônicas (*Humano, Anão da Colina, Elfo da Floresta, Draconato, Meio-Orc, Halfling, Tiefling*) e classes clássicas (*Guerreiro, Clérigo, Paladino, Mago, Patrulheiro, Ladino*).
  * Atributos (*FOR, DES, CON, INT, SAB, CAR*), cálculo automático de modificadores, bônus de proficiência e Classe de Armadura (CA).
  * Sistema de combate bilateral por turnos com iniciativa tática, desacoplamento de seleção de alvo, manobras (Esquivar, Recuar) e sistema de magias/habilidades 5e.
* **🧠 Inteligência Artificial Generativa (Gemini 3.5 Flash-Lite):**
  * Respostas contextuais ultrarrápidas em JSON estruturado com validação de esquema e latência reduzida.
  * Cascata de resiliência com fallback automático (`gemini-3.5-flash-lite` -> `gemini-flash-lite-latest` -> `gemini-flash-latest`).
  * Prólogo de Alta Fantasia Sombria em 3 atos com selo de cera negra e texto dinâmico.
  * Diálogos dinâmicos com NPCs e geração de consequências de combate em tempo real.
* **📜 Interface Gráfica Imersiva & Arquitetura Zero Garbage (1280x720 @ 60 FPS):**
  * **HUD Gótico Modular:** Top Bar (localização e tempo), Action Bar com manobras de combate, Player Card dinâmico com retrato chanfrado e painel de alvos.
  * **Efeito Typewriter Dinâmico:** Animação de digitação caractere por caractere no chat narrativo para imersão dramática.
  * **Grimório do Aventureiro (`Tab`):** Ficha interativa completa com atributos, perícias, magias conhecidas, árvore de habilidades e diário de missões em 1280x720.
  * **Mochila do Aventureiro:** Gerenciamento visual de inventário com capacidade de carga baseada em Força (limite em kg), equipamento de armas em um clique e uso de consumíveis.
  * **Dado d20 Animado:** Feedback visual dinâmico com animação de rolagem de dados durante o processamento da IA.
* **💾 Sistema Multi-Saves Isolado:**
  * 3 slots independentes de salvamento com serialização segura em JSON, isolamento atômico sem vazamento entre slots e tela de pergaminhos dedicada.
* **📚 Bestiário & Compêndio SRD:**
  * Monstros, itens, magias e antecedentes catalogados em bases de dados JSON estruturadas.

---

## 🏛️ Arquitetura do Projeto (MVC Estrito)

O projeto adota uma separação rigorosa entre camadas:

```text
RPGMesaPY/
├── ai_master/          # Cérebro de IA: Integração LLM (Gemini 3.5 Flash-Lite) e persona de Maelor
├── assets/             # Recursos audiovisuais (sprites, retratos, cenários, UI)
│   ├── backgrounds/    # Cenários 1280x720 de vilas, cavernas, tavernas e estradas
│   ├── sprites/        # Tokens de heróis e monstros D&D
│   └── ui/             # Texturas góticas, pergaminho, botões e frames do dado d20
├── core/               # Model/Controller: Regras D&D 5e, Combate, Inventário e Saves
│   ├── combat_system.py # Resolução de iniciativa, ataques, manobras e dano
│   ├── dice_engine.py   # Rolagem de dados criptograficamente robusta
│   ├── dnd_rules.py     # Tabelas D&D 5e oficiais (SRD)
│   ├── game_engine.py   # Gerenciador de sessão, estado, morte/respawn e saves
│   └── magic_system.py  # Espaços de magia, habilidades e efeitos arcanos/divinos
├── data/               # Bases de dados JSON (itens, magias, monstros, quests)
├── docs/               # Diretrizes canônicas, bíblia do motor e relatórios (001 a 074)
├── logs/               # Registros de log de execução (preservado via .gitkeep)
├── saves/              # Armazenamento local de partidas em slots isolados
├── scripts/            # Scripts utilitários e importadores SRD
├── tests/              # Suíte completa de testes automatizados com Pytest (29+ suítes)
├── ui/                 # View: Renderização gráfica Pygame pura (Zero Garbage)
│   ├── asset_manager.py # Cache e carregamento otimizado de imagens/fontes
│   ├── hud_components.py# Modais (Grimório, Mochila, ChatBox, QuickActions)
│   ├── menu_components.py # Menus de Pausa, Criação de Personagem e Saves
│   ├── scene_renderer.py# Renderização do tabuleiro e balões de diálogo
│   └── widgets/        # Arquitetura nativa Zero Garbage 1280x720
│       ├── hud/        # Top Bar, Action Bar, Player Card, Chat Console, Initiative
│       ├── render_cache.py # Atlas e cache de renderização estática
│       └── theme.py    # Paleta gótica escura (Cinzas, Sangue, Dourado envelhecido)
├── main.py             # Ponto de entrada e loop gráfico principal (1280x720 @ 60fps)
├── requirements.txt    # Dependências do projeto
├── .env.example        # Modelo de variáveis de ambiente
└── .gitignore          # Regras de exclusão Git otimizadas
```

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
* **Python 3.11** ou superior instalado ([python.org](https://www.python.org/)).
* **Git** instalado no sistema.
* Uma chave de API do **Google Gemini** ([obtenha gratuitamente no Google AI Studio](https://aistudio.google.com/)).

### 2. Clonando o Repositório
```bash
git clone https://github.com/iagobelloo/RPGMesaPY.git
cd RPGMesaPY
```

### 3. Configurando o Ambiente Virtual
```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar no Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Ou no Windows (CMD):
.venv\Scripts\activate.bat
# Ou no Linux/macOS:
source .venv/bin/activate
```

### 4. Instalando as Dependências
```bash
pip install -r requirements.txt
```

### 5. Configurando a Chave de API
Copie o arquivo `.env.example` para `.env`:
```bash
# No Windows PowerShell:
Copy-Item .env.example .env
```
Abra o arquivo `.env` e insira sua chave:
```env
GEMINI_API_KEY=sua_chave_do_google_gemini_aqui
GEMINI_MODEL=gemini-3.5-flash-lite
```

### 6. Iniciando o Jogo
```bash
python main.py
```

---

## 🎮 Controles e Atalhos

| Comando / Tecla | Ação |
| :--- | :--- |
| **`Enter`** | Envia a mensagem/ação digitada na caixa de texto para o Mestre (IA). |
| **`Tab`** | Abre ou fecha o **Grimório do Aventureiro** (Ficha completa de atributos, magias e perícias). |
| **`Esc`** | Fecha modais abertos ou abre o **Menu de Pausa** (Salvar/Sair). |
| **Clique no Inimigo** | Seleciona o alvo tático no tabuleiro (com retículo e destaque visual no card). |
| **Clique no Herói** | Abre a ficha rápida do herói para inspeção de PV, CA e bônus. |
| **`Atacar` (Action Bar)** | Executa o golpe físico ou conjurado contra o alvo atualmente selecionado. |
| **`Esquivar` (Action Bar)** | Assume postura defensiva, impondo desvantagem aos ataques inimigos até o próximo turno. |
| **`Recuar` (Action Bar)** | Executa manobra de recuo seguro sem provocar ataques de oportunidade. |
| **`Habilidade / Magia`** | Abre o menu de habilidades ativas e magias/truques canônicos do D&D 5e. |
| **`Mochila` / `Grimório`** | Acesso direto ao inventário com limite de carga e ao grimório de feitiços. |

---

## 🧪 Suíte de Testes Automatizados

O projeto conta com ampla cobertura de testes cobrindo o backend de combate, inventário, sanitização de prompts da IA e regras do sistema.

Para rodar todos os testes:
```bash
python -m pytest
```

Para rodar uma suíte específica:
```bash
python -m pytest tests/test_combat_system.py
```

---

## 🤖 Metodologia & Autoria: AI-Driven Development

Este repositório documenta um caso prático e extensivo de **Desenvolvimento de Software Guiado por Inteligência Artificial** (*Prompt-Driven Development / Vibe Coding*):

* **Direção, Especificação e Comando:** [@iagobelloo](https://github.com/iagobelloo)  
  * Atuação como *Product Owner* e *Game Designer*.
  * Definição de visão estética, regras canônicas de D&D 5e e persona de Maelor.
  * Engenharia de prompts e validação dos sistemas implementados.
* **Execução, Arquitetura e Código:** **Inteligência Artificial (Google Antigravity / Gemini)**  
  * Criação e implementação autônoma de 100% da base de código em Python/Pygame.
  * Arquitetura em camadas (MVC estrito: Engine, UI, AI Master).
  * Construção das suítes de testes unitários e de integração (`tests/`).
  * Geração e padronização das bases de dados JSON (`data/`) e documentações técnicas (`docs/`).

---

## 📄 Licença

Este projeto está licenciado sob os termos da licença [MIT](LICENSE).

---

*Desenvolvido com dedicação às noites de RPG de mesa e à literatura Dark Fantasy.*
