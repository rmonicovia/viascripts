SELECT
  cd_mcr AS sku,
  CD_TSMCR, -- sinca apenas A, F, S (predicate default?)
  ST_MCR_SON, -- sinca apenas 2 ou 3, 1 = online
  ST_MCR_LOJ_VRT,  -- sinca apenas 'B', demais são B2C
  ST_MCR_SVV, -- sinca apenas = 'S', demais não é ViaVarejo
  DT_MOD
from
  mcr
where
  cd_mcr = :codigo_mercadoria
