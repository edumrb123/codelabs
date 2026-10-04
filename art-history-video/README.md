# How Humans Learned to Make Pictures

A ~20-minute, 3Blue1Brown-style explainer on the history of art, from the Blombos
Cave ochre (c. 75,000 years ago) to AI images (2022). Made with
[Manim Community](https://www.manim.community/) and narrated by
[Kokoro-82M](https://github.com/thewh1teagle/kokoro-onnx), a free, local,
Apache-2.0 text-to-speech model. No accounts or API keys needed.

The original brief is in [`../prompts/3b1b-art-history-video.md`](../prompts/3b1b-art-history-video.md).

## Files

| File | What it is |
| --- | --- |
| `narration.py` | The full script, split into chapters and "beats" (one audio clip each). Edit this to change what is said. |
| `tts.py` | Turns every beat into a WAV with Kokoro and records its length. Only changed beats are regenerated. |
| `common.py` | Visual style (CMU Serif, dark background, 3b1b palette), the three recurring dials (Space / Purpose / Medium), artwork cards and vector motifs. |
| `scenes.py` | One Manim scene per chapter (`Ch00` ... `Ch12`). Animations are timed to the narration via `NarratedScene.say()`. |
| `build.sh` | Runs TTS, renders all chapters in parallel and joins them into `art_history_<res>.mp4`. |

## Setup (Ubuntu/Debian)

```bash
sudo apt-get install -y libcairo2-dev libpango1.0-dev pkg-config ffmpeg fonts-cmu
python3 -m venv venv && . venv/bin/activate
pip install manim kokoro-onnx soundfile

mkdir models
curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o models/voices-v1.0.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

No LaTeX is needed: all text uses Manim's `Text`.

## Build

```bash
./build.sh                 # 720p30, about 15 min on 4 CPU cores
QUALITY=h ./build.sh       # 1080p60
QUALITY=l ./build.sh       # fast 480p preview
./build.sh Ch05            # re-render one chapter, then re-join the full video
```

### Change the voice

```bash
python tts.py --voice bm_george     # British male; also af_heart, am_adam, bf_emma, ...
python tts.py --speed 0.95
```

Then re-run `./build.sh`. Scenes stretch or shrink automatically to the new clip
lengths.

## Adding real artwork images

Every artwork appears as a framed card. Without an image, the card shows a
simplified vector sketch or a generic icon. To use a real picture, drop a file
named `<slug>.jpg` (or `.png`) into `assets/artworks/` and re-render. Please only
use images you're allowed to use. Good public-domain sources include Wikimedia
Commons and the open-access collections of the Met, Rijksmuseum, Art Institute of
Chicago and National Gallery of Art. Many 20th-century works (Picasso, Dalí, Kahlo,
Magritte, Rothko, Warhol, Kusama, Basquiat...) are still under copyright, so keep
the vector versions for those unless you have permission.

Slugs: `lion_man sulawesi willendorf gobekli_tepe nefertiti standard_of_ur
hammurabi shang_bronze olmec nok kritios_boy doryphoros augustus pantheon pompeii
terracotta_army gandhara_buddha book_of_kells chartres fan_kuan ajanta nataraja
ife_head giotto arnolfini last_supper mona_lisa david sistine school_of_athens
durer bernini_teresa night_watch vermeer_pearl horatii goya_third_may
friedrich_wanderer raft_medusa delacroix_liberty courbet_stonebreakers
manet_dejeuner manet_olympia monet_impression hokusai_wave starry_night cezanne
munch_scream demoiselles af_klint kandinsky black_square fountain magritte_pipe
dali kahlo guernica rothko abramovic spiral_jetty kusama basquiat`

## Accuracy notes

The script follows the brief's rules: approximate dates are marked "c.",
contested points are stated out loud (the earliest cave art, Hilma af Klint vs.
Kandinsky, who made *Fountain*, the debate over Vermeer and optical devices), and
it corrects common myths (white Greek statues, the golden-ratio Parthenon,
Michelangelo painting on his back). Check these before publishing:

- Sulawesi dating (at least 51,200 years, Leang Karampuang, *Nature* 2024). Newer
  finds may have pushed the record back.
- Blombos engraved ochre is given as c. 75,000 years. Different pieces are dated
  roughly 70,000-100,000 years.
- Beeple sale: $69,346,250 at Christie's, March 2021.
