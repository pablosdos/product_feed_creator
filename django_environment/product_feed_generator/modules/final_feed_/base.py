
from product_feed_generator.modules.final_feed_.output.xml import _add_products_to_final_feed






class FinalFeed_:
  def __init__(_self, shop_name):
    # self._shop_name = name
    _self.shop_name = shop_name

  """
  OUTDATED
  SINCE
  240131
  NOT IN USE !
  """
  def save_xml_file(_self, unconfigured_product_list) -> dict:
    """
    Saves XML file.

    And returns a dict with the context, used for the http response (presentation of the page):
    Feed infos, updated products, the form and information message.

    """
    return _add_products_to_final_feed(unconfigured_product_list, _self.shop_name)