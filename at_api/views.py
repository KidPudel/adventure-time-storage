from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import aiohttp
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from .models import ATCharacter
from asgiref.sync import sync_to_async


characters_from_api: list[ATCharacter] = []


# make
@sync_to_async
def add_characters_to_db():
    for character in characters_from_api:
        character.save()


# Create your views here.
async def get_characters_to_db(request):
    # retrieve api characters from api
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://www.giantbomb.com/api/franchise/3025-2327/?api_key=13dc9ad28a61cb1518a45ac93d983e2356a8c28b"
        ) as response:
            if response.ok:
                # parse xml response
                xml_content = await response.text()
                parsed_xml = ET.fromstring(xml_content)
                characters = parsed_xml.findall("results/characters/character")

                character_api_endpoints = list(
                    map(
                        lambda character: character.find("api_detail_url").text
                        + "?api_key=13dc9ad28a61cb1518a45ac93d983e2356a8c28b",
                        characters,
                    )
                )

                # get character details
                for endpoint in character_api_endpoints:
                    async with session.get(endpoint) as response:
                        if response.ok:
                            # name real_name image/medium_url, deck, friends/friend/name
                            character_xml = await response.text()
                            parsed_character_xml = ET.fromstring(character_xml)
                            # add to database
                            character_from_api = ATCharacter(
                                name=parsed_character_xml.find("results/name").text,
                                real_name=parsed_character_xml.find(
                                    "results/real_name"
                                ).text,
                                image=parsed_character_xml.find(
                                    "results/image/medium_url"
                                ).text,
                                short_description=parsed_character_xml.find(
                                    "results/deck"
                                ).text,
                                description=parsed_character_xml.find(
                                    "results/description"
                                ).text,
                                friends=list(
                                    map(
                                        lambda friend: friend.find("name").text,
                                        parsed_character_xml.findall(
                                            "results/friends/friend"
                                        ),
                                    )
                                ),
                            )
                            characters_from_api.append(character_from_api)
                        else:
                            return HttpResponse(response.status)
                    await add_characters_to_db()
                return HttpResponse("ok")
            else:
                return JsonResponse(response.status)


def get_characters(request):
    characters = ATCharacter.objects.all()
    json_characters = []
    for character in characters:
        json_character = character.__dict__
        json_character.pop("_state", None)
        json_characters.append(json_character)
    print(json_characters[0])
    return JsonResponse({"characters": json_characters})
