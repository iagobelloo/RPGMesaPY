# Manual Canônico de Direção de Arte e Iconografia: Árvore de Habilidades (D&D 5e)

**Projeto:** RPGMesaPY (VTT 2D Dark Fantasy Tactical)  
**Estilo Canônico:** 32-bit HD Dark Fantasy Pixel Art (Inspirações: *Tactics Ogre: Reborn*, *Diablo II: Resurrected*, *Blasphemous*, *Castlevania: Symphony of the Night*)  
**Finalidade:** Guia mestre de iconografia e engenharia de prompts (Midjourney v6, SDXL, Flux.1, PixelLab) e especificações procedurais para a Árvore de Habilidades das 6 Classes (24 Habilidades, 4 Tiers por classe).

---

## 1. O Padrão Visual Canônico dos Ícones de Habilidade

Todas as 24 habilidades devem respeitar rigorosamente a seguinte anatomia visual para integração na interface do Grimório Aberto (`GrimoireModal`):

### 1.1 Resolução e Proporção
- **Canvas Canônico:** Quadrado perfeito de **32x32 pixels** ou **40x40 pixels**.
- **Resolução de Renderização para IA:** 512x512 pixels (proporção 1:1, `--ar 1:1`), downscaled com interpolação *Nearest-Neighbor* no motor Pygame.
- **Isolamento de Fundo:** Fundo escuro sólido puro (`#111215` / `#16171a`) para contraste máximo dos glifos luminosos e borda metálica.

### 1.2 Moldura Chanfrada Metálica (Beveled Frame)
Cada ícone possui uma moldura ornamental de metal forjado que ancora o estilo tático clássico:
- **Camada Externa (Borda Chanfrada):** Bronze oxidado com cantos recortados a 45 graus (estilo *dungeon crawler*).
  - Luz de Borda (Top-Left): Ouro envelhecido (`#cda869` / `#d4af37`).
  - Meio-Tom: Bronze martelado (`#8b6f47` / `#735738`).
  - Sombra de Borda (Bottom-Right): Ferro fundido escuro (`#2d251e` / `#1f1a15`).
- **Gemas e Rebites de Canto:** Em Tiers superiores (Tier 3 e Tier 4), pequenos rebites de ferro ou minúsculos fragmentos de rubi/safira adornam os 4 vértices do chanfro.

### 1.3 Estados Visuais dos Ícones na Interface
1. **Bloqueada (Locked / Indisponível):**
   - Paleta 100% monocromática desaturada (tons de ardósia e cinza-chumbo `#3a3f47`, `#23272d`).
   - Glifo translúcido (opacidade 40%).
   - Cadeado ou correntes de ferro forjado sobrepostos no centro (`#4b4f56`).
2. **Disponível para Desbloqueio (Unlockable):**
   - Glifo em tom âmbar suave (`#f59e0b` / `#fbbf24`).
   - Contorno dourado sutil com pulsação de luz no chanfro (efeito *breathing glow* a cada 1.5s).
3. **Adquirida / Pronta para Uso (Active / Ready):**
   - Cores plenas de alto contraste vibrante contra o fundo carvão.
   - Borda chanfrada dourada sólida com brilho especular nos vértices.
   - Partículas e runas arcanas/marciais ativas no centro do glifo.
4. **Em Recarga / Esgotada (Cooldown / Expended):**
   - Véu escuro translúcido com gradiente de ponteiro radial (estilo relógio de sombra).
   - Runa esmaecida aguardando descanso curto ou longo.

### 1.4 Negative Prompt Universal Obrigatório
> `smooth digital painting, 3d render, cgi, vector art, flat modern minimalism, neon plastic, anime, cartoon, chibi, blurry, smooth gradients, photograph, realistic face, text, logo, watermark, modern UI buttons, rounded iOS corners`

---

## 2. Paletas de Cores por Classe e Simbologia

| Classe | Cor Temática Principal | Cor de Destaque / Luz | Cor de Sombra / Fundo | Elementos Simbólicos |
|---|---|---|---|---|
| **Guerreiro** | Vermelho Carmesim Forjado (`#991b1b`) | Aço Polido & Fogo (`#f97316`, `#e2e8f0`) | Carvão & Cinzas (`#1c1917`) | Aço, escudos rachados, punho cerrado, elmo |
| **Clérigo** | Dourado Sacro (`#eab308`) | Branco Puro Radiante (`#fef08a`, `#ffffff`) | Bronze Sagrado (`#451a03`) | Cálice, sol heráldico, asas de luz, cruz solar |
| **Mago** | Azul Safira Etéreo (`#2563eb`) | Ciano Rúnico & Violeta (`#38bdf8`, `#c084fc`) | Obsidiana Arcana (`#0f172a`) | Tomo aberto, olho místico, constelações, chamas |
| **Paladino** | Ouro Divino & Âmbar (`#d97706`) | Luz Solar Purificadora (`#fde047`, `#f8fafc`) | Ferro Sagrado Escuro (`#312e81`) | Espada em chamas celestes, halo, couraça, escudo |
| **Patrulheiro** | Verde Floresta Musgo (`#15803d`) | Prata Lunar & Folha Élfica (`#4ade80`, `#94a3b8`) | Terra Úmida & Casca (`#14532d`) | Flecha em voo, garra de fera, olho de falcão, raízes |
| **Ladino** | Roxo das Sombras (`#581c87`) | Prata Fosca & Sangue Frio (`#a855f7`, `#b91c1c`) | Escuridão Absoluta (`#09090b`) | Adaga envenenada, máscara de ferro, corvo, olho na bruma |

---

## 3. Especificações e Prompts das 24 Habilidades

---

### CLASSE 1: GUERREIRO (FÚRIA MARCIAL & RESILIÊNCIA)

#### [WAR-01] Retomar o Fôlego (*Second Wind*)
- **Tier:** 1 (Nível 1) | **Tipo:** Ação Bônus (1x por descanso)
- **Efeito:** Recupera `1d10 + Nível` PV com vigor e dentes cerrados.
- **Simbologia do Glifo:** Um coração de ferro envolto por correntes arrebentando-se, emitindo vapor vermelho escuro; ou uma mão enluvada em manopla de aço erguendo-se com determinação inabalável.
- **Paleta Hex:** Ouro da Borda (`#cda869`), Vermelho Vigor (`#dc2626`), Aço Manopla (`#cbd5e1`), Sombra Fundo (`#18181b`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Second Wind warrior ability, heavy iron-plated gauntlet clenching tightly while radiating crimson steam and glowing embers, battered steel with metallic dithered highlights, dark fantasy tactical RPG style, sharp square icon format with beveled tarnished bronze and antique gold border, solid dark slate background, crisp pixel clusters, ordered dithering, Blasphemous and Diablo II UI aesthetic --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 32-bit pixel art UI skill icon, Second Wind warrior ability, armored clenched fist releasing red steam, battle damage, dark fantasy, beveled antique bronze square border, crisp pixels, ordered dithering, isolated on dark background
```

---

#### [WAR-02] Surto de Ação (*Action Surge*)
- **Tier:** 2 (Nível 2) | **Tipo:** Ação Especial (1x por combate)
- **Efeito:** Concede 1 ação de ataque adicional imediatamente no mesmo turno.
- **Simbologia do Glifo:** Duas lâminas de espada cruzadas em velocidade frenética, com rastros duplos de faíscas laranjas incandescentes e silhueta de corte em arco.
- **Paleta Hex:** Borda Bronze (`#b45309`), Fagulha Laranja (`#ff7a00`), Lâmina Aço (`#f1f5f9`), Fundo Carvão (`#0c0a09`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Action Surge fighter ability, two broadswords crossing with blistering speed leaving double glowing fiery orange speed arcs and sparks, tactical RPG dark fantasy interface, square icon with beveled weathered bronze and gold frame, crisp pixel edges, dramatic chiaroscuro dithering, Tactics Ogre Reborn style, solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art icon, Action Surge skill, twin crossing broadswords with blazing kinetic trail, orange sparks, dark fantasy 32-bit style, square beveled metallic frame, sharp pixel clusters, dark background
```

---

#### [WAR-03] Foco do Campeão (*Champion's Focus*)
- **Tier:** 3 (Nível 3) | **Tipo:** Passiva
- **Efeito:** Acerto Crítico com rolagem 19 ou 20 no d20.
- **Simbologia do Glifo:** Um elmo de aço de cavaleiro com visor estreito do qual emana um brilho vermelho rubi concentrado, com a silhueta de uma lâmina perfurando o centro de um alvo de ferro trincado.
- **Paleta Hex:** Ouro Nobre (`#eab308`), Vermelho Rubí Crítico (`#ef4444`), Aço Temperado (`#94a3b8`), Fundo Escuro (`#111827`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Champion's Focus warrior passive, steel knight helm with glowing piercing crimson eyes through narrow visor, cracked bullseye target behind it, dark fantasy aesthetic, square icon with ornate beveled bronze and studded gold frame, crisp handcrafted pixels, ordered dithering, high contrast, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art skill icon, Champion's Focus ability, close-up knight helmet with glowing crimson visor slit, precision target symbol, dark fantasy RPG UI, beveled bronze frame, sharp pixel art, dark backdrop
```

---

#### [WAR-04] Ataque Extra (*Extra Attack*)
- **Tier:** 4 (Nível 5) | **Tipo:** Passiva
- **Efeito:** Desfere 2 ataques por turno ao usar a ação Atacar.
- **Simbologia do Glifo:** Uma espada montante descendo em golpe devastador que se desdobra em imagem-fantasma de uma segunda lâmina cortando no sentido oposto, estilhaçando pedras e armaduras.
- **Paleta Hex:** Ouro Brilhante (`#f59e0b`), Aço Cortante (`#ffffff`), Sangue de Batalha (`#7f1d1d`), Fundo Sombrio (`#09090b`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Extra Attack master warrior passive, giant greatsword cleaving downwards with an echoing spectral second blade slashing horizontally, shattering sparks and debris, dark fantasy tactical RPG icon, square ornate beveled antique bronze and gold border with corner rivets, crisp pixel outlines, chiaroscuro shading, isolated on black --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece pixel art UI icon, Extra Attack warrior passive, double greatsword cleave with afterimage ghost blade, kinetic impact, 32-bit dark fantasy, square ornate bronze frame, crisp pixels, solid dark background
```

---

### CLASSE 2: CLÉRIGO (LUZ DIVINA & CURA SACRA)

#### [CLR-01] Bênção da Cura (*Healing Blessing*)
- **Tier:** 1 (Nível 1) | **Tipo:** Passiva
- **Efeito:** Suas magias de cura concedem `+2 + Nível da Magia` PV adicionais.
- **Simbologia do Glifo:** Um cálice de ouro sacro transbordando um líquido luminoso branco-dourado que verte gotas em forma de cruzes solares.
- **Paleta Hex:** Ouro Sacro (`#facc15`), Luz Branca Divina (`#ffffff`), Bronze Cálice (`#78350f`), Fundo Carmesim Velado (`#261510`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Healing Blessing cleric ability, ornate golden holy chalice overflowing with luminous divine white-gold liquid and radiant sun motes, dark fantasy tactical RPG style, square icon with beveled tarnished bronze and holy gold frame, high contrast, clean pixel dithering, Castlevania and Tactics Ogre UI aesthetic, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art UI icon, Healing Blessing cleric spell, glowing holy chalice with radiant healing elixir and sun particles, dark fantasy, beveled bronze border, clean pixel art clusters, dark backdrop
```

---

#### [CLR-02] Preservar a Vida (*Preserve Life*)
- **Tier:** 2 (Nível 2) | **Tipo:** Canalizar Divindade (1x por descanso)
- **Efeito:** Emite uma onda de luz que restaura `5 x Nível` PV instantaneamente.
- **Simbologia do Glifo:** Duas mãos abertas erguidas para os céus canalizando uma explosão circular de raios de sol radiantes que quebram espinhos sombrios ao redor.
- **Paleta Hex:** Âmbar Radiante (`#fbbf24`), Branco Celestial (`#fef9c3`), Ouro Borda (`#b45309`), Fundo Sombra (`#1c1917`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Preserve Life cleric channel divinity, two cupped priest hands releasing a bursting halo of divine solar rays banishing creeping black thorns, sacred dark fantasy, square icon with beveled antique gold and bronze border, crisp pixel clusters, dramatic lighting, Blasphemous UI style, solid dark slate background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art skill icon, Channel Divinity Preserve Life, holy hands radiating bursting sunbeams, healing aura, dark fantasy 32-bit RPG, square ornate bronze frame, sharp pixel dithering, dark background
```

---

#### [CLR-03] Escudo da Fé (*Shield of Faith*)
- **Tier:** 3 (Nível 3) | **Tipo:** Passiva
- **Efeito:** Concede +2 permanente na CA enquanto empunhar um símbolo sagrado ou escudo.
- **Simbologia do Glifo:** Um escudo pesado em forma de gota esculpido com um sol heráldico de oito pontas, envolto por uma aura translúcida de luz sagrada impenetrável.
- **Paleta Hex:** Ouro Heráldico (`#eab308`), Azul Safira Sagrado (`#1d4ed8`), Aço Escudo (`#e2e8f0`), Fundo Escuro (`#0f172a`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Shield of Faith cleric passive, kite shield emblazoned with an eight-pointed radiant sun emblem glowing with an impenetrable translucent holy aura, dark fantasy RPG, square icon framed in beveled weathered bronze and polished gold, crisp pixel outlines, ordered dithering, solid pure dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art skill icon, Shield of Faith cleric passive, divine holy kite shield with glowing golden sun crest, sacred defensive aura, dark fantasy 32-bit, square bronze beveled frame, crisp pixels, dark background
```

---

#### [CLR-04] Fogo Radiante (*Radiant Fire*)
- **Tier:** 4 (Nível 5) | **Tipo:** Passiva
- **Efeito:** Adiciona `+1d8` de dano radiante a ataques e magias de luz.
- **Simbologia do Glifo:** Uma maça de guerra sagrada envolta em labaredas brancas e douradas incandescentes, expelindo fagulhas solares que calcinam as sombras.
- **Paleta Hex:** Fogo Branco-Dourado (`#fef08a`), Fogo Âmbar (`#f97316`), Bronze Maça (`#92400e`), Fundo Obscuro (`#1a0f0a`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Radiant Fire cleric passive, heavy iron war mace engulfed in blazing white-hot solar flames and golden holy sparks, dark fantasy tactical RPG icon, square shape with beveled tarnished bronze frame studded with sacred amber gems, crisp pixel clusters, dramatic chiaroscuro, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece pixel art icon, Radiant Fire cleric ability, flanged war mace burning with divine golden flame and holy embers, dark fantasy 32-bit RPG UI, square beveled frame, sharp pixel art, dark background
```

---

### CLASSE 3: MAGO (CONJURADOR ELEMENTAL & ARCANO)

#### [WIZ-01] Recuperação Arcana (*Arcane Recovery*)
- **Tier:** 1 (Nível 1) | **Tipo:** Passiva
- **Efeito:** Restaura 1 espaço de magia de 1º círculo após um descanso.
- **Simbologia do Glifo:** Um grimório aberto com páginas gastas e folhas levitando, de onde brota uma espiral de runas em ciano etéreo e fumaça mística violeta.
- **Paleta Hex:** Ciano Arcano (`#38bdf8`), Violeta Místico (`#a855f7`), Couro Grimório (`#581c87`), Fundo Escuro (`#030712`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Arcane Recovery wizard passive, ancient leather-bound grimoire open with levitating parchment pages emitting a spiraling helix of glowing cyan runes and purple mist, dark fantasy RPG, square icon with beveled antique bronze and runic silver frame, crisp pixel edges, subtle dithering, Tactics Ogre UI, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art skill icon, Arcane Recovery wizard ability, open spellbook radiating ethereal cyan runic spiral and mana energy, dark fantasy 32-bit, square beveled frame, handcrafted pixel clusters, dark backdrop
```

---

#### [WIZ-02] Evocação Potente (*Potent Evocation*)
- **Tier:** 2 (Nível 2) | **Tipo:** Passiva
- **Efeito:** Suas magias que causam dano adicionam o modificador de Inteligência ao dano total.
- **Simbologia do Glifo:** Uma esfera de energia bruta condensada partindo-se em três elementos primordiais: relâmpago azul, fogo carmesim e gelo esmeralda, canalizados pela ponta de uma varinha rúnica.
- **Paleta Hex:** Azul Relâmpago (`#3b82f6`), Carmesim Fogo (`#ef4444`), Ciano Gelo (`#06b6d4`), Fundo Vácuo (`#0f172a`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Potent Evocation wizard passive, crackling orb of raw primal magic splitting into surging blue lightning, crimson flame, and crystal frost shards, dark fantasy tactical RPG style, square icon with beveled dark bronze and enchanted gold border, crisp pixels, ordered dithering, solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art icon, Potent Evocation spell mastery, concentrated elemental magic orb crackling with fire and lightning, dark fantasy RPG UI, square beveled metallic frame, sharp pixel art, dark background
```

---

#### [WIZ-03] Escudo Arcano (*Shield*)
- **Tier:** 3 (Nível 3) | **Tipo:** Reação (1x por combate)
- **Efeito:** Barreira de energia concedendo +5 na CA contra o próximo ataque.
- **Simbologia do Glifo:** Um hexágono translúcido de puro cristal de força mágica ciano repelindo a ponta de uma flecha ou lâmina que se estilhaça em fagulhas arcanas.
- **Paleta Hex:** Ciano Força (`#22d3ee`), Azul Cobalto (`#1e40af`), Branco Impacto (`#ffffff`), Fundo Carvão (`#09090b`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Shield spell wizard reaction, glowing translucent cyan geometric hexagonal force barrier deflecting an incoming jagged iron arrow into shattering sparks, dark fantasy, square icon with beveled tarnished bronze frame with corner runic glyphs, crisp pixel clusters, high contrast dithering, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art skill icon, Shield spell wizard ability, crystalline hexagonal force shield blocking an attack, glowing cyan runes, dark fantasy 32-bit RPG, square ornate bronze border, sharp pixels, dark background
```

---

#### [WIZ-04] Mestre dos Elementos (*Elemental Master*)
- **Tier:** 4 (Nível 5) | **Tipo:** Passiva
- **Efeito:** Aumenta em +1 a CD de resistência de todas as suas magias.
- **Simbologia do Glifo:** Um olho místico aberto no centro de um triângulo alquímico de fogo, gelo e éter, com runas antigas orbitando a pupila incandescente.
- **Paleta Hex:** Ouro Alquímico (`#f59e0b`), Roxo Éter (`#8b5cf6`), Fogo Alaranjado (`#ea580c`), Fundo Ébano (`#020617`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Elemental Master wizard passive, all-seeing mystical arcane eye inside an alchemical triquetra of orbiting elemental fire, frost, and purple ether runes, dark fantasy RPG, square icon framed in beveled antique gold and bronze with corner rivets, crisp pixel outlines, dramatic chiaroscuro, solid pure dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece pixel art UI icon, Elemental Master wizard archmage passive, mystical arcane eye with orbiting elemental glyphs, dark fantasy 32-bit style, square ornate bronze and gold frame, crisp pixel art, dark backdrop
```

---

### CLASSE 4: PALADINO (VINGADOR SAGRADO & VIRTUDE)

#### [PAL-01] Cura pelas Mãos (*Lay on Hands*)
- **Tier:** 1 (Nível 1) | **Tipo:** Ação (1x por descanso)
- **Efeito:** Toca a si mesmo restaurando `5 x Nível` PV com calor divino.
- **Simbologia do Glifo:** Uma manopla de aço polido pousando suavemente sobre um peito ferido, irradiando ondas concêntricas de luz dourada quente que sela o aço trincado.
- **Paleta Hex:** Ouro Quente (`#f59e0b`), Aço Manopla (`#e2e8f0`), Branco Luz (`#fffbeb`), Fundo Sombra (`#1e1b4b`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Lay on Hands paladin ability, polished steel knight gauntlet resting on a cracked chestplate emitting soothing radiant golden light waves that heal the metal, sacred dark fantasy, square icon with beveled tarnished bronze and holy gold frame, crisp pixel edges, ordered dithering, Blasphemous UI style, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art skill icon, Lay on Hands paladin ability, armored hand glowing with warm golden divine healing light, dark fantasy 32-bit RPG, square beveled bronze frame, sharp pixel dithering, dark background
```

---

#### [PAL-02] Destruição Divina (*Divine Smite*)
- **Tier:** 2 (Nível 2) | **Tipo:** Gasto de Espaço de Magia
- **Efeito:** Infunde a lâmina causando `+2d8` de dano radiante no acerto.
- **Simbologia do Glifo:** Uma espada longa medieval de ponta para baixo, cuja lâmina inteira está envolta em uma explosão de chamas celestes douradas e raios solares ofuscantes.
- **Paleta Hex:** Amarelo Solar (`#fde047`), Ouro Vingador (`#d97706`), Aço Lâmina (`#ffffff`), Fundo Noturno (`#0f172a`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Divine Smite paladin ability, holy longsword pointing downwards erupting in a blinding explosion of celestial golden flames and radiant lightning bolts, dark fantasy tactical RPG interface, square icon with beveled heavy bronze and gold border, high contrast pixel art, Tactics Ogre aesthetic, solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art icon, Divine Smite paladin skill, broadsword engulfed in exploding holy gold sunlight and radiant electricity, dark fantasy 32-bit RPG, square ornate bronze frame, crisp pixels, dark background
```

---

#### [PAL-03] Aura de Coragem (*Aura of Courage*)
- **Tier:** 3 (Nível 3) | **Tipo:** Passiva
- **Efeito:** Imunidade à condição Amedrontado e +1 em todos os Testes de Resistência.
- **Simbologia do Glifo:** Um halo radiante em forma de coroa solar sobre um coração de leão heráldico gravado em uma placa de bronze reluzente.
- **Paleta Hex:** Ouro Coroa (`#facc15`), Âmbar Nobre (`#b45309`), Vermelho Real (`#991b1b`), Fundo Carmim Escuro (`#1f1315`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Aura of Courage paladin passive, radiant sun halo crown hovering above an embossed golden lion crest on a shield, banishing shadows, dark fantasy RPG, square icon framed in beveled antique bronze and studded gold, crisp pixel clusters, dramatic lighting dithering, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art UI icon, Aura of Courage paladin passive, heraldic golden lion crest crowned with radiant sun halo, fearless aura, dark fantasy 32-bit, square beveled bronze frame, sharp pixel art, dark backdrop
```

---

#### [PAL-04] Golpe Abençoado Extra (*Blessed Extra Attack*)
- **Tier:** 4 (Nível 5) | **Tipo:** Passiva
- **Efeito:** Desfere 2 ataques por rodada imbuídos com o favor sagrado.
- **Simbologia do Glifo:** Duas espadas sagradas cruzadas descendo em arco simétrico, unindo chamas douradas e faíscas brancas em um julgamento final impiedoso.
- **Paleta Hex:** Ouro Sagrado (`#fbbf24`), Branco Celestial (`#ffffff`), Bronze Forjado (`#78350f`), Fundo Escuro (`#030712`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Blessed Extra Attack paladin passive, twin holy broadswords crossing downwards in righteous judgment leaving burning golden light trails and divine embers, dark fantasy tactical RPG icon, square ornate beveled antique bronze and gold border with corner gems, crisp pixel outlines, chiaroscuro shading, isolated on black --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece pixel art UI icon, Blessed Extra Attack paladin passive, twin crossing holy blades with golden light trails, dark fantasy 32-bit RPG style, square ornate bronze and gold frame, crisp pixel clusters, solid dark background
```

---

### CLASSE 5: PATRULHEIRO (CAÇADOR DOS ERMOS & PRECISÃO)

#### [RNG-01] Marca do Caçador (*Hunter's Mark*)
- **Tier:** 1 (Nível 1) | **Tipo:** Ação Bônus
- **Efeito:** Marca uma criatura; ataques contra ela causam `+1d6` de dano adicional.
- **Simbologia do Glifo:** Uma mira rúnica em formato de garras cruzadas com um olho de falcão verde esmeralda no centro, sobrepondo a silhueta da caveira de uma fera.
- **Paleta Hex:** Verde Esmeralda (`#10b981`), Prata Lunar (`#cbd5e1`), Musgo Escuro (`#064e3b`), Fundo Pântano (`#022c22`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Hunter's Mark ranger ability, glowing emerald green runic hunting crosshairs centering on a beast skull with piercing hawk eye, dark fantasy tactical RPG style, square icon with beveled weathered bronze and forest-green patina border, crisp pixel clusters, ordered dithering, Tactics Ogre UI, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art skill icon, Hunter's Mark ranger spell, mystical emerald green target reticle over animal skull silhouette, dark fantasy 32-bit RPG, square beveled bronze frame, sharp pixel art, dark backdrop
```

---

#### [RNG-02] Estilo Arquearia (*Archery Fighting Style*)
- **Tier:** 2 (Nível 2) | **Tipo:** Passiva
- **Efeito:** +2 de bônus em todas as jogadas de ataque com armas a distância.
- **Simbologia do Glifo:** Um arco recurvo de madeira nobre e tendão tensionado ao limite, com uma flecha de ponta de ferro farpada perfeitamente alinhada e pronta para o disparo.
- **Paleta Hex:** Madeira Nobre (`#92400e`), Aço Ponta Flecha (`#e2e8f0`), Verde Musgo (`#15803d`), Fundo Noturno (`#0f172a`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Archery Style ranger passive, recurve wooden longbow pulled to maximum tension with razor-sharp barbed iron arrowhead ready to fire, dark fantasy RPG, square icon framed in beveled antique bronze and brass, crisp handcrafted pixels, subtle speed line dithering, solid pure dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art icon, Archery Fighting Style passive, taut wooden longbow with notched barbed arrow, precision aim, dark fantasy 32-bit RPG UI, square beveled bronze frame, sharp pixel clusters, dark background
```

---

#### [RNG-03] Matador de Colossos (*Colossus Slayer*)
- **Tier:** 3 (Nível 3) | **Tipo:** Passiva
- **Efeito:** Causa `+1d8` de dano extra uma vez por turno se o alvo já estiver ferido.
- **Simbologia do Glifo:** Uma ponta de flecha de aço enegrecido trespassando a couraça de um gigante ou monstro descomunal, arrancando um jato de sangue carmesim estilizado em pixels.
- **Paleta Hex:** Vermelho Sangue (`#b91c1c`), Aço Negro (`#334155`), Ouro Borda (`#d97706`), Fundo Carvão (`#111827`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Colossus Slayer ranger passive, heavy black-iron broadhead arrow piercing deep through thick stone armor of a giant with bursting crimson blood droplets, dark fantasy, square icon with beveled weathered bronze and studded gold frame, crisp pixel outlines, dramatic chiaroscuro, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art skill icon, Colossus Slayer ranger ability, massive arrow penetrating armored giant hide with bursting crimson blood impact, dark fantasy 32-bit, square beveled frame, sharp pixel art, dark background
```

---

#### [RNG-04] Rajada de Flechas (*Arrow Volley*)
- **Tier:** 4 (Nível 5) | **Tipo:** Passiva
- **Efeito:** Permite disparar 2 flechas por rodada com cadência implacável.
- **Simbologia do Glifo:** Três flechas em voo rasante em formação cônica, cortando a névoa com rastros de vento e pontas cintilantes de aço frio.
- **Paleta Hex:** Prata Flechas (`#f8fafc`), Verde Vento (`#22c55e`), Bronze Forjado (`#78350f`), Fundo Bruma (`#022c22`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Arrow Volley master ranger passive, three barbed arrows flying in tight formation cutting through thick misty wind trails with silver glints, dark fantasy tactical RPG icon, square shape with beveled antique bronze and gold frame with corner rivets, crisp pixel clusters, high contrast dithering, isolated on black --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece pixel art UI icon, Arrow Volley ranger passive, multiple arrows piercing forward through wind mist, 32-bit dark fantasy RPG style, square ornate bronze and gold frame, crisp pixels, solid dark background
```

---

### CLASSE 6: LADINO (SOMBRA & LETALIDADE)

#### [ROG-01] Ataque Furtivo (*Sneak Attack*)
- **Tier:** 1 (Nível 1) | **Tipo:** Passiva
- **Efeito:** Causa `+1d6` de dano com arma de acuidade sob vantagem ou flanqueamento.
- **Simbologia do Glifo:** Uma adaga serrilhada de aço negro gotejando sangue escuro, surgindo de uma mortalha de névoa e fumaça roxa que oculta uma mão enluvada em couro.
- **Paleta Hex:** Roxo Sombra (`#7e22ce`), Vermelho Sangue (`#991b1b`), Aço Negro (`#1e293b`), Fundo Escuridão (`#09090b`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Sneak Attack rogue ability, black-steel serrated dagger dripping fresh crimson blood emerging silently from swirling purple shadow smoke, dark fantasy tactical RPG style, square icon with beveled tarnished bronze and dark iron border, crisp pixel edges, ordered dithering, Castlevania and Tactics Ogre aesthetic, solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art skill icon, Sneak Attack rogue ability, serrated dagger stabbing from dark purple mist with blood drop, dark fantasy 32-bit RPG, square beveled dark bronze frame, sharp pixel art, dark backdrop
```

---

#### [ROG-02] Ação Ardilosa (*Cunning Action*)
- **Tier:** 2 (Nível 2) | **Tipo:** Ação Bônus
- **Efeito:** Pode Desengajar, Disparar ou Esconder-se como ação bônus a cada turno.
- **Simbologia do Glifo:** Uma bota de couro leve pisando sem som sobre telhas ou pedras úmidas, deixando um rastro espectral de fumaça cinzenta que se dissipa na penumbra.
- **Paleta Hex:** Cinza Fumaça (`#94a3b8`), Couro Escuro (`#334155`), Violeta Penumbra (`#6b21a8`), Fundo Noite (`#020617`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Cunning Action rogue ability, hooded thief silhouette dashing silently across cobblestones leaving a smoky shadow afterimage trail, dark fantasy RPG, square icon framed in beveled weathered bronze and dark steel, crisp pixel clusters, dramatic lighting dithering, solid dark slate background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art icon, Cunning Action rogue skill, shadow dash motion blur silhouette with smoke puff, dark fantasy 32-bit RPG UI, square beveled bronze frame, sharp pixel clusters, dark background
```

---

#### [ROG-03] Emboscada Mortal (*Deadly Ambush*)
- **Tier:** 3 (Nível 3) | **Tipo:** Passiva
- **Efeito:** Dano do Ataque Furtivo sobe para `+2d6` e ignora armaduras leves.
- **Simbologia do Glifo:** Uma máscara de ferro de carrasco com olhos escuros e vazios, atravessada transversalmente pela silhueta de uma lâmina envenenada com brilho púrpura letal.
- **Paleta Hex:** Roxo Veneno (`#9333ea`), Verde Ácido (`#22c55e`), Ferro Frio (`#475569`), Fundo Obscuro (`#030712`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Deadly Ambush rogue passive, executioner iron mask with hollow glowing violet eyes pierced through by an envenomed stiletto dagger, dark fantasy, square icon with beveled dark bronze and studded gold frame, crisp pixel outlines, high contrast chiaroscuro, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art skill icon, Deadly Ambush rogue ability, venomous stiletto dagger slicing through dark mask in shadows, poison drip, dark fantasy 32-bit, square beveled frame, sharp pixel art, dark background
```

---

#### [ROG-04] Esquiva Sobrenatural (*Uncanny Dodge*)
- **Tier:** 4 (Nível 5) | **Tipo:** Reação
- **Efeito:** Reduz pela metade o dano recebido de um ataque direcionado.
- **Simbologia do Glifo:** A silhueta de uma capa de veludo rasgada pelo golpe de um machado colossal, enquanto o corpo do ladino se desvencilha como vapor intocado pelo aço.
- **Paleta Hex:** Prata Reflexo (`#e2e8f0`), Carmesim Capa (`#881337`), Preto Sombra (`#0f172a`), Fundo Vazio (`#020617`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art skill icon, Uncanny Dodge master rogue reaction, giant battleaxe cleaving only empty tattered cape and vaporous shadow while rogue dodges unharmed, dark fantasy tactical RPG icon, square ornate beveled antique bronze and gold border with corner rivets, crisp pixel clusters, dramatic speed line dithering, isolated on black --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece pixel art UI icon, Uncanny Dodge rogue reaction, enemy weapon slicing empty cloth and shadows, elusive evasion, 32-bit dark fantasy RPG style, square ornate bronze and gold frame, crisp pixels, solid dark background
```

---

## 4. Especificações de Renderização Procedural em Código (Fallback Pygame)

Caso as texturas em `.png` ainda não tenham sido geradas no pipeline ou o jogo opere em modo offline/fallback sem assets pesados, o motor de renderização da interface desenha os glifos procedurais com precisão geométrica em matrizes de 32x32 / 40x40:

### 4.1 Borda Chanfrada de Bronze (Algoritmo Geométrico)
```python
def draw_beveled_skill_frame(surface, rect, is_locked=False, is_selected=False):
    x, y, w, h = rect.x, rect.y, rect.width, rect.height
    
    # 1. Paleta de Metais
    if is_locked:
        c_outer = (58, 63, 71)    # Ardósia escurecida
        c_light = (90, 95, 105)   # Aço desaturado
        c_shadow = (31, 35, 41)   # Sombra chumbo
        c_bg = (17, 18, 21)       # Carvão profundo
    else:
        c_outer = (139, 111, 71)  # Bronze martelado base
        c_light = (205, 168, 105) if not is_selected else (245, 158, 11) # Ouro envelhecido ou Ouro ativo
        c_shadow = (45, 37, 30)   # Ferro oxidado escuro
        c_bg = (22, 23, 26)       # Fundo sólido escuro
    
    # Fundo escuro interno
    surface.fill(c_bg, rect)
    
    # Linhas de chanfro da moldura (espessura de 2 pixels)
    # Borda Superior e Esquerda (Luz)
    pygame.draw.line(surface, c_light, (x + 2, y), (x + w - 3, y), 2)
    pygame.draw.line(surface, c_light, (x, y + 2), (x, y + h - 3), 2)
    
    # Borda Inferior e Direita (Sombra)
    pygame.draw.line(surface, c_shadow, (x + 2, y + h - 2), (x + w - 3, y + h - 2), 2)
    pygame.draw.line(surface, c_shadow, (x + w - 2, y + 2), (x + w - 2, y + h - 3), 2)
    
    # Cantos chanfrados a 45 graus (2x2 pixels nos vértices)
    for corner in [(x, y), (x + w - 2, y), (x, y + h - 2), (x + w - 2, y + h - 2)]:
        pygame.draw.rect(surface, (12, 12, 14), (corner[0], corner[1], 2, 2))
```

### 4.2 Matrizes de Glifos Procedurais para as 6 Classes
1. **Guerreiro:** Cruz de ferro espessa (`rect` vertical + horizontal) com centro reforçado em carmesim (`#991b1b`).
2. **Clérigo:** Sol radiante circular (`circle` central com 4 raios em cruz e 4 em diagonal) em dourado (`#eab308`).
3. **Mago:** Triângulo equilátero rúnico invertido com ponto místico central em ciano (`#38bdf8`).
4. **Paladino:** Espada vertical com pomo e guarda em cruz de ouro (`#d97706`) emitindo faíscas brancas.
5. **Patrulheiro:** Flecha em diagonal ascendente com ponta farpada e pena em verde musgo (`#15803d`).
6. **Ladino:** Adaga em ângulo descendente com gume inclinado e rastro em violeta escuro (`#7e22ce`).

---

## 5. Diretrizes de Integração no Grimório Aberto

1. **Localização dos Arquivos de Arte:**  
   `assets/ui/skills/{class_name}_{tier}_{skill_id}.png`  
   Exemplo: `assets/ui/skills/warrior_t1_second_wind.png`, `assets/ui/skills/paladin_t2_divine_smite.png`.
2. **Tamanho na Interface:** 36x36 pixels com margem interna de 6 pixels e espaçamento entre tiers de 12 pixels.
3. **Tooltip Flutuante:** Ao pairar o mouse sobre o ícone, renderizar caixa com borda chanfrada de pergaminho escuro contendo:
   - Nome Canônico e Tier da Habilidade.
   - Custo de Ação / Recarga (ex: *Ação Bônus - 1x por descanso*).
   - Descrição Mecânica de D&D 5e e Flavor Text poético de Maelor das Cordas de Cinza.

---

## 6. Apêndice: Equipamentos Raciais Únicos & Spritesheet do Dado d20 Girando

### 6.1 Os 7 Itens Únicos Raciais (32x32 / 40x40 Pixel Art 32-bit)

1. **Humano — `Sinete da Coroa Partida` (`i_racial_human_signet`):**
   - **Prompt Midjourney v6:** `32-bit pixel art item icon, Signet of the Sundered Crown human racial heirloom, heavy tarnished imperial gold signet ring set with a flat black onyx stone engraved with a cracked royal crown emblem glowing with a faint ember fissure, dark fantasy tactical RPG inventory icon, square format with beveled antique bronze and gold border, crisp pixel clusters, ordered dithering, solid pure dark background --v 6.0 --ar 1:1 --stylize 250`
   - **Prompt SDXL:** `masterpiece 32-bit pixel art UI item icon, weathered gold signet ring with black onyx seal of a shattered crown, human racial relic, dark fantasy RPG, square beveled antique bronze frame, crisp pixel outlines, solid dark background`

2. **Elfo da Floresta — `Manto de Folhas Cinzentas` (`i_racial_elf_cloak`):**
   - **Prompt Midjourney v6:** `32-bit pixel art item icon, Cloak of Ashen Leaves wood elf racial heirloom, hooded elven travel cloak woven from ash-dusted silver-grey and deep emerald forest leaves fastened by a crescent moonstone silver leaf brooch, swirling woodland mist, dark fantasy tactical RPG icon, square format with beveled weathered bronze and gold frame, crisp handcrafted pixels, solid dark background --v 6.0 --ar 1:1 --stylize 250`
   - **Prompt SDXL:** `pixel art RPG item icon, elven cloak of grey ash leaves and emerald moss with silver leaf clasp, wood elf racial relic, dark fantasy 32-bit style, square beveled bronze border, sharp pixel clusters, dark backdrop`

3. **Anão da Colina — `Runa da Pedra-Forja` (`i_racial_dwarf_rune`):**
   - **Prompt Midjourney v6:** `32-bit pixel art item icon, Forge-Stone Rune hill dwarf racial heirloom, heavy octagonal carved basalt tablet bound in riveted iron bands, glowing in the center with an ancient dwarven master-smith rune pulsing with molten gold and magma heat, dark fantasy RPG inventory icon, square shape with beveled tarnished bronze and gold frame, crisp pixel edges, solid dark background --v 6.0 --ar 1:1 --stylize 250`
   - **Prompt SDXL:** `2.5D pixel art item icon, dwarven carved stone rune tablet glowing with molten forge fire and gold veins, hill dwarf racial heirloom, dark fantasy 32-bit RPG UI, square beveled bronze frame, sharp pixels, dark background`

4. **Halfling — `Moeda da Sorte Antiga` (`i_racial_halfling_coin`):**
   - **Prompt Midjourney v6:** `32-bit pixel art item icon, Ancient Lucky Coin halfling racial heirloom, antique hand-struck gold and electrum coin on a worn leather cord, embossed with a mystical wheel of fortune and four-leaf clover motif glinting with golden luck sparkles, dark fantasy tactical RPG icon, square format with beveled antique bronze and gold border, crisp pixel clusters, solid dark background --v 6.0 --ar 1:1 --stylize 250`
   - **Prompt SDXL:** `pixel art UI item icon, ancient minted gold lucky coin charm on leather string with sparkling golden glint, halfling racial relic, dark fantasy 32-bit, square beveled bronze frame, crisp pixel art, dark backdrop`

5. **Draconato — `Escama Ancestral Incandescente` (`i_racial_dragon_scale`):**
   - **Prompt Midjourney v6:** `32-bit pixel art item icon, Incandescent Ancestral Scale dragonborn racial heirloom, thick jagged ancient dragon scale of crimson and blackened obsidian pulsing with internal veins of glowing volcanic ember, mounted in dark bronze claws, dark fantasy tactical RPG icon, square format with beveled weathered bronze and gold frame, crisp pixel outlines, solid pure black background --v 6.0 --ar 1:1 --stylize 250`
   - **Prompt SDXL:** `masterpiece pixel art item icon, glowing red and obsidian dragon scale relic pulsing with molten veins, dragonborn racial heirloom, dark fantasy 32-bit RPG, square beveled bronze border, sharp pixels, dark background`

6. **Meio-Orc — `Presa de Ferro Sangrento` (`i_racial_orc_tusk`):**
   - **Prompt Midjourney v6:** `32-bit pixel art item icon, Blood-Iron Tusk half-orc racial heirloom, savage curved war-boar ivory tusk capped with jagged blackened iron and bound in leather thongs, etched with glowing crimson blood-runes of unyielding fury, dark fantasy tactical RPG icon, square format with beveled tarnished bronze and iron border, crisp pixel clusters, solid dark background --v 6.0 --ar 1:1 --stylize 250`
   - **Prompt SDXL:** `pixel art RPG item icon, brutal ivory tusk amulet tipped with spiked black iron and crimson tribal runes, half-orc racial relic, dark fantasy 32-bit style, square beveled frame, sharp pixel art, dark background`

7. **Tiefling — `Selo de Brasas Abissais` (`i_racial_tiefling_seal`):**
   - **Prompt Midjourney v6:** `32-bit pixel art item icon, Seal of Abyssal Embers tiefling racial heirloom, infernal dark stygian iron talisman shaped like curved demonic horns clasping a burning violet-crimson hellfire gem, wisp of sulfurous smoke and cinders, dark fantasy tactical RPG icon, square format with beveled antique bronze and gold border, crisp pixel edges, solid pure black background --v 6.0 --ar 1:1 --stylize 250`
   - **Prompt SDXL:** `masterpiece 32-bit pixel art item icon, horned infernal iron talisman with glowing hellfire ruby and purple brimstone smoke, tiefling racial relic, dark fantasy RPG, square beveled bronze frame, sharp pixels, dark background`

---

### 6.2 Spritesheet Canônico do Dado d20 Girando (12 Frames)
- **Especificação:** Icosaedro vermelho-rubi facetado (`#b91c1c` / `#dc2626`) com bordas de ouro velho (`#d4af37`) e números em pixel art 32-bit, 12 frames de rotação sobre fundo transparente/preto sólido, idêntico ao d20 da Ficha de Personagem.
- **Prompt Midjourney v6:**
```text
32-bit pixel art game animation spritesheet, 12 sequential frames arranged in a clean grid of a spinning 20-sided polyhedral icosahedron d20 die, faceted deep crimson ruby gemstone body with ornate antique gold metal edges and engraved golden numbers, rotating smoothly across 12 angles with subtle golden spark trails, final frame resting upright showing the number 20 glowing brightly, dark fantasy tabletop RPG UI asset, crisp pixel clusters, ordered dithering, no motion blur, isolated on solid pure black background --v 6.0 --ar 4:3 --stylize 200
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 32-bit pixel art animation spritesheet, 12 frames of a rotating 20-sided d20 icosahedron die, faceted blood-ruby crystal with antique gold wireframe ridges and pixel numbers, dark fantasy RPG dice roll animation, crisp pixel art edges, ordered dithering, isolated on solid black background
```

