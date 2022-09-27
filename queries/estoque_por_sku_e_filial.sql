-- Não leva em conta os depósitos alternativos
select
  cd_empgcb as empresa,
  cd_fil as filial,
  cd_mcr as sku,
  qt_emcfil_cnt as contabil,
  qt_emcfil_inv_cnt as contabil_inventario,
  qt_emcfil_dsp as disponivel,
  qt_emcfil_tsi_ent as transito_recebido,
  qt_emcfil_tsi_sai as transito_nao_confirmado,
  qt_emcfil_sdo as saldo,
  qt_emcfil_rsr_sdo as reservado,
  qt_emcfil_nov as padrao,
  qt_emcfil_suc as sucata,
  qt_emcfil_qbd as quebrada,
  qt_emcfil_trc_for as troca_fora,
  qt_emcfil_mos as mostruario,
  qt_emcfil_rsr_vnd as reservado_venda
from
  etq_mcr_cnt_fil
where
  cd_empgcb=21
  and cd_mcr IN (4854772,4856112,4856120,4856139,4856147,4856155,4856163,4924754,4947525,4947533,4953940,4954050,4960386)
