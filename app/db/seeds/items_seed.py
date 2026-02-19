from app.core.database import SessionLocal
from app.db.models.item import Item


def seed_items(db):
    db = SessionLocal()

    try:

        items = [
            Item(
                id=1,
                slug="item1",
                image_url="https://example.com/item1.png",
                model_url="https://example.com/item1.obj",
                name="Item 1",
                rarity=1.0,
                type="hat",
            ),
            Item(
                id=2,
                slug="item2",
                image_url="https://example.com/item2.png",
                model_url="https://example.com/item2.obj",
                name="Item 2",
                rarity=0.5,
                type="hat",
            ),
            Item(
                id=3,
                slug="item3",
                image_url="https://example.com/item3.png",
                model_url="https://example.com/item3.obj",
                name="Item 3",
                rarity=0.25,
                type="hat",
            ),
            # vilas
            Item(
                id=4,
                slug="itemVillage1",
                image_url="https://example.com/item3.png",
                model_url="https://example.com/item3.obj",
                name="Item 3",
                rarity=0.25,
                type="hat",
            ),
            Item(
                id=5,
                slug="itemVillage2",
                image_url="https://example.com/item3.png",
                model_url="https://example.com/item3.obj",
                name="Item 3",
                rarity=0.25,
                type="hat",
            ),
            Item(
                id=6,
                slug="itemVillage3",
                image_url="https://example.com/item3.png",
                model_url="https://example.com/item3.obj",
                name="Item 3",
                rarity=0.25,
                type="hat",
            ),
            Item(
                id=7,
                slug="itemVillage4",
                image_url="https://example.com/item3.png",
                model_url="https://example.com/item3.obj",
                name="Item 3",
                rarity=0.25,
                type="hat",
            ),
            Item(
                id=8,
                slug="itemVillage5",
                image_url="https://example.com/item3.png",
                model_url="https://example.com/item3.obj",
                name="Item 3",
                rarity=0.25,
                type="hat",
            ),
            # EVENT ITEMS
            Item(
                id=9,
                slug="valentines_dress",
                image_url="https://example.com/item1.png",
                model_url="https://example.com/item1.obj",
                name="Valentine's Dress",
                rarity=1.0,
                type="outfit",
            ),
            Item(
                id=10,
                slug="witch_hat",
                image_url="https://example.com/witch_hat.png",
                model_url="https://example.com/witch_hat.obj",
                name="Mystical Witch's Pointed Hat",
                rarity=0.78,
                type="hat",
            ),
            Item(
                id=11,
                slug="st_patrick_kimono",
                image_url="https://example.com/st_patrick_kimono.png",
                model_url="https://example.com/st_patrick_kimono.obj",
                name="Lucky Green Kimono",
                rarity=0.6,
                type="outfit",
            ),
            Item(
                id=12,
                slug="summer_bikini",
                image_url="https://example.com/summer_bikini.png",
                model_url="https://example.com/summer_bikini.obj",
                name="Tropical Summer Set",
                rarity=0.7,
                type="outfit",
            ),
            Item(
                id=13,
                slug="moon_hat",
                image_url="https://example.com/moon_hat.png",
                model_url="https://example.com/moon_hat.obj",
                name="Celestial Moon Cap",
                rarity=0.8,
                type="hat",
            ),
            Item(
                id=14,
                slug="straw_hat",
                image_url="https://example.com/straw_hat.png",
                model_url="https://example.com/straw_hat.obj",
                name="Farmer's Straw Hat",
                rarity=0.5,
                type="hat",
            ),
            Item(
                id=15,
                slug="santa_claus_dress",
                image_url="https://example.com/santa_claus_dress.png",
                model_url="https://example.com/santa_claus_dress.obj",
                name="Jolly Santa Dress",
                rarity=0.85,
                type="outfit",
            ),
            Item(
                id=16,
                slug="santa_claus_hat",
                image_url="https://example.com/santa_claus_hat.png",
                model_url="https://example.com/santa_claus_hat.obj",
                name="Christmas Spirit Hat",
                rarity=0.8,
                type="hat",
            ),
            Item(
                id=17,
                slug="pajamas",
                image_url="https://example.com/pajamas.png",
                model_url="https://example.com/pajamas.obj",
                name="Cozy Sleepwear",
                rarity=0.6,
                type="outfit",
            ),
            Item(
                id=18,
                slug="school_uniform",
                image_url="https://example.com/school_uniform.png",
                model_url="https://example.com/school_uniform.obj",
                name="Academy Uniform",
                rarity=0.7,
                type="outfit",
            ),
            Item(
                id=19,
                slug="elf_dress",
                image_url="https://example.com/elf_dress.png",
                model_url="https://example.com/elf_dress.obj",
                name="Enchanted Elf Gown",
                rarity=0.75,
                type="outfit",
            ),
            Item(
                id=20,
                slug="medieval_dress",
                image_url="https://example.com/medieval_dress.png",
                model_url="https://example.com/medieval_dress.obj",
                name="Royal Medieval Gown",
                rarity=0.8,
                type="outfit",
            ),
            Item(
                id=21,
                slug="maid_uniform",
                image_url="https://example.com/maid_uniform.png",
                model_url="https://example.com/maid_uniform.obj",
                name="Elegant Maid Outfit",
                rarity=0.65,
                type="outfit",
            ),
            Item(
                id=22,
                slug="police_uniform",
                image_url="https://example.com/police_uniform.png",
                model_url="https://example.com/police_uniform.obj",
                name="Officer's Patrol Suit",
                rarity=0.7,
                type="outfit",
            ),
            Item(
                id=23,
                slug="police_hat",
                image_url="https://example.com/police_hat.png",
                model_url="https://example.com/police_hat.obj",
                name="Authority Police Cap",
                rarity=0.65,
                type="hat",
            ),
            Item(
                id=24,
                slug="office_shirt",
                image_url="https://example.com/office_shirt.png",
                model_url="https://example.com/office_shirt.obj",
                name="Professional Business Shirt",
                rarity=0.55,
                type="outfit",
            ),
            Item(
                id=25,
                slug="army_hat",
                image_url="https://example.com/army_hat.png",
                model_url="https://example.com/army_hat.obj",
                name="Combat Soldier's Cap",
                rarity=0.72,
                type="hat",
            ),
            Item(
                id=26,
                slug="army_armor",
                image_url="https://example.com/army_armor.png",
                model_url="https://example.com/army_armor.obj",
                name="Tactical Battle Armor",
                rarity=0.9,
                type="outfit",
            ),
        ]

        db.bulk_save_objects(items)
        db.flush()
        db.commit()

        print("✅ Items seeded successfully")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    db = SessionLocal()
    seed_items(db)
