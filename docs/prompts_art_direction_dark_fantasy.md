# Manual Canônico de Direção de Arte e Engenharia de Prompts: 2.5D Dark Fantasy Pixel Art (D&D 5e)

**Projeto:** RPGMesaPY  
**Estilo Canônico:** 2.5D HD Pixel Art / 32-bit Dark Fantasy (Inspirações: *Blasphemous*, *Octopath Traveler*, *Tactics Ogre: Reborn*, *Diablo I & II*)  
**Finalidade:** Guia mestre de prompts prontos para geração em ferramentas de IA (Midjourney v6, SDXL, Flux.1) para integração direta no motor gráfico Pygame.

---

## 1. O Padrão Visual Canônico (Blueprint de Direção de Arte em Pixel Art 2.5D)

Todas as artes do projeto — incluindo sprites de batalha, ícones de interface, retratos de diálogo e fundos de cenário — devem seguir **rigorosa e exclusivamente** a diretriz estética de **Pixel Art 2.5D Dark Fantasy**:

1. **Estilo Geral (32-bit / HD Pixel Art):**
   - Gráficos no estilo *tactical HD pixel art* de era 32-bit avançada.
   - Proibições estritas: pinturas digitais lisas (smooth digital painting), modelos 3D, CGI vetorial, arte anime infantilizada e filtros de desfoque/anti-aliasing suaves.
   - Texturas palpáveis compostas por *clusters* bem definidos de pixels, simulando peso tátil em aço forjado, escamas grossas de répteis, couro desgastado, ossos calcinados e madeira carcomida.

2. **Perspectiva 2.5D Tática (3/4 Isometric Battle View):**
   - Sprites de combate posicionados em ângulo de três quartos (3/4 perspective / tactical RPG battle angle), com leve inclinação isométrica para evidenciar profundidade, volume dos ombros, largura das bases e armas em riste.
   - Cenários construídos com profundidade de camadas (*layered pixel depth*), distinguindo primeiro plano tático, plano médio de combate e plano de fundo atmosférico.

3. **Clusterização & Dithering Chiaroscuro:**
   - Contornos escuros e nítidos de pixels (*crisp pixel outlines*) sem sangramento ou borrões.
   - Transições de sombra e luz feitas através de *ordered/cross-hatch pixel dithering*, garantindo sombreamento dramático (*chiaroscuro* de fantasia sombria).
   - Pontos de luz dinâmicos (brasas incandescentes, brilho arcano de runas e fogo fátuo) contrastando contra sombras de carvão e ferro fundido.

4. **Paleta de Cores Sóbria & Opressiva:**
   - Cores primárias dominantes: Carvão (`#1b1c1e`), obsidiana (`#111215`), ferro oxidado (`#4a3f35`), sangue coagulado (`#5c141a`), pergaminho envelhecido (`#bda57b`) e osso (`#ded1c1`).
   - Cores de destaque (*accent lights*): Laranja incandescente de magma/brasas (`#ff5a1f`), azul etéreo espectral (`#38bdf8`) e púrpura necromântico (`#9333ea`).

5. **Negative Prompt Universal Obrigatório:**
   > `smooth digital painting, 3d render, cgi, vector art, smooth gradients, flat modern minimalism, oversaturated cartoon, anime, chibi, blurry anti-aliasing, photorealistic, photo, watermark, signature, modern clothing, neon colors, duplicate limbs, distorted hands`

---

## 2. Bestiário Completo: Sprites de Monstros e Inimigos em Pixel Art 2.5D

> **Instrução de Integração:** Todos os sprites de inimigos devem ser isolados em fundo sólido escuro/preto puro (`isolated on solid pure dark background`) para permitir remoção de fundo com canal alfa e importação direta em `assets/sprites/enemies/`.

---

### [MON-01] Dragão Supremo: O Tirano das Cinzas (Boss Final Colossal)
- **Arquivo Destino:** `assets/sprites/enemies/supreme_dragon.png`
- **Resolução de Render:** 512x512 pixels (Sprite Colossal)
- **Prompt Midjourney v6:**
```text
Colossal ancient dark fantasy supreme dragon sprite, The Tyrant of Ashes, 2.5D HD pixel art, 32-bit tactical RPG battle view, 3/4 isometric perspective, massive obsidian armored scales textured with pixel dithering, glowing incandescent magma veins pulsing through chest and wings, colossal horned draconic head exhaling smoking cinders, jagged volcanic spine, heavy razor-sharp black talons, crisp pixel outlines, handcrafted pixel clusters, Blasphemous and Tactics Ogre aesthetic, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, 32-bit retro tactical RPG sprite of a colossal ancient supreme dragon, dark fantasy, obsidian scales, cracked molten lava veins, dramatic chiaroscuro pixel dithering, 3/4 battle angle, crisp dark contours, sharp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, smooth gradients, blurry, photorealistic, light background`

---

### [MON-02] Gigante do Fogo (`fire_giant.png`)
- **Arquivo Destino:** `assets/sprites/enemies/fire_giant.png`
- **Resolução de Render:** 384x384 pixels (Sprite Grande)
- **Prompt Midjourney v6:**
```text
Full-body Fire Giant battle sprite, imposing brutish warrior, 2.5D HD pixel art, 32-bit tactical RPG angle, 3/4 isometric perspective, coal-grey charcoal skin, fiery glowing beard of smoking embers and pixelated flame, heavy wrought-iron plate armor etched with scorched runes, holding a colossal volcanic greatsword dripping molten slag, crisp pixel outlines, chiaroscuro dithering, dark fantasy aesthetic, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, dark fantasy Fire Giant warrior, 32-bit style, charcoal skin, incandescent flaming beard, rugged wrought-iron armor, giant heated greatsword, ordered dithering, handcrafted pixel clusters, 3/4 isometric perspective, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, blurry, high-res photo, flat shading`

---

### [MON-03] Lorde Lich (`lich.png`)
- **Arquivo Destino:** `assets/sprites/enemies/lich.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Undead ancient Lich sorcerer battle sprite, 2.5D HD pixel art, 32-bit dark fantasy RPG, 3/4 tactical battle angle, emaciated withered skeletal body draped in tattered obsidian and royal violet robes trimmed in tarnished gold, wearing a corroded spiked iron crown, bony skeletal hand grasping a twisted soul-staff topped with a glowing turquoise necromantic jewel, cold cyan flames in hollow eye sockets, ethereal necrotic aura, crisp pixel outlines, delicate dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, ancient skeletal Lich King, tattered dark purple and black robes, spiked iron crown, necromantic cyan glowing eyes, bone staff, 32-bit tactical RPG style, chiaroscuro pixel dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d cgi, smooth gradients, cartoon, anime, blurry, oversaturated`

---

### [MON-04] Quimera Monstruosa (`chimera.png`)
- **Arquivo Destino:** `assets/sprites/enemies/chimera.png`
- **Resolução de Render:** 384x384 pixels
- **Prompt Midjourney v6:**
```text
Ferocious Chimera beast battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric battle stance, muscular scarred lion torso, three terrifying heads: snarling bloodied lion, demonic black horned goat, and scaly spitting serpent dragon, leathery tattered dragon wings folded on back, tail tipped with an active viper head, crisp pixel clusters, dramatic lighting dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, mythical Chimera monster, three heads lion goat dragon, leathery wings, viper tail, dark fantasy 32-bit pixel aesthetic, crisp pixel edges, textured dithering, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector art, oversaturated cartoon, blurry, anime`

---

### [MON-05] Mantícora Alada (`manticore.png`)
- **Arquivo Destino:** `assets/sprites/enemies/manticore.png`
- **Resolução de Render:** 384x384 pixels
- **Prompt Midjourney v6:**
```text
Deadly feral Manticore monster sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 perspective, tawny muscular lion body, jagged bat-like leathery wings, grotesque demonic humanoid face with rows of needle-sharp teeth, long segmented scorpion tail loaded with lethal iron-tipped spines, predatory crouching stance, crisp pixel contours, chiaroscuro dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite of a dark fantasy Manticore, lion body, bat wings, horrific human face, scorpion tail, 32-bit tactical RPG art style, sharp pixel clusters, ordered dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cgi, vector, anime, blurry, clean lines`

---

### [MON-06] Ogro Brutal das Cavernas (`ogre.png`)
- **Arquivo Destino:** `assets/sprites/enemies/ogre.png`
- **Resolução de Render:** 384x384 pixels
- **Prompt Midjourney v6:**
```text
Savage hulking Ogre brute battle sprite, 2.5D HD pixel art, 32-bit dark fantasy RPG, 3/4 tactical battle angle, massive obese muscular frame, sickly pale-grey scarred skin, hunched posture, crude stitched hide loincloth and rusty spiked iron bracers, wielding an enormous tree-trunk club studded with jagged iron spikes, snarling crooked yellow tusks, heavy physical weight, crisp pixel outlines, gritty dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, brutal Ogre warrior sprite, 32-bit dark fantasy tactical RPG style, gigantic muscular frame, spiked wooden log club, scarred grey skin, crisp pixel clusters, cross-hatch dithering, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, chibi, smooth gradients, blurry`

---

### [MON-07] Lobo Atroz Sombrio (`dire_wolf.png`)
- **Arquivo Destino:** `assets/sprites/enemies/dire_wolf.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Ferocious giant Dire Wolf apex predator battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric battle stance, thick matted dark-grey bristling fur caked in dried mud and frost, glowing feral amber eyes, bared fangs dripping saliva, coiled muscular ready-to-pounce stance, scarred muzzle, crisp pixel outlines, cold rim light dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, dark fantasy Dire Wolf, giant predatory wolf, bristling dark grey fur, glowing yellow eyes, sharp fangs, 32-bit tactical RPG style, handcrafted pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cute dog, cartoon, anime, blurry, vector`

---

### [MON-08] Aranha Gigante das Criptas (`giant_spider.png`)
- **Arquivo Destino:** `assets/sprites/enemies/giant_spider.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Terrifying Crypt Giant Spider creature sprite, 2.5D HD pixel art, 32-bit dark fantasy RPG, 3/4 top-down tactical angle, swollen chitinous armored thorax covered in coarse dark bristles, eight long spiny jointed legs gripping stone floor, cluster of glossy black multifaceted eyes reflecting cold light, venomous glistening chelicerae dripping acidic green poison, crisp pixel contours, dramatic dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, giant arachnid monster, dark chitin exoskeleton, hairy barbed legs, dripping venom chelicerae, 32-bit tactical RPG battle view, crisp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, cartoon, anime, bright colorful, blurry`

---

### [MON-09] Cria de Vampiro Noturna (`vampire_spawn.png`)
- **Arquivo Destino:** `assets/sprites/enemies/vampire_spawn.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Feral Vampire Spawn battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 perspective, emaciated wiry muscular frame, deathly pale porcelain skin with visible dark vein clusters, ragged torn noble vestments stained with graveyard dirt, elongated bloody clawed fingers, needle fangs in a hissing snarl, predatory crimson glowing eyes, gothic chiaroscuro pixel dithering, crisp outlines, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, gothic Vampire Spawn, pale skin, blood-stained claws, crimson eyes, tattered nobleman clothes, 32-bit tactical battle angle, sharp pixel outlines, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, smooth anime, sparkling vampire, vector, blurry`

---

### [MON-10] Esqueleto Guerreiro Legionário (`skeleton.png`)
- **Arquivo Destino:** `assets/sprites/enemies/skeleton.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Undead Skeleton Warrior legionnaire battle sprite, 2.5D HD pixel art, 32-bit dark fantasy RPG, 3/4 tactical battle angle, bleached yellowed human bones held by dark necrotic sinew, corroded iron kettle helm, rotting remnants of chainmail shirt, holding a notched pitted iron shortsword and splintered wooden round shield with faded heraldry, faint cold blue embers inside hollow sockets, crisp pixel outlines, gritty bone dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, undead Skeleton soldier, rusty chainmail, iron helm, notched sword, battered round shield, 32-bit dark fantasy tactical RPG, crisp pixel clusters, bone texture dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, funny cartoon skeleton, anime, vector, blurry`

---

### [MON-11] Zumbi Pútrido das Valas (`zombie.png`)
- **Arquivo Destino:** `assets/sprites/enemies/zombie.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Shambling rotting Zombie battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 perspective, decayed greenish-grey putrid flesh with exposed bone and sinew, ragged torn peasant rags caked in grave filth, lifeless milky glazed eyes, lumbering heavy forward stumble, gnarled grasping hands with blackened nails, visceral gothic horror, crisp pixel outlines, earthy muted dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, dark fantasy decaying Zombie, shambling pose, torn filthy clothing, exposed necrotic flesh, 32-bit tactical battle view, handcrafted pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cartoon, modern zombie, anime, smooth gradients`

---

### [MON-12] Lacaio Goblin das Sombras (`goblin.png`)
- **Arquivo Destino:** `assets/sprites/enemies/goblin.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Cunning Goblin Raider battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, small wiry agile stature, mottled olive-green leathery skin, large notched bat-like ears, sharp crooked yellow teeth in a malicious grin, wearing stitched dirty leather armor scraps and rusted iron rings, wielding a jagged serrated iron dagger and a small curved bow strapped on back, dynamic sneaky crouch, crisp pixel contours, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, small agile Goblin warrior, olive green skin, pointed bat ears, ragged leather armor, serrated dagger, 32-bit tactical RPG aesthetic, sharp pixel outlines, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cute cartoon goblin, anime, vector, blurry`

---

### [MON-13] Rastreador Kobold (`kobold.png`)
- **Arquivo Destino:** `assets/sprites/enemies/kobold.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Reptilian Kobold Scout battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 perspective, small scaly humanoid with dark rust-red scales, small draconic snout with miniature backwards horns, slitted glowing orange reptilian eyes, scavenged leather harness equipped with pouches and bone traps, holding a fire-hardened hunting spear and a crude sling, hunched nervous alert posture, crisp pixel outlines, scale dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, reptilian Kobold scout sprite, reddish scales, tiny horns, spear, scavenged leather gear, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, cute lizard, anime, smooth shading`

---

### [MON-14] Bandido Fora-da-Lei Veterano (`bandit.png`)
- **Arquivo Destino:** `assets/sprites/enemies/bandit.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Hardened ruthless Bandit Highwayman battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical battle angle, middle-aged scarred human mercenary, rugged scruffy beard, cold calculating glare, wearing boiled brown leather brigandine with studded iron bracers and a weather-beaten dark tattered hooded cowl, wielding a notched iron scimitar and a concealed dagger, combat-ready stance, crisp pixel outlines, grounded muted colors, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, gritty dark fantasy Bandit warrior, scarred face, dark hooded cloak, studded leather armor, curved scimitar, 32-bit tactical RPG style, handcrafted pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, bright colorful, smooth gradients`

---

### [MON-15] Kraken Abissal das Profundezas (`kraken.png`)
- **Arquivo Destino:** `assets/sprites/enemies/kraken.png`
- **Resolução de Render:** 512x512 pixels (Sprite Colossal)
- **Prompt Midjourney v6:**
```text
Abyssal Eldritch Kraken sea terror battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 perspective rising from churning dark water, monstrous bloated cephalopod mantle with barnacles and dark oceanic scales, massive writhing barbed tentacles with glowing bioluminescent deep-sea suckers, horrific predatory beak surrounded by multiple cold black compound eyes, dark stormy mist, crisp pixel contours, oceanic chiaroscuro dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, colossal dark fantasy Kraken monster, writhing barbed tentacles, bioluminescent suckers, leviathan beak, 32-bit tactical RPG aesthetic, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cartoon squid, vector, anime, blurry, photorealistic`

---

### [MON-16] Mímico Voraz do Calabouço (`mimic.png`)
- **Arquivo Destino:** `assets/sprites/enemies/mimic.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Monstrous Mimic Chest creature battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric perspective, antique dark oak treasure chest with ornate wrought-iron bands cracking open into a grotesque gaping maw, rows of jagged irregular human-like yellow teeth, long dripping purple fleshy tongue extending outwards, predatory glistening pseudopod eyes emerging from the wood grain, crisp pixel outlines, wood and saliva dithering, isolated on solid black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, dark fantasy Mimic monster disguised as a treasure chest bursting with teeth and huge sticky purple tongue, iron fittings, 32-bit tactical RPG style, crisp pixel edges, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cute cartoon chest, vector, anime, blurry`

---

## 3. Compêndio Canônico de Heróis e Aliados: 42 Heróis Únicos (7 Raças x 6 Classes)

> **Diretriz de Identidade e Motor da História:**  
> Esta seção apresenta os **42 heróis e aliados únicos** do RPGMesaPY. Nenhum personagem é genérico: cada um possui **nome canônico, epíteto épico, marcas físicas de batalha, armas forjadas sob medida e personalidade visual marcante**.  
> - **Sprites de Corpo Inteiro:** `assets/sprites/heroes/{raca}_{classe}_{genero}.png` (256x256 pixels, ângulo 3/4 tático isométrico).  
> - **Ícones de Retrato (HUD / Fichas):** `assets/sprites/heroes/icones/{raca}_{classe}_{genero}.png` (128x128 pixels, moldura de pixel art em ferro forjado, pedra ou ouro envelhecido).

---

### 3.1 Linhagem Humana (`humano_*.png`)

---

#### [HERO-01] Sir Alistair Valerius, o Cavaleiro da Vigília Quebrada
- **Classe:** Guerreiro (Cavaleiro) | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/humano_cavaleiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/humano_cavaleiro_male.png`
- **Detalhes Visuais Únicos:** Cicatriz vertical sobre o olho esquerdo cego, mecha grisalha no cabelo preto cortado curto, armadura de placas de aço escovado com arranhões de garras dracônicas no peitoral, capa azul-marinho rasgada com broche de grifo em bronze oxidado.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Sir Alistair Valerius, human knight veteran, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric battle stance, scarred rugged face with blind milky left eye, heavy brushed steel plate armor with claw gouges on breastplate, tattered navy-blue cape with bronze griffin brooch, resting both hands on the pommel of an ancestral two-handed greatsword grounded on cobblestone, heater shield on back, crisp pixel outlines, metallic reflections dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Sir Alistair Valerius, male human knight, 32-bit dark fantasy avatar, stern weathered face, scarred blind eye, short black hair with streak of silver, steel gorget with bronze studs, dramatic chiaroscuro lighting, framed by a rusted iron knightly chain pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, Sir Alistair human knight, scarred veteran, battle-worn steel plate armor, claw marks, ancestral greatsword, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, young boy, clean armor, blurry`

---

#### [HERO-02] Padre Lucien, o Confessor das Chamas Sagradas
- **Classe:** Clérigo | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/humano_clerigo_male.png`
- **Ícone:** `assets/sprites/heroes/icones/humano_clerigo_male.png`
- **Detalhes Visuais Únicos:** Tonsura monástica, expressão austera de penitência, cota de malha pesada sob túnica de feltro cinza salpicada de cera de vela derretida, peitoral estampado com o sol flamejante de ferro forjado, empunhando maça estriada de ferro e turíbulo de prata de onde saem brasas douradas sagradas.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Father Lucien, male human battle cleric, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical angle, solemn monkish face with tonsure hair, riveted chainmail under dark ash-grey vestments marked with candlewax drips, wrought-iron blazing sun holy symbol breastplate, gripping a fluted iron mace in right hand and swinging a silver censer smoking with golden embers in left hand, warm divine ember dithering, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Father Lucien, male human cleric, 32-bit dark fantasy avatar, hollow cheeks, solemn pious brown eyes, tonsure hair, iron holy collar, warm directional holy glow reflecting on face, surrounded by a carved stone cathedral arch pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Father Lucien human cleric, monkish battle priest, fluted iron mace, smoking holy censer, chainmail and ash vestments, 32-bit tactical RPG style, divine chiaroscuro dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, colorful cartoon, anime, smiling, blurry`

---

#### [HERO-03] Lorde Barent de Oakhaven, o Bastião da Alvorada
- **Classe:** Paladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/humano_paladino_male.png`
- **Ícone:** `assets/sprites/heroes/icones/humano_paladino_male.png`
- **Detalhes Visuais Únicos:** Armadura completa de prata polida ornamentada com versos sagrados em relevo, manto carmesim real, elmo alado com visor levantado revelando olhar nobre e maxilar firme, empunhando a lendária lâmina solar "Alvorada Radiante" crepitando com faíscas douradas e escudo heráldico com leão de ouro.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Lord Barent of Oakhaven, male human paladin champion, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 heroic battle stance, pristine engraved silver full plate armor etched with holy scripture, crimson velvet cloak, winged open-faced barbute helm, wielding a radiant broadsword glowing with incandescent golden sunlight, massive heraldic kite shield with golden lion crest, crisp pixel outlines, divine light dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Lord Barent, human paladin, 32-bit dark fantasy avatar, noble chiseled jaw, piercing golden-brown eyes, silver winged helmet collar, divine golden aura reflection, framed by an ornate gold and silver filigree pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Lord Barent human paladin, shining engraved silver armor, glowing solar broadsword, golden lion shield, 32-bit tactical battle angle, crisp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, anime, modern soldier, blurry, plastic armor`

---

#### [HERO-04] Arquimago Vane, o Tecelão do Vazio Astral
- **Classe:** Mago | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/humano_mago_male.png`
- **Ícone:** `assets/sprites/heroes/icones/humano_mago_male.png`
- **Detalhes Visuais Únicos:** Olhos azul-cobalto que brilham levemente no escuro, barba curta e grisalha bem cuidada, vestes acadêmicas azul-meia-noite com constelações bordadas em fios de prata, cajado entalhado de freixo com cristal de quartzo astral na ponta, grimório acorrentado ao cinto flutuando suavemente com páginas de runas violetas.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Archmage Vane, male human wizard scholar, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical angle, trim salt-and-pepper beard, glowing cobalt-blue eyes, layered midnight-navy scholarly robes with embroidered silver constellations, holding a twisted ash-wood staff tipped with a glowing astral quartz crystal, floating chained leather grimoire radiating violet runic glyphs, crisp pixel outlines, mystical particle dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Archmage Vane, male human wizard, 32-bit dark fantasy avatar, intellectual gaze, glowing azure eyes, high embroidered scholar collar, subtle floating arcane purple sparks, framed by an ancient celestial star-chart pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Archmage Vane human wizard, glowing blue eyes, constellation robes, crystal staff, floating spellbook with violet runes, 32-bit tactical RPG aesthetic, handcrafted pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime boy, blurry, bright neon`

---

#### [HERO-05] Garrick Rastreador-de-Pegadas, o Sentinela dos Ermos
- **Classe:** Patrulheiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/humano_patrulheiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/humano_patrulheiro_male.png`
- **Detalhes Visuais Únicos:** Pele bronzeada e áspera pelas intempéries, olhar atento de caçador, capuz verde-floresta desbotado cobrindo a fronte, armadura de couro endurecido reforçada com escamas de ferro nas articulações, arco longo recurvo de teixo reforçado com tiras de tendão, aljava lateral de flechas com penas de falcão, facão de mato no cinto.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Garrick the Track-Finder, male human ranger scout, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, weathered frontiersman with sharp keen grey eyes, deep forest-green hooded cloak, boiled brown leather brigandine reinforced with iron scales, drawing a heavy recurve yew longbow notched with a hawk-fletched arrow, hunting machete at belt, outdoor atmospheric rim lighting, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Garrick human ranger, 32-bit dark fantasy avatar, rugged stubble jaw, sharp hunting gaze, deep green leather cowl framing face, subtle camouflaged face paint, framed by a carved yew wood and ivy pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Garrick human ranger hunter, hooded cloak, leather armor, yew warbow, hawk feathers, 32-bit tactical RPG angle, crisp pixel clusters, earthy palette, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, clean clothing, blurry`

---

#### [HERO-06] Corbin Mãos-de-Sombra, o Fantasma dos Becos
- **Classe:** Ladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/humano_rogue_male.png`
- **Ícone:** `assets/sprites/heroes/icones/humano_rogue_male.png`
- **Detalhes Visuais Únicos:** Sorriso de canto de boca audacioso, máscara de pano escuro na mandíbula que pode ser puxada, armadura de couro flexível tratada com óleo de carvão para não refletir luz, coldre no antebraço com gazuas e agulhas envenenadas, empunhando rapieira de duelo prateada e adaga misericórdia no punho reverso.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Corbin Shadow-Hands, male human rogue thief, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 low stealth crouch, agile street-smart infiltrator in blackened oiled leather armor, half-face dark cloth bandit mask lowered to chin, sly cynical smirk, wielding a slender silver dueling rapier and a reverse-grip parrying stiletto, lockpick harness across chest, high-contrast shadow dithering, crisp pixel contours, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Corbin human rogue, 32-bit dark fantasy avatar, sharp perceptive amber eyes, dark cowl hood cast in shadow, cocky half-smirk, dark leather high collar, framed by a dagger-and-iron-chains pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Corbin human rogue, stealth infiltrator, blackened leather, slender rapier and stiletto, lockpicks, 32-bit tactical RPG aesthetic, dramatic chiaroscuro dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, colorful cloth, blurry`

---

### 3.2 Linhagem Anã da Colina (`anao_*.png`)

---

#### [HERO-07] Brakus Barba-de-Ferro, o Inabalável Muro de Pedra
- **Classe:** Guerreiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/anao_guerreiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/anao_guerreiro_male.png`
- **Detalhes Visuais Únicos:** Barba ruiva volumosa trançada em quatro mechas presas com anéis pesados de ferro forjado, elmo nasal de bronze com chifres curtos de bode montês, armadura pesada de placas escalonadas sobre cota de malha anã, empunhando monumental machado de guerra duplo de duas mãos entalhado com runas anãs.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Brakus Ironbeard, male Hill Dwarf fighter champion, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric stance, low-center muscular powerhouse, magnificent fiery-red beard braided in four strands with heavy iron rings, bronze nasal helm with short ram horns, heavy blackened iron scale mail armor, wielding an enormous double-bitted dwarven battleaxe with runic engravings, round spiked iron buckler on back, stoic ferocious grimace, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Brakus Ironbeard, male dwarf warrior, 32-bit dark fantasy avatar, thick fiery red beard with iron bands, fierce steely grey eyes, bronze nasal helmet, scarred brow, framed by a heavy dwarven geometric iron anvil pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Brakus dwarf warrior, red braided beard with iron rings, horned bronze helm, massive double-bitted battleaxe, 32-bit tactical RPG angle, heavy cross-hatch dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cartoon dwarf, anime, smooth skin, blurry`

---

#### [HERO-08] Kargan Forja-Divina, o Patriarca do Templo Telúrico
- **Classe:** Clérigo | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/anao_clerigo_male.png`
- **Ícone:** `assets/sprites/heroes/icones/anao_clerigo_male.png`
- **Detalhes Visuais Únicos:** Barba cinzenta majestosa até os joelhos decorada com pequenos sinos de prata silenciosos, elmo cerimonial de ouro velho com entalhes de martelos sagrados, peitoral de bronze martelado com o sol de Moradin, empunhando o martelo de guerra "Quebrador de Heresias" brilhando com brasas douradas e relicário de pedra sagrada.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Kargan Forge-Divine, male Hill Dwarf cleric high priest, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric stance, magnificent snow-white beard reaching knees adorned with engraved silver bell-rings, burnished bronze breastplate stamped with the holy forge sun, holding the holy warhammer "Heresy-Breaker" radiating golden molten sparks in one hand and an ancestral stone relic in other, pious intense glare, crisp pixel contours, divine lighting dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Kargan Forge-Divine, male dwarf cleric, 32-bit dark fantasy avatar, flowing white beard with sacred silver beads, wise venerable eyes with golden divine glint, ornate gold forge crown, framed by a sacred dwarven rune-stone pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Kargan dwarf cleric, long white braided beard, bronze plate, glowing holy warhammer, stone relic, 32-bit tactical RPG style, handcrafted pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, blurry, clean clothes`

---

#### [HERO-09] Thalgrim Escudo-da-Montanha, o Jurado das Profundezas
- **Classe:** Paladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/anao_paladino_male.png`
- **Ícone:** `assets/sprites/heroes/icones/anao_paladino_male.png`
- **Detalhes Visuais Únicos:** Armadura pesada de placas de adamante escurecido com runas de juramento douradas, ombreiras maciças esculpidas como cabeças de carneiro de pedra, capa de pele de urso da caverna, espada curta de guerra sagrada forjada em aço estelar e imenso escudo de torre de granito entalhado com o voto de proteção.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Thalgrim Mountain-Shield, male Hill Dwarf paladin defender, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 defensive battle stance, massive dark adamantine plate armor etched with glowing gold oath runes, stone ram-head pauldrons, cave bear fur mantle, holding a glowing star-steel short broadsword and a colossal granite tower shield carved with dwarven vows, unwavering heroic poise, crisp pixel outlines, metallic reflections, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Thalgrim dwarf paladin, 32-bit dark fantasy avatar, thick iron-grey beard, resolute golden-amber eyes, heavy dark steel gorget with ram crest, holy golden rim lighting, framed by a carved granite shield-wall pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Thalgrim dwarf paladin, adamantine plate armor, ram pauldrons, massive granite tower shield, glowing shortsword, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, anime, cute dwarf, vector, blurry`

---

#### [HERO-10] Orin Forjador-de-Runas, o Sábio das Linhas Ley
- **Classe:** Mago | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/anao_mago_male.png`
- **Ícone:** `assets/sprites/heroes/icones/anao_mago_male.png`
- **Detalhes Visuais Únicos:** Barba castanha escura presa com anéis de cobre condutores de eletricidade mágica, óculos mecânicos de latão com múltiplas lentes de safira ajustáveis, túnica de ferreiro arcano em couro reforçado com placas de cobre polido, cinzel rúnico em uma mão esculpindo placas flutuantes de ardósia que soltam faíscas arcanas alaranjadas.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Orin Runeforger, male Hill Dwarf runesmith wizard, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical angle, dark brown beard clamped with magical copper conductor rings, brass magnifying goggles with glowing blue lenses pushed up on brow, heavy leather smith apron over scholar robes reinforced with copper plates, chiseling floating basalt slate tablets emitting crackling orange runes, smoking runic staff in off-hand, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Orin Runeforger, dwarf wizard, 32-bit dark fantasy avatar, intense clever eyes behind multi-lens brass goggles, beard with copper bands, floating small orange runic sparks, framed by an interlocking brass-and-copper gear pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Orin dwarf wizard runesmith, brass goggles, copper plate robes, floating glowing rune slates, runic chisel staff, 32-bit tactical RPG style, spark dithering, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, blurry, modern machinery`

---

#### [HERO-11] Durnik Olho-de-Rapina, o Batedor das Fendas
- **Classe:** Patrulheiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/anao_patrulheiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/anao_patrulheiro_male.png`
- **Detalhes Visuais Únicos:** Pele bronzeada e vincada pelos ventos glaciais dos picos, barba castanha curta e prática trançada para não prender na corda do arco, capa com pelo de lobo cinzento, empunhando uma engenhosa besta pesada anã de repetição com alavanca de recarga rápida, picareta de escalada na cintura e bolsa de virotes de aço.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Durnik Hawk-Eye, male Hill Dwarf ranger scout, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, rugged mountaineer with short practical braided brown beard, winter wolf pelt mantle over studded boiled leather armor, aiming a mechanical dwarven repeating heavy crossbow with iron crank, climbing ice-axe at belt, squinting lethal sharpshooter glare, crisp pixel contours, mountain palette, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Durnik dwarf ranger, 32-bit dark fantasy avatar, windburned scarred face, squinting keen amber eye, wolf fur hood framing rugged features, framed by a frost-covered pine and rope pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Durnik dwarf ranger, repeating heavy crossbow, wolf pelt cloak, mountain climber gear, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, colorful, blurry`

---

#### [HERO-12] Morgran Dedos-de-Ouro, o Ladrão de Cofres Ancestrais
- **Classe:** Ladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/anao_rogue_male.png`
- **Ícone:** `assets/sprites/heroes/icones/anao_rogue_male.png`
- **Detalhes Visuais Únicos:** Anão veterano de proporções táticas maduras, barba preta aparada com presilha de ferro, monóculo de latão de relojoeiro sobre o olho direito, capuz de couro envelhecido escuro, empunhando adagas duplas de trincheira de aço com reflexos metálicos, postura tática séria e letal, iluminação chiaroscuro dramática.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Morgran Gold-Fingers, male Hill Dwarf rogue assassin, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 battle stance, mature dark fantasy proportions, weathered dwarf thief in dark studded leather brigandine with bronze fittings, short trimmed black beard, brass jeweler loupe over right eye, dual-wielding serrated steel trench daggers with reflective blades, dark travel cowl draped over shoulders, cold calculating gaze, dramatic dark fantasy chiaroscuro rim lighting, crisp pixel outlines, intricate pixel dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Morgran dwarf rogue, 32-bit dark fantasy avatar, 3/4 stealth perspective, jeweler loupe magnifying one cunning dark eye, neat trimmed black beard, dark leather cowl, sly calculating smirk, dramatic chiaroscuro shadow dithering, framed by an ornate heavy iron vault-lock and crossed lockpicks relief sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, Morgran dwarf rogue assassin, mature dark fantasy proportions, pitch black background, blackened padded armor, trench daggers, jeweler loupe, 32-bit tactical RPG aesthetic, sharp pixel edges, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, smooth digital painting, 3d render, anime, blurry`

---

### 3.3 Linhagem Draconata (`draconato_*.png`)

---

#### [HERO-13] General Vrakhas, o Flagelo de Escamas Vermelhas
- **Classe:** Guerreiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/draconato_guerreiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/draconato_guerreiro_male.png`
- **Detalhes Visuais Únicos:** Escamas vermelho-escuras grossas com reflexos de brasa incandescente, focinho réptil imponente com chifres bifurcados estendidos para trás, olhos cor de âmbar flamejante, fumaça saindo das narinas, armadura completa de ferro negro pontiagudo com cristas dorsais, empunhando espada larga colossal de duas mãos notched por batalhas sangrentas.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of General Vrakhas, male Dragonborn warrior warlord, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric stance, colossal reptilian frame with deep blood-crimson armored scales, swept-back jagged volcanic horns, burning ember reptilian eyes, smoke puffing from nostrils, spiked blackened iron full plate armor with draconic crests, wielding a notched colossal two-handed jagged steel greatsword, aggressive towering posture, crisp pixel outlines, scale dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of General Vrakhas, male dragonborn fighter, 32-bit dark fantasy avatar, crimson reptilian scales, burning amber slitted eyes, smoking nostrils, spiked blackened gorget, framed by a jagged volcanic obsidian pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, General Vrakhas dragonborn fighter, dark red scales, volcanic horns, smoking nostrils, blackened spiked plate, colossal greatsword, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cute dragon cartoon, anime, blurry, smooth skin`

---

#### [HERO-14] Sacerdote Baham-Raza, a Voz da Chama Platina
- **Classe:** Clérigo | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/draconato_clerigo_male.png`
- **Ícone:** `assets/sprites/heroes/icones/draconato_clerigo_male.png`
- **Detalhes Visuais Únicos:** Raras escamas platinadas reluzentes, olhos prateados desprovidos de pupilas, vestes sagradas de seda branca e ouro sobre placas de peitoral cerimonial de prata, empunhando cajado com cabeça de dragão cuspidor de fogo sagrado e símbolo sagrado de Bahamut em platina pura.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Priest Baham-Raza, male Dragonborn cleric of light, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical angle, rare glistening platinum scales reflecting holy light, solid pupilless silver eyes, flowing white silk and gold sacerdotal vestments over ceremonial silver dragon breastplate, holding a dragon-headed holy staff spouting sacred white fire and a pure platinum dragon talismans, benevolent yet terrifying draconic majesty, crisp pixel contours, ethereal glow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Baham-Raza, dragonborn cleric, 32-bit dark fantasy avatar, gleaming platinum scales, pupilless silver eyes, silver dragon gorget, holy white aura rim lighting, framed by an ancient silver dragon-wing pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Baham-Raza dragonborn cleric, glistening platinum scales, silver eyes, white and gold vestments, staff with holy white fire, 32-bit tactical RPG style, sharp pixel outlines, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, blurry, green scales`

---

#### [HERO-15] Balthazar Escama-Dourada, o Campeão do Sol Flamejante
- **Classe:** Paladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/draconato_paladino_male.png`
- **Ícone:** `assets/sprites/heroes/icones/draconato_paladino_male.png`
- **Detalhes Visuais Únicos:** Escamas douradas reluzentes com reflexos metálicos, chifres nobres esculpidos com inscrições sagradas em dracônico, armadura de placas completas em aço espelhado e filigrana de ouro, empunhando montante reluzente envolta em chamas sagradas radiantes e escudo de dragão imponente.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Balthazar Gold-Scale, male Dragonborn paladin champion, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 heroic battle stance, glistening polished gold-brass draconic scales, noble backward-sweeping horns engraved with holy draconic runes, ornate mirrored silver-steel full plate with gold filigree, wielding an incandescent radiant longsword bathed in sacred gold flame, heavy ceremonial tower shield with dragon crest, crisp pixel outlines, metallic reflections dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Balthazar Gold-Scale, male Dragonborn paladin champion, 32-bit dark fantasy avatar, 3/4 heroic battle angle, radiant golden reptilian scales, righteous slitted amber eyes, silver gorget with glowing holy oaths, framed by an ornate sculpted gold dragon-crest relief pixel art border fitting flush edge-to-edge against all canvas boundaries, solid pure black background extending behind character, full-bleed 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Balthazar dragonborn paladin, gleaming gold scales, engraved horns, silver plate armor, blazing holy longsword, tower shield, 32-bit tactical RPG angle, crisp pixel clusters, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, smooth digital painting, 3d render, anime lizard, vector, blurry, dark matte skin`


---

#### [HERO-16] Ignisrax, o Piromante do Fogo Dracônico
- **Classe:** Mago | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/draconato_mago_male.png`
- **Ícone:** `assets/sprites/heroes/icones/draconato_mago_male.png`
- **Detalhes Visuais Únicos:** Escamas de carvão com veios internos de lava brilhante pulsante no pescoço e peito, olhos de fogo líquido, vestes escuras chamuscadas com runas arcanas queimadas no tecido, garras estalando com labaredas de fogo fátuo, cajado esculpido de osso de dragão ancestral encimado por orbe de magma.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Ignisrax, male Dragonborn evoker pyromancer wizard, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, charcoal-black draconic scales with internal glowing red magma veins pulsing at the throat and chest, molten orange reptilian eyes, charred dark scholar robes with burning hem runes, talons crackling with roaring pyromantic flames, holding an ancient dragon-bone staff crowned with a floating orb of bubbling magma, crisp pixel contours, intense fire glow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Ignisrax, male Dragonborn pyromancer wizard, 32-bit dark fantasy avatar, 3/4 sorcerous angle, charcoal reptilian snout with glowing molten throat vents, fierce fiery eyes, blackened hood, floating flame sparks, framed by a heavy square relief sculpted molten lava rock and volcanic basalt pixel art border fitting flush edge-to-edge against all canvas boundaries, glowing magma veins carved within the frame face, solid pure black background extending behind character, full-bleed 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, protruding rocks, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Ignisrax dragonborn pyromancer, black scales, glowing lava veins, molten eyes, dragon-bone magma staff, charred robes, 32-bit tactical RPG style, fiery particle dithering, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, smooth digital painting, 3d render, vector, anime, blurry, ice magic, flat colors`

---

#### [HERO-17] Kresh Veneno-Silencioso, o Rastreador da Selva Negra
- **Classe:** Patrulheiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/draconato_patrulheiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/draconato_patrulheiro_male.png`
- **Detalhes Visuais Únicos:** Escamas verde-escuras camufladas com manchas de musgo, crista de chifres aerodinâmica com penas de predador amarradas, armadura de couro de serpente gigante, arco de guerra pesado feito de chifre de besta com flechas embebidas em veneno verde cáustico.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Kresh Silent-Venom, male Dragonborn ranger apex-scout, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, mottled dark moss-green reptilian scales with camouflage pattern, streamlined horn crest bound with raven feathers, giant serpent-leather armor, drawing a massive recurve warbow carved from beast horn with arrow dripping emerald venom, slitted predatory yellow eyes, crisp pixel outlines, jungle shadow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Kresh Silent-Venom, male Dragonborn ranger apex-scout, 32-bit dark fantasy avatar, 3/4 hunter angle, mottled green scales, keen amber reptilian eyes, horn crest with feathers, dark snake-leather cowl, framed by an ornate sculpted solid ironwood and carved horn square relief pixel art border fitting flush edge-to-edge against all canvas boundaries, toxic vine glyphs engraved within the frame face, solid pure black background extending behind character, full-bleed 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, protruding horns, outer vines, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Kresh dragonborn ranger, dark moss-green scales, serpent leather, horn warbow with venomous arrows, 32-bit tactical RPG angle, crisp pixel clusters, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, smooth digital painting, 3d render, vector, anime lizard, blurry, bright red scales`

---

#### [HERO-18] Zyrak Escama-de-Sombra, o Carrasco das Trevas
- **Classe:** Ladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/draconato_rogue_male.png`
- **Ícone:** `assets/sprites/heroes/icones/draconato_rogue_male.png`
- **Detalhes Visuais Únicos:** Escamas de obsidiana fosca que absorvem a luz, postura predatória agachada réptil quase inaudível, olhos estreitos felinos brilhando na penumbra, capa com capuz de camuflagem de fumaça, empunhando adagas duplas curvas em empunhadura invertida gotejando óleo paralisante.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Zyrak Shadow-Scale, male Dragonborn rogue assassin, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 low stealth crouch, sleek matte-obsidian scales that absorb ambient light, compact predatory reptilian stance, dark oiled leather armor with smoke-weave cloak, dual-wielding curved serrated obsidian daggers in reverse grip dripping dark paralyzing venom, narrow glowing amber slit eyes under pulled cowl, crisp pixel contours, stealth chiaroscuro dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Zyrak dragonborn rogue, 32-bit dark fantasy avatar, matte black scales, predatory glowing amber eyes emerging from shadow, black cowl hood, framed by an obsidian daggers-and-smoke pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Zyrak dragonborn rogue assassin, matte obsidian scales, low stalking crouch, reverse-grip obsidian daggers, 32-bit tactical RPG aesthetic, dramatic shadow dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cartoon, anime, bright shiny scales, blurry`

---

### 3.4 Linhagem Élfica da Floresta (`elfo_*.png`)

---

#### [HERO-19] Dama Aeloria Vento-Cortante, a Mestra das Lâminas da Canópia
- **Classe:** Guerreira | **Gênero:** Feminino
- **Sprite:** `assets/sprites/heroes/elfo_guerreiro_female.png`
- **Ícone:** `assets/sprites/heroes/icones/elfo_guerreiro_female.png`
- **Detalhes Visuais Únicos:** Físico atlético e esguio, pele bronzeada pelo sol da floresta, cabelos castanho-avermelhados presos em trança de combate com adornos de prata élfica, armadura de malha prateada flexível sobre couro de cervo, empunhando graciosa espada bastarda élfica de lâmina curva em guarda alta e postura letal impecável.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Lady Aeloria Wind-Cutter, female Wood Elf fighter blademaster, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 elegant battle stance, athletic lean frame, sun-bronzed skin, braided auburn hair with silver elven cuffs, leaf-patterned flexible silver chainmail over supple stag-leather, brandishing a graceful two-handed curved elven greatsword in lethal high guard, intense focused emerald eyes, crisp pixel outlines, silver steel reflection dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Lady Aeloria, female elf warrior, 32-bit dark fantasy avatar, sharp noble jawline, piercing emerald eyes, auburn warrior braid, silver leaf gorget, framed by an interlocking silver leaf and elven sword pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Lady Aeloria wood elf blademaster, athletic female warrior, silver leaf mail, curved elven greatsword, auburn braid, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, anime waifu, cute chibi, vector, blurry, smooth skin`

---

#### [HERO-20] Sacerdotisa Faen, a Guardiã do Carvalho Primordial
- **Classe:** Clériga | **Gênero:** Feminino
- **Sprite:** `assets/sprites/heroes/elfo_clerigo_female.png`
- **Ícone:** `assets/sprites/heroes/icones/elfo_clerigo_female.png`
- **Detalhes Visuais Únicos:** Olhar sereno com olhos verde-folha brilhantes, guirlanda de folhas de hera de prata nos cabelos ruivos, vestes fluidas de seda verde-musgo sobre armadura de placas de casca de árvore ancestral reforçada por ferro dos bosques, cajado vivo com botões de flores que florescem e emitem luz divina dourada.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Priestess Faen, female Wood Elf life cleric, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical angle, serene beautiful elven healer, deep green leaf eyes, silver ivy garland in copper hair, flowing moss-green silk vestments over iron-wood bark plate armor, holding a living sacred wooden staff that sprouts blooming golden blossoms radiating holy warmth and a silver leaf talisman, crisp pixel contours, divine nature glow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Priestess Faen, female Wood Elf life cleric, 32-bit dark fantasy avatar, 3/4 solemn angle, compassionate wise leaf-green eyes, silver ivy wreath in copper hair, silver leaf gorget, warm divine sunlight glow, framed by an ornate sculpted solid silver-oak and sacred ivy square relief pixel art border fitting flush edge-to-edge against all canvas boundaries, flowering leaf filigree carved within the frame face, solid pure black background extending behind character, full-bleed 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, protruding branches, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Priestess Faen elf cleric, moss-green robes, ironwood bark plate, staff blooming with holy light, 32-bit tactical RPG style, delicate nature dithering, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, smooth digital painting, 3d render, anime, vector, oversaturated, blurry`

---

#### [HERO-21] Sylphira Lâmina-do-Amanhecer, a Vingadora dos Bosques Sagrados
- **Classe:** Paladina | **Gênero:** Feminino
- **Sprite:** `assets/sprites/heroes/elfo_paladino_female.png`
- **Ícone:** `assets/sprites/heroes/icones/elfo_paladino_female.png`
- **Detalhes Visuais Únicos:** Armadura de placas élficas em esmeralda e prata forjada no formato de folhas entrelaçadas, capa de veludo verde-escuro bordada com fios de ouro, rapieira de guerra brilhando com a radiância da luz solar filtrada pelas copas, escudo em formato de folha de lótus de ferro estelar.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Sylphira Dawn-Blade, female Wood Elf paladin of the ancients, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, magnificent polished emerald and star-silver leaf-carved full plate armor, dark forest-green velvet cloak edged in gold, brandishing a radiant glowing war-rapier blazing with holy dawnlight, sacred leaf-shaped star-iron shield, poised lethal grace, crisp pixel outlines, holy chiaroscuro dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Sylphira Dawn-Blade, female elf paladin, 32-bit dark fantasy avatar, noble cheekbones, determined jade eyes, emerald-and-silver winged gorget, golden halo light reflection, framed by an engraved silver dawn-sun pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Sylphira wood elf paladin, emerald-and-silver plate armor, radiant rapier of dawn, leaf star-iron shield, 32-bit tactical RPG battle angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, anime waifu, vector, blurry, plastic shine`

---

#### [HERO-22] Arquimaga Caelynn, a Astróloga das Estrelas Cadentes
- **Classe:** Maga | **Gênero:** Feminino
- **Sprite:** `assets/sprites/heroes/elfo_mago_female.png`
- **Ícone:** `assets/sprites/heroes/icones/elfo_mago_female.png`
- **Detalhes Visuais Únicos:** Orelhas élficas finas e pontiagudas com argolas de ametista, cabelos prateados como luar, túnica de seda azul-índigo com mapas celestes flutuantes ao seu redor em runas de luz estelar, segurando um orbe de cristal prismático de onde orbitam pequenas luas de luz espectral.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Archmage Caelynn, female Wood Elf celestial wizard, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical angle, long silver-white moonlight hair, delicate pointed ears with amethyst cuffs, deep indigo-blue silk robes embroidered with celestial silver constellations, floating glowing star charts and parchment scrolls orbiting her shoulders, holding a prismatic crystal orb radiating soft spectral starlight, crisp pixel outlines, arcane sparkle dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Archmage Caelynn, female elf wizard, 32-bit dark fantasy avatar, mysterious violet eyes, silver hair, amethyst ear cuffs, high indigo collar with silver stars, framed by a cosmic lunar phase pixel art border, 1:1 square RPG token --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Archmage Caelynn elf wizard, silver hair, indigo starlight robes, floating glowing celestial runes, crystal orb, 32-bit tactical RPG aesthetic, sharp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, anime girl, cute vector, blurry, pink hair`

---

#### [HERO-23] Sylas Rastreadora-da-Lua, a Caçadora Fantasma
- **Classe:** Patrulheira | **Gênero:** Feminino
- **Sprite:** `assets/sprites/heroes/elfo_patrulheiro_female.png`
- **Ícone:** `assets/sprites/heroes/icones/elfo_patrulheiro_female.png`
- **Detalhes Visuais Únicos:** Olhos penetrantes de predador com pintura facial de camuflagem de cinzas florestais, túnica ajustada de couro flexível marrom e verde com folhas secas trançadas na capa de viagem, arco longo de teixo curvo finamente entalhado, aljava cheia de flechas de ponta de sílex e par de adagas de caça no cinto.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Sylas Moon-Tracker, female Wood Elf ranger sniper, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, athletic agile frame, sun-bronzed skin, braided dark copper hair with bone beads, subtle ash camouflage markings across cheekbones, fitted supple dark forest-green and deer-hide leather armor, drawing a finely carved composite recurve yew longbow, quiver of fletched flint-tipped arrows, hunting daggers at hip, crisp pixel contours, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Sylas Moon-Tracker, female Wood Elf ranger, 32-bit dark fantasy avatar, 3/4 hunter angle, piercing green eyes, ash camouflage face markings, copper braid, leather cowl framing shoulders, outdoor rim lighting, framed by an ornate sculpted solid ironwood and silver leaf square relief pixel art border fitting flush edge-to-edge against all canvas boundaries, solid pure black background extending behind character, full-bleed 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, protruding branches, outer leaves, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Sylas wood elf ranger, copper braids, ash warpaint, supple leather armor, recurve yew longbow, 32-bit tactical RPG angle, crisp pixel edges, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, smooth digital painting, 3d render, vector, anime, colorful modern clothes, blurry`

---

#### [HERO-24] Kaelen Passo-de-Névoa, a Lâmina Silenciosa do Crepúsculo
- **Classe:** Ladina | **Gênero:** Feminino
- **Sprite:** `assets/sprites/heroes/elfo_rogue_female.png`
- **Ícone:** `assets/sprites/heroes/icones/elfo_rogue_female.png`
- **Detalhes Visuais Únicos:** Postura acrobática agachada pronta para salto acrobático, capuz de veludo preto cobrindo o rosto deixando à mostra apenas os lábios e olhos esmeralda faiscantes, armadura de couro negro acolchoado, empunhando duas adagas curvas prateadas com cabos de osso gravados.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Kaelen Mist-Step, female Wood Elf rogue shadow-dancer, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 agile crouch stance, sleek athletic frame in form-fitting form-sculpted matte black leather armor, deep cowl framing face with intense glowing emerald eyes and dark lips, dual-wielding curved silver daggers with engraved bone hilts in ready combat grip, light-footed coiled poise, crisp pixel outlines, stealth chiaroscuro dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Kaelen Mist-Step, female Wood Elf rogue shadow-dancer, 32-bit dark fantasy avatar, 3/4 stealth perspective, shadow-veiled face, intense predatory emerald eyes glowing from inside black velvet cowl, dark lips, subtle silver dagger hilts, framed by an ornate sculpted blackened-iron relief pixel art border with miniature silver stiletto daggers and shadow vines engraved flush within the square frame, edge-to-edge full-bleed composition touching all canvas boundaries, solid pure black background, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, protruding blades, swords sticking out, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Kaelen elf rogue, matte black form-fitting leather, deep hood, glowing emerald eyes, curved bone-hilt daggers, 32-bit tactical RPG style, sharp pixel clusters, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, smooth digital painting, 3d render, anime waifu, cute chibi, vector, blurry`

---

### 3.5 Linhagem Halfling (`halfling_*.png`)

---

#### [HERO-25] Tobias Bravo-Coração, o Escudeiro dos Pequenos
- **Classe:** Guerreiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/halfling_guerreiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/halfling_guerreiro_male.png`
- **Detalhes Visuais Únicos:** Halfling veterano de guerra de proporções maduras e robustas, rosto marcado por cicatriz no queixo, cabelos castanhos ondulados, peitoral de aço forjado sob medida com cota de malha, empunhando espada curta pesada de aço e escudo redondo reforçado com ferro, postura de prontidão tática firme e decidida.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Tobias Brave-Heart, male Halfling fighter vanguard, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 isometric stance, mature dark fantasy proportions, seasoned halfling warrior with battle-scarred chin, custom-fitted dark steel breastplate over heavy chainmail, wielding a broad steel shortsword and an iron-rimmed oak round shield with hound crest, grounded tactical battle posture, crisp pixel outlines, metallic reflections dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, child, toy, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Tobias Brave-Heart, male Halfling warrior champion, 32-bit dark fantasy avatar, 3/4 portrait angle, mature resolute hazel eyes, battle-scarred jawline, wavy brown hair, polished dark steel gorget with bronze rivets, dramatic side chiaroscuro lighting, framed by an ornate wrought-iron and hunting-hound relief sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi, child
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Tobias halfling warrior, mature dark fantasy proportions, pitch black background, steel breastplate, short broadsword, oak round shield, 32-bit tactical RPG battle angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, child, smooth digital painting, 3d render, anime, blurry`

---

#### [HERO-26] Milo Concha-de-Ouro, o Abade da Lareira Aconchegante
- **Classe:** Clérigo | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/halfling_clerigo_male.png`
- **Ícone:** `assets/sprites/heroes/icones/halfling_clerigo_male.png`
- **Detalhes Visuais Únicos:** Sacerdote halfling maduro e resoluto, vestes de lã escura acolchoada sobre cota de malha de bronze envelhecido, amuleto de cornucópia e lareira brilhando com fogo dourado sagrado, martelo pesado de guerra esculpido em ferro rúnico, olhar sereno e inabalável contra o mal.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Milo Gold-Ladle, male Halfling hearth cleric, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 tactical angle, mature weathered halfling battle priest, dark traveler wool tunic over bronze ringmail, gripping a carved iron war-mallet and a holy golden cornucopia talisman glowing with warm amber divine embers, resolute solemn gaze, crisp pixel contours, warm holy chiaroscuro dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, child, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Milo Gold-Ladle, male Halfling hearth cleric priest, 32-bit dark fantasy avatar, 3/4 portrait angle, kind weathered face with curly brown hair, wise warm amber eyes, bronze ringmail collar, radiant golden hearth-ember directional rim lighting, framed by an ornate antique bronze wheat-and-sacred-flame sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi, child
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Milo halfling cleric, mature dark fantasy proportions, pitch black background, traveler wool, bronze mail, wheat war-mallet, glowing golden cornucopia, 32-bit tactical RPG style, warm light dithering, isolated on solid black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, child, smooth digital painting, 3d render, vector, anime, blurry`

---

#### [HERO-27] Sir Pip, o Campeão Valente dos Indefesos
- **Classe:** Paladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/halfling_paladino_male.png`
- **Ícone:** `assets/sprites/heroes/icones/halfling_paladino_male.png`
- **Detalhes Visuais Únicos:** Nobre cavaleiro halfling em armadura completa de placas prateadas com detalhes em bronze antigo, capa azul-escuro esfarrapada nas bordas pela batalha, empunhando espada montante sagrada flamejando em luz divina dourada e escudo de armas da fé.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Sir Pip, male Halfling paladin knight champion, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 heroic battle stance, mature proportions, seasoned halfling knight clad in heavy custom plate armor of blackened silver, dark royal navy cape, wielding a glowing sacred broadsword infused with brilliant golden divine fire, silver heater shield, fearless courageous posture, crisp pixel outlines, metallic reflections dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, child, toy, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Sir Pip, male Halfling paladin knight champion, 32-bit dark fantasy avatar, 3/4 heroic battle angle, noble determined amber eyes, polished silver visored helm, engraved steel gorget, brilliant golden divine aura reflection, framed by an ornate sculpted silver-and-gold holy filigree pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi, child
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Sir Pip halfling paladin, mature dark fantasy proportions, pitch black background, silver plate armor, giant glowing holy broadsword, blue cape, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon child, anime, plastic toy armor, blurry`

---

#### [HERO-28] Wilkin Faísca-Rápida, o Mestre dos Truques Arcanos
- **Classe:** Mago | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/halfling_mago_male.png`
- **Ícone:** `assets/sprites/heroes/icones/halfling_mago_male.png`
- **Detalhes Visuais Únicos:** Ilusionista experiente de feições maduras e perspicazes, óculos de armação de latão escuro na testa, túnica de veludo roxo-escuro e couro desgastado com bolsos de reagentes, varinha de jacarandá da qual saltam faíscas arcanas violetas e grimório de couro amarrado na cintura.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Wilkin Quick-Spark, male Halfling illusionist arcanist wizard, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 battle stance, mature halfling spellcaster in dark plum velvet robes with leather straps, dark brass spectacles on brow, holding a carved rosewood wand sparking with violet and silver arcane embers, iron-bound leather spellbook at hip, calculating sharp gaze, crisp pixel contours, magical sparks dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, child, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Wilkin Quick-Spark, male Halfling illusionist wizard, 32-bit dark fantasy avatar, 3/4 perspective, keen perceptive gaze behind brass magnifying spectacles, dark plum velvet scholar collar, floating arcane violet embers, framed by an ornate clockwork brass-and-astral-runes sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi, child
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Wilkin halfling wizard, mature dark fantasy proportions, pitch black background, plum robes, copper spectacles, sparking rosewood wand, spellbook, 32-bit tactical RPG aesthetic, sharp pixel edges, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, child, smooth digital painting, 3d render, vector, anime, blurry`

---

#### [HERO-29] Caelen Olho-de-Lebre, o Batedor das Tocas Ocultas
- **Classe:** Patrulheiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/halfling_patrulheiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/halfling_patrulheiro_male.png`
- **Detalhes Visuais Únicos:** Rastreador maduro e calejado da floresta, capuz de couro curtido verde-musgo escuro com folhagens secas, arco recurvo curto de teixo com corda encerada em posição de disparo, aljava de virotes de caça na perna, olhar implacável de caçador em emboscada.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Caelen Hare-Eye, male Halfling ranger scout, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 agile battle stance, mature halfling hunter in patched forest-green wool and dark studded leather armor, leather archer hood, drawing a finely balanced recurve shortbow with barbed hunting arrow, side-quiver of fletched arrows, sharp lethal sharpshooter posture, crisp pixel outlines, earthy woodland palette, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, child, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Caelen Hare-Eye, male Halfling ranger scout, 32-bit dark fantasy avatar, 3/4 hunter angle, intense keen grey-amber eyes, weathered leather archer cowl, dark green leather collar, cool woodland twilight rim lighting, framed by an ornate carved yew-wood and barbed briar-thorn sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi, child
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Caelen halfling ranger scout, mature dark fantasy proportions, pitch black background, camouflaged leather, recurve shortbow, hood, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, child, smooth digital painting, 3d render, vector, anime, blurry`

---

#### [HERO-30] Finn Pés-Leves, o Mestre dos Gazetes e Sombras
- **Classe:** Ladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/halfling_rogue_male.png`
- **Ícone:** `assets/sprites/heroes/icones/halfling_rogue_male.png`
- **Detalhes Visuais Únicos:** Ladino adulto esguio e letal, cabelos castanhos curtos despenteados, olhar afiado e perigoso, armadura de couro preto batido com tachas de ferro escurecido, capa curta de seda escura para movimentos silenciosos, empunhando duas adagas afiadas de estilete prateado em empunhadura invertida.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Finn Light-Feet, male Halfling rogue assassin, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 low tactical crouch stance, mature adult halfling infiltrator, tousled dark brown hair, sharp calculating hazel eyes, fitted studded charcoal leather brigandine, dark cowl mantle, dual-wielding balanced silver stiletto daggers in reverse combat grip, chest harness with lockpicks and muffled utility pouches, crisp pixel contours, stealth chiaroscuro dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, child, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Finn Light-Feet, male Halfling rogue assassin, 32-bit dark fantasy avatar, 3/4 stealth angle, sharp dangerous hazel eyes gleaming under dark leather cowl, sly confident half-smirk, high studded leather collar, dramatic low-key shadow dithering, framed by an ornate blackened-iron lock and crossed daggers sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi, child
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Finn halfling rogue, mature dark fantasy proportions, pitch black background, studded leather, silver daggers, lockpicks, 32-bit tactical RPG style, sharp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, child, smooth digital painting, 3d render, blurry`

---

### 3.6 Linhagem Meio-Orc (`meio_orc_*.png`)

---

#### [HERO-31] Thorgar Quebrador-de-Ossos, o Flagelo dos Campos de Sangue
- **Classe:** Guerreiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/meio_orc_guerreiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/meio_orc_guerreiro_male.png`
- **Detalhes Visuais Únicos:** Massa muscular descomunal, cicatrizes de corte e queimadura por todo o torso, presas inferiores maciças projetando-se da boca, tranças de guerra negras presas com argolas de ferro, armadura de placas de ferro negro com pele de lobo nas costas, empunhando machado de batalha de duas mãos monumental.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Thorgar Bone-Breaker, male Half-Orc warrior mercenary, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 isometric battle stance, colossal muscular frame, mottled greyish-green skin covered in slashing scars, prominent lower canine tusks jutting upwards, dreadlock battle braids bound with iron rings, heavy blackened iron splint plate armor with dark wolf pelt over shoulders, wielding a monstrous notched two-handed battleaxe, ferocious disciplined war glare, crisp pixel outlines, heavy metal dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, bright green, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Thorgar Bone-Breaker, male Half-Orc barbarian warlord, 32-bit dark fantasy avatar, 3/4 fierce battle angle, heavy scarred grey-green jaw, massive lower tusks, predatory glowing amber eyes, iron torque with wolf fur mantle, dramatic high-contrast chiaroscuro lighting, framed by a colossal spiked wrought-iron and battle-chain relief sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Thorgar half-orc warrior, pitch black background, grey-green skin, massive tusks, blackened splint armor, giant notched two-handed battleaxe, wolf pelt, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon shrek, anime, bright green skin, blurry, smooth digital painting, 3d render`

---

#### [HERO-32] Gromph Clamor-do-Trovão, o Xamã das Tempestades de Batalha
- **Classe:** Clérigo | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/meio_orc_clerigo_male.png`
- **Ícone:** `assets/sprites/heroes/icones/meio_orc_clerigo_male.png`
- **Detalhes Visuais Únicos:** Pinturas de guerra brancas simulando uma caveira no rosto acinzentado, túnica ritual de couro cru reforçada com anéis de ferro, mangual pesado de ferro com três correntes cravadas de cravos emitindo estalos elétricos e orbes de sangue sagrado no cinto.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Gromph Thunder-Clamor, male Half-Orc war priest cleric, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 tactical stance, towering grey-skinned half-orc with chalk-white skull warpaint across face, ritual raw-hide vestments reinforced with rusted iron rings and blood-red prayer wraps, swinging a heavy three-headed spiked iron flail crackling with blue thunderstorm arcana, heavy iron tower shield bearing skull sigil, zealous ferocious roar, crisp pixel contours, lightning glow dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, bright green, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Gromph Blind-Eye, male Half-Orc tempest cleric shaman, 32-bit dark fantasy avatar, 3/4 ritual angle, white bone warpaint across grim grey-green brow, heavy tusks, crackling blue divine spark in dark eyes, iron ring gorget, electric blue rim lighting, framed by a heavy solid square wrought-iron relief sculpted pixel art border with flush straight outer edges touching all canvas boundaries, storm-lightning glyphs and skull runes engraved within the frame face, full-bleed edge-to-edge 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, protruding spikes, outer jagged edges, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Gromph half-orc cleric, pitch black background, skull warpaint, three-headed spiked flail with lightning sparks, iron ring armor, 32-bit tactical RPG style, electrical spark dithering, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, chibi, cartoon, anime, peaceful priest, blurry, smooth digital painting, 3d render`

---

#### [HERO-33] Varek o Redentor, o Algoz dos Juramentos Quebrados
- **Classe:** Paladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/meio_orc_paladino_male.png`
- **Ícone:** `assets/sprites/heroes/icones/meio_orc_paladino_male.png`
- **Detalhes Visuais Únicos:** Olhar severo de determinação trágica, peitoral de ferro escurecido com o selo da justiça divina gravado a fogo, manto carmesim gasto, espada de execução de duas mãos brilhando com uma chama branca purificadora em contraste com sua pele escura cinzenta.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Varek the Redeemer, male Half-Orc paladin of vengeance, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 battle stance, towering muscular half-orc in heavy battle-dented blackened steel plate with faded crimson tabard, gripping a massive two-handed executioner greatsword blazing with brilliant white-hot holy fire, tragic stern scarred face, jutting lower tusks, unwavering righteous conviction, crisp pixel outlines, intense holy chiaroscuro dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, bright green, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Varek Doom-Blade, male Half-Orc redemption paladin, 32-bit dark fantasy avatar, 3/4 solemn heroic angle, scarred stoic grey-green features, noble tusks, glowing righteous gold spark in deep eyes, blackened steel and silver gorget, sacred white-gold rim lighting, framed by an ornate sculpted silver-and-blackened-iron executioner crest pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Varek half-orc paladin, pitch black background, blackened steel plate, blazing white executioner greatsword, tusks, scars, 32-bit tactical RPG battle view, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, anime, bright green, blurry, smooth digital painting, 3d render`

---

#### [HERO-34] Morgok Sangue-Feiticeiro, o Evocador das Chamas Negras
- **Classe:** Mago | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/meio_orc_mago_male.png`
- **Ícone:** `assets/sprites/heroes/icones/meio_orc_mago_male.png`
- **Detalhes Visuais Únicos:** Cicatrizes rituais arcanas que brilham em púrpura sobre o crânio raspado, vestes de couro de batalha combinadas com túnica rasgada de mago, empunhando um cajado feito de ferro fundido com uma caveira de demônio fumegante, runas de destruição entalhadas nas presas.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Morgok Blood-Sorcerer, male Half-Orc war wizard, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 battle angle, imposing muscular half-orc with shaved skull carved with glowing purple arcane scar-runes, tattered dark scholarly vestments over mail bracers, tusks engraved with destructive glyphs, brandishing a heavy wrought-iron staff topped with a smoking horned demon skull emitting violet plasma, crackling dark magic sparks, crisp pixel contours, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, bright green, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Shaman Rok, male Half-Orc blood-arcane wizard, 32-bit dark fantasy avatar, 3/4 sorcerous perspective, scarred skull glowing with violet arcane runes, heavy tusks banded with silver, sinister golden eyes, high charcoal collar, floating purple magical embers, framed by a solid square relief sculpted obsidian block pixel art border touching all four canvas edges seamlessly, flush straight outer perimeter with glowing violet runic glyphs and demon skull filigree carved within the frame face, full-bleed edge-to-edge 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, protruding horns, outer gaps, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Morgok half-orc war wizard, pitch black background, glowing violet scar-runes, tattered robes, iron demon-skull staff, engraved tusks, 32-bit tactical RPG aesthetic, magical plasma dithering, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, chibi, cartoon, anime, weak wizard, blurry, smooth digital painting, 3d render`

---

#### [HERO-35] Kallor Dente-de-Lobo, o Rastreador de Feras Sangrentas
- **Classe:** Patrulheiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/meio_orc_patrulheiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/meio_orc_patrulheiro_male.png`
- **Detalhes Visuais Únicos:** Capuz feito do crânio de um urso pardo sobre a cabeça, pele verde-acinzentada com tintura de terra batida, arco longo pesado de guerra com corda de tripa reforçada capaz de atravessar armaduras, facão tático com cabo de chifre no quadril.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Kallor Wolf-Tooth, male Half-Orc ranger beast-hunter, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 battle stance, towering muscular frontiersman wearing a ferocious brown bear skull headdress, grey-green skin stained with mud camouflage, heavy studded wolf-pelt cuirass, drawing an enormous recurve warbow strung with heavy gut cord, notched hunting broadhead arrow, horn-hilted tactical machete at waist, predatory focused stance, crisp pixel edges, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, bright green, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Kallor Bear-Claw, male Half-Orc primeval ranger hunter, 32-bit dark fantasy avatar, 3/4 feral hunter angle, massive bear skull cowl over weathered green brow, protruding lower tusks, piercing amber predator eyes, heavy grizzly fur mantle, cold outdoor rim light, framed by a heavy solid square wrought-iron relief sculpted pixel art border fitting flush edge-to-edge against all canvas boundaries, ancestral beast bone engravings carved within the frame face, solid pure black background extending behind character, full-bleed 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, protruding bones, outer claws, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Kallor half-orc ranger hunter, bear skull cowl, studded wolf pelt, heavy recurve warbow, 32-bit tactical RPG angle, crisp pixel clusters, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, chibi, cartoon, anime, bright clean clothes, blurry, smooth digital painting, 3d render`

---

#### [HERO-36] Zulgor Mão-de-Ferro, o Degolador dos Calos
- **Classe:** Ladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/meio_orc_rogue_male.png`
- **Ícone:** `assets/sprites/heroes/icones/meio_orc_rogue_male.png`
- **Detalhes Visuais Únicos:** Gigante esguio e surpreendentemente silencioso, armadura de couro endurecido preto com ombreiras de ferro batido, capuz profundo ocultando as presas e o olhar amarelado, punhais pesados de lâmina triangular curvada perfeitos para estocadas mortais nas sombras.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Zulgor Iron-Hand, male Half-Orc rogue thug-enforcer, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 low stealth crouch, hulking yet light-footed assassin in dark reinforced leather brigandine and hooded mantle, dual-wielding heavy serrated meat-cleaver daggers with dark oiled blades, jutting tusks, shadowy silhouette, crisp pixel contours, stealth chiaroscuro dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, bright green, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Zulgor Iron-Hand, male Half-Orc rogue assassin enforcer, 32-bit dark fantasy avatar, 3/4 stealth angle, shadows cloaking scarred brow, glowing yellow feline predator eyes, wicked tusks gleaming in dark, dark leather cowl, dramatic low-key chiaroscuro dithering, framed by an ornate heavy iron chains and meat-cleaver relief sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Zulgor half-orc rogue assassin, pitch black background, crouching in shadows, dark leather armor, heavy cleaver daggers, tusks, 32-bit tactical RPG style, sharp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, anime, bright colors, blurry, smooth digital painting, 3d render`

---

### 3.7 Linhagem Tiefling (`tiefling_*.png`)

---

#### [HERO-37] Malakor Chifre-Partido, o Espadachim do Fogo Infernal
- **Classe:** Guerreiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/tiefling_guerreiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/tiefling_guerreiro_male.png`
- **Detalhes Visuais Únicos:** Pele carmesim profunda, chifre esquerdo quebrado e reforçado com uma braçadeira de ferro gravada com runas infernais, chifre direito longo e afiado para trás, armadura de ferro batido escurecido com cota de malha vermelha, empunhando espada bastarda larga serrilhada gotejando brasas negras, cauda preênsil chicoteando em guarda.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Malakor Broken-Horn, male Tiefling fighter hell-blade, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 battle stance, deep crimson-red skin, left horn snapped short and banded with runic iron bracket, right horn long and swept back, blackened iron plate armor with infernal brass filigree, wielding a heavy jagged bastard sword dripping black smoking embers, barbed tail lashed in combat balance, glowing amber slit eyes, crisp pixel outlines, metallic fire dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, pink skin, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Malakor Broken-Horn, male Tiefling hell-blade warrior, 32-bit dark fantasy avatar, 3/4 battle stance, deep crimson skin, broken horn banded in runic iron, long sweeping right horn, glowing amber slit eyes, blackened iron collar, subtle black smoke rising, dramatic firelight rim lighting, framed by an ornate barbed iron and sculpted infernal flame relief pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Malakor tiefling fighter, pitch black background, crimson skin, broken banded horn, blackened plate armor, jagged ember bastard sword, barbed tail, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, anime demon boy, vector, blurry, pink skin, smooth digital painting, 3d render`

---

#### [HERO-38] Irmão Damian, o Inquisidor do Crepúsculo Abissal
- **Classe:** Clérigo | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/tiefling_clerigo_male.png`
- **Ícone:** `assets/sprites/heroes/icones/tiefling_clerigo_male.png`
- **Detalhes Visuais Únicos:** Chifres curvos polidos como obsidiana, olhos brancos perolados desprovidos de pupila, vestes talares de veludo roxo-escuro e prata com estola de seda, empunhando maça estrela de ferro negro com pontas afiadas e relicário de prata em forma de lua minguante que queima com fogo fátuo azul.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Brother Damian, male Tiefling twilight inquisitor cleric, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 tactical angle, deep maroon skin, elegant curved obsidian horns, solid pupilless pearl-white eyes, regal midnight-violet and silver priestly vestments over scale mail, wielding a star-headed blackened iron morningstar and an ethereal silver crescent-moon holy talisman emitting cold blue will-o'-the-wisp flames, calm mysterious expression, crisp pixel outlines, ethereal violet dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, pink skin, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Brother Damian, male Tiefling twilight inquisitor cleric, 32-bit dark fantasy avatar, 3/4 solemn angle, deep maroon skin, polished curved black obsidian horns, solid pearlescent pupilless white eyes, silver inquisitor gorget, ethereal cold blue will-o'-the-wisp rim lighting, framed by an ornate carved black obsidian and silver twilight-rune sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Brother Damian tiefling cleric, pitch black background, maroon skin, obsidian horns, white eyes, midnight-violet vestments, spiked morningstar, blue flame talisman, 32-bit tactical RPG style, sharp pixel edges, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, cute anime, vector, blurry, smooth digital painting, 3d render`

---

#### [HERO-39] Valravn o Purificado, o Paladino das Asas de Cinza
- **Classe:** Paladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/tiefling_paladino_male.png`
- **Ícone:** `assets/sprites/heroes/icones/tiefling_paladino_male.png`
- **Detalhes Visuais Únicos:** Pele carmesim adornada por tatuagens douradas de votos sagrados de purificação, armadura de prata imaculada e marfim com bordas douradas, empunhando espada longa sagrada brilhando com luz divina branca cegante contrastando dramaticamente com sua herança infernal, escudo com brasão solar.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Valravn the Purified, male Tiefling redemption paladin, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 heroic battle stance, noble crimson devil with large backwards horns engraved with holy gold script, wearing immaculate engraved silver and ivory plate armor with golden borders, wielding a radiant longsword blazing with blinding white-gold holy fire contrasting with his fiendish skin, kite shield with radiant sun sigil, tragic noble gaze, crisp pixel contours, divine chiaroscuro, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, pink skin, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Valravn the Purified, male Tiefling redemption paladin champion, 32-bit dark fantasy avatar, 3/4 heroic battle angle, crimson skin etched with holy gold tattoo script, horns banded in gold runes, righteous amber eyes, engraved silver gorget, radiant white-gold holy aura reflection, framed by an ornate sculpted silver and radiant holy sun filigree pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Valravn tiefling paladin, pitch black background, crimson skin, gold engraved horns, shining silver and ivory armor, blazing white holy sword, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, anime waifu, evil demon, blurry, dark corrupt armor, smooth digital painting, 3d render`

---

#### [HERO-40] Azaroth o Necro-Arcanista, o Senhor dos Pactos Astrais
- **Classe:** Mago | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/tiefling_mago_male.png`
- **Ícone:** `assets/sprites/heroes/icones/tiefling_mago_male.png`
- **Detalhes Visuais Únicos:** Chifres longos e elegantes coroados de anéis de prata, olhos de ouro sólido incandescente, túnica acadêmica azul-meia-noite e púrpura bordada com runas cósmicas, flutuando ao seu redor um grimório de couro de dragão com páginas emanando chamas violetas arcanas, cajado de ébano encimado por orbe de ametista.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Azaroth the Astral Arcanist, male Tiefling wizard master, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 isometric stance, deep crimson-red skin, long sweeping obsidian horns banded in silver rings, solid glowing pupilless golden eyes, layered midnight-violet and charcoal embroidered scholarly robes with silver constellations, holding a floating open leather grimoire spouting violet arcane runes in one hand and a carved ebony focus staff topped with a dark amethyst orb, crisp pixel contours, magical glow dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, pink skin, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Azaroth the Astral Arcanist, male Tiefling wizard master, 32-bit dark fantasy avatar, 3/4 intellectual sorcery angle, crimson skin, polished sweeping horns with silver rings, solid glowing pupilless golden eyes, dark midnight-violet scholar cowl, floating purple magical embers, framed by an ornate sculpted solid obsidian block relief pixel art border fitting flush edge-to-edge against all canvas boundaries, celestial silver runes engraved within the frame face, solid pure black background extending behind character, full-bleed 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, white border, white margin, outer border, padding, blank margin, sticker, drop shadow, protruding horns, outer gaps, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Azaroth tiefling wizard, pitch black background, crimson skin, sweeping horns with silver rings, glowing gold eyes, floating violet rune grimoire, amethyst staff, 32-bit tactical RPG style, magical dithering, solid black background, full bleed
```
- **Negative Prompt:** `white border, white margin, outer margin, padding, white background, light background, sticker, chibi, cartoon, vector, anime, cute boy, blurry, smooth digital painting, 3d render`

---

#### [HERO-41] Kallisto Sombra-da-Penumbra, o Caçador de Demônios Renegado
- **Classe:** Patrulheiro | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/tiefling_patrulheiro_male.png`
- **Ícone:** `assets/sprites/heroes/icones/tiefling_patrulheiro_male.png`
- **Detalhes Visuais Únicos:** Olhos âmbar felinos penetrantes na escuridão, pele avermelhada mesclada com tons acinzentados de cinza de fogueira, capuz de caçador com aberturas precisas para os chifres, arco de madeira negra com flechas envoltas em névoa gelada lilás, cauda ágil mantendo equilíbrio perfeito em terrenos íngremes.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Kallisto Gloom-Stalker, male Tiefling ranger bounty-hunter, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 battle stance, lean crimson-skinned hunter with sleek horns swept behind a dark travel cowl, wearing dark studded leather with shadow-weave cloak, drawing a recurve ebony longbow loaded with an arrow tipped in cold violet flame, barbed tail flicking in balance, sharp focused slit eyes, crisp pixel edges, shadowy outdoor dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, pink skin, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Kallisto Gloom-Stalker, male Tiefling ranger hunter, 32-bit dark fantasy avatar, 3/4 stealth hunter angle, dark crimson face, sleek horns projecting through travel hood, piercing amber feline eyes, dark studded leather collar, cold violet twilight rim light, framed by an ornate carved ebony wood and barbed iron arrowheads sculpted pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Kallisto tiefling ranger, pitch black background, crimson skin, dark travel cowl, ebony longbow with violet fire arrow, barbed tail, 32-bit tactical RPG angle, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, vector, anime, bright colorful clothing, blurry, smooth digital painting, 3d render`

---

#### [HERO-42] Balthazar Pé-de-Cabra, o Dançarino das Sombras Enxofradas
- **Classe:** Ladino | **Gênero:** Masculino
- **Sprite:** `assets/sprites/heroes/tiefling_rogue_male.png`
- **Ícone:** `assets/sprites/heroes/icones/tiefling_rogue_male.png`
- **Detalhes Visuais Únicos:** Sorriso diabólico encantador com caninos afiados, capa de seda preta que parece se dissolver em fumaça de enxofre nas bordas, armadura de couro preto sob medida com detalhes em fivelas de bronze, adagas gêmeas kris onduladas de prata, cauda enrolada segurando discretamente uma chave mestra.
- **Prompt Sprite (Midjourney v6):**
```text
Full-body battle sprite of Balthazar Goat-Foot, male Tiefling rogue shadow-blade, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, pitch black solid background, 3/4 low stealth stance, agile crimson-skinned rogue with sleek swept horns, wearing form-fitting midnight-black leather with charcoal cowl, dual-wielding wavy silver kris daggers, prehensile barbed tail holding a smoke vial, sly devilish smirk revealing sharp caninos, glowing golden slit eyes, crisp pixel outlines, stealth chiaroscuro dithering, completely isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250 --no white background, light background, white border, sticker, chibi, cartoon, anime, pink skin, smooth digital painting, 3d render
```
- **Prompt Retrato (128x128 Token):**
```text
Detailed 2.5D pixel art portrait icon of Balthazar Goat-Foot, male Tiefling rogue shadow-blade, 32-bit dark fantasy avatar, 3/4 rogue perspective, handsome crimson features, sleek swept horns, glowing golden slit eyes, sly devilish smirk with sharp canines, black leather cowl with bronze buckles, subtle sulfur smoke wisps, dramatic chiaroscuro shadow, framed by an ornate sculpted blackened-iron and wavy silver kris daggers relief pixel art border, 1:1 square RPG portrait --v 6.0 --ar 1:1 --stylize 250 --no round border, circular frame, circle, coin, medallion, round shield, white background, light background, sticker, cartoon, chibi
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Balthazar tiefling rogue assassin, pitch black background, form-fitting black leather, wavy kris daggers, tail holding smoke bomb, sly smirk, 32-bit tactical RPG style, sharp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `white background, light background, sticker, chibi, cartoon, anime waifu, blurry, vector, smooth digital painting, 3d render`

---

## 4. Cenários dos Atos (Fundos Cinematográficos Widescreen 16:9 em Pixel Art 2.5D)

> **Formato de Exportação:** Imagens 16:9 widescreen (`--ar 16:9`), resolução nativa recomendada de **1280x720** em `assets/backgrounds/Fases/`.  
> **Composição:** Profundidade de camadas (*parallax multi-layered pixel art*), piso com perspectiva isométrica/2.5D para encaixe dos sprites de combate e iluminação de atmosfera em dithering refinado.

---

### ATO I: O Despertar da Maldição

#### [BG-01] Taverna do Dragão Acordado (`tavern_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/tavern_bg.jpg`
```text
Panoramic interior wide shot of a rustic medieval dark fantasy tavern, The Awoken Dragon Tavern, 2.5D HD pixel art environment, 32-bit tactical RPG background, massive crackling stone hearth with glowing orange embers illuminating heavy oak tables and benches, weathered timber ceiling beams, hanging iron chandeliers with dripping candles, ale casks and vintage weapons on stone walls, dark rain lash visible through leaded gothic windows, warm amber firelight fighting deep shadow dithering, handcrafted pixel clusters, Octopath and Tactics Ogre style --ar 16:9 --v 6.0 --stylize 250
```

#### [BG-02] Estrada de Terra & Planícies Nevoentas (`dirt_road_plains_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/dirt_road_plains_bg.jpg`
```text
Wide panoramic landscape of a desolate muddy dirt road cutting through bleak misty plains, 2.5D HD pixel art environment, 32-bit tactical RPG background, low perspective showing wheel ruts and wet gravel in layered pixel texture, scattered dead twisted trees, rolling dark storm clouds over distant jagged mountain silhouettes, cold volumetric fog clinging to ground via ordered dithering, desaturated earth tones with slate sky, crisp pixel detailing, dark fantasy mood --ar 16:9 --v 6.0 --stylize 250
```

#### [BG-03] Floresta Sombria Noturna (`dark_forest_night_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/dark_forest_night_bg.jpg`
```text
Dark haunting ancient forest at night, 2.5D HD pixel art landscape, 32-bit dark fantasy tactical RPG backdrop, colossal gnarled trees with roots like claws framing the sides, dense ground mist swirling through thorny briars in dithering layers, eerie pale blue moonlight cutting through dense canopy branches, glowing fungal spores and distant will-o'-the-wisps, mysterious oppressive depth, handcrafted pixel clusters, Blasphemous atmosphere --ar 16:9 --v 6.0 --stylize 250
```

#### [BG-04] Acampamento dos Bandidos no Cânion (`bandit_camp_canyon_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/bandit_camp_canyon_bg.jpg`
```text
Wide panoramic view of a fortified bandit encampment inside a jagged rocky canyon at dusk, 2.5D HD pixel art environment, 32-bit tactical RPG background, sheer slate-grey cliff walls, ragged leather tents, smoking central bonfire roasting game, wooden palisades and sharpened stakes, stolen crates and iron wagons, ominous blood-red dusk horizon glowing in the background, campfire light cast on stone ground in warm pixel dithering --ar 16:9 --v 6.0 --stylize 250
```

---

### ATO II: A Jornada pelas Terras Amaldiçoadas

#### [BG-05] Passo da Montanha Congelada (`snowy_mountain_pass_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/snowy_mountain_pass_bg.jpg`
```text
Treacherous frozen mountain pass, 2.5D HD pixel art environment, 32-bit dark fantasy tactical RPG background, sheer obsidian cliffs dusted with heavy blizzard snow, howling wind blowing ice particles rendered in delicate pixel dithering, narrow frozen stone ledge path overlooking a bottomless freezing abyss, ancient frozen skeleton markers, cold slate-blue and bone-white color grading, epic cinematic scale --ar 16:9 --v 6.0 --stylize 250
```

#### [BG-06] Ruínas da Fortaleza Esquecida (`forgotten_fort_ruins_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/forgotten_fort_ruins_bg.jpg`
```text
Wide landscape of the crumbling ruins of an ancient dark stone fortress, 2.5D HD pixel art scenery, 32-bit tactical RPG battle backdrop, shattered gothic parapets, collapsed stone arches overgrown with dead black vines, broken rusted iron portcullis, overgrown flagstone courtyard, overcast sky with pale sunbeams piercing through clouds in ordered pixel dithering, ancient headless stone statues, dark fantasy ruins --ar 16:9 --v 6.0 --stylize 250
```

#### [BG-07] Pântano dos Lamentos Tóxicos (`toxic_swamp_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/toxic_swamp_bg.jpg`
```text
Fetid stagnant toxic swamp, 2.5D HD pixel art landscape, 32-bit dark fantasy RPG backdrop, murky dark green waters reflecting a sickly yellow-grey sky, gnarled decaying trees draped in dripping Spanish moss, bubbling poisonous swamp gas, floating spectral emerald will-o'-the-wisps, submerged mossy stone markers and forgotten coffins, sinister eerie atmosphere, crisp pixel clusters with rich water dithering --ar 16:9 --v 6.0 --stylize 250
```

#### [BG-08] Cripta & Cemitério Ancestral (`ancient_cemetery_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/ancient_cemetery_bg.jpg`
```text
Ancient haunted subterranean crypt and graveyard, 2.5D HD pixel art environment, 32-bit dark fantasy tactical RPG background, cracked stone sarcophagi and weathered mossy tombstones, vaulted subterranean corridor with crumbling gothic pillars, iron braziers glowing with dying cyan ethereal flames, cracked marble floor with creeping weeds, pale moonlight filtering through broken stone grates above, solemn chilling chiaroscuro dithering --ar 16:9 --v 6.0 --stylize 250
```

---

### ATO III: As Cinzas da Perdição

#### [BG-09] Caverna de Lava dos Ermos (`lava_cave_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/lava_cave_bg.jpg`
```text
Subterranean volcanic lava cavern, 2.5D HD pixel art battle backdrop, 32-bit dark fantasy tactical RPG arena, basalt rock platforms surrounded by flowing rivers of glowing molten magma, bubbling heat distortion rendered in pixel art dithering, stalactites of black obsidian, floating sparks and sulfurous smoke plumes, dramatic warm glow against pitch-black subterranean stone, intense chiaroscuro --ar 16:9 --v 6.0 --stylize 250
```

#### [BG-10] Observatório Astral Quebrado (`arcane_observatory_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/arcane_observatory_bg.jpg`
```text
Ruined celestial arcane observatory perched atop a mountain spire, 2.5D HD pixel art environment, 32-bit dark fantasy RPG background, colossal shattered brass armillary sphere and giant cracked telescope apparatus, broken domed gothic roof revealing a swirling cosmic rift of deep violet and starlight, glowing mystic zodiac runes burning into cracked marble tiles, magical ethereal particles, epic astronomical grandeur --ar 16:9 --v 6.0 --stylize 250
```

#### [BG-11] O Covil do Tirano: Caldeira de Obsidiana (`O_Covil_do_Tirano_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/O_Covil_do_Tirano_bg.jpg`
```text
Colossal volcanic throne caldera of the Tyrant Supreme Dragon, 2.5D HD pixel art final boss arena, 32-bit dark fantasy tactical RPG background, towering monolithic obsidian spires, boiling lake of molten scarlet and gold lava, massive throne altar carved from charred dragon bones and hoards of melted gold, thick swirling sulfurous smoke and ashfall, terrifying divine scale, dramatic crimson chiaroscuro dithering, Blasphemous and Diablo 2 climax aesthetic --ar 16:9 --v 6.0 --stylize 280
```

#### [BG-12] Cena de Clímax & Déjà Vu (`deja_vu_bg.jpg`)
- **Arquivo:** `assets/backgrounds/Fases/deja_vu_bg.jpg`
```text
Surreal liminal time-rift chamber, climax scene of temporal loop, 2.5D HD pixel art backdrop, 32-bit dark fantasy RPG setting, crumbling stone floor floating above an endless void of shattered hourglasses and frozen clock gears, ethereal chromatic aberration and monochrome ash particles, ghostly silhouettes of the party repeated in temporal echoes, pale spectral white and deep charcoal contrast, haunting psychological mystery --ar 16:9 --v 6.0 --stylize 260
```

---

## 5. Elementos de Interface Gráfica (UI Textures em Pixel Art)

> **Regra de UI:** Texturas de interface em Pixel Art puro, com paleta de couro, pergaminho, latão e ferro forjado, sem gradientes suaves modernos ou vidro translúcido contemporâneo.

---

### [UI-01] Mochila do Aventureiro (`backpack_bg.png`)
- **Arquivo:** `assets/ui/backpack_bg.png`
- **Dimensões:** 800x600 pixels (Modal de Inventário)
- **Prompt Midjourney v6:**
```text
Top-down adventurer's open backpack inventory container, 2.5D HD pixel art UI asset, 32-bit dark fantasy RPG interface, worn dark brown oiled leather exterior with stitched borders, antique brass buckles and iron eyelets, symmetrical compartmentalized slots lined with dark charcoal velvet for holding potions weapons and scrolls, clean pixel grid layout, rustic handcrafted pixel clusters, no text, transparent or solid neutral background --ar 4:3 --v 6.0 --stylize 200
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art UI texture, open adventurer leather backpack inventory screen, brown distressed leather, brass buckles, organized grid slots for items, dark fantasy 32-bit style, crisp pixel edges, isolated
```
- **Negative Prompt:** `smooth digital painting, 3d render, modern zipper, cartoon, anime, blurry, gradient UI`

---

### [UI-02] Grimório Aberto (`open_book.png`)
- **Arquivo:** `assets/ui/open_book.png`
- **Dimensões:** 800x500 pixels (Modal de Magias / Diário de Quests)
- **Prompt Midjourney v6:**
```text
Open ancient spellbook and leather grimoire, 2.5D HD pixel art UI asset, 32-bit dark fantasy RPG interface, heavy open volume with weathered yellowish parchment pages, dark cracked brown leather binding with tarnished brass corner brackets, delicate pixelated magical margins with faded alchemical watermarks, blank center pages ready for text rendering, ornate antique bookmark ribbon, crisp pixel borders, isolated on black background --ar 16:10 --v 6.0 --stylize 200
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art UI asset, open ancient grimoire book, aged yellow parchment pages, leather binding with brass corners, 32-bit dark fantasy style, clean central space for text, sharp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, clean modern paper, glossy, anime, blurry`

---

## 6. Formatos de Exportação, Resoluções e Checklist Técnico para Pygame

Para assegurar que o Pygame renderize o Pixel Art 2.5D com nitidez cristalina, sem desfoque bilinear indesejado e com desempenho ótimo:

### 1. Tabela Canônica de Formatos e Pastas do Projeto

| Categoria | Caminho do Diretório | Formato | Dimensão Gerada | Dimensão no Pygame | Notas Técnicas |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Boss Colossal** | `assets/sprites/enemies/` | `.png` | 512x512 | 512x512 | Canal Alfa (RGBA), fundo transparente |
| **Monstros Médios/Grandes** | `assets/sprites/enemies/` | `.png` | 256x256 / 384x384 | 256x256 / 384x384 | Canal Alfa (RGBA), 3/4 ângulo tático |
| **Sprites de Heróis** | `assets/sprites/heroes/` | `.png` | 256x256 | 256x256 | Canal Alfa (RGBA), postura 2.5D |
| **Ícones de Retrato (HUD)** | `assets/sprites/heroes/icones/` | `.png` | 128x128 | 128x128 ou 64x64 | 1:1 quadrado, moldura integrada |
| **Cenários dos Atos** | `assets/backgrounds/Fases/` | `.jpg` / `.png` | 1280x720 | 1280x720 | 16:9 widescreen, otimizado |
| **Texturas de UI** | `assets/ui/` | `.png` | 800x600 | Variável | Canal Alfa (RGBA), fivelas e abas |

---

### 2. Tratamento de Imagem Pós-Geração (Pipeline Anti-Blur)

1. **Remoção de Fundo Seguro:**
   - Como os monstros e heróis foram gerados sobre preto puro (`#000000`), use a ferramenta *Color to Alpha* (GIMP/Photoshop/Aseprite) ou recorte por varinha mágica sem suavização de aresta (*Anti-aliasing = OFF*, *Tolerance = 10-15*).
   - Nunca use recorte com desfoque gaussiano, pois bordas semitransparentes criam anéis brilhantes nos motores 2D.

2. **Escala sem Borrão no Pygame (Nearest Neighbor):**
   - No código Python/Pygame, ao redimensionar qualquer sprite de Pixel Art, utilize sempre `pygame.transform.scale(surface, (w, h))` — que preserva a integridade dos pixels através do algoritmo vizinho mais próximo (*Nearest Neighbor*).
   - **NUNCA** utilize `pygame.transform.smoothscale()` em sprites pixel art, pois este comando introduz interpolação bilinear que destrói o charme dos pixels nítidos.

3. **Validação da Paleta:**
   - Execute um teste visual de contraste colocando o sprite do monstro sobre o cenário `O_Covil_do_Tirano_bg.jpg` e `dark_forest_night_bg.jpg`.
   - Se o sprite se misturar excessivamente com o fundo, reforce o contorno externo com uma linha de 1 pixel em carvão escuro (`#111215`).

---

### 3. Checklist Rápido Pré-Commit de Novos Assets

- [ ] A imagem é genuinamente **Pixel Art 2.5D / 32-bit** (sem gradientes vetoriais ou render 3D)?
- [ ] O sprite está em ângulo de **três quartos tático (3/4 perspective)**?
- [ ] O fundo foi removido e salvo como **PNG-32 com transparência (RGBA)**?
- [ ] O arquivo foi nomeado exatamente com o nome padrão em minúsculas (ex: `fire_giant.png`, `tavern_bg.jpg`)?
- [ ] O arquivo foi alocado na pasta correta sob `assets/`?

---

## 7. Expansão Canônica: Bestiário Faltante e Variações de Linha

Esta seção complementa e expande o ecossistema visual do RPGMesaPY para cobrir 100% dos monstros e variações catalogados no código-fonte, nos arquivos de dados (`data/bestiary.json`) e na estrutura de diretórios do motor Pygame.

---

### 7.1 Bestiário Faltante (Monstros e Subchefes do Motor de Jogo)

Todos os monstros listados abaixo pertencem ao bestiário oficial do jogo e devem ser renderizados rigorosamente no padrão **2.5D HD Pixel Art / 32-bit**, isolados sobre fundo preto puro para extração de canal alfa.

---

#### [MON-17] Armadura Animada (`animated_armor.png`)
- **Arquivo Destino:** `assets/sprites/enemies/animated_armor.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Hollow ancient suit of Animated Armor battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric perspective, blackened battered steel plate armor with brass filigree, empty visor helmet glowing with subtle eerie violet arcana, spectral blue magical energy pulsing faintly through articulated joints and gorget, brandishing a heavy notched steel longsword and a dented iron tower shield, heavy metallic weight, crisp pixel outlines, chiaroscuro metal dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, hollow magical Animated Armor, battered gothic steel plate, glowing violet empty visor, longsword and shield, 32-bit tactical RPG style, metallic reflections dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, human face inside helmet, blurry`

---

#### [MON-18] Gárgula de Pedra Ancestral (`gargoyle.png`)
- **Arquivo Destino:** `assets/sprites/enemies/gargoyle.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Monstrous stone Gargoyle creature battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 perspective crouching on stone corbel, weathered chiseled granite body with mossy fissures and stone cracks, grotesque demonic horned head with leering jagged teeth, colossal stone bat wings half-spread, razor-sharp rocky talons gripping the edge, cold glowing yellow gemstone eyes, crisp pixel outlines, gritty chiseled rock dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, gothic stone Gargoyle monster, chiseled rock texture, mossy fissures, bat wings, horn crest, glowing eyes, 32-bit tactical RPG angle, handcrafted pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, plastic, smooth gradients, cartoon, anime, blurry`

---

#### [MON-19] Geleia Ocre Ácida (`ochre_jelly.png`)
- **Arquivo Destino:** `assets/sprites/enemies/ochre_jelly.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Amorphous predatory Ochre Jelly ooze battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 top-down tactical perspective, pulsating mass of corrosive yellowish-amber gelatinous slime pooling across flagstones, semi-translucent jelly body dissolving digested iron fragments and bone shards inside, thick dripping acidic pseudopods lashing outwards with smoking sizzle, glistening specular highlight clusters, delicate translucent pixel dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, Ochre Jelly acidic ooze monster, pulsating amber sludge, dissolving bones and rusty metal, dripping pseudopods, 32-bit retro tactical RPG battle view, crisp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cute slime cartoon, anime, flat color, blurry`

---

#### [MON-20] Ogro Brutal Campeão (`ogre_brute.png`)
- **Arquivo Destino:** `assets/sprites/enemies/ogre_brute.png`
- **Resolução de Render:** 384x384 pixels (Sprite Grande)
- **Prompt Midjourney v6:**
```text
Colossal elite Ogre Brute warlord battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric battle stance, gigantic scarred grey-skinned body wrapped in rusted iron chains and crude iron scrap armor plates, horned brutal iron skullcap helm, huge protruding yellow lower tusks in a vicious roar, wielding a terrifying spiked two-handed iron warclub banded with barbed wire, brutal muscle definition, crisp pixel outlines, heavy cross-hatch dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, elite Ogre Brute champion, iron chains, scrap plate armor, massive barbed club, tusks and scars, 32-bit dark fantasy tactical RPG aesthetic, sharp pixel edges, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, cute, blurry, smooth gradients`

---

#### [MON-21] Guerreiro Orc das Hordas (`orc.png`)
- **Arquivo Destino:** `assets/sprites/enemies/orc.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Savage Orc Warrior frontline raider battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical battle angle, muscular hulking frame, mottled dark grey-green leathery skin with ritual battle scars, prominent jagged lower canine tusks, aggressive snarling brow, wearing battered studded leather armor reinforced with dark iron plates and fur pauldrons, wielding a heavy notched iron greataxe with both hands, aggressive forward rush stance, crisp pixel outlines, gritty dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, brutal dark fantasy Orc warrior sprite, grey-green skin, tusks, studded armor, heavy two-handed greataxe, 32-bit tactical RPG angle, crisp pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cartoon orc, anime, bright green skin, blurry`

---

#### [MON-22] Rakshasa Feérico Infernal (Subchefe - `rakshasa.png`)
- **Arquivo Destino:** `assets/sprites/enemies/rakshasa.png`
- **Resolução de Render:** 384x384 pixels
- **Prompt Midjourney v6:**
```text
Sinister Rakshasa fiend noble sub-boss battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 isometric perspective, humanoid feline body with a menacing royal Bengal tiger head, predatory slitted yellow eyes, backward-inverted feline hands tipped with razor claws holding a curved gilded dagger and an illusion orb, dressed in opulent regal imperial robes of dark crimson and gold brocade, floating illusory purple and gold magical glyphs, aristocratic menacing posture, crisp pixel outlines, rich fabric dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 260
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Rakshasa fiend noble, tiger head, inverted hands, ornate crimson and gold silk robes, glowing illusion magic, 32-bit tactical RPG sub-boss style, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cute tiger, vector, anime furry, blurry, flat color`

---

#### [MON-23] Sombra Mortífera Incorpórea (`shadow.png`)
- **Arquivo Destino:** `assets/sprites/enemies/shadow.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Undead Shadow incorporeal wraith-creature battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 perspective, terrifying living humanoid silhouette composed of swirling pitch-black smoke and liquid darkness, ragged wispy shadow tendrils drifting from limbs, two pinprick cold white ethereal eyes staring through the darkness, claws reaching forward to drain vitality, dark aura devouring light in ordered pixel dithering, crisp silhouette contours, Blasphemous aesthetic, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art, incorporeal Shadow monster, swirling pure darkness and black smoke, cold glowing pinprick eyes, wispy tendrils, 32-bit tactical RPG style, subtle shadow dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, colorful, cartoon, vector, blurry anti-aliasing`

---

#### [MON-24] Solar Celestial Caído / Corrompido (`solar.png`)
- **Arquivo Destino:** `assets/sprites/enemies/solar.png`
- **Resolução de Render:** 512x512 pixels (Sprite Colossal)
- **Prompt Midjourney v6:**
```text
Corrupted Fallen Solar angel supreme warrior battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 majestic isometric battle stance, colossal divine being with six enormous feathered wings stained in ash and burning dark embers, cracked blackened gold plate armor over mourning robes, blindfolded face weeping tears of dark ichor, wielding a towering colossal greatsword burning with righteous dark-gold flame, radiant yet tragic aura rendered in delicate pixel dithering, crisp pixel outlines, Tactics Ogre aesthetic, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 280
```
- **Prompt SDXL / Flux.1:**
```text
colossal 2.5D pixel art sprite, Fallen Solar archangel, six ash-stained feathered wings, cracked golden plate armor, burning divine greatsword, 32-bit dark fantasy tactical RPG, chiaroscuro dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cute anime angel, vector, oversaturated, blurry`

---

#### [MON-25] Veterano Mercenário de Elite (`veteran.png`)
- **Arquivo Destino:** `assets/sprites/enemies/veteran.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Elite Veteran Mercenary champion battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, battle-tested middle-aged warrior, graying hair and beard, scarred stony face, wearing heavy steel splint plate armor over reinforced chainmail, faded heraldic surcoat of a fallen kingdom, wielding an ornate balanced steel bastard sword and an iron parrying dagger in off-hand, grounded military precision, crisp pixel contours, steel reflection dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, Veteran Mercenary warrior, scarred knight, heavy plate and chainmail, bastard sword and parrying dagger, 32-bit tactical RPG aesthetic, handcrafted pixel clusters, isolated on solid black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, vector, anime, bright colors, blurry`

---

#### [MON-26] Aparição Espectral / Wraith (Subchefe - `wraith.png`)
- **Arquivo Destino:** `assets/sprites/enemies/wraith.png`
- **Resolução de Render:** 384x384 pixels
- **Prompt Midjourney v6:**
```text
Terrifying Wraith sub-boss floating specter battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 perspective hovering above the floor, hollow crowned cowl draped in tattered pitch-black shadowy burial shrouds trailing into smoke, skeletal gauntlets crackling with cold cyan necrotic flames, faceless dark void inside hood with two piercing malevolent turquoise eyes, brandishing a ghostly ethereal scythe that weeps soul particles, atmospheric chilling dithering, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 260
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 2.5D pixel art sprite, dark fantasy Wraith specter, floating hooded phantom, tattered black robes, cyan necrotic fire, spectral scythe, 32-bit tactical RPG sub-boss, crisp pixel clusters, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cartoon ghost, anime, blurry, vector`

---

#### [MON-27] Zumbi Rastejador Veloz (`zombie_fast.png`)
- **Arquivo Destino:** `assets/sprites/enemies/zombie_fast.png`
- **Resolução de Render:** 256x256 pixels
- **Prompt Midjourney v6:**
```text
Feral Fast Runner Zombie predator battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 low crouched tactical perspective, emaciated frenzied decaying corpse in a low quad sprint posture ready to leap, hyper-extended jaws with jagged blood-stained teeth, wild hollow milk-white eyes, shredded clothing scraps, skeletal sinewy muscles visible under pale mottled rotting skin, frantic vicious energy, crisp pixel contours, gritty dirt dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art sprite, fast feral runner Zombie, low crouching leaping pose, decaying flesh, vicious open maw, 32-bit tactical RPG style, crisp pixel edges, earthy horror dithering, isolated on black background
```
- **Negative Prompt:** `smooth digital painting, 3d render, cartoon, anime, slow walker, blurry`

---

### 7.2 Variações Táticas para Monstros Comuns (Tropas e Lacaios de Linha)

Para evitar repetição visual em combates contra hordas, criamos variações táticas canônicas em Pixel Art 2.5D para todos os monstros comuns de infantaria.

---

#### [VAR-01] Arqueiro Goblin (`goblin_archer.png`)
- **Arquivo:** `assets/sprites/enemies/goblin_archer.png`
- **Prompt Midjourney v6:**
```text
Goblin Archer sniper battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, wiry olive-green skin, notched large pointed ears, wearing scavenged leather jerkin with bone shoulder guard, drawing a crude bent shortbow notched with a barbed bone-tipped arrow, leather quiver slung on back, squinting cunning red eye, crouching ready to fire, crisp pixel outlines, earthy dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-02] Xamã Goblin dos Ossos (`goblin_shaman.png`)
- **Arquivo:** `assets/sprites/enemies/goblin_shaman.png`
- **Prompt Midjourney v6:**
```text
Goblin Witch Doctor Shaman battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 tactical angle, wizened wrinkled goblin draped in ragged crow feathers and rodent skulls, wielding a crooked gnarled wooden staff crowned with a horned ram skull emitting sickly green poisonous smoke, left hand crackling with wild sparks, ritual mud war paint, crisp pixel contours, magical dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-03] Esqueleto Arqueiro das Tumbas (`skeleton_archer.png`)
- **Arquivo:** `assets/sprites/enemies/skeleton_archer.png`
- **Prompt Midjourney v6:**
```text
Undead Skeleton Archer sniper battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, yellowed skeletal human bones held together by dark rot, wearing broken rusted iron chainmail scraps, drawing a blackened yew composite longbow loaded with an ancient iron-tipped arrow, ribs acting as a quiver holding spare rusted shafts, faint cold cyan pinpoint light in hollow eye sockets, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-04] Esqueleto Cavaleiro de Escudo (`skeleton_knight.png`)
- **Arquivo:** `assets/sprites/enemies/skeleton_knight.png`
- **Prompt Midjourney v6:**
```text
Heavy Skeleton Knight guardian battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 defensive isometric stance, skeletal warrior encased in heavily corroded blackened iron full plate and a visored sallet helm, holding a heavy notched broadsword resting on a colossal rusted iron tower shield bearing a desecrated holy crest, impenetrable defensive stance, crisp pixel contours, metallic rust dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-05] Zumbi Encouraçado (`zombie_armored.png`)
- **Arquivo:** `assets/sprites/enemies/zombie_armored.png`
- **Prompt Midjourney v6:**
```text
Armored Zombie brute battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 lumbering angle, rotting swollen corpse tightly crammed into punctured, rusted plate breastplate and broken iron gorget, dragging a heavy corroded iron mace behind on stone, dull lifeless eyes, unstoppable heavy shambling momentum, flies and decay rendered in subtle pixel clusters, crisp outlines, dark gritty palette, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-06] Orc Berserker em Fúria (`orc_berserker.png`)
- **Arquivo:** `assets/sprites/enemies/orc_berserker.png`
- **Prompt Midjourney v6:**
```text
Frenzied Orc Berserker battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 dynamic attack stance, bare-chested hulking muscular orc covered in crimson war paint and slashing scars, wearing spiky iron greaves and wolf pelt belt, dual-wielding brutal barbed one-handed waraxes with bloodied edges, glowing bloodshot red eyes, roaring wide jaw exposing deadly lower tusks, crisp pixel outlines, visceral action dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-07] Orc Arqueiro de Guerra (`orc_archer.png`)
- **Arquivo:** `assets/sprites/enemies/orc_archer.png`
- **Prompt Midjourney v6:**
```text
Orc Heavy Archer sniper battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 battle stance, broad-shouldered muscular orc wearing thick boiled leather brigandine, pulling the heavy string of an enormous dark iron-reinforced warbow, heavy barbed iron arrow aimed at player, iron nasal helmet, grim disciplined glare with jutting tusks, heavy physical mass, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-08] Bandido Balestreiro Emboscador (`bandit_crossbow.png`)
- **Arquivo:** `assets/sprites/enemies/bandit_crossbow.png`
- **Prompt Midjourney v6:**
```text
Bandit Crossbowman sniper battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 crouched shooting angle, stealthy mercenary highwayman wearing dark leather cuirass with shoulder cape, dark cloth mask concealing lower face, aiming a heavy cocked iron-and-wood crossbow loaded with an armor-piercing steel bolt, bandolier of quarrel bolts across chest, calculating lethal stance, crisp pixel contours, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-09] Bandido Degolador Furtivo (`bandit_cutthroat.png`)
- **Arquivo:** `assets/sprites/enemies/bandit_cutthroat.png`
- **Prompt Midjourney v6:**
```text
Bandit Cutthroat assassin battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 low stealth stance, wiry rogue mercenary wrapped in a tattered dark travel cloak with pulled cowl, dual-wielding serrated curved daggers dripping black paralyzing oil, agile light-footed ready-to-lunge crouch, shadows cloaking features with only cold eyes glinting, crisp pixel outlines, stealth chiaroscuro dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-10] Kobold Armadilheiro / Alquimista (`kobold_trapper.png`)
- **Arquivo:** `assets/sprites/enemies/kobold_trapper.png`
- **Prompt Midjourney v6:**
```text
Kobold Trapper Saboteur battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 agile perspective, small rust-scaled reptilian scout carrying an oversized wicker pack overflowing with coiled ropes, bear traps, and glass flasks of volatile alchemical fire, holding a smoking ceramic fire-bomb ready to hurl, manic grinning snout with sharp teeth, twitching reptilian tail, crisp pixel contours, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-11] Kobold Fundibulário Ágil (`kobold_slinger.png`)
- **Arquivo:** `assets/sprites/enemies/kobold_slinger.png`
- **Prompt Midjourney v6:**
```text
Kobold Slinger skirmisher battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 agile stance, small lean reptilian humanoid with dark copper scales, spinning a weighted leather sling overhead loaded with a heavy lead bullet, pouch of projectiles strapped to hip, scavenged rat-skull helmet, nervous darting amber eyes, dynamic dodging posture, crisp pixel outlines, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

#### [VAR-12] Lobo Atroz Alfa das Matas (`dire_wolf_alpha.png`)
- **Arquivo:** `assets/sprites/enemies/dire_wolf_alpha.png`
- **Prompt Midjourney v6:**
```text
Dire Wolf Alpha pack-leader battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 majestic predatory battle stance, massive prime predator twice the size of standard wolves, jet-black thick matted fur with silver battle-scars, glowing crimson predatory eyes, long sabre-like fangs dripping steam in cold night air, muscular coiled shoulders raised in a terrifying dominant posture, crisp pixel outlines, atmospheric frost dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 260
```

#### [VAR-13] Aranha Gigante Cuspidora de Ácido (`giant_spider_spitter.png`)
- **Arquivo:** `assets/sprites/enemies/giant_spider_spitter.png`
- **Prompt Midjourney v6:**
```text
Giant Spitter Spider arachnid battle sprite, 2.5D HD pixel art, 32-bit dark fantasy tactical RPG, 3/4 top-down tactical angle, bloated bulbous abdomen glowing with pulsating toxic fluorescent green venom glands, barbed spiny chitinous legs splayed, reared-up posture spitting a concentrated stream of sticky acidic web and green venom, cluster of gleaming obsidian eyes, crisp pixel clusters, venom glow dithering, isolated on solid pure black background --v 6.0 --ar 1:1 --stylize 250
```

---

### 7.3 Diretriz de Integração dos Heróis no Motor da História

Os 42 heróis catalogados exaustivamente na **Seção 3** deste manual constituem a base canônica tanto para o protagonista selecionado pelo jogador quanto para o recrutamento dinâmico de aliados no decorrer da campanha:
1. **Identificadores Canônicos:** Os nomes e epítetos introduzidos (ex: *Sir Alistair*, *Kargan*, *Balthazar*, *Aeloria*, *Thorgar*, *Malakor*) devem ser utilizados pelo Mestre de IA em diálogos, descrições de combate e eventos de história.
2. **Resolução e Nomenclatura:** Todos os arquivos de sprites devem ser depositados em `assets/sprites/heroes/` (256x256 pixels com canal alfa) e os respectivos ícones em `assets/sprites/heroes/icones/` (128x128 pixels com moldura de pixel art).
3. **Escalonamento sem Borrão:** A interface Pygame deve renderizar os sprites através de `pygame.transform.scale` (Nearest-Neighbor), assegurando o charme e a nitidez dos pixels 32-bit.

---

## 8. Compêndio de Equipamentos Raciais Únicos & Spritesheet do Dado d20 Girando

### 8.1 Os 7 Itens Únicos Raciais (Herança Ancestral)

Cada raça inicia sua jornada carregando uma relíquia ancestral única no slot de Acessório/Herança, esculpida em **32-bit Pixel Art Dark Fantasy** (formato quadrado **32x32 / 40x40 pixels**, moldura chanfrada de bronze envelhecido e ouro, fundo escuro sólido `#111215`).

---

#### [RAC-01] Humano: Sinete da Coroa Partida (`i_racial_human_signet`)
- **Arquivo Destino:** `assets/ui/items/i_racial_human_signet.png`
- **Semiótica Visual:** Anel de sinete pesado em ouro imperial oxidado, ostentando uma pedra de ônix negro cravejada com o brasão em relevo de uma coroa real partida ao meio por uma fissura incandescente.
- **Paleta Hex:** Ouro Imperial (`#d4af37`), Ônix Negro (`#18181b`), Brasa Real (`#f97316`), Bronze Chanfro (`#8b6f47`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art item icon, Signet of the Sundered Crown human racial heirloom (`i_racial_human_signet`), heavy tarnished imperial gold signet ring set with a flat black onyx stone engraved with a cracked royal crown emblem glowing with a faint ember fissure, dark fantasy tactical RPG inventory icon, square format with beveled antique bronze and gold border, crisp pixel clusters, ordered dithering, Diablo II and Blasphemous UI aesthetic, solid pure dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 32-bit pixel art UI item icon, weathered gold signet ring with black onyx seal of a shattered crown, human racial relic, dark fantasy RPG, square beveled antique bronze frame, crisp pixel outlines, ordered dithering, solid dark background
```

---

#### [RAC-02] Elfo da Floresta: Manto de Folhas Cinzentas (`i_racial_elf_cloak`)
- **Arquivo Destino:** `assets/ui/items/i_racial_elf_cloak.png`
- **Semiótica Visual:** Manto élfico de viagem tecido com folhas de outono cinzentas e musgo esmeralda petrificado, preso no colarinho por um broche de prata lunar em forma de folha de freixo.
- **Paleta Hex:** Verde Musgo Élfico (`#15803d`), Cinza Fuligem (`#64748b`), Prata Lunar (`#e2e8f0`), Fundo Penumbra (`#052e16`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art item icon, Cloak of Ashen Leaves wood elf racial heirloom (`i_racial_elf_cloak`), hooded elven travel cloak woven from ash-dusted silver-grey and deep emerald forest leaves fastened by a crescent moonstone silver leaf brooch, swirling woodland mist, dark fantasy tactical RPG icon, square format with beveled weathered bronze and gold frame, crisp handcrafted pixels, ordered dithering, Tactics Ogre UI style, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art RPG item icon, elven cloak of grey ash leaves and emerald moss with silver leaf clasp, wood elf racial relic, dark fantasy 32-bit style, square beveled bronze border, sharp pixel clusters, dark backdrop
```

---

#### [RAC-03] Anão da Colina: Runa da Pedra-Forja (`i_racial_dwarf_rune`)
- **Arquivo Destino:** `assets/ui/items/i_racial_dwarf_rune.png`
- **Semiótica Visual:** Placa octagonal de granito e basalto das profundezas, reforçada com grampos de ferro batido e entalhada no centro com uma runa ancestral de forja preenchida por ouro e lava incandescente.
- **Paleta Hex:** Laranja Forja (`#ea580c`), Amarelo Magma (`#facc15`), Pedra Basalto (`#334155`), Ferro Forjado (`#1e293b`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art item icon, Forge-Stone Rune hill dwarf racial heirloom (`i_racial_dwarf_rune`), heavy octagonal carved basalt tablet bound in riveted iron bands, glowing in the center with an ancient dwarven master-smith rune pulsing with molten gold and magma heat, dark fantasy RPG inventory icon, square shape with beveled tarnished bronze and gold frame, crisp pixel edges, chiaroscuro dithering, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
2.5D pixel art item icon, dwarven carved stone rune tablet glowing with molten forge fire and gold veins, hill dwarf racial heirloom, dark fantasy 32-bit RPG UI, square beveled bronze frame, sharp pixels, dark background
```

---

#### [RAC-04] Halfling: Moeda da Sorte Antiga (`i_racial_halfling_coin`)
- **Arquivo Destino:** `assets/ui/items/i_racial_halfling_coin.png`
- **Semiótica Visual:** Antiga moeda de ouro e electrum batida de forma irregular, com furo quadrado central atravessado por um cordão de couro gasto, gravada com uma roda da fortuna e trevo estilizado que reluz com faíscas douradas.
- **Paleta Hex:** Ouro Reluzente (`#fbbf24`), Cobre Antigo (`#b45309`), Brilho da Sorte (`#fef08a`), Couro Cordão (`#451a03`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art item icon, Ancient Lucky Coin halfling racial heirloom (`i_racial_halfling_coin`), antique hand-struck gold and electrum coin on a worn leather cord, embossed with a mystical wheel of fortune and four-leaf clover motif glinting with golden luck sparkles, dark fantasy tactical RPG icon, square format with beveled antique bronze and gold border, crisp pixel clusters, ordered dithering, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art UI item icon, ancient minted gold lucky coin charm on leather string with sparkling golden glint, halfling racial relic, dark fantasy 32-bit, square beveled bronze frame, crisp pixel art, dark backdrop
```

---

#### [RAC-05] Draconato: Escama Ancestral Incandescente (`i_racial_dragon_scale`)
- **Arquivo Destino:** `assets/ui/items/i_racial_dragon_scale.png`
- **Semiótica Visual:** Escama espessa e facetada de dragão ancestral em obsidiana e carmesim, sulcada por veios internos de brasa vulcânica que nunca se apagam, engastada em um suporte de bronze negro.
- **Paleta Hex:** Vermelho Dracônico (`#dc2626`), Brasa Viva (`#f97316`), Escama Obsidiana (`#1c1917`), Ouro Velho (`#cda869`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art item icon, Incandescent Ancestral Scale dragonborn racial heirloom (`i_racial_dragon_scale`), thick jagged ancient dragon scale of crimson and blackened obsidian pulsing with internal veins of glowing volcanic ember, mounted in dark bronze claws, dark fantasy tactical RPG icon, square format with beveled weathered bronze and gold frame, crisp pixel outlines, dramatic firelight dithering, solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece pixel art item icon, glowing red and obsidian dragon scale relic pulsing with molten veins, dragonborn racial heirloom, dark fantasy 32-bit RPG, square beveled bronze border, sharp pixels, dark background
```

---

#### [RAC-06] Meio-Orc: Presa de Ferro Sangrento (`i_racial_orc_tusk`)
- **Arquivo Destino:** `assets/ui/items/i_racial_orc_tusk.png`
- **Semiótica Visual:** Amuleto brutal formado por uma presa curva de marfim amarelado com a ponta encapada em ferro negro afiado, amarrada com tiras de couro e gravada com marcas tribais de sangue seco.
- **Paleta Hex:** Marfim Osso (`#ded1c1`), Sangue Coagulado (`#991b1b`), Ferro Negro (`#334155`), Fundo Carvão (`#09090b`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art item icon, Blood-Iron Tusk half-orc racial heirloom (`i_racial_orc_tusk`), savage curved war-boar ivory tusk capped with jagged blackened iron and bound in leather thongs, etched with glowing crimson blood-runes of unyielding fury, dark fantasy tactical RPG icon, square format with beveled tarnished bronze and iron border, crisp pixel clusters, gritty dithering, solid dark background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
pixel art RPG item icon, brutal ivory tusk amulet tipped with spiked black iron and crimson tribal runes, half-orc racial relic, dark fantasy 32-bit style, square beveled frame, sharp pixel art, dark background
```

---

#### [RAC-07] Tiefling: Selo de Brasas Abissais (`i_racial_tiefling_seal`)
- **Arquivo Destino:** `assets/ui/items/i_racial_tiefling_seal.png`
- **Semiótica Visual:** Talismã infernal de ferro estígio forjado no formato de dois chifres curvados que abraçam uma gema de enxofre rubi-violeta, exalando volutas de fumaça sulfúrica e faíscas abissais.
- **Paleta Hex:** Carmesim Infernal (`#be123c`), Violeta Abissal (`#9333ea`), Fogo Enxofre (`#fb923c`), Ferro Estígio (`#1e1b4b`).
- **Prompt Midjourney v6:**
```text
32-bit pixel art item icon, Seal of Abyssal Embers tiefling racial heirloom (`i_racial_tiefling_seal`), infernal dark stygian iron talisman shaped like curved demonic horns clasping a burning violet-crimson hellfire gem, wisp of sulfurous smoke and cinders, dark fantasy tactical RPG icon, square format with beveled antique bronze and gold border, crisp pixel edges, ordered dithering, Blasphemous UI aesthetic, solid pure black background --v 6.0 --ar 1:1 --stylize 250
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 32-bit pixel art item icon, horned infernal iron talisman with glowing hellfire ruby and purple brimstone smoke, tiefling racial relic, dark fantasy RPG, square beveled bronze frame, sharp pixels, dark background
```

---

### 8.2 Spritesheet Canônico da Animação do Dado d20 Girando

Para unificar a identidade visual entre o **Dado d20 da Ficha de Personagem** e a **Animação de Rolagem de Dados na Tela de Jogo**, o d20 deve ser renderizado como um icosaedro facetado de rubi carmesim com gaiola/arestas de ouro velho em 12 quadros de rotação contínua.

- **Arquivo Destino:** `assets/ui/dice/d20_spin_spritesheet.png`
- **Layout do Spritesheet:** Fita horizontal `12x1` (ex: `768x64` pixels, sendo 12 frames de `64x64` pixels cada) ou Grid `4x3` (12 frames).
- **Design Visual Idêntico à Ficha:**
  - **Corpo do Dado:** Cristal de rubi sangue facetado (`#991b1b` nas faces de sombra, `#dc2626` nas faces médias, `#ef4444` nas faces iluminadas).
  - **Arestas e Engastes:** Filigrana de ouro velho e bronze polido (`#cda869`, `#d4af37`, `#78350f`).
  - **Numeração:** Algarismos serrilhados em pixel art dourado-claro (`#fef08a`), exibindo o número `20` com brilho crítico no frame final de parada.
- **Prompt Midjourney v6 (Spritesheet de 12 Frames):**
```text
32-bit pixel art game animation spritesheet, 12 sequential frames arranged in a clean grid of a spinning 20-sided polyhedral icosahedron d20 die, faceted deep crimson ruby gemstone body with ornate antique gold metal edges and engraved golden numbers, rotating smoothly across 12 angles with subtle golden spark trails, final frame resting upright showing the number 20 glowing brightly, dark fantasy tabletop RPG UI asset, crisp pixel clusters, ordered dithering, no motion blur, isolated on solid pure black background --v 6.0 --ar 4:3 --stylize 200
```
- **Prompt SDXL / Flux.1:**
```text
masterpiece 32-bit pixel art animation spritesheet, 12 frames of a rotating 20-sided d20 icosahedron die, faceted blood-ruby crystal with antique gold wireframe ridges and pixel numbers, dark fantasy RPG dice roll animation, crisp pixel art edges, ordered dithering, isolated on solid black background
```
- **Negative Prompt:** `smooth 3d render, vector art, motion blur, blurry anti-aliasing, plastic modern dice, neon colors, white background, cropped edges, inconsistent sizes`

