"""
action_service.py

Executes everything after a product is recognized.
"""

from app.services.esp32_service import ESP32Service


class ActionService:

    @staticmethod
    def execute(product):

        if product is None:
            return

        print("--------------------------------")
        print("PRODUCT :", product.name)
        print("LED     :", product.led_effect)
        print("--------------------------------")

        # LED Effect
        ESP32Service.send_effect(product.led_effect)

        # Future
        # MediaService.show(product)
        # AudioService.speak(product)
        # AnalyticsService.log(product)