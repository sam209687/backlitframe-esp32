"""
voice_service.py

Voice activation and product matching logic
"""


from app.core.database import get_session

from app.models.welcome_keyword import WelcomeKeyword
from app.models.product import Product




class VoiceService:


    def __init__(self):

        self.active = False



    def check_welcome_phrase(
        self,
        text
    ):

        """
        Checks if user said activation phrase
        """


        text = text.lower()



        session = get_session()


        try:


            keywords = session.query(
                WelcomeKeyword
            ).filter_by(
                enabled=True
            ).all()



            for item in keywords:


                if item.phrase.lower() in text:


                    print(
                        "Voice activated:",
                        item.phrase
                    )


                    self.active = True


                    return True



        finally:

            session.close()



        return False




    def find_product(
        self,
        text
    ):

        """
        Finds product from voice keywords
        """


        text = text.lower()



        session = get_session()



        try:


            products = session.query(
                Product
            ).all()



            for product in products:


                for keyword in product.keywords_list():


                    if keyword.lower() in text:


                        print(
                            "Product matched:",
                            product.name
                        )


                        return product



        finally:

            session.close()



        return None




    def process_voice(
        self,
        text
    ):


        if not self.active:


            activated = self.check_welcome_phrase(
                text
            )


            if activated:

                return "LISTENING"



        else:


            product = self.find_product(
                text
            )


            if product:


                self.active = False


                return product



        return None