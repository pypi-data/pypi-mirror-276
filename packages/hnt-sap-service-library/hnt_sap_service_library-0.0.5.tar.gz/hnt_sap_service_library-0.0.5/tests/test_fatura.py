import json
from hnt_sap_gui import SapGui
# from hnt_sap_gui.nota_fiscal.nota_pedido_transaction import NotaPedidoTransaction

def test_create():
    with open("./devdata/json/fatura_expected.json", "r", encoding="utf-8") as fatura_arquivo_json: fatura = json.load(fatura_arquivo_json)

    data = {
        "fatura": fatura,
    }
    result = SapGui().hnt_run_transaction_FV60(data)
    assert result is not None