import logging
from hnt_sap_gui.common.sap_status_bar import sbar_extracted_text
from hnt_sap_gui.common.tx_result import TxResult

logger = logging.getLogger(__name__)
MSG_SAP_CODIGO_NOTA_PEDIDO = "^Ped.C.Custo\\/Ordem criado sob o nº ([0-9]{10,11})$"
class NotaPedidoTransaction:
    def __init__(self) -> None:
        pass

    def execute(self, sapGuiLib, nota_pedido):
        logger.info(f"enter execute nota_pedido:{nota_pedido}")
        # ABRE TRANSAÇÃO
        sapGuiLib.run_transaction('/nme21n')
        sapGuiLib.send_vkey(0)

        # REORGANIZA ELEMENTOS PARA GARANTIR QUE CABEÇALHO ESTEJA ABERTO
        sapGuiLib.send_vkey(29) # Fechar Cabeçalho
        sapGuiLib.send_vkey(30) # Fechar Síntese de itens
        sapGuiLib.send_vkey(31) # Fechar Detahe de item
        sapGuiLib.send_vkey(26) # Abrir Cabeçalho

        # PREENCHE DADOS INICIAIS (Antes do cabeçalho)
        sapGuiLib.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB0:SAPLMEGUI:0030/subSUB1:SAPLMEGUI:1105/cmbMEPO_TOPLINE-BSART").Key = nota_pedido['tipo'] # Define o tipo de pedido como Ped.C.Custo/Ordem
        sapGuiLib.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB0:SAPLMEGUI:0030/subSUB1:SAPLMEGUI:1105/ctxtMEPO_TOPLINE-SUPERFIELD").Text = nota_pedido['cod_fornecedor']

        # CABEÇALHO | Aba Dados Organizacionais
        sapGuiLib.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB1:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1102/tabsHEADER_DETAIL/tabpTABHDT9").Select() #Seleciona a aba Dados organizacionais
        sapGuiLib.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB1:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1102/tabsHEADER_DETAIL/tabpTABHDT9/ssubTABSTRIPCONTROL2SUB:SAPLMEGUI:1221/ctxtMEPO1222-EKORG").Text = nota_pedido['org_compras']  # (orgCompras)
        sapGuiLib.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB1:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1102/tabsHEADER_DETAIL/tabpTABHDT9/ssubTABSTRIPCONTROL2SUB:SAPLMEGUI:1221/ctxtMEPO1222-EKGRP").Text = nota_pedido['grp_compradores'] # grpCompradores)
        sapGuiLib.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB1:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1102/tabsHEADER_DETAIL/tabpTABHDT9/ssubTABSTRIPCONTROL2SUB:SAPLMEGUI:1221/ctxtMEPO1222-BUKRS").Text = nota_pedido['empresa']  # (Empresa)

        # REORGANIZA ELEMENTOS PARA GARANTIR QUE SÍNTESE DE ITENS ESTEJA ABERTO
        sapGuiLib.send_vkey(29) #Fechar cabeçalho
        sapGuiLib.send_vkey(27) #Abrir Síntese de itens
        sapGuiLib.send_vkey(31) #Fechar Detahe de item
        sapGuiLib.send_vkey(26) #Abrir Cabeçalho
        sapGuiLib.send_vkey(29) #Fechar cabeçalho


        # SÍNTESE DE ITENS
        for index, sintese_item in enumerate(nota_pedido['sintese_itens']):

            item = sintese_item['item']
            fatura = sintese_item['fatura']

            id_0015  = "wnd[0]/usr/subSUB0:SAPLMEGUI:0015"
            id_0016  = "wnd[0]/usr/subSUB0:SAPLMEGUI:0016"
            id_0019  = "wnd[0]/usr/subSUB0:SAPLMEGUI:0019"

            check_id_sintese  = sapGuiLib.session.findById(id_0016, False) != None
            id_gui_sintese    = id_0016 if check_id_sintese else id_0019

            check_id_detalhes = sapGuiLib.session.findById(id_0015, False) != None
            id_gui_detalhes   = id_0015 if check_id_detalhes else id_0019

            sapGuiLib.session.findById(f"{id_gui_sintese}/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/ctxtMEPO1211-KNTTP[2,{index}]").Text = sintese_item['categoria_cc']  # (Categoria C|C)
            sapGuiLib.session.findById(f"{id_gui_sintese}/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/ctxtMEPO1211-EPSTP[3,{index}]").Text = sintese_item['categoria_item']  # (Categoria do item)
            sapGuiLib.session.findById(f"{id_gui_sintese}/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/txtMEPO1211-TXZ01[5,{index}]").Text = sintese_item['texto_breve']  # (Texto breve)
            sapGuiLib.session.findById(f"{id_gui_sintese}/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/txtMEPO1211-MENGE[6,{index}]").Text = sintese_item['quantidade']  # (Qtd.do pedido)
            sapGuiLib.session.findById(f"{id_gui_sintese}/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/ctxtMEPO1211-NAME1[10,{index}]").Text = sintese_item['centro']  # (Centro)
            sapGuiLib.session.findById(f"{id_gui_sintese}/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/ctxtMEPO1211-WGBEZ[19,{index}]").Text = sintese_item['grp_mercadorias']  # (Grupo de mercadorias)
            sapGuiLib.send_vkey(0)

            # DETALHES DE ITEM | Aba Serviços
            check_id_detalhes = sapGuiLib.session.findById(id_0015, False) != None
            id_gui_detalhes   = id_0015 if check_id_detalhes else id_0019
            # id_gui_detalhes   = id_0015

            if sapGuiLib.session.findById(f"{id_gui_detalhes}/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT1", False) != None:  
                # Seleciona aba "Serviços"
                sapGuiLib.session.findById(f"{id_gui_detalhes}/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT1").select()

            sapGuiLib.session.findById(f"{id_gui_detalhes}/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT1/ssubTABSTRIPCONTROL1SUB:SAPLMEGUI:1328/subSUB0:SAPLMLSP:0400/tblSAPLMLSPTC_VIEW/ctxtESLL-SRVPOS[2,{index}]").Text = item['nro_servico'] # (Nº serviço)
            sapGuiLib.session.findById(f"{id_gui_detalhes}/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT1/ssubTABSTRIPCONTROL1SUB:SAPLMEGUI:1328/subSUB0:SAPLMLSP:0400/tblSAPLMLSPTC_VIEW/ctxtRM11P-KOSTL[3,{index}]").Text = item['centro_custo']  # (Centro custo)
            sapGuiLib.session.findById(f"{id_gui_detalhes}/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT1/ssubTABSTRIPCONTROL1SUB:SAPLMEGUI:1328/subSUB0:SAPLMLSP:0400/tblSAPLMLSPTC_VIEW/txtESLL-MENGE[4,{index}]").Text = item['quantidade']  # (Quantidade)
            sapGuiLib.session.findById(f"{id_gui_detalhes}/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT1/ssubTABSTRIPCONTROL1SUB:SAPLMEGUI:1328/subSUB0:SAPLMLSP:0400/tblSAPLMLSPTC_VIEW/txtESLL-TBTWR[5,{index}]").Text = item['valor_bruto'] # (Preço bruto)
            sapGuiLib.send_vkey(0)

            check_id_detalhes = sapGuiLib.session.findById(id_0015, False) != None
            id_gui_detalhes   = id_0015 if check_id_detalhes else id_0019

            # DETALHES DE ITEM | Aba Fatura
            if sapGuiLib.session.findById(f"{id_gui_detalhes}/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT7", False) != None:
                sapGuiLib.session.findById(f"{id_gui_detalhes}/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT7").Select() #Seleciona a aba "Fatura"

            sapGuiLib.session.findById(f"{id_gui_detalhes}/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT7/ssubTABSTRIPCONTROL1SUB:SAPLMEGUI:1317/ctxtMEPO1317-MWSKZ").Text = fatura['cod_imposto']  # (Cód.imposto)
            sapGuiLib.send_vkey(0)


        # PROCESSO PARA ANEXAR O DOCUMENTO NO PEDIDO
        for anexo in nota_pedido['anexo']:
            sapGuiLib.session.findById("wnd[0]/titl/shellcont/shell").pressButton("%GOS_TOOLBOX")
            sapGuiLib.session.findById("wnd[0]/shellcont[1]/shell").pressContextButton("CREATE_ATTA")
            sapGuiLib.session.findById("wnd[0]/shellcont[1]/shell").selectContextMenuItem("PCATTA_CREA")
            sapGuiLib.session.findById("wnd[1]/usr/ctxtDY_PATH").Text = anexo['path'] #Diretório de NFs
            sapGuiLib.session.findById("wnd[1]/usr/ctxtDY_FILENAME").Text = anexo['filename'] #PDF da DANFE
            sapGuiLib.session.findById("wnd[1]/tbar[0]/btn[0]").press()

        sapGuiLib.session.findById("wnd[0]/tbar[0]/btn[11]").press() # Grava o lançamento
        sbar = sapGuiLib.session.findById("wnd[0]/sbar").Text # Captura do nº do documento exibido na barra de status do SAP (últimos 10 caracteres da mensagem)
        cod_nota_pedido = sbar_extracted_text(MSG_SAP_CODIGO_NOTA_PEDIDO, sbar)
        tx_result = TxResult(cod_nota_pedido, sbar)
        logger.info(f"Leave execute code service_note:{str(tx_result)}")

        return tx_result