SELECT * FROM (
SELECT
	ROW_NUMBER() OVER (ORDER BY cd_mcr asc) AS rowno,
	cd_mcr
FROM
	nsvp.mcr
WHERE
	dt_mod > '2022-09-24 00:00:00'
)
WHERE rowno BETWEEN 7000 AND 8999
ORDER BY rowno
