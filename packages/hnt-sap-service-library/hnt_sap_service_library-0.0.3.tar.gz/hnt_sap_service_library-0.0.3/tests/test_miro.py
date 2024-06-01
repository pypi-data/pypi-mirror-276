import json
from os import getcwd, makedirs, path
from hnt_sap_gui import SapGui

def test_create():
    with open("./miro_expected.json", "r", encoding="utf-8") as miro_arquivo_json: miro = json.load(miro_arquivo_json)

    data = {
        "miro": miro,
    }
    result = SapGui().hnt_run_transaction_miro( "4506203094", data["miro"])
    assert result is not None