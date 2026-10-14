# Manual Canônico de Prompts dos Protagonistas: 42 Arquétipos de Personagem do Jogador (7 Raças x 6 Classes)

**Projeto:** RPGMesaPY (D&D 5e VTT)  
**Finalidade:** Guia completo de prompts de geração de imagem (Midjourney v6, SDXL, Flux.1) para os **Avatares do Jogador / Protagonista**, selecionáveis na tela de Criação de Personagem.  
**Estilo Canônico:** 2.5D HD Pixel Art / 32-bit Tactical Dark Fantasy (Inspirações: *Tactics Ogre: Reborn*, *Blasphemous*, *Octopath Traveler*, *Diablo I & II*).

---

## 1. Diretriz de Diferenciação: Protagonistas vs Heróis Aliados

> [!IMPORTANT]
> **Diferença Crucial de Conceito:**
> - **Os 42 Heróis Aliados (`HERO-01` a `HERO-42`):** São NPCs específicos do mundo com nome próprio (Sir Alistair, Padre Lucien, etc.), biografias de perda pelo cataclismo, personalidades pré-moldadas e missões pessoais.
> - **Os 42 Arquétipos de Protagonistas (`PROT-01` a `PROT-42`):** São os avatares visuais para o **PERSONAGEM DO JOGADOR**. Eles **NÃO possuem nome fixo nem história pré-fabricada** (o jogador define seu nome e constrói seu passado no Prólogo/Antecedentes).
> - **Visual Totalmente Inédito e Distinto:** Nenhum protagonista deve se parecer com o aliado da mesma classe e raça. Cada protagonista possui silhueta, armadura, vestimentas, armas e postura de combate exclusivas para garantir que o jogador tenha identidade visual única e marcante na mesa.

### Especificações Técnicas de Exportação
* **Sprites de Combate (Corpo Inteiro):** `assets/sprites/heroes/{raca}_{classe}_{genero}.png` (256x256 pixels, ângulo tático 3/4 isométrico).
* **Ícones de Retrato (HUD / Ficha):** `assets/sprites/heroes/icones/{raca}_{classe}_{genero}.png` (128x128 pixels, moldura quadrada de pixel art em ferro forjado, pedra esculpida ou ouro envelhecido).
* **Negative Prompt Universal:**
  > `smooth digital painting, 3d render, cgi, vector art, flat modern minimalism, anime, chibi, blurry, photorealistic, watermark, signature, modern clothing, neon colors, duplicate limbs, deformed hands, clean white background`

---

## 2. Linhagem Humana (6 Arquétipos do Jogador)

---

### [PROT-01] Protagonista Humano Guerreiro
* **Diferença do Aliado Sir Alistair:** Alistair é um cavaleiro veterano caolho de montante e placa pesada. O Guerreiro Protagonista é um veterano mercenário veloz, empunhando espada bastarda e escudo broquel reforçado, vestindo armadura de escamas de aço escurecido e capa de viagem verde-musgo desfiada.
* **Sprite:** `assets/sprites/heroes/humano_guerreiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/humano_guerreiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male human warrior protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric battle stance, dark steel scale mail armor with riveted leather straps, tattered moss-green travel cloak, leather wrist bracers, holding a sharp steel bastard sword in high guard and a round iron buckler on off-hand, determined focused expression, brown hair tied back with leather cord, crisp pixel outlines, chiaroscuro dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male human warrior protagonist, 32-bit dark fantasy avatar, intense piercing amber eyes, determined jawline, dark hair tied in low warrior knot, blackened scale gorget, directional warm torchlight dithering, framed by a studded blackened iron square pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art battle sprite, human warrior protagonist, dark scale mail armor, moss-green cloak, bastard sword and iron buckler, 32-bit tactical RPG angle, crisp pixel clusters, dark fantasy chiaroscuro dithering, isolated on solid black background
```

---

### [PROT-02] Protagonista Humana Clériga
* **Diferença do Aliado Padre Lucien:** Lucien é um sacerdote idoso de tonsura e turíbulo. A Clériga Protagonista é uma combatente fervorosa de campo, vestindo cota de malha fosca com tabardo azul-marinho decorado com cálice de prata gravado, empunhando martelo de guerra de duas mãos e elmo aberto com tiara de aço.
* **Sprite:** `assets/sprites/heroes/humano_clerigo_female.png`
* **Retrato:** `assets/sprites/heroes/icones/humano_clerigo_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female human battle cleric protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric stance, matte riveted chainmail armor under navy-blue crusader tabard with silver chalice emblem, steel open-faced barbuta helm showing braids of auburn hair, two-handed warhammer resting on shoulder with faint sacred glyph glowing on hammer head, steel knee greaves, crisp pixel outlines, divine light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female human cleric protagonist, 32-bit dark fantasy avatar, resolute silver-grey eyes, calm pious expression, steel headpiece over braided auburn hair, polished steel gorget, subtle soft white divine glow on cheekbone, framed by an ancient carved stone sanctuary arch pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female human battle cleric, matte chainmail armor, navy tabard with silver chalice, steel warhammer, 32-bit retro tactical RPG style, divine chiaroscuro pixel dithering, isolated on black background
```

---

### [PROT-03] Protagonista Humano Paladino
* **Diferença do Aliado Lorde Barent:** Barent é um nobre de armadura de prata polida e manto de veludo com leão de ouro. O Paladino Protagonista é um cruzado do sol poente, com armadura de placas de bronze escovado marcada por chamas, capa carmesim de feltro áspero, empunhando uma claymore com empunhadura dourada e escudo estriado.
* **Sprite:** `assets/sprites/heroes/humano_paladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/humano_paladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male human paladin crusader protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 heroic battle angle, heavy brushed bronze plate armor with sunburst engravings, coarse crimson wool cape with brass clasp, open-faced steel bascinet helm, wielding a heavy claymore broadsword pulsing with radiant golden sparks, kite shield on back, disciplined warrior posture, crisp pixel outlines, metallic reflections dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male human paladin protagonist, 32-bit dark fantasy avatar, steadfast intense gaze, chiseled face with stubble, bronze gorget with sun motif, warm golden light reflecting across brow, framed by an engraved bronze filigree square pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, human paladin protagonist, brushed bronze plate armor, crimson wool cape, glowing radiant broadsword, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-04] Protagonista Humana Maga
* **Diferença do Aliado Arquimago Vane:** Vane é um acadêmico idoso com barba grisalha e manto de constelações. A Maga Protagonista é uma jovem evocadora errante, com túnica cor de vinho com capuz pontiagudo aberto, bandoleira de pergaminhos e poções, empunhando uma varinha de jacarandá e um tomo elemental crepitando fogo fátuo na mão esquerda.
* **Sprite:** `assets/sprites/heroes/humano_mago_female.png`
* **Retrato:** `assets/sprites/heroes/icones/humano_mago_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female human wizard evoker protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical casting stance, layered burgundy robes with brass trim, leather scroll bandolier across chest, pointed hood resting back on shoulders, raven-black hair, holding a runic rosewood wand in right hand and floating glowing orb of arcane blue fire in left palm, mystical particle dithering, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female human wizard protagonist, 32-bit dark fantasy avatar, intelligent sharp hazel eyes, raven hair with bangs, embroidered burgundy cowl collar, gentle azure arcane sparks dancing near cheek, framed by a runic arcane circle pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female human wizard, burgundy robes, leather scroll bandolier, rosewood wand, arcane blue flames, 32-bit retro tactical RPG style, chiaroscuro pixel dithering, isolated on black background
```

---

### [PROT-05] Protagonista Humana Patrulheira
* **Diferença do Aliado Garrick:** Garrick é um batedor taciturno com casaco de peles e arco curto. A Patrulheira Protagonista é uma atiradora de elite das fronteiras, com gibão de couro reforçado com tachas de ferro, manto camuflado cinza-esverdeado com capuz ajustado, aljava de flechas de ponta larga nas costas e arco composto longo esticado.
* **Sprite:** `assets/sprites/heroes/humano_patrulheiro_female.png`
* **Retrato:** `assets/sprites/heroes/icones/humano_patrulheiro_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female human ranger sniper protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 dynamic archery stance, studded boiled-leather brigandine, ash-grey camouflaged hood and half-cloak, fingerless archer gloves, drawing an iron-reinforced composite recurve bow with nocked broadhead arrow, wooden quiver of fletched arrows on back, hunting knife at belt, crisp pixel outlines, earthy palette dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female human ranger protagonist, 32-bit dark fantasy avatar, sharp focused green eyes, dark blonde hair tucked under grey leather hood, leather gorget, soft ambient forest twilight lighting, framed by an intertwined wooden branch and leather twine pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, human female ranger, studded leather brigandine, grey archer hood, composite recurve bow, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-06] Protagonista Humano Ladino
* **Diferença do Aliado Corbin:** Corbin é um contrabandista urbano de capuz e adaga envenenada. O Ladino Protagonista é um espadachim acrobático de duelismo, com gibão preto de couro flexível com detalhes em couro cru, máscara leve cobrindo a mandíbula, empunhando rapieira esbelta em guarda e adaga de aparar na mão esquerda.
* **Sprite:** `assets/sprites/heroes/humano_ladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/humano_ladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male human rogue duelist protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 agile fencing stance, form-fitting midnight-black supple leather armor with dark bronze buckles, short cloak thrown over left shoulder, lower face wrapped in dark linen cloth, wielding a gleaming steel rapier in front guard and a parrying main-gauche dagger in off-hand, dynamic shadow dithering, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male human rogue protagonist, 32-bit dark fantasy avatar, cunning sharp dark eyes, dark messy hair, black linen mask covering mouth and jaw, oiled leather collar, high-contrast moonlit shadow chiaroscuro, framed by a serrated blackened steel daggers pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, male human rogue duelist, midnight-black leather armor, steel rapier and parrying dagger, linen half-mask, 32-bit tactical RPG style, sharp pixel dithering, isolated on solid black background
```

---

## 3. Linhagem Anã da Colina (6 Arquétipos do Jogador)

---

### [PROT-07] Protagonista Anão Guerreiro
* **Diferença do Aliado Thorgar/Kargan:** Kargan é um ferreiro com maça cerimonial. O Guerreiro Protagonista Anão é um colosso de cerco, com elmo com chifres curtos de carneiro, barba ruiva trançada presa ao cinto com aros de bronze, armadura de placas pesadas com relevos geométricos de montanha, empunhando machado de guerra duplo e escudo pavise de carvalho com ferro.
* **Sprite:** `assets/sprites/heroes/anao_guerreiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/anao_guerreiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male hill dwarf warrior vanguard protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 low-center-of-gravity battle stance, stocky muscular build, heavy segmented iron plate armor with runic mountain geometric engravings, iron horned helmet, thick braided fiery-red beard tucked through bronze belt loops, brandishing a massive double-bitted bearded battleaxe and a heavy iron-banded oak tower shield, crisp pixel outlines, heavy metal dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male hill dwarf warrior protagonist, 32-bit dark fantasy avatar, fierce battle-hardened brown eyes, braided red beard with bronze rings, horned iron helm visor, heavy forged steel gorget, framed by a carved granite dwarven rune pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male hill dwarf warrior, heavy iron plate armor, braided red beard, double-bitted battleaxe and tower shield, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```

---

### [PROT-08] Protagonista Anã Clériga
* **Diferença do Aliado Karg:** Karg é um monge anão devoto de maça simples. A Clériga Protagonista Anã é uma zeladora de pedras sagradas, com peitoral de latão polido sobre cota de escamas de ferro, tranças loiras escuras adornadas com contas de jade, empunhando uma maça em forma de tocha sagrada e um escudo redondo de bronze estampado com a bigorna primordial.
* **Sprite:** `assets/sprites/heroes/anao_clerigo_female.png`
* **Retrato:** `assets/sprites/heroes/icones/anao_clerigo_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female hill dwarf cleric protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 sturdy battle stance, polished brass cuirass over iron scalemail, dark-blonde thick braids draped over shoulders with green jade beads, gripping a heavy brazier-headed torch mace leaking golden holy sparks, round bronze shield embossed with divine anvil emblem, stout boots, crisp pixel outlines, warm divine glow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female hill dwarf cleric protagonist, 32-bit dark fantasy avatar, wise stubborn hazel eyes, braided blonde hair with jade clasps, engraved brass collar, soft golden halo reflection, framed by an embossed bronze dwarven anvil pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female hill dwarf cleric, brass cuirass, braided blonde hair with jade beads, brazier mace, bronze anvil shield, 32-bit retro tactical RPG style, divine chiaroscuro dithering, isolated on black background
```

---

### [PROT-09] Protagonista Anão Paladino
* **Diferença do Aliado Thalgrim:** Thalgrim usa montante e armadura de obsidiana. O Paladino Protagonista Anão é um guardião do juramento da forja, com armadura completa de placas douradas envelhecidas gravadas com versos arcanos em anão antigo, elmo com crista de crina de cavalo preta, empunhando martelo de guerra brilhando em brasa incandescente e broquel de mithral.
* **Sprite:** `assets/sprites/heroes/anao_paladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/anao_paladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male hill dwarf paladin defender protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 steadfast stance, ancient engraved gold-washed heavy plate armor with dwarven oaths in relief, dark beard split into twin braids with silver filigree, bascinet helm with black horsehair crest, wielding a heavy forge warhammer glowing with molten divine heat and a mithral heater shield, crisp pixel outlines, ember dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male hill dwarf paladin protagonist, 32-bit dark fantasy avatar, noble unyielding dark eyes, twin braided dark beard with silver clasps, golden helm crest, polished heavy steel-gold gorget, framed by a forged gold and iron interlocking chain pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male hill dwarf paladin, gold-washed plate armor, twin braided beard, glowing incandescent warhammer, mithral shield, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```

---

### [PROT-10] Protagonista Anão Mago (Geomante)
* **Diferença dos Magos Aliados:** Este é um lançador de runas telúricas raras entre anões. Veste túnica pesada de couro de boi recoberta por placas de obsidiana nos ombros e peito, barba grisalha presa por aneis de pedra-sabão, empunhando um cetro de ferro rúnico cravado de cristais de ametista brilhantes e um livro de lajotas de pedra entalhada.
* **Sprite:** `assets/sprites/heroes/anao_mago_male.png`
* **Retrato:** `assets/sprites/heroes/icones/anao_mago_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male hill dwarf runic geomancer wizard protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical casting stance, thick ox-hide robes reinforced with obsidian shoulder pauldron plates, broad salt-and-pepper beard tied in twin bundles with soapstone rings, wielding a heavy runic iron scepter tipped with a glowing raw amethyst geode, floating stone tablets inscribed with glowing violet earth runes, crisp pixel outlines, crystal light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male hill dwarf wizard protagonist, 32-bit dark fantasy avatar, intense intellectual amber eyes, weathered furrowed brow, stone rings in salt-and-pepper beard, leather and obsidian collar, purple runic glimmer reflecting on cheeks, framed by an ancient chiseled runic stone tablet pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, male hill dwarf wizard geomancer, ox-hide robes, obsidian pauldrons, amethyst runic iron scepter, floating stone tablets, 32-bit retro tactical RPG style, chiaroscuro pixel dithering, isolated on black background
```

---

### [PROT-11] Protagonista Anã Patrulheira
* **Diferença dos Patrulheiros Aliados:** Uma caçadora das cavernas profundas e ravinas rochosas. Veste camisão de malha fina de bronze sob colete de couro de urso escuro com gola de peles, empunhando uma besta pesada de manivela mecânica com mira de bronze e machadinha de caça curta no cinto.
* **Sprite:** `assets/sprites/heroes/anao_patrulheiro_female.png`
* **Retrato:** `assets/sprites/heroes/icones/anao_patrulheiro_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female hill dwarf subterranean ranger protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 kneeling ambush battle stance, fine bronze chainmail shirt under dark bearskin vest with thick fur collar, braided dark chestnut hair pinned up with bone needles, aiming a heavy mechanical dwarven crank-crossbow with bronze sights, small throwing hatchet at hip, crisp pixel outlines, earthy shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female hill dwarf ranger protagonist, 32-bit dark fantasy avatar, vigilant sharp dark eyes, chestnut braided hair with bone pins, fur collar, directional lantern lighting, framed by a carved cavern stalactite and crossed bolts pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, female hill dwarf ranger, bearskin vest, fur collar, mechanical dwarven heavy crossbow, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-12] Protagonista Anão Ladino (Escavador das Sombras)
* **Diferença dos Ladinos Aliados:** Um especialista em infiltração de túneis e abrir cofres de fortalezas. Veste couro curtido em óleo negro sem partes metálicas soltas, capuz de veludo fosco, cinto utilitário repleto de gazuas e cinzéis de aço, empunhando duas adagas grossas de ponta triangulada para perfurar armaduras pesadas.
* **Sprite:** `assets/sprites/heroes/anao_ladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/anao_ladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male hill dwarf rogue sapper protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 low crouched stealth stance, oiled silent matte-black leather armor, short soot-black beard trimmed square, tight dark velvet hood, utility bandolier with lockpicks and steel chisels, dual-wielding heavy triangular armor-piercing daggers in reverse grip, dramatic rim-light dithering, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male hill dwarf rogue protagonist, 32-bit dark fantasy avatar, calculating piercing dark grey eyes, square trimmed black beard, tight black hood casting deep shadow over brow, muffled dark leather collar, high-contrast chiaroscuro, framed by an interlocking iron picklock and chain pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, male hill dwarf rogue sapper, oiled black leather armor, tight hood, dual armor-piercing daggers, 32-bit tactical RPG style, sharp pixel dithering, isolated on black background
```

---

## 4. Linhagem Draconata (6 Arquétipos do Jogador)

---

### [PROT-13] Protagonista Draconato Guerreiro
* **Diferença dos Aliados Draconatos:** Escamas vermelhas carmesim de dragão vermelho, chifres pontiagudos curvados para trás, armadura de placas de ferro forjado negro com aberturas de ventilação para o vapor, empunhando um machadão de duas mãos com ponta serrilhada de ferro cru e olhar furioso de batalha.
* **Sprite:** `assets/sprites/heroes/draconato_guerreiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/draconato_guerreiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male red dragonborn warrior juggernaut protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 imposing battle stance, thick deep-crimson draconic scales, swept-back sharp dragon horns, heavy blackened-iron plate armor with glowing steam vents, exhaling faint smoke ribbons from draconic nostrils, wielding a colossal serrated two-handed greataxe with scorched blade, crisp pixel outlines, fiery rim-light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male red dragonborn warrior protagonist, 32-bit dark fantasy avatar, glowing reptilian orange slit eyes, sharp crimson scales, swept-back horns, heavy scorched iron gorget, orange ember backlighting, framed by a serrated dragon-scale and jagged iron pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, red dragonborn warrior, heavy blackened-iron plate armor, swept-back horns, serrated greataxe, smoking breath, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```

---

### [PROT-14] Protagonista Draconata Clériga
* **Diferença dos Aliados Clérigos:** Escamas prateadas de dragão de prata com brilho perolado, vestes sagradas de lã branca com bordas azuis sobre cota de malha leve de aço, empunhando uma maça longa com símbolo de sol celestial na cabeça e um livro de preces aberto preso ao escudo de prata.
* **Sprite:** `assets/sprites/heroes/draconato_clerigo_female.png`
* **Retrato:** `assets/sprites/heroes/icones/draconato_clerigo_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female silver dragonborn cleric protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 noble casting stance, pearlescent silver reptilian scales, elegant curved crest horns, bright white cleric vestments with sky-blue trim over light steel chainmail, brandishing a long-hafted solar mace emitting radiant pale-blue frost sparks, heavy silver kite shield, crisp pixel outlines, holy cold-light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female silver dragonborn cleric protagonist, 32-bit dark fantasy avatar, serene glowing sapphire reptilian eyes, shimmering silver scales, crested horns, engraved silver holy collar, soft pale-blue divine aura reflection, framed by an ornate silver filigree snowflake dragon pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female silver dragonborn cleric, pearlescent silver scales, white and sky-blue vestments, solar mace, silver shield, 32-bit retro tactical RPG style, divine frost dithering, isolated on black background
```

---

### [PROT-15] Protagonista Draconato Paladino
* **Diferença do Aliado Balthazar:** Balthazar é dourado com manto carmesim e espada solar. O Paladino Protagonista Draconato tem escamas de bronze antigo escurecido, peitoral de adamante maciço com entalhes de tempestade e raios, empunhando uma alabarda pesada com ponta crepitando eletricidade azul e capa azul-tempestade.
* **Sprite:** `assets/sprites/heroes/draconato_paladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/draconato_paladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male bronze dragonborn paladin sentinel protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 resolute heroic stance, metallic weathered bronze reptilian scales, heavy adamantine plate armor etched with lightning bolt runes, tattered storm-blue cape, wielding a massive polearm halberd crackling with divine blue electrical sparks, heavy battle greaves, crisp pixel outlines, electric arc dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male bronze dragonborn paladin protagonist, 32-bit dark fantasy avatar, noble electric-cyan draconic eyes, weathered bronze scales, swept horns, adamantine collar, subtle blue lightning spark reflecting on snout, framed by an etched adamantine and lightning bolt pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, bronze dragonborn paladin, adamantine plate armor, storm-blue cape, crackling electric halberd, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-16] Protagonista Draconato Mago
* **Diferença dos Magos Aliados:** Escamas azul-meia-noite de dragão azul com espinhos nas têmporas, manto leve de seda preta com runas arcanas bordadas em fios de ouro, sem cajado: canaliza magia diretamente através de manoplas de ferro esculpidas com garras e foco arcano de orbe de tempestade.
* **Sprite:** `assets/sprites/heroes/draconato_mago_male.png`
* **Retrato:** `assets/sprites/heroes/icones/draconato_mago_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male blue dragonborn wizard elementalist protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 dynamic spellcasting stance, dark cobalt-blue scales, twin sharp temporal horns, flowing midnight-black silk robes trimmed in arcane golden glyphs, wearing runic iron dragon-claw gauntlets, left hand conjuring a swirling spherical vortex of crackling lightning and arcane runes, crisp pixel outlines, arcane glow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male blue dragonborn wizard protagonist, 32-bit dark fantasy avatar, piercing electric-yellow slit eyes, deep blue scales, sharp horned crest, high black scholar collar, blue magical arcs illuminating draconian jaw, framed by an ancient runic constellation circle pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, male blue dragonborn wizard, cobalt scales, black and gold silk robes, dragon-claw gauntlets, swirling lightning sphere, 32-bit retro tactical RPG style, chiaroscuro pixel dithering, isolated on black background
```

---

### [PROT-17] Protagonista Draconata Patrulheira
* **Diferença dos Patrulheiros Aliados:** Escamas verde-floresta escuras com padrões de camuflagem reptiliana, armadura flexível de couro de crocodilo com ombros protegidos por couraça de chifre, empunhando um arco composto maciço de teixo negro com flechas pesadas projetadas para monstros grandes.
* **Sprite:** `assets/sprites/heroes/draconato_patrulheiro_female.png`
* **Retrato:** `assets/sprites/heroes/icones/draconato_patrulheiro_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female green dragonborn ranger stalker protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 predatory archery stance, deep forest-green camouflaged scales, backward-curving streamlined horns, tough reptile-leather brigandine, olive-green hooded scarf, drawing a massive heavy yew recurve bow with jagged broadhead arrow, leather quiver on back, crisp pixel outlines, forest shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female green dragonborn ranger protagonist, 32-bit dark fantasy avatar, sharp predatory golden-green reptilian eyes, forest-green scales, olive scarf collar, dappled forest canopy lighting, framed by an intertwined thorned vine and carved dragon horn pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, female green dragonborn ranger, camouflage scales, reptile-leather armor, heavy yew bow, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-18] Protagonista Draconato Ladino
* **Diferença dos Ladinos Aliados:** Escamas pretas de dragão negro com acabamento acetinado fosco, silhueta esguia e ameaçadora, gibão de couro endurecido untado em resina silenciosa, empunhando uma cimitarra curta curva e um estilete de obsidiana, cauda enrolada estrategicamente e olhos dourados espreitando das trevas.
* **Sprite:** `assets/sprites/heroes/draconato_ladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/draconato_ladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male black dragonborn rogue assassin protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 low stalking shadow stance, sleek matte-black reptilian scales, forward-curving ram-like black horns, fitted blackened boiled leather armor, dark cowl wrapped around neck, wielding an acid-etched curved scimitar in right hand and an obsidian stiletto dagger in reverse grip, crisp pixel outlines, midnight shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male black dragonborn rogue protagonist, 32-bit dark fantasy avatar, menacing narrow slit amber eyes, matte-black scales, forward-curving horns, dark cowl collar, extreme chiaroscuro moonlight backlighting, framed by a serrated obsidian dragon tooth pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, male black dragonborn rogue assassin, matte-black scales, boiled leather armor, acid-etched scimitar and obsidian stiletto, 32-bit tactical RPG style, sharp pixel dithering, isolated on black background
```

---

## 5. Linhagem Élfica da Floresta (6 Arquétipos do Jogador)

---

### [PROT-19] Protagonista Elfo Guerreiro (Lâmina-da-Floresta)
* **Diferença dos Guerreiros Aliados:** Um mestre espadachim élfico veloz com armadura de placas de madeira-férrea entalhada com motivos de folhas secas, capa verde-esmeralda profunda, empunhando duas espadas longas élficas curvas (estilo gêmeo) com velocidade e graça letais.
* **Sprite:** `assets/sprites/heroes/elfo_guerreiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/elfo_guerreiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male wood elf blademaster warrior protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 graceful dual-wielding battle stance, tall slender athletic build, pointed ears, long silver hair with warrior side-braids, lacquered ironwood plate armor etched with autumn leaf patterns, emerald-green silk cloak, dual-wielding twin curved elven scimitars with razor edges, crisp pixel outlines, leaf and steel reflection dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male wood elf warrior protagonist, 32-bit dark fantasy avatar, sharp proud golden eyes, long silver hair with side braids, pointed elven ear, carved ironwood collar with autumn leaf filigree, elegant directional lighting, framed by an ancient carved ironwood branch pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male wood elf warrior, ironwood plate armor, emerald cloak, dual twin curved elven swords, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-20] Protagonista Elfa Clériga (Druídica / Vida)
* **Diferença da Aliada Faen:** Faen é uma sacerdotisa reclusa de túnica branca simples. A Clériga Protagonista Elfa é uma defensora do bosque sagrado, vestindo cota de malha de folhas de bronze sobre túnica verde-oliva, coroa de galhos de faia entalhados, empunhando um bordão com cristal de âmbar luminoso e broquel de madeira ancestral.
* **Sprite:** `assets/sprites/heroes/elfo_clerigo_female.png`
* **Retrato:** `assets/sprites/heroes/icones/elfo_clerigo_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female wood elf cleric of life protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 elegant casting stance, bronze leaf-mail armor over moss-olive tunic, long braided auburn hair crowned with a carved beech-branch circlet, pointed ears, holding a living wooden quarterstaff capped with an amber solar crystal radiating golden healing mist, small carved buckler on off-hand, crisp pixel outlines, verdant light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female wood elf cleric protagonist, 32-bit dark fantasy avatar, serene compassionate emerald eyes, auburn braids, pointed ears, carved wooden circlet, soft warm amber glow lighting face, framed by an ornate living vine and amber leaf pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female wood elf cleric, bronze leaf-mail, amber solar staff, living wooden buckler, 32-bit retro tactical RPG style, divine green chiaroscuro dithering, isolated on black background
```

---

### [PROT-21] Protagonista Elfo Paladino (Juramento dos Anciões)
* **Diferença dos Paladinos Aliados:** Veste armadura de placas de mithral com incrustações de musgo sagrado e runas élficas de florescer, capa verde-escura como a copa das árvores antigas, empunhando uma lança de guerra élfica cintilante com estandarte e escudo em forma de folha.
* **Sprite:** `assets/sprites/heroes/elfo_paladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/elfo_paladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male wood elf paladin of the ancients protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 noble spearman stance, shimmering greenish mithral plate armor inlaid with golden ivy vines, deep forest canopy cloak, pointed ears, long golden-brown hair, wielding a gleaming elven winged spear crackling with radiant emerald divine light and a leaf-shaped mithral shield, crisp pixel outlines, radiant pollen dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male wood elf paladin protagonist, 32-bit dark fantasy avatar, noble resolute turquoise eyes, golden-brown hair, pointed ears, engraved mithral gorget with golden ivy motif, soft green-gold divine radiance, framed by an ornate mithral ivy and leaf pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, wood elf paladin, mithral plate armor with golden ivy, winged elven spear, leaf shield, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-22] Protagonista Elfa Maga (Arcanista das Folhas)
* **Diferença dos Magos Aliados:** Veste mantos fluidos cor de casca de carvalho e verde-azulado com mangas compridas abertas, grimório entalhado em casca de bétula ancestral levitando ao seu lado, empunhando um cetro de madeira curva com flores de cristal que canalizam relâmpagos verdes.
* **Sprite:** `assets/sprites/heroes/elfo_mago_female.png`
* **Retrato:** `assets/sprites/heroes/icones/elfo_mago_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female wood elf mage protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 floating casting stance, layered teal and oak-bark silk robes with trailing sleeves, pointed ears, flowing silvery-white hair, floating birch-bark grimoire surrounded by glowing green runic letters, left hand channeling crackling emerald lightning sparks, crisp pixel outlines, mystical particle dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female wood elf mage protagonist, 32-bit dark fantasy avatar, mystical glowing violet eyes, porcelain skin, silver hair, pointed ears, embroidered teal cowl, floating emerald sparks near cheek, framed by a delicate silver birch and runic leaf pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female wood elf mage, teal and oak-bark robes, silver hair, floating birch grimoire, emerald lightning sparks, 32-bit tactical RPG style, sharp pixel dithering, isolated on black background
```

---

### [PROT-23] Protagonista Elfo Patrulheiro
* **Diferença da Aliada Sylas:** Sylas é uma caçadora noturna com capuz fechado e arco curto. O Patrulheiro Protagonista Elfo é um mestre batedor de longo alcance das copas das árvores, com armadura leve de couro de veado com placas de casca endurecida, cabelos castanhos trançados, arco longo recurvo élfico de duas pontas e aljava lateral.
* **Sprite:** `assets/sprites/heroes/elfo_patrulheiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/elfo_patrulheiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male wood elf ranger marksman protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 dynamic archery draw stance, deer-leather tunic with hardened bark shoulder guards, forest-brown braided hair, pointed ears, drawing a tall dual-tipped elven greatbow with broadhead arrow, side-mounted wicker quiver, twin hunting daggers at lower back, crisp pixel outlines, dappled forest light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male wood elf ranger protagonist, 32-bit dark fantasy avatar, hawk-like intense hazel eyes, pointed ears, braided brown hair, leather collar with leaf pin, soft forest rim-lighting, framed by a carved oak branch and fletched arrows pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male wood elf ranger, deer-leather tunic, bark guards, tall elven greatbow, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-24] Protagonista Elfa Ladina (Sombra das Copas)
* **Diferença dos Ladinos Aliados:** Veste armadura de couro de serpente negra com forro verde-escuro, capuz justo com abertura que revela os olhos afiados e as orelhas pontiagudas, empunhando duas adagas élficas recurvadas transparentes de vidro vulcânico.
* **Sprite:** `assets/sprites/heroes/elfo_ladino_female.png`
* **Retrato:** `assets/sprites/heroes/icones/elfo_ladino_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female wood elf rogue infiltrator protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 swift stalking crouch stance, form-fitting black snakeskin leather armor with dark green velvet accents, tight assassin cowl showing pointed ears, piercing amber eyes, dual-wielding curved translucent obsidian-glass daggers with venomous sheen, crisp pixel outlines, moonlit shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female wood elf rogue protagonist, 32-bit dark fantasy avatar, dangerous cunning amber eyes, dark hair under tight cowl, pointed ears sticking out, black leather mask covering mouth, cold moonlight chiaroscuro, framed by crossed glass daggers and black ivy pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female wood elf rogue, black snakeskin armor, obsidian-glass curved daggers, tight cowl, 32-bit retro tactical RPG style, sharp chiaroscuro dithering, isolated on black background
```

---

## 6. Linhagem Halfling (6 Arquétipos do Jogador)

---

### [PROT-25] Protagonista Halfling Guerreiro
* **Diferença do Aliado Finn:** Finn é um ladino ágil de rapieira. O Guerreiro Protagonista Halfling é um soldado destemido de infantaria pequena, com cota de malha pesada adaptada ao tamanho, elmo cônico de aço, capa curta azul-real, empunhando uma espada curta larga de gume duplo e escudo redondo de madeira reforçado com tachas de ferro.
* **Sprite:** `assets/sprites/heroes/halfling_guerreiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/halfling_guerreiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male halfling warrior defender protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 low-center battle stance, petite stocky athletic build, fitted riveted steel chainmail over blue tunic, conical steel helmet over messy brown curly hair, oversized pointed ears, wielding a broad double-edged shortsword in right hand and a round iron-studded wooden shield in left, crisp pixel outlines, metallic reflections dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male halfling warrior protagonist, 32-bit dark fantasy avatar, brave determined blue eyes, curly brown hair sticking out from under steel conical helm, pointed ear, steel chainmail gorget, directional lantern lighting, framed by a round iron-studded shield rim pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male halfling warrior, fitted chainmail, conical steel helmet, broad shortsword and round shield, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```

---

### [PROT-26] Protagonista Halfling Clériga
* **Diferença dos Clérigos Aliados:** Veste túnica de feltro amarelo-mostarda com capuz fofo, peitoral de couro cozido com o emblema do trevo de prata, empunhando uma maça leve com cabeça de bronze esculpida em forma de sino e um relicário sagrado no cinto.
* **Sprite:** `assets/sprites/heroes/halfling_clerigo_female.png`
* **Retrato:** `assets/sprites/heroes/icones/halfling_clerigo_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female halfling cleric protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 cheerful determined casting stance, mustard-yellow wool vestments over boiled-leather breastplate with embossed silver clover, ginger curly hair with pointed ears, holding a bell-headed bronze mace emitting warm comforting golden sparks, leather-wrapped holy book at hip, crisp pixel outlines, warm hearth-light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female halfling cleric protagonist, 32-bit dark fantasy avatar, warm kind hazel eyes, round rosy cheeks, curly ginger hair, pointed ears, silver clover collar clasp, warm golden divine backlighting, framed by an embossed silver clover and wheat grain pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female halfling cleric, mustard wool vestments, boiled leather breastplate, bell-headed bronze mace, ginger curly hair, 32-bit retro tactical RPG style, warm dithering, isolated on black background
```

---

  ### [PROT-27] Protagonista Halfling Paladino
  * **Diferença dos Paladinos Aliados:** Veste armadura de placas completa miniaturizada de ferro polido com brasão de coração dourado, capa curta carmesim, empunhando uma lança de justa adaptada e escudo gota brilhando com luz sagrada protetora.
  * **Sprite:** `assets/sprites/heroes/halfling_paladino_male.png`
  * **Retrato:** `assets/sprites/heroes/icones/halfling_paladino_male.png`
  * **Prompt Sprite (Midjourney v6):**
  ```text
  Full-body player character battle sprite, male halfling paladin cavalier protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 heroic defensive stance, miniature shining steel full plate armor with golden heart crest, crimson mantle, steel helmet with small plume, pointed ears, brandishing a gleaming lance-style shortspear glowing with pure white divine radiance and a teardrop kite shield, crisp pixel outlines, divine sparkle dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
  ```
  * **Prompt Retrato (128x128 Token):**
  ```text
  Detailed 2.5D pixel art portrait icon of male halfling paladin protagonist, 32-bit dark fantasy avatar, earnest proud brown eyes, young face, steel sallet helmet with visor up, polished steel gorget, brilliant white holy glow reflection, framed by an ornate miniature gold-filigree shield pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
  ``` 
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male halfling paladin, miniature full plate armor, crimson mantle, radiant shortspear, teardrop shield, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-28] Protagonista Halfling Mago
* **Diferença dos Magos Aliados:** Veste casaco longo xadrez de veludo azul com grandes bolsos cheios de componentes de magia, chapéu mole dobrado para trás, empunhando um bordão curto com uma lamparina mágica acesa na ponta que queima com fogo arcano multicolorido.
* **Sprite:** `assets/sprites/heroes/halfling_mago_male.png`
* **Retrato:** `assets/sprites/heroes/icones/halfling_mago_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male halfling illusionist wizard protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 whimsical casting stance, oversized deep-blue velvet traveling coat with brass buttons, floppy slouch hat tilted back showing brown curls and pointed ears, holding a short wooden walking cane staff dangling a miniature brass lantern burning with multi-colored arcane flame, floating illusory spell cards, crisp pixel outlines, prismatic light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male halfling wizard protagonist, 32-bit dark fantasy avatar, mischievous intelligent green eyes, messy curls under floppy blue hat, pointed ears, velvet coat collar, glowing prismatic sparks dancing around face, framed by a brass lantern and star-glyph pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, male halfling wizard, blue velvet coat, floppy slouch hat, cane staff with arcane lantern, prismatic particles, 32-bit tactical RPG style, sharp pixel dithering, isolated on black background
```

---

### [PROT-29] Protagonista Halfling Patrulheiro (Fundeiro / Funda de Guerra)
* **Diferença dos Patrulheiros Aliados:** Especialista em atirar pedras encantadas e chumbo com funda tradicional e arco curto de caça. Veste gibão de couro acolchoado com capa de camuflagem terrosa, cinto com bolsa de balas de chumbo, girando uma funda de couro reforçado em guarda e adaga de osso.
* **Sprite:** `assets/sprites/heroes/halfling_patrulheiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/halfling_patrulheiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male halfling slinger ranger protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 dynamic skirmisher stance, padded leather jerkin with autumn-leaf camouflage poncho, pointed ears, spinning a heavy braided leather sling in right hand loaded with a glowing lead bullet, small hunting horn and pouch of riverstones at hip, hunting knife in off-hand, crisp pixel outlines, earthy shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male halfling ranger protagonist, 32-bit dark fantasy avatar, sharp alert brown eyes, windblown hair, pointed ears, camouflage poncho collar, dappled sunlight lighting, framed by a braided leather sling and riverstone pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male halfling slinger ranger, padded leather jerkin, camouflage poncho, braided leather sling, riverstones, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-30] Protagonista Halfling Ladina (Gatuna das Sombras)
* **Diferença do Aliado Finn:** Finn usa rapieira em duelo aberto. A Ladina Protagonista Halfling é uma batedora de carteiras e infiltradora acrobática, com túnica de veludo preto colada ao corpo com solas de sapato silenciosas de feltro, capuz justo e duas adagas de arremesso leves com lâminas curvas.
* **Sprite:** `assets/sprites/heroes/halfling_ladino_female.png`
* **Retrato:** `assets/sprites/heroes/icones/halfling_ladino_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female halfling burglar rogue protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 agile crouching stealth stance, compact nimble frame, fitted soot-grey leather armor, soft black hood showing dark curly hair strands and pointed ears, lockpick pouch strapped to thigh, wielding twin delicate throwing daggers with hooked blades, dramatic shadow dithering, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female halfling rogue protagonist, 32-bit dark fantasy avatar, sly quick amber eyes, dark curls tucked under black hood, pointed ears, dark leather mask resting on chin, high-contrast cool moonlight chiaroscuro, framed by a lockpick and shadow-smoke pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female halfling burglar rogue, soot-grey leather armor, soft black hood, twin hooked throwing daggers, 32-bit tactical RPG style, sharp pixel dithering, isolated on black background
```

---

## 7. Linhagem Meio-Orc (6 Arquétipos do Jogador)

---

### [PROT-31] Protagonista Meio-Orc Guerreiro
* **Diferença do Aliado Thorgar:** Thorgar usa machado de batalha tradicional e peitoral de ferro. O Guerreiro Protagonista Meio-Orc é um gladiador calejado, com armadura de placas assimétricas sobre peito tatuado com cicatrizes tribais, elmo gladiatório de bronze oxidado, empunhando uma espada pesada de carrasco de lâmina reta e mangual com corrente estalando.
* **Sprite:** `assets/sprites/heroes/meio_orc_guerreiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/meio_orc_guerreiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male half-orc gladiator warrior protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 imposing wide battle stance, tall massive muscular build, grey-green skin, protruding lower tusk fangs, asymmetrical scarred iron plate armor on one shoulder leaving ritual-scarred chest exposed, wielding a colossal flat-headed executioner greatsword in two hands, spiked chain wrapped on forearm, crisp pixel outlines, grim shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male half-orc warrior protagonist, 32-bit dark fantasy avatar, fierce battle-hardened yellow eyes, grey-green skin, prominent lower tusks, war scars across nose, bronze gladiator collar, dramatic harsh top-lighting, framed by a spiked iron chain and bone pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male half-orc warrior gladiator, grey-green skin, lower tusks, asymmetrical plate armor, executioner greatsword, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```

---

### [PROT-32] Protagonista Meio-Orc Clérigo (Tempestade / Guerra)
* **Diferença dos Clérigos Aliados:** Um xamã sagrado de batalha que invoca trovões. Veste cota de malha rústica de elos grossos coberta por pele de lobo cinzento, empunhando uma maça de guerra em forma de totem de pedra gravado com runas de raio que brilham em azul elétrico e um escudo de ferro negro.
* **Sprite:** `assets/sprites/heroes/meio_orc_clerigo_male.png`
* **Retrato:** `assets/sprites/heroes/icones/meio_orc_clerigo_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male half-orc storm war cleric protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 commanding battle stance, olive-grey skin, sharp lower tusks, heavy iron ringmail armor draped with a dark wolf-pelt mantle, holding a massive stone-carved totem mace crackling with intense blue lightning arcs, heavy blackened-iron round shield, crisp pixel outlines, electric thunder dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male half-orc cleric protagonist, 32-bit dark fantasy avatar, intense storm-blue glowing eyes, olive skin, prominent tusks, wolf-pelt cowl, blue lightning reflections across cheeks, framed by an iron wolf-skull and lightning bolt pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, male half-orc cleric of storm, ringmail armor, wolf-pelt mantle, crackling stone totem mace, 32-bit retro tactical RPG style, electrical chiaroscuro dithering, isolated on black background
```

---

### [PROT-33] Protagonista Meio-Orc Paladino (Juramento de Vingança)
* **Diferença do Aliado Varek:** Varek é um cavaleiro calmo de espada rúnica. O Paladino Protagonista Meio-Orc é uma força implacável de retribuição, com armadura de placas completas de aço escuro com pontas afiadas nos ombros, capa esfarrapada preta, empunhando uma montante com runas sagradas gravadas a fogo na lâmina.
* **Sprite:** `assets/sprites/heroes/meio_orc_paladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/meio_orc_paladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male half-orc vengeance paladin protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 aggressive charging stance, grey-green skin, fierce lower tusks, dark jagged plate armor with spiked pauldrons, tattered charcoal cape, wielding a massive two-handed greatsword engulfed in radiant white and golden divine vengeance flames, heavy sabatons, crisp pixel outlines, divine fire dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male half-orc paladin protagonist, 32-bit dark fantasy avatar, stern resolute golden eyes, grey-green skin, tusks, spiked dark steel gorget, brilliant white holy flame backlighting, framed by a jagged dark iron and holy flame pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male half-orc paladin, dark jagged plate armor, tattered cape, greatsword engulfed in divine flames, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-34] Protagonista Meio-Orc Mago (Mago de Batalha / Abjurador)
* **Diferença dos Magos Aliados:** Raro feiticeiro orc que combina força física com barreiras mágicas. Veste túnica reforçada de couro de mamute com ombreiras de osso, cabeça raspada com tatuagens rúnicas brilhantes, empunhando um bastão pesado de ferro fundido que canaliza escudos arcanos cintilantes.
* **Sprite:** `assets/sprites/heroes/meio_orc_mago_male.png`
* **Retrato:** `assets/sprites/heroes/icones/meio_orc_mago_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male half-orc abjurer battlemage protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 sturdy arcane stance, muscular grey skin with lower tusks, shaved head adorned with glowing blue runic tattoos, heavy mammoth-hide coat with carved bone pauldrons, wielding a heavy wrought-iron quarterstaff radiating a translucent blue hexagonal arcane shield barrier in off-hand, crisp pixel outlines, magical barrier dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male half-orc wizard protagonist, 32-bit dark fantasy avatar, focused glowing cyan eyes, grey skin with prominent tusks, glowing scalp tattoos, mammoth-hide collar, blue protective barrier reflection, framed by an etched bone and arcane rune pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, male half-orc wizard battlemage, mammoth-hide coat, bone pauldrons, glowing runic tattoos, iron quarterstaff, arcane shield barrier, 32-bit tactical RPG style, sharp pixel dithering, isolated on black background
```

---

### [PROT-35] Protagonista Meio-Orc Patrulheiro (Rastreador das Estepes)
* **Diferença dos Patrulheiros Aliados:** Caçador selvagem de feras colossais. Veste couro de rinoceronte com peles grossas, arco composto pesado reforçado com ossos nas extremidades, aljava de dardos de arremesso e lança curta presa às costas.
* **Sprite:** `assets/sprites/heroes/meio_orc_patrulheiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/meio_orc_patrulheiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male half-orc savage hunter ranger protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 alert wilderness stance, weathered olive-grey skin, sharp tusks, heavy rhino-hide brigandine with dark fur shoulder mantle, pulling back a massive bone-reinforced recurve war bow with barbed arrow, heavy hunting machete at belt, crisp pixel outlines, wilderness shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male half-orc ranger protagonist, 32-bit dark fantasy avatar, keen observant yellow eyes, weathered olive skin, tusks, fur-lined leather collar, low-angle rugged campfire lighting, framed by a carved mammoth tusk and barbed arrow pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male half-orc ranger hunter, rhino-hide armor, bone-reinforced war bow, barbed arrow, fur mantle, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-36] Protagonista Meio-Orc Ladina (Bruta das Sombras)
* **Diferença dos Ladinos Aliados:** Uma assassina de impacto físico que prefere emboscadas implacáveis. Veste couro negro laminado com pregos de ferro, capuz justo de lã escura, empunhando duas machadinhas de arremesso balanceadas e um facão curvo de cortar tendões.
* **Sprite:** `assets/sprites/heroes/meio_orc_ladino_female.png`
* **Retrato:** `assets/sprites/heroes/icones/meio_orc_ladino_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female half-orc enforcer rogue protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 aggressive crouched ambush stance, athletic muscular build, dark olive-grey skin, sharp lower tusks, fitted studded black leather armor, dark cowl wrapped tightly, dual-wielding blackened throwing hatchets with serrated edges, cleaver dagger at hip, crisp pixel outlines, moonlight chiaroscuro dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female half-orc rogue protagonist, 32-bit dark fantasy avatar, lethal cold amber eyes, olive skin with small tusks, dark cowl over braided black hair, studded leather collar, high-contrast cool moonlight lighting, framed by crossed serrated hatchets pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female half-orc rogue enforcer, studded black leather armor, tight cowl, serrated throwing hatchets, 32-bit tactical RPG style, sharp pixel dithering, isolated on black background
```

---

## 8. Linhagem Tiefling (6 Arquétipos do Jogador)

---

### [PROT-37] Protagonista Tiefling Guerreiro (Cavaleiro do Fogo Fátuo)
* **Diferença dos Guerreiros Aliados:** Pele carmesim profunda, chifres grossos que se projetam para cima como uma coroa, armadura de placas completas de ferro fundido com sulcos por onde escapa calor avermelhado, empunhando uma espada larga de gume recortado que crepita em brasas e escudo com face demoníaca em ferro batido.
* **Sprite:** `assets/sprites/heroes/tiefling_guerreiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_guerreiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male tiefling hellknight warrior protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 menacing battle stance, deep-crimson skin, crown-like sweeping horns, heavy cast-iron plate armor with glowing red heat grooves, spade-tipped tail curling behind, brandishing an infernal jagged broadsword dripping glowing embers and a demon-faced wrought-iron shield, crisp pixel outlines, hellfire dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male tiefling warrior protagonist, 32-bit dark fantasy avatar, glowing solid-gold demonic eyes without pupils, crimson skin, crowned horns, cast-iron gorget with glowing red runes, intense ember backlighting, framed by a wrought-iron horned demon skull pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male tiefling warrior hellknight, crimson skin, crowned horns, cast-iron plate armor with heat grooves, jagged ember broadsword, demon shield, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```

---

### [PROT-38] Protagonista Tiefling Clériga (Domínio do Fogo / Luz)
* **Diferença dos Clérigos Aliados:** Pele lilás-cinzenta com chifres graciosos em espiral, vestes sacerdotais escuras com estola carmesim bordada em chamas douradas sobre cota de malha, empunhando um cetro de ferro batido com uma chama sagrada perpétua flutuando na ponta e escudo de prata polida.
* **Sprite:** `assets/sprites/heroes/tiefling_clerigo_female.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_clerigo_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female tiefling sacred flame cleric protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 graceful casting stance, lavender-grey skin, elegant spiral horns, dark monastic vestments with crimson stole embroidered with golden flames over steel chainmail, holding a wrought-iron holy scepter topped with a perpetual hovering golden flame, polished silver shield on off-hand, crisp pixel outlines, warm holy fire dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female tiefling cleric protagonist, 32-bit dark fantasy avatar, serene glowing silver eyes, lavender skin, spiral horns, crimson stole collar, soft golden holy fire glow illuminating brow, framed by an interlocking silver flame and sacred rune pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female tiefling cleric of light, lavender-grey skin, spiral horns, crimson and gold vestments, holy flame scepter, silver shield, 32-bit retro tactical RPG style, divine flame dithering, isolated on black background
```

---

### [PROT-39] Protagonista Tiefling Paladino (Juramento da Redenção)
* **Diferença dos Paladinos Aliados:** Um cruzado que busca redimir sua herança infernal. Veste armadura de placas completas de aço escovado branco com bordas douradas, capa branca de seda pesada, chifres adornados com tiras de linho sagrado e preces, empunhando uma maça pesada brilhando com luz pura e escudo oval imaculado.
* **Sprite:** `assets/sprites/heroes/tiefling_paladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_paladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male tiefling redemption paladin protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 noble champion stance, dusky-red skin, backward horns wrapped in sacred white parchment ribbons, pristine white-enamelled plate armor with gold filigree, pure white flowing cape, wielding a heavy flanged holy mace glowing with intense celestial white radiance and an oval steel shield, crisp pixel outlines, divine light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male tiefling paladin protagonist, 32-bit dark fantasy avatar, sorrowful yet resolute glowing white eyes, dusky-red skin, parchment-wrapped horns, white-and-gold plate gorget, brilliant celestial halo reflection, framed by an ornate white enamel and gold holy chain pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, male tiefling paladin of redemption, dusky-red skin, parchment-wrapped horns, white-and-gold plate armor, celestial glowing mace, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-40] Protagonista Tiefling Mago (Evocador Infernal)
* **Diferença do Aliado Azaroth:** Azaroth veste túnica escura clássica com mísseis mágicos. O Mago Protagonista Tiefling tem pele carmesim com escamas sutis nas maçãs do rosto, vestes de couro de dragão negro com gola alta pontiaguda, flutuando grimório com fecho de crânio com chamas púrpuras e canalizando relâmpagos infernais de ambas as mãos.
* **Sprite:** `assets/sprites/heroes/tiefling_mago_male.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_mago_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male tiefling pyromancer wizard protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 dynamic floating casting stance, vivid crimson skin, long sweeping obsidian horns, high-collared dragon-leather wizard coat trimmed in purple silk, pointed tail swishing, floating skull-clasped grimoire radiating violet infernal glyphs, dual-channeling crackling dark-purple and orange flame arcs from open clawed hands, crisp pixel outlines, magical fire dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of male tiefling wizard protagonist, 32-bit dark fantasy avatar, intense pupil-less burning violet eyes, crimson skin, sweeping obsidian horns, high black leather collar, dramatic purple fire illumination, framed by an ancient infernal rune circle and blackened skull pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, male tiefling wizard pyromancer, crimson skin, sweeping obsidian horns, high-collar dragon-leather coat, floating skull grimoire, violet infernal flames, 32-bit tactical RPG style, sharp pixel dithering, isolated on black background
```

---

### [PROT-41] Protagonista Tiefling Patrulheira (Caçadora dos Ermos Vulcânicos)
* **Diferença dos Patrulheiros Aliados:** Especialista em caçar aberrações e demônios nas fendas de cinzas. Veste couraça de couro de quimera com proteções de osso negro, manto cinzento camuflado com fuligem, arco composto de ferro negro que dispara flechas embebidas em óleo incandescente.
* **Sprite:** `assets/sprites/heroes/tiefling_patrulheiro_female.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_patrulheiro_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female tiefling ashland ranger protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 agile draw stance, dusk-purple skin, sleek backwards-swept horns, chimera-hide brigandine with dark bone pauldrons, soot-grey ragged cloak, tail with small blade tip, drawing a heavy blackened-iron recurve bow with incandescent flaming arrow, leather quiver on back, crisp pixel outlines, ember shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female tiefling ranger protagonist, 32-bit dark fantasy avatar, sharp predatory yellow slit eyes, dusk-purple skin, sleek horns, soot-grey cowl collar, warm ember sparks drifting across cheek, framed by a blackened iron thorn and smoking arrow pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, female tiefling ranger, dusk-purple skin, sleek horns, chimera-hide armor, blackened-iron bow with flaming arrow, soot cloak, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```

---

### [PROT-42] Protagonista Tiefling Ladina (Sombra Infernal)
* **Diferença dos Ladinos Aliados:** Uma ladra acrobática que usa sua cauda preênsil para roubar chaves e desarmar armadilhas. Veste couro preto flexível fosco, capuz recortado para os chifres, máscara leve e duas adagas de estilete em aço azulado envenenado.
* **Sprite:** `assets/sprites/heroes/tiefling_ladino_female.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_ladino_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female tiefling shadow rogue protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 stealth crouching stance, obsidian-red skin, small elegant curved horns poking through fitted black leather hood, prehensile spade tail holding a stolen brass key, dual-wielding needle-thin blued-steel stiletto daggers in reverse grip, silent dark leather boots, crisp pixel outlines, midnight chiaroscuro dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of female tiefling rogue protagonist, 32-bit dark fantasy avatar, cunning glowing golden eyes, obsidian-red skin, sleek horns through tight black hood, dark leather half-mask, high-contrast cool moonlit shadows, framed by a serrated blued-steel stiletto and shadow-wisp pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, female tiefling rogue, obsidian-red skin, curved horns, fitted black leather hood, prehensile tail, twin blued-steel stiletto daggers, 32-bit tactical RPG style, sharp pixel dithering, isolated on black background
```

---

## 9. Matriz Geral de Roteamento de Arquivos dos Protagonistas

Para integração direta com o método `AssetManager.resolve_hero_candidates(race, char_class, gender)`:

| ID | Raça | Classe | Arquivo do Sprite (`assets/sprites/heroes/`) | Arquivo do Ícone (`assets/sprites/heroes/icones/`) |
|---|---|---|---|---|
| `PROT-01` | Humano | Guerreiro | `humano_guerreiro_male.png` | `humano_guerreiro_male.png` |
| `PROT-02` | Humano | Clérigo | `humano_clerigo_female.png` | `humano_clerigo_female.png` |
| `PROT-03` | Humano | Paladino | `humano_paladino_male.png` | `humano_paladino_male.png` |
| `PROT-04` | Humano | Mago | `humano_mago_female.png` | `humano_mago_female.png` |
| `PROT-05` | Humano | Patrulheiro | `humano_patrulheiro_female.png` | `humano_patrulheiro_female.png` |
| `PROT-06` | Humano | Ladino | `humano_ladino_male.png` | `humano_ladino_male.png` |
| `PROT-07` | Anão da Colina | Guerreiro | `anao_guerreiro_male.png` | `anao_guerreiro_male.png` |
| `PROT-08` | Anão da Colina | Clérigo | `anao_clerigo_female.png` | `anao_clerigo_female.png` |
| `PROT-09` | Anão da Colina | Paladino | `anao_paladino_male.png` | `anao_paladino_male.png` |
| `PROT-10` | Anão da Colina | Mago | `anao_mago_male.png` | `anao_mago_male.png` |
| `PROT-11` | Anão da Colina | Patrulheiro | `anao_patrulheiro_female.png` | `anao_patrulheiro_female.png` |
| `PROT-12` | Anão da Colina | Ladino | `anao_ladino_male.png` | `anao_ladino_male.png` |
| `PROT-13` | Draconato | Guerreiro | `draconato_guerreiro_male.png` | `draconato_guerreiro_male.png` |
| `PROT-14` | Draconato | Clérigo | `draconato_clerigo_female.png` | `draconato_clerigo_female.png` |
| `PROT-15` | Draconato | Paladino | `draconato_paladino_male.png` | `draconato_paladino_male.png` |
| `PROT-16` | Draconato | Mago | `draconato_mago_male.png` | `draconato_mago_male.png` |
| `PROT-17` | Draconato | Patrulheiro | `draconato_patrulheiro_female.png` | `draconato_patrulheiro_female.png` |
| `PROT-18` | Draconato | Ladino | `draconato_ladino_male.png` | `draconato_ladino_male.png` |
| `PROT-19` | Elfo da Floresta | Guerreiro | `elfo_guerreiro_male.png` | `elfo_guerreiro_male.png` |
| `PROT-20` | Elfo da Floresta | Clérigo | `elfo_clerigo_female.png` | `elfo_clerigo_female.png` |
| `PROT-21` | Elfo da Floresta | Paladino | `elfo_paladino_male.png` | `elfo_paladino_male.png` |
| `PROT-22` | Elfo da Floresta | Mago | `elfo_mago_female.png` | `elfo_mago_female.png` |
| `PROT-23` | Elfo da Floresta | Patrulheiro | `elfo_patrulheiro_male.png` | `elfo_patrulheiro_male.png` |
| `PROT-24` | Elfo da Floresta | Ladino | `elfo_ladino_female.png` | `elfo_ladino_female.png` |
| `PROT-25` | Halfling | Guerreiro | `halfling_guerreiro_male.png` | `halfling_guerreiro_male.png` |
| `PROT-26` | Halfling | Clérigo | `halfling_clerigo_female.png` | `halfling_clerigo_female.png` |
| `PROT-27` | Halfling | Paladino | `halfling_paladino_male.png` | `halfling_paladino_male.png` |
| `PROT-28` | Halfling | Mago | `halfling_mago_male.png` | `halfling_mago_male.png` |
| `PROT-29` | Halfling | Patrulheiro | `halfling_patrulheiro_male.png` | `halfling_patrulheiro_male.png` |
| `PROT-30` | Halfling | Ladino | `halfling_ladino_female.png` | `halfling_ladino_female.png` |
| `PROT-31` | Meio-Orc | Guerreiro | `meio_orc_guerreiro_male.png` | `meio_orc_guerreiro_male.png` |
| `PROT-32` | Meio-Orc | Clérigo | `meio_orc_clerigo_male.png` | `meio_orc_clerigo_male.png` |
| `PROT-33` | Meio-Orc | Paladino | `meio_orc_paladino_male.png` | `meio_orc_paladino_male.png` |
| `PROT-34` | Meio-Orc | Mago | `meio_orc_mago_male.png` | `meio_orc_mago_male.png` |
| `PROT-35` | Meio-Orc | Patrulheiro | `meio_orc_patrulheiro_male.png` | `meio_orc_patrulheiro_male.png` |
| `PROT-36` | Meio-Orc | Ladino | `meio_orc_ladino_female.png` | `meio_orc_ladino_female.png` |
| `PROT-37` | Tiefling | Guerreiro | `tiefling_guerreiro_male.png` | `tiefling_guerreiro_male.png` |
| `PROT-38` | Tiefling | Clérigo | `tiefling_clerigo_female.png` | `tiefling_clerigo_female.png` |
| `PROT-39` | Tiefling | Paladino | `tiefling_paladino_male.png` | `tiefling_paladino_male.png` |
| `PROT-40` | Tiefling | Mago | `tiefling_mago_male.png` | `tiefling_mago_male.png` |
| `PROT-41` | Tiefling | Patrulheiro | `tiefling_patrulheiro_female.png` | `tiefling_patrulheiro_female.png` |
| `PROT-42` | Tiefling | Ladino | `tiefling_ladino_female.png` | `tiefling_ladino_female.png` |

