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

### [PROT-35] Protagonista Meio-Orc Patrulheiro (Rastreador dos Ermos Ferozes)
* **Diferença dos Patrulheiros Aliados:** Caçador veterano e implacável das tundras e estepes cinzentas. Pele verde-oliva acinzentada marcada por escarificações rituais de caça e pinturas de guerra em ocre, presas inferiores irregulares reforçadas com aros de arame de bronze, coque de guerreiro alto preso com tendão e atravessado por uma garra de urso das cavernas. Veste couraça de couro pesado de mamute rebitada com escamas de serpe e tachas de ferro batido, manto assimétrico de pele de lobo atroz sobre o ombro direito preso por fivela de crânio de fera em ferro negro, bandoleira de dardos com pontas de osso entalhado. Empunha um arco recurvo de guerra colossal de chifre de monstro e madeira negra reforçado com tendões, puxando uma flecha pesada com ponta de obsidiana farpada; na cintura, traz um facão serrilhado de desossar com cabo de osso.
* **Sprite:** `assets/sprites/heroes/meio_orc_patrulheiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/meio_orc_patrulheiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male half-orc beast-tracker ranger protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 dynamic stalking stance, weathered ash-olive skin, tribal ritual scars across brow, sharp lower tusks bound in bronze wire, high warrior topknot tied with sinew and pierced by a cave-bear claw, heavy mammoth-leather brigandine with dark wyvern scales and forged iron rivets, asymmetrical dire-wolf fur pelt over right shoulder fastened by an iron wolf-skull buckle, drawing a massive recurve war bow crafted from blackened horn and darkwood with sinew wrapping, nocking a heavy barbed hunting arrow with black obsidian broadhead, serrated bone-handled gutting cleaver at hip, bandolier of bone-tipped hunting darts, crisp pixel outlines, gritty chiaroscuro shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token - Midjourney v6):**
```text
Detailed 2.5D pixel art portrait icon of male half-orc ranger protagonist, 32-bit dark fantasy avatar, intense piercing amber predator eyes, weathered ash-olive skin with deep ritual hunt scarification across cheekbone and brow, sharp lower tusks bound in bronze wire, coarse black hair tied in topknot with bone pins, thick dire-wolf fur mantle collar with iron wolf-skull clasp, dramatic low-angle torchlight dithering, enclosed within a thick square chiseled weathered granite and iron studs pixel art border flush to the canvas edges, full-bleed edge-to-edge square framing, solid dark pitch-black background extending completely into all four corners without any white space or margins --v 6.0 --ar 1:1 --stylize 250 --no white background, white corners, circular frame, rounded corners, white margins, empty borders, vignette, smooth, 3d, cgi, text, watermark
```
* **Prompt SDXL / Flux.1 (Sprite):**
```text
masterpiece 2.5D pixel art sprite, male half-orc ranger tracker, ash-olive skin, ritual scarification, tusk rings, mammoth-leather brigandine with wyvern scales, dire-wolf fur mantle, massive horn recurve war bow with obsidian barbed arrow, 32-bit tactical RPG angle, crisp pixel clusters, gritty chiaroscuro dithering, isolated on solid black background
```
* **Prompt SDXL / Flux.1 (Retrato 128x128):**
```text
masterpiece 2.5D pixel art portrait icon, male half-orc ranger protagonist, intense amber eyes, ritual scars, tusks bound in bronze wire, dire-wolf fur collar, 32-bit retro tactical RPG token, full-bleed square portrait, thick square pixel art border flush to canvas edge, solid pure black background in all corners, no white margins, chiaroscuro lighting
```

---

### [PROT-36] Protagonista Meio-Orc Ladina (Bruta das Sombras)
* **Diferença dos Ladinos Aliados:** Uma assassina furtiva de impacto devastador e agilidade física incomparável. Pele verde-ardósia escura, têmporas e laterais da cabeça raspadas com dreadlocks grossos presos por anéis de ferro escurecido, presas inferiores afiadas como agulhas entalhadas com ranhuras de contagem ritual, olhos ferozes cor de cobre-âmbar sob pintura facial de fuligem ao redor dos olhos. Veste gibão ajustado de couro preto flexível curtido a carvão com placas de aço escurecido nos ombros, gola alta de linho negro dobrada como meia-máscara, luvas sem dedos com nós dos dedos reforçados por bronze. Empunha duas machadinhas de arremesso em aço escurecido com gumes serrilhados e lâminas barbudas em guarda cruzada ágil, além de um facão curvo de decepar tendões preso à coxa.
* **Sprite:** `assets/sprites/heroes/meio_orc_ladino_female.png`
* **Retrato:** `assets/sprites/heroes/icones/meio_orc_ladino_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female half-orc shadow enforcer rogue protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 agile low-crouched ambush stance, athletic muscular silhouette, dark slate-green skin, side-shaved hair with thick dreadlocks bound in blackened-iron bands, sharp needle-pointed lower tusks etched with tally marks, charcoal warpaint mask across eyes, form-fitting oil-treated matte-black leather cuirass with blackened steel shoulder plates, midnight linen cowl pulled to collar, dual-wielding blackened-steel bearded throwing hatchets with serrated edges, curved tendon-cleaving trench knife strapped to thigh, fingerless knuckle-reinforced brawler gloves, dynamic cold moonlight chiaroscuro dithering, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token - Midjourney v6):**
```text
Detailed 2.5D pixel art portrait icon of female half-orc rogue protagonist, 32-bit dark fantasy avatar, cold calculating copper-amber eyes, dark slate-green skin, sharp needle-pointed tusks etched with ritual tally notches, charcoal stealth warpaint around eye sockets, side-shaved dreadlocks with dark metal rings, high matte-black leather collar with studded rivets, harsh angular moonlit edge lighting, enclosed within a thick square blackened forged-steel pixel art border flush to the canvas edges, full-bleed edge-to-edge square framing, solid dark pitch-black background extending completely into all four corners without any white space or margins --v 6.0 --ar 1:1 --stylize 250 --no white background, white corners, circular frame, rounded corners, white margins, empty borders, vignette, smooth, 3d, cgi, text, watermark
```
* **Prompt SDXL / Flux.1 (Sprite):**
```text
masterpiece 2.5D pixel art sprite, female half-orc rogue assassin, slate-green skin, dreadlocks with iron rings, charcoal eye warpaint, matte-black leather cuirass, dual serrated throwing hatchets, 32-bit tactical RPG angle, crisp pixel clusters, high-contrast moonlit dithering, isolated on solid black background
```
* **Prompt SDXL / Flux.1 (Retrato 128x128):**
```text
masterpiece 2.5D pixel art portrait icon, female half-orc rogue protagonist, copper-amber eyes, charcoal warpaint, engraved tusks, side-shaved dreadlocks, studded black collar, 32-bit retro tactical RPG token, full-bleed square portrait, thick square pixel art border flush to canvas edge, solid pure black background in all corners, no white margins, moonlight chiaroscuro
```

---

## 8. Linhagem Tiefling (6 Arquétipos do Jogador)

---

### [PROT-37] Protagonista Tiefling Guerreiro (Cavaleiro do Fogo Fátuo)
* **Diferença dos Guerreiros Aliados:** Um tirano de batalha implacável forjado no calor infernal. Pele carmesim-sangue escura com escamas sutis de obsidiana nas maçãs do rosto, par de chifres maciços e anelados de obsidiana que se projetam para cima como uma coroa recortada gravada com runas que brilham em brasa rubra, olhos cor de latão incandescente sem pupilas exalando filamentos sutis de fumaça. Veste armadura articulada pesada de ferro gusa bruto com fissuras térmicas por onde brilha magma líquido, gorjal espinhoso no formato de queixada demoníaca, ombreiras serrilhadas, cauda espessa terminada em lâmina afiada de ferro. Empunha uma montante brutal de lâmina ondulada estilo flamberge em ferro negro que verte brasas e chamas laranjas, acompanhada de um pesado escudo de torre retangular com rebites de ferro forjado.
* **Sprite:** `assets/sprites/heroes/tiefling_guerreiro_male.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_guerreiro_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male tiefling hellknight juggernaut warrior protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 imposing heavy battle stance, dark blood-crimson skin with obsidian micro-scales on temples, massive sweeping ribbed obsidian horns carved with glowing ember-hot infernal runes, pupil-less molten-brass demonic eyes venting faint smoke, heavy articulated cast-iron plate armor with glowing red volcanic fissure lines, spiked segmented pauldrons, demon-jaw gorget, thick spade-bladed tail coiled low, wielding a colossal wavy flamberge broadsword dripping orange glowing embers and sparks, heavy square iron-banded tower shield on off-hand, crisp pixel outlines, infernal furnace chiaroscuro dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token - Midjourney v6):**
```text
Detailed 2.5D pixel art portrait icon of male tiefling warrior protagonist, 32-bit dark fantasy avatar, glowing pupil-less molten-brass eyes with curling smoke wisps, dark blood-crimson skin, heavy ribbed obsidian horns engraved with glowing red runes, articulated cast-iron gorget with smoldering internal heat vents, fierce angular jawline, intense furnace-light rim dithering, enclosed within a thick square scorched black-iron and glowing rivet pixel art border flush to the canvas edges, full-bleed edge-to-edge square framing, solid dark pitch-black background extending completely into all four corners without any white space or margins --v 6.0 --ar 1:1 --stylize 250 --no white background, white corners, circular frame, rounded corners, white margins, empty borders, vignette, smooth, 3d, cgi, text, watermark
```
* **Prompt SDXL / Flux.1 (Sprite):**
```text
masterpiece 2.5D pixel art sprite, male tiefling hellknight warrior, blood-crimson skin, runic ribbed obsidian horns, cast-iron plate armor with glowing magma veins, ember flamberge greatsword, heavy square iron shield, 32-bit tactical RPG angle, crisp pixel clusters, volcanic fire dithering, isolated on solid black background
```
* **Prompt SDXL / Flux.1 (Retrato 128x128):**
```text
masterpiece 2.5D pixel art portrait icon, male tiefling warrior protagonist, glowing molten brass eyes, blood-crimson skin, runic horns, smoldering iron gorget, 32-bit retro tactical RPG token, full-bleed square portrait, thick square pixel art border flush to canvas edge, solid pure black background in all corners, no white margins, furnace chiaroscuro
```

---

### [PROT-38] Protagonista Tiefling Clériga (Domínio do Fogo / Luz)
* **Diferença dos Clérigos Aliados:** Uma sacerdotisa solene que consagrou suas chamas ancestrais à liturgia sagrada da redenção. Pele lilás-cinzenta com finas escarificações litúrgicas em prata ao redor dos olhos, chifres delgados em espiral graciosa adornados com correntes finas de prata e berloques votivos, olhos prateados incandescentes e serenos. Veste cota de malha fosca sob vestes monásticas de veludo azul-profundo e estola sacerdotal carmesim bordada a ouro com versículos da chama divina; empunha um báculo de ferro forjado culminando em uma lanterna gótica hexagonal com uma chama sagrada dourada viva, e um escudo aquecedor de prata polida marcado em relevo com o cálice sagrado.
* **Sprite:** `assets/sprites/heroes/tiefling_clerigo_female.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_clerigo_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female tiefling sacred pyre cleric protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 solemn liturgical battle stance, soft lavender-grey skin with faint silver devotional scarification, elegant backwards-curving spiral horns draped in delicate silver reliquary chains and charms, glowing translucent silver-white eyes, blackened steel chainmail under midnight-blue robes with deep crimson stole embroidered in gold flame scriptures, gripping a forged-iron holy scepter topped with a gothic brazier cage sheltering a perpetual bright golden divine flame, polished mirror-sheen silver heater shield bearing an embossed sunburst chalice, slender tail draped gracefully, crisp pixel outlines, radiant holy fire dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token - Midjourney v6):**
```text
Detailed 2.5D pixel art portrait icon of female tiefling cleric protagonist, 32-bit dark fantasy avatar, serene glowing silver-white eyes, pale lavender-grey skin with fine silver prayer scars, spiral horns draped with miniature silver prayer chains, embroidered crimson silk liturgical cowl, soft golden radiance from holy flame reflecting warmly on cheek and forehead, enclosed within a thick square engraved antique silver and sanctified iron pixel art border flush to the canvas edges, full-bleed edge-to-edge square framing, solid dark pitch-black background extending completely into all four corners without any white space or margins --v 6.0 --ar 1:1 --stylize 250 --no white background, white corners, circular frame, rounded corners, white margins, empty borders, vignette, smooth, 3d, cgi, text, watermark
```
* **Prompt SDXL / Flux.1 (Sprite):**
```text
masterpiece 2.5D pixel art sprite, female tiefling cleric of holy pyre, lavender-grey skin, spiral horns with silver chains, midnight-blue and crimson robes, holy brazier scepter with golden divine flame, silver sunburst shield, 32-bit tactical RPG angle, crisp pixel clusters, radiant chiaroscuro dithering, isolated on solid black background
```
* **Prompt SDXL / Flux.1 (Retrato 128x128):**
```text
masterpiece 2.5D pixel art portrait icon, female tiefling cleric protagonist, glowing silver-white eyes, lavender skin, chained horns, embroidered crimson stole, 32-bit retro tactical RPG token, full-bleed square portrait, thick square pixel art border flush to canvas edge, solid pure black background in all corners, no white margins, divine flame lighting
```

---

### [PROT-39] Protagonista Tiefling Paladino (Juramento da Redenção)
* **Diferença dos Paladinos Aliados:** Um penitente sagrado que jurou quebrar as correntes da tirania infernal. Pele vermelho-fuligem escura, chifres compridos curvados para trás envoltos em faixas de pergaminho sagrado com orações em caligrafia dourada afixadas por pregos rituais de ferro, olhos dourados de compaixão severa com cicatriz vertical sobre o supercílio esquerdo. Veste armadura pesada de placas completas de aço revestida por esmalte branco desgastado de batalha com biséis de latão martelado inscritos com votos de proteção, capa grossa de lã crua cor de marfim com fecho de sol radiante em bronze, empunhando uma maça de guerra flangeada pulsando luz solar dourada ofuscante e escudo gota de aço esmaltado exibindo o relevo de uma espada partida.
* **Sprite:** `assets/sprites/heroes/tiefling_paladino_male.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_paladino_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male tiefling redemption paladin champion protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 unyielding heroic stance, dusky ash-rose skin, backwards-sweeping horns bound tight in white vellum scripture banners inscribed with golden litanies and iron devotional nails, noble sorrowful golden eyes with vertical dueling scar over left brow, heavy battle-worn plate armor of ivory-white enamel over dark steel with chased brass edges, coarse off-white wool cloak with heavy bronze sunburst clasp, wielding a heavy flanged holy war-mace pulsing with radiant solar dawnlight, pristine kite shield bearing an embossed broken sword emblem, crisp pixel outlines, celestial solar dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token - Midjourney v6):**
```text
Detailed 2.5D pixel art portrait icon of male tiefling paladin protagonist, 32-bit dark fantasy avatar, steadfast compassionate golden eyes, dusky ash-rose skin, scar over left eye, horns wrapped in sacred vellum scripture ribbons with golden calligraphy, weathered ivory-enamel and brass gorget, warm celestial solar backlight illuminating brow, enclosed within a thick square hammered ivory-enamel and burnished brass pixel art border flush to the canvas edges, full-bleed edge-to-edge square framing, solid dark pitch-black background extending completely into all four corners without any white space or margins --v 6.0 --ar 1:1 --stylize 250 --no white background, white corners, circular frame, rounded corners, white margins, empty borders, vignette, smooth, 3d, cgi, text, watermark
```
* **Prompt SDXL / Flux.1 (Sprite):**
```text
masterpiece 2.5D pixel art sprite, male tiefling redemption paladin, ash-rose skin, scripture-wrapped horns, ivory-white plate armor with brass trim, radiant solar flanged war-mace, broken sword kite shield, 32-bit tactical RPG angle, crisp pixel clusters, celestial light dithering, isolated on solid black background
```
* **Prompt SDXL / Flux.1 (Retrato 128x128):**
```text
masterpiece 2.5D pixel art portrait icon, male tiefling paladin protagonist, compassionate golden eyes, scarred brow, scripture-bound horns, ivory-enamel gorget, 32-bit retro tactical RPG token, full-bleed square portrait, thick square pixel art border flush to canvas edge, solid pure black background in all corners, no white margins, solar rim light
```

---

### [PROT-40] Protagonista Tiefling Mago (Evocador Infernal)
* **Diferença do Aliado Azaroth:** Um conjurador aristocrático das forças cósmicas e do abismo que canaliza energia bruta através de foco alquímico. Pele carmesim-viva com minúsculas escamas pretas brilhantes nas têmporas e queixo, chifres recurvados imponentes de obsidiana lapidada entalhados com runas abissais fluorescentes em ametista, olhos violeta incandescentes com pupilas em fenda felina, cabelos negros compridos presos em coque acadêmico alto com alfinete de osso esculpido. Veste casaco ajustado de couro de dragão negro com gola alta espetada forrado em seda púrpura imperial, bandoleira com filactérias de vidro fundido cheias de essências arcanas brilhantes, grimório flutuante com fecho de crânio em bronze irradiando círculos concêntricos de runas arcanas roxas enquanto suas mãos estalando canalizam arcos de relâmpagos violeta e plasma ardente.
* **Sprite:** `assets/sprites/heroes/tiefling_mago_male.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_mago_male.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, male tiefling abyssal evoker wizard protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 floating dynamic casting stance, rich blood-crimson skin with fine obsidian scales along cheekbones, sweeping crown-like horns of polished obsidian etched with glowing amethyst abyssal runes, burning slit-pupil violet eyes, raven-black hair tied in high scholar topknot with carved demon-bone hairpin, tailored black dragon-hide coat with pointed high collar and royal-purple silk lining, bandolier of glowing alchemical phylacteries, floating brass-skull grimoire radiating violet runic script, dual-channeling crackling bifurcated purple lightning arcs and dark flame plasma from clawed fingers, whip-like spade tail, crisp pixel outlines, eldritch flame dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token - Midjourney v6):**
```text
Detailed 2.5D pixel art portrait icon of male tiefling wizard protagonist, 32-bit dark fantasy avatar, intense burning violet slit eyes, blood-crimson skin with obsidian facial scales, sweeping black horns etched with glowing violet runes, high pointed black dragon-leather collar with royal-purple lapel, eerie purple plasma backlighting illuminating sharp cheekbones, enclosed within a thick square obsidian and runic dark-bronze pixel art border flush to the canvas edges, full-bleed edge-to-edge square framing, solid dark pitch-black background extending completely into all four corners without any white space or margins --v 6.0 --ar 1:1 --stylize 250 --no white background, white corners, circular frame, rounded corners, white margins, empty borders, vignette, smooth, 3d, cgi, text, watermark
```
* **Prompt SDXL / Flux.1 (Sprite):**
```text
masterpiece 2.5D pixel art sprite, male tiefling abyssal wizard evoker, blood-crimson skin, runic obsidian horns, dragon-leather high-collar coat, floating brass skull grimoire, bifurcated purple lightning arcs, 32-bit tactical RPG angle, crisp pixel clusters, arcane plasma dithering, isolated on solid black background
```
* **Prompt SDXL / Flux.1 (Retrato 128x128):**
```text
masterpiece 2.5D pixel art portrait icon, male tiefling wizard protagonist, slit violet eyes, obsidian scales, runic horns, dragon-leather collar, 32-bit retro tactical RPG token, full-bleed square portrait, thick square pixel art border flush to canvas edge, solid pure black background in all corners, no white margins, purple eldritch lighting
```

---

### [PROT-41] Protagonista Tiefling Patrulheira (Caçadora dos Ermos Vulcânicos)
* **Diferença dos Patrulheiros Aliados:** Uma perseguidora mortal acostumada a sobreviver em caldeiras vulcânicas e desertos de cinzas asfixiantes. Pele púrpura-vulcânica escura salpicada com poeira de cinzas, chifres delgados varridos para trás rente ao crânio envoltos em tiras de couro e penas negras de corvo, olhos predatórios cor de enxofre com pupilas em fenda e pinturas tribais de cinza em divisas no nariz. Veste couraça de couro escamado de quimera com ombreiras de osso fossilizado negro, meia-capa com capuz desfiado manchada de fuligem, braçadeiras de arqueiro em couro escurecido. Empunha um arco recurvo pesado forjado em ferro negro e osso de monstro com roldanas de latão, disparando flechas de ponta de sílex embebidas em óleo incandescente que ardem em fumaça espessa; aljava no quadril com flechas de empenagem preta e cauda delgada armada com ponta cortante.
* **Sprite:** `assets/sprites/heroes/tiefling_patrulheiro_female.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_patrulheiro_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female tiefling ashland apex ranger protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 low stalking archery stance, dusky volcanic-purple skin dusted with grey soot, sleek swept-back horns wrapped in weathered leather bands with raven feathers, predatory sulfur-yellow slit eyes with tribal ash chevron marks on nose bridge, scaled chimera-hide cuirass reinforced with charred black bone pauldrons, tattered soot-grey travel cowl and half-cloak, drawing a heavy recurve war bow of blackened iron and fossil horn, nocking a flint-tipped broadhead arrow igniting with fiery pitch and trailing dark smoke, hip quiver of black-fletched arrows, sinewy bladed tail, crisp pixel outlines, ember smoke chiaroscuro dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token - Midjourney v6):**
```text
Detailed 2.5D pixel art portrait icon of female tiefling ranger protagonist, 32-bit dark fantasy avatar, predatory luminous sulfur-yellow slit eyes, dusky volcanic-purple skin, chevron ash warpaint across nose bridge, sleek horns wrapped in dark leather with feather charms, soot-grey cowl collar, drifting burning ember particles casting warm directional light, enclosed within a thick square scorched basalt stone and iron rivet pixel art border flush to the canvas edges, full-bleed edge-to-edge square framing, solid dark pitch-black background extending completely into all four corners without any white space or margins --v 6.0 --ar 1:1 --stylize 250 --no white background, white corners, circular frame, rounded corners, white margins, empty borders, vignette, smooth, 3d, cgi, text, watermark
```
* **Prompt SDXL / Flux.1 (Sprite):**
```text
masterpiece 2.5D pixel art sprite, female tiefling ashland ranger, volcanic-purple skin, sleek wrapped horns, sulfur-yellow eyes, chimera-hide armor, charred bone pauldrons, blackened iron war bow with smoking fire arrow, soot cloak, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```
* **Prompt SDXL / Flux.1 (Retrato 128x128):**
```text
masterpiece 2.5D pixel art portrait icon, female tiefling ranger protagonist, sulfur-yellow slit eyes, ash warpaint, wrapped horns, soot-grey cowl collar, 32-bit retro tactical RPG token, full-bleed square portrait, thick square pixel art border flush to canvas edge, solid pure black background in all corners, no white margins, ember glow lighting
```

---

### [PROT-42] Protagonista Tiefling Ladina (Sombra Infernal)
* **Diferença dos Ladinos Aliados:** Uma infiltradora felina e ladra acrobática sem rival em arrombamentos de tesouros arcanos e criptas lacradas. Pele obsidiana com reflexos de vinho escuro, chifres curvos esguios que despontam graciosamente através de um capuz recortado sob medida, olhos brilhantes cor de topázio incandescente vigiando por trás de um véu semitransparente de seda preta cobrindo boca e queixo, tranças pretas ajustadas com ganzuas de prata e ganchos embutidos. Veste gibão colado ao corpo de couro fosco lubrificado e sem rebites barulhentos, bandoleira de agulhas de arremesso, cauda preênsil flexível que manipula com astúcia um chaveiro de bronze com chave mestra roubada, enquanto as mãos empunham dois estiletes de perfuração em aço azulado em pegada invertida rápida.
* **Sprite:** `assets/sprites/heroes/tiefling_ladino_female.png`
* **Retrato:** `assets/sprites/heroes/icones/tiefling_ladino_female.png`
* **Prompt Sprite (Midjourney v6):**
```text
Full-body player character battle sprite, female tiefling shadow phantom rogue protagonist, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 acrobatic stealth prowl stance, deep obsidian-maroon skin, slender pointed horns poking precisely through a fitted matte-black cowl, glowing incandescent topaz-yellow eyes behind a gossamer black veil half-mask, tight braided dark hair interwoven with silver lockpicks, form-fitting silent oiled leather brigandine with muffled joints, prehensile spade-tipped tail deftly twirling a stolen glowing brass skeleton key, dual-wielding needle-thin triangular blued-steel stiletto daggers in reverse assassination grip, bandolier of throwing needles, soft-soled shadow boots, crisp pixel outlines, high-contrast moonlit shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
* **Prompt Retrato (128x128 Token - Midjourney v6):**
```text
Detailed 2.5D pixel art portrait icon of female tiefling rogue protagonist, 32-bit dark fantasy avatar, piercing incandescent topaz eyes, deep obsidian-maroon skin, sleek horns piercing through black leather cowl, sheer black veil mask over mouth and nose, silver lockpick charms in hair, oiled leather collar, high-contrast cool moonlight rim lighting, enclosed within a thick square blued-steel and studded dark-leather pixel art border flush to the canvas edges, full-bleed edge-to-edge square framing, solid dark pitch-black background extending completely into all four corners without any white space or margins --v 6.0 --ar 1:1 --stylize 250 --no white background, white corners, circular frame, rounded corners, white margins, empty borders, vignette, smooth, 3d, cgi, text, watermark
```
* **Prompt SDXL / Flux.1 (Sprite):**
```text
masterpiece 2.5D pixel art sprite, female tiefling rogue infiltrator, obsidian-maroon skin, slender horns through cowl, topaz eyes, sheer veil mask, prehensile tail with skeleton key, twin blued-steel stiletto daggers, 32-bit tactical RPG angle, crisp pixel clusters, moonlit shadow dithering, isolated on solid black background
```
* **Prompt SDXL / Flux.1 (Retrato 128x128):**
```text
masterpiece 2.5D pixel art portrait icon, female tiefling rogue protagonist, luminous topaz eyes, sheer veil mask, horns through hood, silver lockpicks in hair, 32-bit retro tactical RPG token, full-bleed square portrait, thick square pixel art border flush to canvas edge, solid pure black background in all corners, no white margins, moonlight chiaroscuro
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

