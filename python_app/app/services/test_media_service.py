from app.services.media_engine import MediaService

media = MediaService.get_media(1)

print(f"Found {len(media)} media")

for item in media:

    print("----------------")

    print(item.id)
    print(item.media_name)
    print(item.media_type)
    print(item.file_path)
    print(item.duration)