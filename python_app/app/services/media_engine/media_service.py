"""
media_service.py

Database service for Media.

Responsibilities
----------------
- Load media
- Add media
- Delete media
- Enable / Disable media
- Update display order
- Validate media files

No UI.
No playback.
"""

from pathlib import Path

from app.core.database import get_session
from app.models.media import Media


class MediaService:

    @staticmethod
    def get_media(product_id):

        session = get_session()

        try:

            return (
                session.query(Media)
                .filter(
                    Media.product_id == product_id,
                    Media.is_active == 1
                )
                .order_by(Media.display_order.asc())
                .all()
            )

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def get_all_for_product(product_id):

        session = get_session()

        try:

            return (
                session.query(Media)
                .filter(Media.product_id == product_id)
                .order_by(Media.display_order.asc(), Media.id.asc())
                .all()
            )

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def get_images(product_id):

        return [
            m for m in MediaService.get_media(product_id)
            if m.media_type.lower() == "image"
        ]

    # --------------------------------------------------

    @staticmethod
    def get_videos(product_id):

        return [
            m for m in MediaService.get_media(product_id)
            if m.media_type.lower() == "video"
        ]

    # --------------------------------------------------

    @staticmethod
    def get_default_media(product_id):

        session = get_session()

        try:

            media = (
                session.query(Media)
                .filter(
                    Media.product_id == product_id,
                    Media.is_default == 1,
                    Media.is_active == 1
                )
                .first()
            )

            return media

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def media_exists(media):

        return Path(media.file_path).exists()

    # --------------------------------------------------

    @staticmethod
    def validate_media(product_id):

        return [
            media
            for media in MediaService.get_media(product_id)
            if MediaService.media_exists(media)
        ]

    # --------------------------------------------------

    @staticmethod
    def add_media(
        product_id,
        media_name,
        media_type,
        file_path,
        duration=10,
        display_order=1,
        is_default=0,
        is_active=1,
        description=""
    ):

        session = get_session()

        try:

            media = Media(
                product_id=product_id,
                media_name=media_name,
                media_type=media_type,
                file_path=file_path,
                duration=duration,
                display_order=display_order,
                is_default=is_default,
                is_active=is_active,
                description=description
            )

            session.add(media)

            session.commit()

            session.refresh(media)

            return media

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def update_media(
        media_id,
        media_name,
        media_type,
        file_path,
        duration=10,
        display_order=1,
        is_default=0,
        is_active=1,
        description=""
    ):

        session = get_session()

        try:

            media = session.get(Media, media_id)

            if not media:
                return None

            media.media_name = media_name
            media.media_type = media_type
            media.file_path = file_path
            media.duration = duration
            media.display_order = display_order
            media.is_default = is_default
            media.is_active = is_active
            media.description = description

            session.commit()

            session.refresh(media)

            return media

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def delete_media(media_id):

        session = get_session()

        try:

            media = session.get(Media, media_id)

            if not media:
                return False

            session.delete(media)

            session.commit()

            return True

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def update_order(media_id, order):

        session = get_session()

        try:

            media = session.get(Media, media_id)

            if not media:
                return False

            media.display_order = order

            session.commit()

            return True

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def enable(media_id):

        session = get_session()

        try:

            media = session.get(Media, media_id)

            if media:
                media.is_active = 1
                session.commit()

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def disable(media_id):

        session = get_session()

        try:

            media = session.get(Media, media_id)

            if media:
                media.is_active = 0
                session.commit()

        finally:
            session.close()
