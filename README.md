# tbmm-crawler
Crawler for [TBMM website](https://www.tbmm.gov.tr).

## Usage

Run the command below in terminal. See `main.py` for options to run the script.

```bash
$ python3 main.py
```

## TODO

- In MP pages ([example](https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi?p_donem=27&p_sicil=7542))
1. Parse tasks better (currently list. Can be empty, singleten or multiple elements)
2. Parse contact better (currently list. Inconsistencies)
3. Parse CV better (currently response do not capture CV at all)

- Solve SSL warning (InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning))