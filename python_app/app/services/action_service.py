"""
action_service.py

Executes the showroom action after a product
has been matched.

Responsibilities

• LED Effect
• Media Playback
• Dashboard Update

Nothing else.
"""

from app.services.esp32_service import ESP32Service
from app.services.media_service import MediaService


class ActionService:

    @staticmethod
    def execute(product):

        print()
        print("================================")
        print("ACTION SERVICE")
        print("================================")
        print("Product :", product.name)
        print("Effect  :", product.led_effect)
        print("Media   :", product.media_path)
        print("================================")

        # -----------------------------
        # LED
        # -----------------------------

        if product.led_effect:

            try:

                ESP32Service.send_effect(
                    product.led_effect
                )

                print(
                    "LED Effect Started"
                )

            except Exception as e:

                print(
                    "LED Error:",
                    e
                )

        # -----------------------------
        # Media
        # -----------------------------

        if product.media_path:

            try:

                MediaService.play_folder(
                    product.media_path
                )

                print(
                    "Media Started"
                )

            except Exception as e:

                print(
                    "Media Error:",
                    e
                )

        print("Action Complete")