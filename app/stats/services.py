import aiohttp

from app.config import settings
from app.stats.dao import StatsDAO


BASE_URL = "https://api.stratz.com"

ABILITY_URL = f"{BASE_URL}/api/v1/Ability"
GAME_VERSION_URL = f"{BASE_URL}/api/v1/GameVersion"
HERO_URL = f"{BASE_URL}/api/v1/Hero"
ITEM_URL = f"{BASE_URL}/api/v1/Item"
MATCH_URL = f"{BASE_URL}/api/v1/match/"
LANG_URL = f"{BASE_URL}/api/v1/Language"
PLAYER_URL = f"{BASE_URL}/api/v1/Player"

HEADERS = {"Authorization": f"bearer {settings.STRATZ_TOKEN}"}


def define_role(role: int, lane: int) -> str:
    if role == 2:
        return "full support"
    elif role == 1:
        return "support"
    else:
        if lane == 1:
            return "carry"
        elif lane == 2:
            return "mid"
        else:
            return "offlane"


def define_award(award: int) -> str:
    award_dict = {
        0: "no award",
        1: "MVP",
        2: "Best Core",
        3: "Best Support",
    }
    return award_dict.get(award)


async def get_hero_name(hero_id: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(HERO_URL, headers=HEADERS) as response:
            full_data = await response.json()
            return full_data.get(hero_id).get("displayName")


async def retrive_ability_damage(raw_data: list[dict]) -> str:
    if not raw_data:
        return "No data"
    result_data = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(ABILITY_URL, headers=HEADERS) as response:
            ability_data = await response.json()
            for ability in raw_data:
                name = ability_data.get(str(ability.get("abilityId"))).get("language").get("displayName")
                result_data += f'{name}({ability.get("count")}) - {ability.get("amount")}\n'
    return result_data[:-1]


async def retrive_items_damage(raw_data: list[dict]) -> str:
    if not raw_data:
        return "No data"
    result_data = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(ITEM_URL, headers=HEADERS) as response:
            items_data = await response.json()
            for item in raw_data:
                name = items_data.get(str(item.get("itemId"))).get("language").get("displayName")
                result_data += f'{name}({item.get("count")}) - {item.get("amount")}\n'
    return result_data[:-1]


async def get_match_stats(user_id: int, match_id: str, steam_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{MATCH_URL}/{match_id}', headers=HEADERS) as response:
            full_data = await response.json()
            user_stats = None
            for player in full_data.get("players"):
                if player.get("steamAccountId") == steam_id:
                    user_stats = player
                    break
            valuable_data = {
                "user_id": user_id,
                "match_id": int(match_id),
                "hero": await get_hero_name(hero_id=str(user_stats.get("heroId"))),
                "role": define_role(role=user_stats.get("role"), lane=user_stats.get("lane")),
                "result": "Win" if user_stats.get("isVictory") else "Lose",
                "kills": user_stats.get("numKills"),
                "deaths": user_stats.get("numDeaths"),
                "assists": user_stats.get("numAssists"),
                "gpm": user_stats.get("goldPerMinute"),
                "epm": user_stats.get("experiencePerMinute"),
                "gold_spent": user_stats.get("goldSpent"),
                "hero_damage": user_stats.get("heroDamage"),
                "tower_damage": user_stats.get("towerDamage"),
                "imp": user_stats.get("imp"),
                "hero_healing": user_stats.get("heroHealing"),
                "award": define_award(award=user_stats.get("award")),

                "deal_physical_damage": user_stats.get("stats").get("heroDamageReport").get("dealtTotal").get(
                    "physicalDamage"),
                "deal_magic_damage": user_stats.get("stats").get("heroDamageReport").get("dealtTotal").get(
                    "magicalDamage"),
                "deal_pure_damage": user_stats.get("stats").get("heroDamageReport").get("dealtTotal").get("pureDamage"),
                "stun_count": user_stats.get("stats").get("heroDamageReport").get("dealtTotal").get("stunCount"),
                "stun_duration": round(
                    user_stats.get("stats").get("heroDamageReport").get("dealtTotal").get("stunDuration") / 100,
                    2
                ),
                "disable_count": user_stats.get("stats").get("heroDamageReport").get("dealtTotal").get("disableCount"),
                "disable_duration": round(
                    user_stats.get("stats").get("heroDamageReport").get("dealtTotal").get("disableDuration") / 100,
                    2
                ),
                "slow_count": user_stats.get("stats").get("heroDamageReport").get("dealtTotal").get("slowCount"),
                "slow_duration": round(
                    user_stats.get("stats").get("heroDamageReport").get("dealtTotal").get("slowDuration") / 100,
                    2
                ),

                "received_physical_damage": user_stats.get("stats").get("heroDamageReport").get("receivedTotal").get(
                    "physicalDamage"),
                "received_magic_damage": user_stats.get("stats").get("heroDamageReport").get("receivedTotal").get(
                    "magicalDamage"),
                "received_pure_damage": user_stats.get("stats").get("heroDamageReport").get("receivedTotal").get(
                    "pureDamage"),

                "deal_ability_damage": await retrive_ability_damage(
                    raw_data=user_stats.get("stats").get("heroDamageReport").get("dealtSourceAbility")),

                "deal_item_damage": await retrive_items_damage(
                    raw_data=user_stats.get("stats").get("heroDamageReport").get("dealtSourceItem")
                ),
            }

            await StatsDAO.create(**valuable_data)
