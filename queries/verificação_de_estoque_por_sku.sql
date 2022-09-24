-- Verificação de estoque por sku (não leva em conta depósitos alternativos)

select
    cd_mcr as mercadoria,
    qt_emcfil_nov as estoque,
    qt_emcfil_cnt as estoque_contabil,
    *
from
    etq_mcr_cnt_fil as estoque_mercadoria_conjunto_por_filial
where
    cd_empgcb=21
    and cd_fil={filial}
    and cd_mcr={sku}
