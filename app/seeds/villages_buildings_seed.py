from app.core.database import SessionLocal
from app.models.building import Building
from app.models.villages import Villages


def seed_villages_and_buildings(db):
    db = SessionLocal()

    try:
        # =========================
        # VILLAGES
        # =========================
        villages = [
            Villages(
                id=1,
                name="Vila Inicial",
                # building_cost_modifier=1.00,
                starting_reward_coins=1500,
                starting_reward_gems=1,
                starting_reward_xp=0,
                starting_reward_energy=10,
                starting_reward_item_slug="itemVillage1",
            ),
            Villages(
                id=2,
                name="Vila Mercantil",
                # building_cost_modifier=1.15,
                starting_reward_coins=2500,
                starting_reward_gems=2,
                starting_reward_xp=400,
                starting_reward_energy=12,
                starting_reward_item_slug="itemVillage2",
            ),
            Villages(
                id=3,
                name="Vila Real",
                # building_cost_modifier=1.8,
                starting_reward_coins=4000,
                starting_reward_gems=3,
                starting_reward_xp=700,
                starting_reward_energy=15,
                starting_reward_item_slug="itemVillage3",
            ),
            Villages(
                id=4,
                name="Vila Imperial",
                # building_cost_modifier=2.7,
                starting_reward_coins=6500,
                starting_reward_gems=5,
                starting_reward_xp=1100,
                starting_reward_energy=18,
                starting_reward_item_slug="itemVillage4",
            ),
            Villages(
                id=5,
                name="Capital Lendária",
                # building_cost_modifier=3.9,
                starting_reward_coins=10000,
                starting_reward_gems=8,
                starting_reward_xp=1700,
                starting_reward_energy=22,
                starting_reward_item_slug="itemVillage5",
            ),
        ]

        db.bulk_save_objects(villages)
        db.flush()

        # =========================
        # BUILDINGS
        # XP é por estágio (4 estágios)
        # =========================
        buildings = [
            # =========================
            # VILA 1 — INICIAL
            # =========================
            Building(
                id=1,
                village_id=1,
                name="Casa Simples",
                building_stages=4,
                base_cost=300,
                cost_multiplier=1.25,
                base_completion_reward_xp=8,
            ),
            Building(
                id=2,
                village_id=1,
                name="Poço",
                building_stages=4,
                base_cost=450,
                cost_multiplier=1.28,
                base_completion_reward_xp=10,
            ),
            Building(
                id=3,
                village_id=1,
                name="Celeiro",
                building_stages=4,
                base_cost=650,
                cost_multiplier=1.30,
                base_completion_reward_xp=12,
            ),
            Building(
                id=4,
                village_id=1,
                name="Prefeitura",
                building_stages=4,
                base_cost=900,
                cost_multiplier=1.35,
                base_completion_reward_xp=16,
            ),  # âncora

            # =========================
            # VILA 2 — MERCANTIL
            # =========================
            Building(
                id=5,
                village_id=2,
                name="Mercado",
                building_stages=4,
                base_cost=900,
                cost_multiplier=1.30,
                base_completion_reward_xp=18,
            ),
            Building(
                id=6,
                village_id=2,
                name="Moinho",
                building_stages=4,
                base_cost=1200,
                cost_multiplier=1.32,
                base_completion_reward_xp=20,
            ),
            Building(
                id=7,
                village_id=2,
                name="Oficina",
                building_stages=4,
                base_cost=1500,
                cost_multiplier=1.35,
                base_completion_reward_xp=22,
            ),
            Building(
                id=8,
                village_id=2,
                name="Banco Mercantil",
                building_stages=4,
                base_cost=2000,
                cost_multiplier=1.40,
                base_completion_reward_xp=28,
            ),  # âncora

            # =========================
            # VILA 3 — REAL
            # =========================
            Building(
                id=9,
                village_id=3,
                name="Guarda Real",
                building_stages=4,
                base_cost=1800,
                cost_multiplier=1.35,
                base_completion_reward_xp=30,
            ),
            Building(
                id=10,
                village_id=3,
                name="Jardins Reais",
                building_stages=4,
                base_cost=2400,
                cost_multiplier=1.38,
                base_completion_reward_xp=34,
            ),
            Building(
                id=11,
                village_id=3,
                name="Salão do Trono",
                building_stages=4,
                base_cost=3200,
                cost_multiplier=1.42,
                base_completion_reward_xp=38,
            ),
            Building(
                id=12,
                village_id=3,
                name="Castelo",
                building_stages=4,
                base_cost=4200,
                cost_multiplier=1.45,
                base_completion_reward_xp=46,
            ),  # âncora

            # =========================
            # VILA 4 — IMPERIAL
            # =========================
            Building(
                id=13,
                village_id=4,
                name="Quartel Imperial",
                building_stages=4,
                base_cost=3000,
                cost_multiplier=1.38,
                base_completion_reward_xp=48,
            ),
            Building(
                id=14,
                village_id=4,
                name="Aqueduto",
                building_stages=4,
                base_cost=3600,
                cost_multiplier=1.40,
                base_completion_reward_xp=52,
            ),
            Building(
                id=15,
                village_id=4,
                name="Câmara Imperial",
                building_stages=4,
                base_cost=4800,
                cost_multiplier=1.42,
                base_completion_reward_xp=58,
            ),
            Building(
                id=16,
                village_id=4,
                name="Palácio Imperial",
                building_stages=4,
                base_cost=6000,
                cost_multiplier=1.48,
                base_completion_reward_xp=68,
            ),  # âncora

            # =========================
            # VILA 5 — LENDÁRIA
            # =========================
            Building(
                id=17,
                village_id=5,
                name="Santuário Antigo",
                building_stages=4,
                base_cost=4500,
                cost_multiplier=1.45,
                base_completion_reward_xp=72,
            ),
            Building(
                id=18,
                village_id=5,
                name="Biblioteca Arcana",
                building_stages=4,
                base_cost=5500,
                cost_multiplier=1.48,
                base_completion_reward_xp=78,
            ),
            Building(
                id=19,
                village_id=5,
                name="Forja Lendária",
                building_stages=4,
                base_cost=7000,
                cost_multiplier=1.50,
                base_completion_reward_xp=86,
            ),
            Building(
                id=20,
                village_id=5,
                name="Trono dos Deuses",
                building_stages=4,
                base_cost=9000,
                cost_multiplier=1.55,
                base_completion_reward_xp=100,
            ),
        ]

        db.bulk_save_objects(buildings)
        db.commit()

        print("✅ Villages and Buildings seeded successfully")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
