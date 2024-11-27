#!/bin/env python3.10
# -*- coding: utf-8 -*-


def check_vitrine(skus):
    import requests

    url = f'http://api-jornada.casasbahia.net/vv-vitrine/catalogo/catalogo?per_page=10&q={",".join(skus)}&tipoBusca=DEPARTAMENTO&fields=estruturasMercadologicas,filtros,totalProdutos,indiceRentabilidade,detalhe,produtos.sku,produtos.tipoProduto,produtos.nomeResumido,produtos.nomeCompleto,produtos.estado,produtos.estados,produtos.imagemPrincipal,produtos.tagVitrine,produtos.slugCategoria,produtos.canal,produtos.setor'
    headers = { 'Authorization': _get_token() }

    response = requests.get(url, headers = headers)

    if response.status == 200:
        print(response.json())
    else:
        print(response.text)


def check_catalogo():
    print('TODO')
    # curl http://localhost:8080/produto/MERCADORIA/4623410\?filial\=1000\&exibirIndisponibilidade\=false\&limparCache\=true -H "Authorization: bearer $(viatoken)"
    # Pegar a outra request para conjunto

def _get_token():
    # Deve devolver o token com "bearer " no começo
    raise Exception('TODO')



def main():
    import viatoken

    # params = {
    #         "empresaFuncionario": "21",
    #         "empresaFilial": "21",
    #         "filial": "1000",
    #         "bandeira": "1",
    #         "username": "549126",
    #         "password": "homolog01",
    #     }

    token = viatoken.generate('49', '21', 1000, 1, '60000723', 'JANELA35')
    # token = viatoken.generate(**params)

    print(f'Token gerado: {token}')


if __name__ == '__main__':
    main()

