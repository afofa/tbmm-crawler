# tbmm-crawler
Crawler for [TBMM website](https://www.tbmm.gov.tr).

## Usage

Run the command below in terminal. See `main.py` for options to run the script.

```bash
$ python3 main.py
```

## TODO

- In MP pages ([example](https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi?p_donem=27&p_sicil=7542))
1. Parse CV better (currently response do not capture CV at all)

- Crawl more stuff?
1. https://www.tbmm.gov.tr/develop/owa/mv_e_posta_sd.uye_e_posta
2. https://www.tbmm.gov.tr/develop/owa/mvtelefon.liste
3. Tutanaklar, soru onergeleri, kanun teklifleri etc.

- Solve SSL warning (InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning))