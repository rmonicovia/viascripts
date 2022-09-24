-- Devolve a comercialização padrão por SKU (mercadoria apenas)
SELECT
    t1.cd_mcr,
    T1.CD_CMC,
    T1.DT_MCRCMC_INI_VIG,
    T1.DT_MCRCMC_FIM_VIG,
    t1.dt_mod,
    t5.cd_tippco,
    t3.cd_bnd
FROM
    NSVP.MCR_CMC T1,
    NSVP.CMC_TIP_AGP_VLD T2,
    NSVP.BND_CMC T3,
    NSVP.cmc t5,
    NSVP.mcr t6
WHERE
    T1.CD_MCR = 4810678
    AND T1.CD_EMPGCB = 21
    AND T1.DT_MCRCMC_INI_VIG <= CURRENT DATE
    AND (T1.DT_MCRCMC_FIM_VIG IS NULL
        OR T1.DT_MCRCMC_FIM_VIG >= CURRENT DATE)
    AND T2.CD_CMC = T1.CD_CMC
    AND T2.CD_EMPGCB = T1.CD_EMPGCB
    AND T2.CD_TAVCMC IN (1, 2)
    AND T3.CD_BND IN (1, 2)
    AND T3.CD_EMPGCB = T2.CD_EMPGCB
    AND T3.CD_CMC = T2.CD_CMC
    AND t5.cd_empgcb = t1.cd_empgcb
    AND t5.cd_cmc = t1.cd_cmc
    AND t5.cd_tippco = 17231891
    AND t6.cd_mcr = t1.cd_mcr
    AND t6.cd_tsmcr = 'A'
WITH UR