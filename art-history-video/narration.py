"""Narration script for "How Humans Learned to Make Pictures".

Each chapter is a list of (beat_id, text). Every beat becomes its own audio
clip, and the Manim scene for that chapter times its animations to the clip
lengths (see common.py: NarratedScene.say).
"""

CHAPTERS = [
    ("ch00", "Cold open", [
        ("q1", "Here is a flat surface. It has two dimensions: width and height."),
        ("q2", "And here is the world. It has three. Every picture anyone has "
               "ever made is a way of dealing with that mismatch."),
        ("q3", "But there's a second, deeper question hiding underneath. Not just "
               "how do you make a picture, but what is a picture for?"),
        ("q4", "The history of art is the story of humans changing their answers "
               "to those two questions, over and over, for at least seventy "
               "thousand years."),
        ("axes", "To keep track, let's use three dials. The first is space: how "
                 "much does the image try to look like a window into a real, "
                 "deep world? The second is purpose: who is the art for? Spirits, "
                 "gods, kings, merchants, the artist, or the public? And the "
                 "third is medium: what tools and materials make new kinds of "
                 "art possible?"),
        ("q5", "We'll turn these dials as we go. Notice that they don't only "
               "turn in one direction. Art history is not a straight march "
               "toward realism. It's much more interesting than that."),
    ]),
    ("ch01", "Prehistory: the first marks", [
        ("p1", "Let's start as far back as the evidence allows. On a timeline "
               "of human image-making, almost all of it is prehistory."),
        ("p2", "Around seventy-five thousand years ago, at Blombos Cave in South "
               "Africa, someone scratched a crosshatched pattern into a piece of "
               "red ochre. It doesn't depict anything. It's pattern, before "
               "pictures."),
        ("p3", "About forty thousand years ago, in what is now Germany, someone "
               "carved the Lion-Man from mammoth ivory: a figure with a human "
               "body and a lion's head. A creature that doesn't exist. This is "
               "imagination made solid."),
        ("p4", "In Sulawesi, Indonesia, a painted scene of human-like figures "
               "and a pig has been dated to at least fifty-one thousand years "
               "ago, according to a 2024 study. Notice the careful wording: "
               "earliest known. New discoveries keep pushing these dates back."),
        ("p5", "In France, the painters of Chauvet Cave, around thirty-six "
               "thousand years ago, and Lascaux, around seventeen thousand years "
               "ago, did something clever with space. They used the natural "
               "bulges of the rock to give animals volume, and overlapped "
               "figures to suggest a herd in motion."),
        ("p6", "Hand stencils appear on cave walls across the world: pigment "
               "blown around a hand pressed to the rock. A mark that says, "
               "simply, someone was here."),
        ("p7", "Small figures like the Venus of Willendorf, roughly thirty "
               "thousand years old, and huge carved pillars at Göbekli Tepe in "
               "Turkey, around eleven and a half thousand years old, show that "
               "monumental art came even before farming towns."),
        ("p8", "So what was all this for? Honestly, we don't know. Hunting magic, "
               "storytelling, ritual, initiation, or simply the pleasure of "
               "making: each idea has supporters, and the evidence doesn't "
               "settle it. Let's set the purpose dial to a question mark."),
    ]),
    ("ch02", "The first civilizations: art as order", [
        ("e1", "With cities and writing came kings, and with kings came art "
               "whose job was to show order and power."),
        ("e2", "Look at how Egyptian artists drew a person. The head is in "
               "profile, but the eye is drawn from the front. The shoulders "
               "face us, the legs turn sideways again."),
        ("e3", "This isn't a failure to see. Each part is shown from its most "
               "recognizable angle. The picture is a list of complete, "
               "permanent facts about the body, not a snapshot from one place."),
        ("e4", "Size meant importance, not distance. The pharaoh is drawn "
               "larger than everyone else. This is called hierarchical scale, "
               "and you can see it on the Narmer Palette, from around thirty-"
               "one hundred BCE."),
        ("e5", "Artists even laid figures out on a grid, so proportions stayed "
               "consistent. That's a big reason Egyptian art looks so stable "
               "across nearly three thousand years."),
        ("e6", "There were brief experiments. The bust of Queen Nefertiti, "
               "around thirteen forty-five BCE, comes from a short period of "
               "unusual naturalism."),
        ("e7", "And this was happening everywhere at once: the Standard of Ur "
               "and the Stele of Hammurabi in Mesopotamia, Shang dynasty bronzes "
               "in China, the colossal stone heads of the Olmec in Mexico, and "
               "the Nok terracottas of Nigeria. Different answers, same "
               "questions."),
    ]),
    ("ch03", "Greece and Rome: the body in motion", [
        ("g1", "Early Greek statues, around six hundred BCE, look a lot like "
               "Egyptian ones: stiff, symmetric, one foot forward, weight evenly "
               "split."),
        ("g2", "Then, over about a century, something changes. Watch the line "
               "through the hips and the line through the shoulders."),
        ("g3", "Put the weight on one leg, and that hip rises. To balance, the "
               "shoulders tilt the opposite way. The body forms a gentle S-curve. "
               "This is called contrapposto, and it makes stone look alive."),
        ("g4", "You can see it arriving in the Kritios Boy, around four eighty "
               "BCE, and perfected in Polykleitos' Spear Bearer, around four "
               "forty BCE, which we know mostly from Roman copies."),
        ("g5", "Now, a myth to correct. We picture Greek sculpture as pure white "
               "marble. But these statues were painted, often brightly. Traces of "
               "pigment survive, and researchers have reconstructed the colors."),
        ("g6", "Another myth: that the Parthenon was designed around the golden "
               "ratio. You can draw a golden rectangle over a photo of almost "
               "anything if you choose your edges. There's no good evidence the "
               "builders used it. What they did use were subtle curves that "
               "correct optical illusions."),
        ("g7", "Rome added realistic portrait busts, wrinkles and all, and huge "
               "engineering, like the dome of the Pantheon. Wall paintings at "
               "Pompeii even tried to suggest depth, though without one "
               "consistent system."),
        ("g8", "Meanwhile, the Terracotta Army was buried in China around two "
               "ten BCE, and in Gandhara, in today's Pakistan and Afghanistan, "
               "Greek and Indian styles blended in early Buddhist sculpture. "
               "Our space dial has moved a long way toward realism."),
    ]),
    ("ch04", "Faith and the flattened world", [
        ("f1", "And then, it turns back. After about three hundred CE, "
               "European art becomes flatter, more symbolic, less concerned "
               "with realistic bodies and space."),
        ("f2", "It's tempting to call this a loss of skill. But a better "
               "explanation is a change of goal. If a picture is a window onto "
               "heaven, not onto the physical world, then realistic depth "
               "isn't the point."),
        ("f3", "In Byzantine mosaics and icons, figures float on a field of "
               "gold. The gold isn't a sky or a wall. It's a kind of non-space: "
               "the divine."),
        ("f4", "So the space dial turns down, on purpose, and the purpose dial "
               "points firmly at the Church. The so-called Dark Ages were not an "
               "artistic void: think of the Book of Kells, around eight hundred, "
               "or the light pouring through the stained glass of Chartres "
               "Cathedral."),
        ("f5", "In the Islamic world, religious art largely avoided depicting "
               "figures, and turned instead to geometry. Start with a square. "
               "Rotate a copy by forty-five degrees. Repeat the tile, and the "
               "plane fills with stars."),
        ("f6", "In Song dynasty China, landscape painters like Fan Kuan, "
               "around the year one thousand, used shifting viewpoints, so the "
               "eye travels up a mountain instead of seeing it from one fixed "
               "spot. In India, the Ajanta cave paintings and the Chola bronzes "
               "of the dancing Shiva. In West Africa, the remarkably naturalistic "
               "brass heads of Ife."),
    ]),
    ("ch05", "The Renaissance: the window", [
        ("r1", "Back in Italy, around thirteen-oh-five, Giotto painted the "
               "Arena Chapel in Padua. His figures have weight. They sit inside "
               "boxy spaces. But the space doesn't quite add up."),
        ("r2", "The fix came from geometry. Around fourteen fifteen, the "
               "architect Filippo Brunelleschi demonstrated linear perspective, "
               "and in fourteen thirty-five Leon Battista Alberti wrote down the "
               "method. Let's build it."),
        ("r3", "Draw a horizon line at the viewer's eye level. Pick a single "
               "point on it: the vanishing point."),
        ("r4", "Now every line that runs straight away from the viewer, the "
               "edges of a floor, a ceiling, a row of columns, must meet at that "
               "point. These are called orthogonals."),
        ("r5", "Across them, draw horizontal lines for the rows of floor tiles. "
               "But how far apart should they be? They have to get closer "
               "together as they recede."),
        ("r6", "Alberti's trick: draw one diagonal across the floor. Wherever it "
               "crosses an orthogonal, that's where the next row begins. The "
               "squares shrink correctly, automatically."),
        ("r7", "Masaccio used exactly this in his Holy Trinity fresco, around "
               "fourteen twenty-seven. The painted chapel seems to cut a "
               "hole in the church wall. People had never seen anything like "
               "it."),
        ("r8", "In the North, Jan van Eyck pushed a different technology: oil "
               "paint. Thin, translucent layers let him render glowing light "
               "and tiny detail, as in the Arnolfini Portrait of fourteen "
               "thirty-four, with its convex mirror."),
        ("r9", "Then came the giants. Leonardo's Last Supper places the "
               "vanishing point right at Christ's head. His Mona Lisa uses "
               "soft, smoky transitions called sfumato, and hazy blue distance. "
               "Michelangelo carved David and painted the Sistine Chapel "
               "ceiling, standing on scaffolding, not lying on his back. "
               "Raphael gathered the philosophers in the School of Athens."),
        ("r10", "Who paid for all this? Increasingly, wealthy merchant families "
                "like the Medici, alongside the Church. And printmaking, through "
                "artists like Albrecht Dürer, meant images could be copied and "
                "spread across Europe."),
    ]),
    ("ch06", "Baroque: drama and light", [
        ("b1", "Once you've mastered the window, what next? The Baroque answer: "
               "drama."),
        ("b2", "Caravaggio lit his scenes like a stage. Most of the picture "
               "falls into darkness, and a hard beam of light picks out the "
               "action. In The Calling of Saint Matthew, finished in sixteen "
               "hundred, the light itself seems to point at Matthew."),
        ("b3", "Bernini did the same in marble, with the Ecstasy of Saint "
               "Teresa. The Catholic Church wanted art that hit you "
               "emotionally, as an answer to the Protestant Reformation."),
        ("b4", "In the Protestant Dutch Republic, there was a new kind of "
               "buyer: ordinary prosperous citizens, buying paintings on an "
               "open market. Rembrandt painted The Night Watch in sixteen "
               "forty-two. Vermeer painted quiet rooms full of light, and "
               "scholars still debate whether he used optical devices to help."),
        ("b5", "And in Spain, in sixteen fifty-six, Diego Velázquez painted Las "
               "Meninas, a painting about looking. The princess looks at us. "
               "Velázquez himself looks out from behind his canvas. And in a "
               "mirror at the back, we glimpse the king and queen."),
        ("b6", "Follow the sightlines. Everyone is looking at the spot where "
               "the king and queen must be standing, which is exactly where you, "
               "the viewer, are standing. The painting quietly puts you inside "
               "it."),
    ]),
    ("ch07", "Revolutions", [
        ("v1", "The late seventeen hundreds brought political revolution, and "
               "art took sides. Jacques-Louis David's Oath of the Horatii, "
               "from seventeen eighty-four, is all crisp lines and civic duty."),
        ("v2", "The Romantics answered with emotion and the sublime. Goya's "
               "Third of May, eighteen fourteen, shows a firing squad as a "
               "faceless machine. Caspar David Friedrich's wanderer stares "
               "into fog. Géricault painted shipwreck survivors, and Delacroix, "
               "Liberty leading the people."),
        ("v3", "Courbet's Realism insisted on painting ordinary labor, at life "
               "size, with no heroics."),
        ("v4", "And then, in eighteen thirty-nine, a new medium was announced to "
               "the world: photography."),
        ("v5", "The principle was old. Light through a small hole projects an "
               "upside-down image of the world. That's a camera obscura. What "
               "was new was a way to fix that image permanently."),
        ("v6", "Now ask what this does to painting. For centuries, one big job "
               "of painting was recording what things look like. Suddenly a "
               "machine could do that. So, what is painting for now?"),
    ]),
    ("ch08", "Breaking the window", [
        ("m1", "In eighteen sixty-three, Édouard Manet showed paintings that "
               "felt deliberately flat, with harsh light and modern subjects. "
               "Le Déjeuner sur l'herbe and Olympia caused scandals."),
        ("m2", "A technology helped too. Paint in portable tubes, patented in "
               "eighteen forty-one, meant artists could work outdoors, quickly, "
               "chasing changing light."),
        ("m3", "In eighteen seventy-four, a group of artists held an independent "
               "exhibition. A critic mocked Claude Monet's painting Impression, "
               "Sunrise, and the insult stuck. They became the Impressionists. "
               "Their subject was light and time itself."),
        ("m4", "They borrowed ideas from color science. Colors opposite each "
               "other on the color wheel, called complementaries, make each "
               "other look more intense when placed side by side."),
        ("m5", "Georges Seurat took it further. In A Sunday on La Grande Jatte, "
               "from eighteen eighty-four to eighty-six, he placed tiny dots of "
               "separate colors side by side, hoping your eye would blend them "
               "from a distance."),
        ("m6", "Japanese woodblock prints, newly flooding into Europe, showed "
               "another way to see: flat color, bold outlines, unusual "
               "cropping, like Hokusai's Great Wave, from around eighteen "
               "thirty-one."),
        ("m7", "Vincent van Gogh used color and brushwork to express feeling, "
               "as in The Starry Night, eighteen eighty-nine. Paul Cézanne "
               "talked about treating nature through the cylinder, the sphere "
               "and the cone. And Edvard Munch's Scream, eighteen ninety-three, "
               "painted an inner state rather than an outer view."),
    ]),
    ("ch09", "The picture becomes the idea", [
        ("c1", "In nineteen-oh-seven, Pablo Picasso painted Les Demoiselles "
               "d'Avignon, drawing in part on African and Iberian sculpture, an "
               "influence that's now discussed with much more care about who "
               "gets credit."),
        ("c2", "With Georges Braque, he developed Cubism. Here's the core idea. "
               "Take an object and look at it from the front, from the side, "
               "and from above."),
        ("c3", "Linear perspective says: pick one of these views. Cubism says: "
               "why choose? Break the views into pieces and assemble them on "
               "one surface. The single fixed viewpoint of the Renaissance is "
               "gone."),
        ("c4", "Next, abstraction. Watch Piet Mondrian's path over a few years. "
               "A tree. Its branches simplified into curves. Then straight "
               "lines. Then just a grid. By the nineteen-twenties, his "
               "paintings are only black lines and blocks of primary color."),
        ("c5", "Who painted the first abstract picture? Kandinsky is often "
               "named, around nineteen eleven, but the Swedish artist Hilma af "
               "Klint was making abstract works from nineteen-oh-six. And in "
               "nineteen fifteen, Kazimir Malevich showed a black square. The "
               "space dial hits zero."),
        ("c6", "In nineteen seventeen, a factory-made urinal was submitted to an "
               "exhibition as a sculpture called Fountain. It's credited to "
               "Marcel Duchamp, though some historians argue it may have "
               "involved the artist Elsa von Freytag-Loringhoven. Either way, "
               "the idea was explosive: art can be a choice, not a craft."),
        ("c7", "René Magritte painted a pipe and wrote underneath: this is not a "
               "pipe. And he's right. It's a picture of a pipe. The whole "
               "question of representation, folded into one joke."),
        ("c8", "Meanwhile, Salvador Dalí painted melting clocks, Frida Kahlo "
               "turned self-portraiture into autobiography, and Picasso's "
               "Guernica, in nineteen thirty-seven, answered the bombing of a "
               "Spanish town with a scream in black and white."),
    ]),
    ("ch10", "After 1945: art about art", [
        ("a1", "After the Second World War, the center of the art world moved "
               "toward New York. Jackson Pollock laid canvases on the floor and "
               "dripped and poured paint across them. The painting became a "
               "record of an action."),
        ("a2", "Mark Rothko painted huge, soft rectangles of color, meant to be "
               "seen up close, to surround you."),
        ("a3", "Pop Art turned to mass culture. Andy Warhol painted thirty-two "
               "Campbell's Soup cans in nineteen sixty-two. Roy Lichtenstein "
               "painted the printed dots of comic books. Notice the echo: "
               "Seurat's dots, eighty years later, now made by a printing "
               "press."),
        ("a4", "Minimalism stripped things down further: a metal box is just a "
               "metal box. And in conceptual art, Sol LeWitt's wall drawings "
               "were sets of instructions. Anyone could carry them out. The "
               "idea was the artwork."),
        ("a5", "Artists left the canvas entirely: performance art, like Marina "
               "Abramović's, land art, like Robert Smithson's Spiral Jetty, and "
               "immersive installations, like Yayoi Kusama's infinity rooms. "
               "And in the early nineteen-eighties, Jean-Michel Basquiat "
               "carried street culture into the gallery."),
    ]),
    ("ch11", "Now", [
        ("n1", "Which brings us to now. The art world is global, and the "
               "medium dial keeps spinning: video, digital, the internet."),
        ("n2", "In twenty eighteen, a Banksy painting shredded itself moments "
               "after selling at auction. The market itself had become part of "
               "the artwork."),
        ("n3", "In twenty twenty-one, a purely digital work by the artist "
               "Beeple, sold as an NFT, went for about sixty-nine million "
               "dollars."),
        ("n4", "And in twenty twenty-two, an image made with an AI image "
               "generator won a prize at the Colorado State Fair, and set off a "
               "fierce debate that is still going."),
        ("n5", "Is that a new kind of art, or not art at all? Notice that it's "
               "the same argument people had about photography, and about "
               "Duchamp's Fountain. The medium changed. The question did not."),
    ]),
    ("ch12", "Closing", [
        ("z1", "So let's replay the whole story on our three dials."),
        ("z2", "Space rose toward realism in Greece and Rome, fell on purpose in "
               "the medieval world, peaked with the Renaissance window, and "
               "then, after photography, was taken apart until nothing was left "
               "but the surface itself."),
        ("z3", "Purpose moved from spirits and gods, to kings and the Church, to "
               "merchants, to the artist's own vision, and finally to ideas, "
               "markets and the public."),
        ("z4", "And every new medium, from ochre to oil paint to cameras to "
               "code, forced the question to be asked again."),
        ("z5", "So maybe the history of art isn't a story of progress. It's a "
               "long record of the different answers people have given to one "
               "simple question."),
        ("z6", "What should a picture do?"),
    ]),
]
