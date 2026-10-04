"""Download public-domain artwork images from The Met's open-access set.

Images come from the public Google Cloud mirror of The Met's open-access
collection (gs://gcs-public-data--met). Each entry's caption describes the
object actually shown, which is sometimes a related work rather than the one
named in the narration (for example a Vermeer at the Met instead of Girl with
a Pearl Earring).

Writes assets/artworks/<slug>.jpg and assets/artworks/credits.json.
"""
import io
import json
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

OUT = Path(__file__).parent / "assets" / "artworks"
BUCKET = "https://storage.googleapis.com/gcs-public-data--met"

# slug: (Met object ID, title, artist, date)
ART = {
    "kouros": (253370, "Marble statue of a kouros", "Greek, Attic", "c. 590-580 BCE"),
    "nefertiti": (545803, "Relief of Queen Nefertiti", "Egypt, Amarna period", "c. 1353-1336 BCE"),
    "standard_of_ur": (322903, "Headdress, Royal Cemetery at Ur", "Sumerian", "c. 2600-2500 BCE"),
    "hammurabi": (329072, "Statue of Gudea", "Neo-Sumerian", "c. 2090 BCE"),
    "shang_bronze": (76974, "Ritual altar set", "Shang dynasty, China", "late 11th c. BCE"),
    "olmec": (310279, "Mask", "Olmec, Mexico", "900-400 BCE"),
    "doryphoros": (246991, "Diadoumenos, after Polykleitos", "Roman copy", "1st-2nd c. CE"),
    "augustus": (247993, "Portrait of the emperor Augustus", "Roman, marble", "c. 14-37 CE"),
    "pantheon": (348799, "The Pantheon", "etching by G. B. Piranesi", "18th c."),
    "pompeii": (247017, "Cubiculum from a villa at Boscoreale", "Roman wall painting", "c. 50-40 BCE"),
    "chartres": (466580, "Stained glass, Legend of St. Vincent", "French", "c. 1245-47"),
    "fan_kuan": (40002, "Landscape in the style of Fan Kuan", "China, Northern Song", "early 12th c."),
    "ife_head": (312290, "Head of an Oba", "Edo artist, Benin", "16th c."),
    "giotto": (436504, "The Adoration of the Magi", "Giotto", "possibly c. 1320"),
    "arnolfini": (436282, "The Crucifixion; The Last Judgment", "Jan van Eyck", "c. 1440-41"),
    "mona_lisa": (337496, "Head of the Virgin (study)", "Leonardo da Vinci", "1510-13"),
    "sistine": (337497, "Studies for the Libyan Sibyl", "Michelangelo", "c. 1510-11"),
    "school_of_athens": (342969, "The Group, from the School of Athens", "Agostino Veneziano after Raphael", "1523"),
    "durer": (366555, "Draughtsman Drawing a Reclining Woman", "after Albrecht Dürer", "design 1525"),
    "caravaggio": (437986, "The Denial of Saint Peter", "Caravaggio", "1610"),
    "bernini_teresa": (206399, "Bacchanal: A Faun Teased by Children", "Gian Lorenzo Bernini", "c. 1616-17"),
    "night_watch": (437397, "Self-Portrait", "Rembrandt", "1660"),
    "vermeer_pearl": (437879, "Study of a Young Woman", "Johannes Vermeer", "c. 1665-67"),
    "horatii": (436105, "The Death of Socrates", "Jacques-Louis David", "1787"),
    "friedrich_wanderer": (438417, "Two Men Contemplating the Moon", "Caspar David Friedrich", "c. 1825-30"),
    "delacroix_liberty": (438814, "The Abduction of Rebecca", "Eugène Delacroix", "1846"),
    "courbet_stonebreakers": (438820, "Young Ladies of the Village", "Gustave Courbet", "1851-52"),
    "manet_dejeuner": (436947, "Boating", "Édouard Manet", "1874"),
    "manet_olympia": (436964, "Young Lady in 1866", "Édouard Manet", "1866"),
    "monet_impression": (437127, "Bridge over a Pond of Water Lilies", "Claude Monet", "1899"),
    "seurat_jatte": (437658, "Study for A Sunday on La Grande Jatte", "Georges Seurat", "1884"),
    "hokusai_wave": (45434, "Under the Wave off Kanagawa", "Katsushika Hokusai", "c. 1830-32"),
    "starry_night": (436535, "Wheat Field with Cypresses", "Vincent van Gogh", "1889"),
    "cezanne": (435878, "Mont Sainte-Victoire", "Paul Cézanne", "c. 1902-06"),
    "munch_scream": (340029, "The Scream (lithograph)", "Edvard Munch", "1895"),
}

MAX_SIDE = 1400


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    credits = {}
    for slug, (oid, title, artist, date) in ART.items():
        dest = OUT / f"{slug}.jpg"
        if not dest.exists():
            try:
                data = urllib.request.urlopen(f"{BUCKET}/{oid}/0.jpg", timeout=120).read()
            except urllib.error.HTTPError as e:
                print(f"{slug}: skipped ({e.code})")
                continue
            img = Image.open(io.BytesIO(data)).convert("RGB")
            img.thumbnail((MAX_SIDE, MAX_SIDE))
            img.save(dest, quality=88)
            print(f"{slug}: {img.size}")
        credits[slug] = {
            "title": title, "artist": artist, "date": date,
            "source": f"The Metropolitan Museum of Art, object {oid}",
            "url": f"https://www.metmuseum.org/art/collection/search/{oid}",
        }
    (OUT / "credits.json").write_text(json.dumps(credits, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
