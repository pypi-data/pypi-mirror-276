import json
import requests


class EasyPedidoInterfaceBase:
    host = None
    main_trade_id = None
    token = None

    # ---- Urls -------
    variants_update_url = '/api/product/variant/update/'

    def __init__(self, host, main_trade_id, token):
        self.host = host
        self.main_trade_id = main_trade_id
        self.token = token

    def get_url(self, url):
        return "{}{}".format(self.host, url)

    def get_variants_content(self):
        """
            :return (String):
                Returns a weft with the data to update variants. Each item has the next structure and is separated
                by pipe '|':

                '[TRADE_IDS];[KEY_FIELD_VALUE];[NAME];[DESCRIPTION];[CURRENCY];[PRICE];
                [TRACK_INVENTORY];[STOCK];[IS_ACTIVE]'
        """
        serialized_data = []
        variants = []

        for variant in variants:
            serialized_data.append(
                '[TRADE_IDS];[KEY_FIELD_VALUE];[NAME];[DESCRIPTION];[CURRENCY];[PRICE];'
                '[TRACK_INVENTORY];[STOCK];[IS_ACTIVE]'
                .replace('[TRADE_IDS]', variant.get('trade_ids'))
                .replace('[KEY_FIELD_VALUE]', variant.get('key_field'))
                .replace('[NAME]', variant.get('name'))
                .replace('[DESCRIPTION]', variant.get('description'))
                .replace('[CURRENCY]', variant.get('currency'))
                .replace('[PRICE]', str(variant.get('price')))
                .replace('[TRACK_INVENTORY]', variant.get('track_inventory'))
                .replace('[STOCK]', variant.get('stock'))
                .replace('[IS_ACTIVE]', variant.get('is_active'))
            )

        return '|'.join(serialized_data) if len(serialized_data) > 0 else None

    def mark_variants_as_updated(self):
        pass

    def update_variants(self, key_field_name):
        content = self.get_variants_content()
        if content:
            return self.send_updated_variants(key_field_name, content)
        else:
            return 'No hay productos para actualizar'

    def send_updated_variants(self, key_field_name, content):
        if content:
            data = {
                "main_trade_id": self.main_trade_id,
                "token": self.token,
                "key_field_name": key_field_name,
                "content": content
            }
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
            }

            response = requests.post(self.get_url(
                self.variants_update_url), data=data, headers=headers)
            if response.status_code == 200:
                res = json.loads(response.content)
                if res.get('success'):
                    self.mark_variants_as_updated()

            return response.content
