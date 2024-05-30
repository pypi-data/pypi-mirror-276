import pyodbc
from ..base import EasyPedidoInterfaceBase


class AdatecInterface(EasyPedidoInterfaceBase):

    db_host = None
    db_name = None
    db_user = None
    db_password = None
    db_driver = 'ODBC Driver 18 for SQL Server'
    db_encrypt = 'yes'
    company_code = None
    trade_ids_by_location_code = {
        # "[LOCATION_CODE]": "[TRADE_ID]"
    }

    updated_products_by_price_code = {}
    updated_products_by_location_code = {}

    # Querys
    query_get_products_to_update = (
        "SELECT "
        "   P.PRODUCTO_CODIGO, "
        "   INV.UBICACION, "
        "   PR.LISTA_CODIGO, "
        "   PR.PRECIO, "
        "   INV.DISPONIBLE, "
        "   P.PROCESO AS P_PROC, "
        "   PR.PROCESO AS PR_PROC, "
        "   INV.PROCESO AS INV_PROC, "
        "   P.PRODUCTO_IMPUESTO AS IMPUESTO_PORCENTAJE "
        "FROM PRODUCTOS P INNER JOIN PRECIOS PR ON ( "
        "   P.EMPRESA_CODIGO = PR.EMPRESA_CODIGO "
        "   AND P.PRODUCTO_CODIGO = PR.PRODUCTO_CODIGO "
        ") INNER JOIN INVENTARIO INV ON( "
        "   P.EMPRESA_CODIGO = INV.EMPRESA_CODIGO "
        "   AND P.PRODUCTO_CODIGO = INV.PRODUCTO_CODIGO "
        ") "
        "WHERE "
        "   P.EMPRESA_CODIGO = '{company_code}' "
        "   AND INV.UBICACION in ({location_codes})"
        "   AND PR.LISTA_CODIGO in ({price_list_codes}) "
        "   AND (P.PROCESO IN('U', 'Y') AND (PR.PROCESO <> 'Y' OR INV.PROCESO <> 'Y')) "
    )

    query_mark_prices_as_updated = (
        "UPDATE PRECIOS "
        "SET PROCESO = 'Y' "
        "WHERE EMPRESA_CODIGO = '{company_code}' "
        "AND PROCESO IN ('I', 'U') "
        "AND LISTA_CODIGO = '{price_list_code}' "
        "AND PRODUCTO_CODIGO IN ({product_codes}) "
    )

    query_mark_stock_as_updated = (
        "UPDATE INVENTARIO "
        "SET PROCESO = 'Y' "
        "WHERE EMPRESA_CODIGO = '{company_code}' "
        "AND PROCESO IN ('I', 'U') "
        "AND UBICACION = '{location_code}' "
        "AND PRODUCTO_CODIGO IN ({product_codes}) "
    )

    def __init__(self, host, main_trade_id, token, db_host, db_name, db_user, db_password, company_code,
                 trade_ids_by_location_code, db_driver=None, db_encrypt=None):
        super(AdatecInterface, self).__init__(host, main_trade_id, token)
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.company_code = company_code
        self.trade_ids_by_location_code = trade_ids_by_location_code

        if db_driver:
            self.db_driver = db_driver

        if db_encrypt:
            self.db_encrypt = db_encrypt

    def connect_to_db(self):
        connection = pyodbc.connect(
            'DRIVER={driver};SERVER={server};DATABASE={database};ENCRYPT={encrypt};'
            'Trust Server Certificate=true;'
            'UID={username};PWD={password}'.format(
                driver=self.db_driver,
                server=self.db_host,
                database=self.db_name,
                encrypt=self.db_encrypt,
                username=self.db_user,
                password=self.db_password
            )
        )
        return connection.cursor()

    def get_variants_content(self, location_codes=None, price_list_codes=None):
        """
            :return (String):
                Returns a weft with the data to update products

                '[TRADE_IDS];[KEY_FIELD_VALUE];[NAME];[DESCRIPTION];[CURRENCY];[PRICE];
                [TRACK_INVENTORY];[STOCK];[IS_ACTIVE]'
        """
        self.updated_products_by_price_code = {}
        self.updated_products_by_location_code = {}

        cursor = self.connect_to_db()
        cursor.execute('EXEC AllMerge @LOG_ID=NULL')
        cursor.commit()
        cursor.execute(self.query_get_products_to_update.format(
            company_code=self.company_code,
            location_codes=','.join(["'{}'".format(code)
                                    for code in location_codes]),
            price_list_codes=','.join(["'{}'".format(code)
                                      for code in price_list_codes]),
        ))

        db_results = cursor.fetchall()
        cursor.close()

        results = {}
        for db_result in db_results:
            # prepare prices data to mark as updated
            if db_result[2] not in self.updated_products_by_price_code:
                codes = set()
                codes.add(db_result[0])
                self.updated_products_by_price_code.update({
                    db_result[2]: codes
                })
            else:
                self.updated_products_by_price_code.get(
                    db_result[2]).add(db_result[0])

            # prepare location data to mark as updated
            if db_result[1] not in self.updated_products_by_location_code:
                codes = set()
                codes.add(db_result[0])
                self.updated_products_by_location_code.update({
                    db_result[1]: codes
                })
            else:
                self.updated_products_by_location_code.get(
                    db_result[1]).add(db_result[0])

            # prepare result
            product_code = db_result[0]
            price = str(db_result[3])
            is_active = 'true' if db_result[4] == 'Y' else 'false'
            tax_percentage = str(db_result[8])
            product_key = '{product_code};{price};{is_active};{tax_percentage}'.format(
                product_code=product_code,
                price=price,
                is_active=is_active,
                tax_percentage=tax_percentage
            )

            if product_key not in results:
                trade_ids = set()
                trade_ids.add(self.get_trade_id(db_result[1]))
                results.update({
                    product_key: trade_ids
                })
            else:
                results.get(product_key).add(self.get_trade_id(db_result[1]))

        serialized_data = []
        for product_key in results:
            item = product_key.split(';')
            serialized_data.append(
                '[TRADE_IDS];[KEY_FIELD_VALUE];[NAME];[DESCRIPTION];[CURRENCY];[PRICE];'
                '[TRACK_INVENTORY];[STOCK];[IS_ACTIVE];[TAX_PERCENTAGE]'
                .replace('[TRADE_IDS]', ','.join(results[product_key]))
                .replace('[KEY_FIELD_VALUE]', item[0])
                .replace('[NAME]', '')
                .replace('[DESCRIPTION]', '')
                .replace('[CURRENCY]', '')
                .replace('[PRICE]', item[1])
                .replace('[TRACK_INVENTORY]', '')
                .replace('[STOCK]', '')
                .replace('[IS_ACTIVE]', item[2])
                .replace('[TAX_PERCENTAGE]', item[3])
            )

        return '|'.join(serialized_data) if len(serialized_data) > 0 else None

    def mark_variants_as_updated(self):
        cursor = self.connect_to_db()
        # Update prices
        for price_code in self.updated_products_by_price_code:
            cursor.execute(self.query_mark_prices_as_updated.format(
                company_code=self.company_code,
                price_list_code=price_code,
                product_codes=','.join(["'{}'".format(code) for code
                                        in self.updated_products_by_price_code[price_code]])
            ))

        # Update Stocks
        for location_code in self.updated_products_by_location_code:
            cursor.execute(self.query_mark_stock_as_updated.format(
                company_code=self.company_code,
                location_code=location_code,
                product_codes=','.join(["'{}'".format(code) for code
                                        in self.updated_products_by_location_code[location_code]])
            ))

        cursor.commit()
        cursor.close()

    def get_trade_id(self, location_code):
        if location_code in self.trade_ids_by_location_code:
            return self.trade_ids_by_location_code.get(location_code)
        else:
            raise Exception(
                'trade_id to location code {} not found'.format(location_code))

    def update_variants(self, key_field_name, location_codes=None, price_list_codes=None):
        content = self.get_variants_content(location_codes, price_list_codes)
        if content:
            return self.send_updated_variants(key_field_name, content)
        else:
            return 'No hay productos para actualizar'
