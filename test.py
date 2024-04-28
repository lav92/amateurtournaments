import requests

"""
    open dota api
"""
# url_match = "https://api.opendota.com/api/matches/7707960268"
#
# url_request_match = "https://api.opendota.com/api/request/7707960268"
# url_job = "https://api.opendota.com/api/request/196559881"
#
# parsed = "https://api.opendota.com/api/parsedMatches"
# # response = requests.get(url_match)
# # response_req = requests.post(url_request_match) #{"job":{"jobId":196559881}}
# response = requests.get(url_job)
#
# # print(response_req.text)
# # print(response.text)
# print(response, response.text, response.content, sep='\n')
#
# response_parse = requests.get(parsed)
#
# print(response_parse.text)

"""
    stratz api
    token - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYTgzM2QwOTEtNzFlZS00MWIzLWJiZjUtMDllYTAxZjYyNTA1IiwiU3RlYW1JZCI6IjEyMzMwNDUwNjQiLCJuYmYiOjE3MTQyNDI5NzcsImV4cCI6MTc0NTc3ODk3NywiaWF0IjoxNzE0MjQyOTc3LCJpc3MiOiJodHRwczovL2FwaS5zdHJhdHouY29tIn0.WAk48WeRVjCcO1r3cFVxwOKH9u4PwhN3ix64a-72uS4
"""

BASE_URL = "https://api.stratz.com"

ABILITY_URL = f"{BASE_URL}/api/v1/Ability"
GAME_VERSION_URL = f"{BASE_URL}/api/v1/GameVersion"
HERO_URL = f"{BASE_URL}/api/v1/Hero"
ITEM_URL = f"{BASE_URL}/api/v1/Item"
MATCH_URL = f"{BASE_URL}/api/v1/match/7707584671"
LANG_URL = f"{BASE_URL}/api/v1/Language"
PLAYER_URL = f"{BASE_URL}/api/v1/Player"

HEADERS = {
    "Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYTgzM2QwOTEtNzFlZS00MWIzLWJiZjUtMDllYTAxZjYyNTA1IiwiU3RlYW1JZCI6IjEyMzMwNDUwNjQiLCJuYmYiOjE3MTQyNDI5NzcsImV4cCI6MTc0NTc3ODk3NywiaWF0IjoxNzE0MjQyOTc3LCJpc3MiOiJodHRwczovL2FwaS5zdHJhdHouY29tIn0.WAk48WeRVjCcO1r3cFVxwOKH9u4PwhN3ix64a-72uS4"}

my_steam_id = "1233045064"

response = requests.get(MATCH_URL, headers=HEADERS)

print(response, response.text, response.content, '\n')
