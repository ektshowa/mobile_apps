from django.test import TestCase

from .models import Country, Address, City, Region, Commune 


class AddressTestCase(TestCase):
    def test_address(self):
        country = Country.objects.create(english_name="D.R. Congo",
                                        french_name="R.D. Congo",
                                        local_name="R.D. Congo",
                                        region="Central Africa",
                                        continent="Africa") 
        province = Region.objects.create(name="Kinshasa",
                                        country=country,
                                        is_active=True)
        city = City.objects.create(name="Funa District",
                                    region=province,
                                    country=country,
                                    city_type="District",
                                    is_active=True)
        commune = Commune.objects.create(name="Selembao",
                                        city=city,
                                        is_active=True)

        self.assertEquals(
            Address.objects.count(),
            0
        )
        Address.objects.create(region=province,
                                city=city,
                                commune=commune,
                                street="14 Avenue du Commerce")

        self.assertEquals(
            Address.objects.count(),
            1
        )




