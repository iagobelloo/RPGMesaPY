# ⚔️ RPGMesaPY — D&D 5e VTT com IA Game Master

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5%2B-green.svg?logo=python)](https://pyga.me/)
[![Google Gemini API](https://img.shields.io/badge/Google_Gemini-2.5_Flash-orange.svg?logo=google)](https://ai.google.dev/)
[![D&D 5e Ruleset](https://img.shields.io/badge/Ruleset-D%26D_5e_SRD-red.svg)](https://dnd.wizards.com/)
[![Tests](https://img.shields.io/badge/Tests-Pytest_Passing-brightgreen.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

O **RPGMesaPY** é uma plataforma **VTT (Virtual Tabletop) 2D** desenvolvida em Python e Pygame, projetada para proporcionar uma experiência imersiva de RPG de mesa solo ou guiado, ambientada em um universo de **Grounded Dark Fantasy (Grimdark Tático)**.

O diferencial central do projeto é a integração profunda de um **Motor de Regras D&D 5e autêntico** com um **Game Master impulsionado por Inteligência Artificial (Google Gemini API)**, batizado de **Maelor das Cordas de Cinza**.

---

## 🎭 O Mestre da Masmorra: Maelor das Cordas de Cinza

> *"O aço não mente sob a chuva fria. O Tirano queima vilas, mas são as escolhas de um único viajante que decidem se as cinzas se levantarão ou se espalharão pelo vento."*

Maelor não é um assistente genérico: ele é um bardo e cronista taciturno sentado ao canto da fogueira, dedilhando um alaúde cujas cordas foram trançadas com tendões de wyrm.
* **Prosa dos Cinco Sentidos:** Descrições ricas em cheiro de fuligem, o tinir surdo do ferro, o gosto amargo do sangue e o vento cortante.
* **Respeito à Matemática do D&D:** Maelor nunca inventa números; ele recebe o resultado das rolagens do motor físico (D20 + Modificadores vs CA/CD) e traduz o resultado em narrativa tática (*Fail Forward*).
* **Narrativa Consequente:** Suas escolhas, descanso, inventário e ferimentos impactam diretamente a atitude dos NPCs e o rumo dos capítulos (*Beats 1 a 15*).

---

## ✨ Funcionalidades Principais

* **⚔️ Motor de Regras D&D 5e Completo:**
  * Criação de personagem com raças canônicas (*Humano, Anão da Colina, Elfo da Floresta, Draconato, Meio-Orc, Halfling, Tiefling*) e classes clássicas (*Guerreiro, Clérigo, Paladino, Mago, Patrulheiro, Ladino*).
  * Atributos (*FOR, DES, CON, INT, SAB, CAR*), cálculo automático de modificadores, bônus de proficiência e Classe de Armadura (CA).
  * Sistema de combate bilateral por turnos com iniciativa, dano, tipos de armas e magias.
* **🧠 Inteligência Artificial Generativa (Gemini 2.5):**
  * Respostas contextuais rápidas em JSON estruturado com validação de esquema.
  * Prólogo personalizado e reativo à raça, classe e antecedente escolhidos.
  * Diálogos dinâmicos com NPCs e geração de consequências de combate em tempo real.
* **📜 Interface Gráfica Imersiva (Pygame):**
  * **Grimório do Aventureiro (`Tab`):** Ficha interativa completa com atributos, perícias, magias conhecidas e diário de missões.
  * **Mochila do Aventureiro:** Gerenciamento visual de inventário com capacidade de carga baseada em Força (limite em kg), equipamento de armas em um clique e uso de consumíveis.
  * **Tabuleiro Tático 2D:** Visualização de tokens de heróis e monstros em campo, com hitboxes clicáveis para ações rápidas.
  * **Dado d20 Animado:** Feedback visual dinâmico com animação de rolagem de dados durante o processamento da IA.
* **💾 Sistema Multi-Saves:**
  * 3 slots independentes de salvamento com serialização segura em JSON e tela de seleção dedicada.
* **📚 Bestiário & Compêndio SRD:**
  * Monstros, itens, magias e antecedentes catalogados em bases de dados JSON estruturadas.

---

## 🏛️ Arquitetura do Projeto (MVC Estrito)

O projeto adota uma separação rigorosa entre camadas:

```text
RPGMesaPY/
├── ai_master/          # Cérebro de IA: Integração LLM (Gemini) e persona de Maelor
├── assets/             # Recursos audiovisuais (sprites, retratos, cenários, UI)
│   ├── backgrounds/    # Cenários de vilas, cavernas, tavernas e masmorras
│   ├── sprites/        # Tokens de heróis e monstros D&D
│   └── ui/             # Texturas de pergaminho, botões e frames do dado d20
├── core/               # Model/Controller: Regras D&D 5e, Combate, Inventário e Saves
│   ├── combat_system.py # Resolução de iniciativa, ataques e dano
│   ├── dice_engine.py   # Rolagem de dados criptograficamente robusta
│   ├── dnd_rules.py     # Tabelas D&D 5e oficiais (SRD)
│   ├── game_engine.py   # Gerenciador de sessão e estado da partida
│   └── magic_system.py  # Espaços de magia e efeitos arcanos/divinos
├── data/               # Bases de dados JSON (itens, magias, monstros, quests)
├── docs/               # Diretrizes canônicas, bíblia do motor e relatórios
├── logs/               # Registros de log de execução (preservado via .gitkeep)
├── saves/              # Armazenamento local de partidas (preservado via .gitkeep)
├── scripts/            # Scripts utilitários e importadores SRD
├── tests/              # Suíte completa de testes automatizados com Pytest
├── ui/                 # View: Renderização gráfica Pygame pura
│   ├── asset_manager.py # Cache e carregamento otimizado de imagens/fontes
│   ├── hud_components.py# Modais (Grimório, Mochila, ChatBox, QuickActions)
│   ├── menu_components.py # Menus de Pausa, Criação de Personagem e Saves
│   └── scene_renderer.py# Renderização do tabuleiro e balões de diálogo
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
* Uma chave de API gratuita do **Google Gemini** ([obtenha em ai.google.dev](https://aistudio.google.com/)).

### 2. Clonando o Repositório
```bash
git clone https://github.com/SEU_USUARIO/RPGMesaPY.git
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
Copie o arquivo [.env.example](file:///c:/Users/iagob/RPGMesaPY/.env.example) para `.env`:
```bash
# No Windows PowerShell:
Copy-Item .env.example .env
```
Abra o arquivo `.env` e insira sua chave:
```env
GEMINI_API_KEY=sua_chave_do_google_gemini_aqui
GEMINI_MODEL=gemini-2.5-flash
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
| **`Tab`** | Abre ou fecha o **Grimório do Aventureiro** (Ficha completa). |
| **`Esc`** | Fecha modais abertos ou abre o **Menu de Pausa** (Salvar/Sair). |
| **Clique no Inimigo** | Executa um ataque direto contra o alvo clicado no tabuleiro. |
| **Clique no Herói** | Abre o Grimório do Herói para inspeção rápida. |
| **Quick Action Bar** | Botões na base da tela para `Atacar`, `Mochila`, `Grimório`, `Observar`, `Conversar` e `Descansar`. |

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

## 📄 Licença

Este projeto está licenciado sob os termos da licença [MIT](LICENSE).

---

*Desenvolvido com dedicação às noites de RPG de mesa e à literatura Dark Fantasy.*
