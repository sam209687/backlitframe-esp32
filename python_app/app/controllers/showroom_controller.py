"""
showroom_controller.py

Central coordinator of the Smart Showroom.

VoiceEngine never controls LEDs or media directly.
Everything goes through this controller.
"""

from app.services.product_matcher import ProductMatcher
from app.services.action_service import ActionService


class ShowroomController:

    def __init__(self):

        self.current_product = None

    # -------------------------------------------------

    def process_voice(self, text):

        print()
        print("================================")
        print("SHOWROOM CONTROLLER")
        print("================================")
        print("Customer :", text)

        result = ProductMatcher.match(text)

        if not result:

            print("No Product Found")

            return False

        product = result["product"]

        self.current_product = product

        ActionService.execute(product)

        return True

    # -------------------------------------------------

    def stop(self):

        print("Stopping current presentation")

        self.current_product = None

    # -------------------------------------------------

    def current(self):

        return self.current_product