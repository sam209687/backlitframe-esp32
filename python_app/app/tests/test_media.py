from app.services.media_engine.media_service import MediaService

media = MediaService.get_media(1)

print(len(media))

for item in media:
    print(item.media_name)