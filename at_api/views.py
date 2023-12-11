from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import aiohttp
import xml.etree.ElementTree as ET

# Create your views here.

async def get_characters(request):
    # retrieve api characters from api
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.giantbomb.com/api/franchise/3025-2327/?api_key=13dc9ad28a61cb1518a45ac93d983e2356a8c28b") as response:
            if (response.ok):
                # parse xml response
                xml_content = await response.text()
                parsed_xml = ET.fromstring(xml_content)
                characters = parsed_xml.findall("results/characters/character")
                character_api_endpoints = list(map(lambda character: character.find('api_detail_url').text + "?api_key=13dc9ad28a61cb1518a45ac93d983e2356a8c28b", characters))

                for endpoint in character_api_endpoints:
                    print(endpoint)
                    async with session.get(endpoint) as response:
                        if (response.ok):
                            print(response.status)
                        else:
                            return HttpResponse(response.status)

                return HttpResponse("ok")
            else:
                return JsonResponse(response.status)