select
	t1.cd_mcr, -- sku
	t1.cd_cmc, -- código de comercialização
	t1.dt_mcrcmc_ini_vig, -- início da vigência da comercialização
	t1.dt_mcrcmc_fim_vig, -- fim da vigência da comercialização
	t1.dt_mod, -- data de modificação da mercadoria
	t4.cd_fil, -- código da filial
	t5.cd_tippco, -- código do tipo de preço
	t3.cd_bnd, -- ????
	t7.vr_pcomcr -- valor da mercadoria

from
	nsvp.mcr_cmc t1

    left join nsvp.cmc_tip_agp_vld t2 on
        t2.cd_empgcb = t1.cd_empgcb
        and t2.cd_cmc = t1.cd_cmc

    left join nsvp.bnd_cmc t3 on
	    t3.cd_empgcb = t2.cd_empgcb
	    and t3.cd_cmc = t2.cd_cmc

    left join nsvp.cmc_fil t4 on
	    t4.cd_empgcb = t1.cd_empgcb
	    and t4.cd_cmc = t1.cd_cmc

    left join nsvp.cmc t5 on
	    t5.cd_empgcb = t1.cd_empgcb
	    and t5.cd_cmc = t1.cd_cmc

    left join nsvp.mcr t6 on
	    t6.cd_mcr = t1.cd_mcr

    left join nsvp.htr_pco_mcr_alt t7 on
	    t7.cd_tippco = t5.cd_tippco
	    and t7.cd_mcr = t1.cd_mcr
	    and t7.dt_pcomcr_ini_vig = t1.dt_mcrcmc_ini_vig
	    and t7.cd_empgcb_opr = t1.cd_empgcb

where
	t1.cd_empgcb = 21 -- empresa
	and t1.cd_mcr = 4810678
	and t4.cd_fil = 1059 -- filial
	and t1.dt_mcrcmc_ini_vig <= current date
	and (t1.dt_mcrcmc_fim_vig is null
		or t1.dt_mcrcmc_fim_vig >= current date)
	and t2.cd_tavcmc between 3 and 4
	and t3.cd_bnd in (1, 2)
	and t4.dt_cmcfil_ini_vig <= current date
	and (t4.dt_cmcfil_fim_vig is null
		or t4.dt_cmcfil_fim_vig >= current date)
	and t6.cd_tsmcr = 'A'
	and date(t7.dt_mod) = current date

with ur
