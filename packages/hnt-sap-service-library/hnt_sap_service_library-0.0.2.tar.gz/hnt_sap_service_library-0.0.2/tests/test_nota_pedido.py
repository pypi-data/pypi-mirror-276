import json
from os import getcwd, makedirs, path
from hnt_sap_gui import SapGui

def test_create():
    with open("./expected_nota_servico.json", "r", encoding="utf-8") as nota_pedido_arquivo_json: nota_pedido = json.load(nota_pedido_arquivo_json)

    data = {
        "nota_pedido": nota_pedido,
    }
    result = SapGui().hnt_run_transaction(data)
    assert result is not None

def test_get_many_codes():

    code_array = []

    for index in range(5):
        with open("./expected_nota_servico.json", "r", encoding="utf-8") as nota_pedido_arquivo_json: nota_pedido = json.load(nota_pedido_arquivo_json)

        data = {
            "nota_pedido": nota_pedido,
        }
        result = SapGui().hnt_run_transaction(data)
        code_array.append(result['nota_pedido'].codigo)

    # path_dir = path.join(getcwd(), 'devdata', 'json')
    # if not path.exists(path_dir):
    #     makedirs(path_dir)

    with open(f"./servico_sap_pedido_codes.json", "w", encoding="utf-8") as json_file:
        json.dump( code_array, json_file, ensure_ascii=False, indent=4)

    assert result is not None