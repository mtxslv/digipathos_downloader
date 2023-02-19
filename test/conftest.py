import pytest

@pytest.fixture
def short_zips_table():
    """an excerpt of zips_table containing metadata from only three sample images.

    Returns:
        zips_table (list): a list containing sample metadata.
    """
    zips_table = [
        {'size': '636.43 kB',
         'bsLink': '/jspui/bitstream/123456789/871/4/Abacaxi%20%28Pineapple%29%20-%20Broca%20%28Pineapple%20Fruit%20Borer%29%20-%201.zip',
         'name': 'Abacaxi (Pineapple) - Broca (Pineapple Fruit Borer) - 1.zip',
         'format': 'ZIP'},
        {'size': '20.45 MB',
         'bsLink': '/jspui/bitstream/123456789/985/11/Abacaxi%20%28Pineapple%29%20-%20Fusariose%20%28Fusariose%29%20-%201.zip',
         'name': 'Abacaxi (Pineapple) - Fusariose (Fusariose) - 1.zip',
         'format': 'ZIP'},
        {'size': '17.01 MB',
         'bsLink': '/jspui/bitstream/123456789/884/7/Abacaxi%20%28Pineapple%29%20-%20Podrid%c3%a3o%20%28Black%20Rot%29%20-%201.zip',
         'name': 'Abacaxi (Pineapple) - Podridão (Black Rot) - 1.zip',
         'format': 'ZIP'}]
    return zips_table