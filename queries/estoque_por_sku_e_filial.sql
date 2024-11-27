-- fonte: br.com.viavarejo.domain.repository.db2.impl.EstoqueDb2RepositoryImpl#obterAtualizacoes
-- Não leva em conta os depósitos alternativos
select
    CD_EMPGCB as empresa,
    CD_FIL as filial,
    CD_MCR as sku,
    QT_EMCFIL_CNT as contabil,
    QT_EMCFIL_INV_CNT as contabil_inventario,
    QT_EMCFIL_DSP as disponivel,
    QT_EMCFIL_TSI_ENT as transito_recebido,
    QT_EMCFIL_TSI_SAI as transito_nao_confirmado,
    QT_EMCFIL_SDO as saldo,
    QT_EMCFIL_RSR_SDO as reservado,
    QT_EMCFIL_NOV as padrao,
    QT_EMCFIL_SUC as sucata,
    QT_EMCFIL_QBD as quebrado,
    QT_EMCFIL_TRC_FOR as troca_fora,
    QT_EMCFIL_MOS as mostruario,
    QT_EMCFIL_RSR_VND as reservado_venda
from
    ETQ_MCR_CNT_FIL
where
    CD_EMPGCB = 21
    and CD_FIL = :filial
    and DT_MOD = :dt_mod
order by
    CD_EMPGCB,
    CD_FIL,
    CD_MCR

