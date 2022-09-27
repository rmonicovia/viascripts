-- Como está em br.com.viavarejo.domain.repository.db2.impl.DepositoAlternativoDb2RepositoryImpl#obterDepositosAlternativos
select
  filial.cd_empgcb as empresa,
  filial.cd_fil as filial,
  ponto_atendimento.cd_empgcb_atn as empresa_alternativo,
  ponto_atendimento.cd_fil_atn as filial_alternativo,
  ponto_atendimento.cd_tafil_atn as tipo_atividade_alternativo,
  ponto_atendimento.cd_empgcb_dst as empresa_destino,
  ponto_atendimento.cd_fil_dst as filial_destino,
  ponto_atendimento.cd_tafil_dst as tipo_atividade_destino

from
  nsvp.fil filial

  inner join nsvp.mic_zen zona_entrega on
    zona_entrega.cd_est_sig_zen = filial.cd_est_sig_zen
    and zona_entrega.cd_zen = filial.cd_zen
    and zona_entrega.cd_miczen = filial.cd_miczen
    and zona_entrega.cd_empgcb_atd = filial.cd_empgcb

  inner join nsvp.atn_pto_atv ponto_atendimento on
    ponto_atendimento.cd_empgcb = zona_entrega.cd_empgcb_dpo_etg
    and ponto_atendimento.cd_fil = zona_entrega.cd_fil_dpo_etg
    and ponto_atendimento.cd_tafil = zona_entrega.cd_tafil_dpo_etg
    and ponto_atendimento.cd_tafil_atn = 'D'
    and ponto_atendimento.st_apatv_ato = 'S'

where
  filial.cd_empgcb = 21

order by
  filial.cd_empgcb,
  filial.cd_fil