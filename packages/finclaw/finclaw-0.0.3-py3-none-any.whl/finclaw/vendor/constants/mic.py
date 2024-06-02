MIC_TO_CURRENCY = {
    "ASX": "AUD",  # Australian Dollar
    "XIDX": "IDR",  # Indonesian Rupiah
    "SGX": "SGD",  # Singapore Dollar
    "MYX": "MYR",  # Malaysian Ringgit
    "XKRX": "KRW",  # South Korean Won
    "KOSDAQ": "KRW",  # South Korean Won
    "XTKS": "JPY",  # Japanese Yen
    "XNZE": "NZD",  # New Zealand Dollar
    "XNAS": "USD",  # US Dollar
    "XCSE": "DKK",  # Danish Krone
    "B3": "BRL",  # Brazilian Real
    "XBUE": "ARS",  # Argentine Peso
    "XTSE": "CAD",  # Canadian Dollar
    "NEO": "CAD",  # Canadian Dollar
    "XNYS": "USD",  # US Dollar
    "ARCA": "USD",  # US Dollar
    "XASE": "USD",  # US Dollar
    "BATS": "USD",  # US Dollar
    "XBKK": "THB",  # Thai Baht
    "CNSX": "CAD",  # Canadian Dollar
    "XMEX": "MXN",  # Mexican Peso
    "XSTU": "EUR",  # Euro
    "XFRA": "EUR",  # Euro
    "XTSX": "CAD",  # Canadian Dollar
    "XBER": "EUR",  # Euro
    "XHAM": "EUR",  # Euro
    "XSGO": "CLP",  # Chilean Peso
    "XMUN": "EUR",  # Euro
    "XLON": "GBP",  # British Pound
    "IOB": "Various",  # International, multiple currencies
    "XDUS": "EUR",  # Euro
    "XDUB": "EUR",  # Euro
    "XJSE": "ZAR",  # South African Rand
    "XMAD": "EUR",  # Euro
    "XMIL": "EUR",  # Euro
    "XPAR": "EUR",  # Euro
    "XAMS": "EUR",  # Euro
    "XWBO": "EUR",  # Euro
    "XBRU": "EUR",  # Euro
    "XLIS": "EUR",  # Euro
    "XETR": "EUR",  # Euro
    "XSWX": "CHF",  # Swiss Franc
    "XSTO": "SEK",  # Swedish Krona
    "XHEL": "EUR",  # Euro
    "XICE": "ISK",  # Icelandic Króna
    "CBOE": "USD/EUR",  # Operates in both USD and EUR
    "AQSE": "GBP",  # British Pound
    "XNGM": "SEK",  # Swedish Krona
    "XBUD": "HUF",  # Hungarian Forint
    "XIST": "TRY",  # Turkish Lira
    "XWAR": "PLN",  # Polish Zloty
    "XTAE": "ILS",  # Israeli New Shekel
    "XOSL": "NOK",  # Norwegian Krone
    "XATH": "EUR",  # Euro
    "XPRA": "CZK",  # Czech Koruna
    "XBOM": "INR",  # Indian Rupee
    "XSAU": "SAR",  # Saudi Riyal
    "XCAI": "EGP",  # Egyptian Pound
    "XDFM": "AED",  # UAE Dirham
    "XRIS": "EUR",  # Euro
    "XKUW": "KWD",  # Kuwaiti Dinar
    "XNSE": "INR",  # Indian Rupee
    "DSM": "QAR",  # Qatari Riyal
    "XSHE": "CNY",  # Chinese Yuan
    "XSHG": "CNY",  # Chinese Yuan
    "XHKG": "HKD",  # Hong Kong Dollar
    "TWO": "TWD",  # New Taiwan Dollar
    "XTAI": "TWD",  # New Taiwan Dollar
    "MOEX": "RUB",  # Russian Ruble
}

EXCHANGE_TO_MIC = {
    "Australian Securities Exchange": "ASX",
    "Jakarta Stock Exchange": "XIDX",
    "Stock Exchange of Singapore": "SGX",  # This is an old name; now it's Singapore Exchange
    "Kuala Lumpur": "MYX",  # Kuala Lumpur Stock Exchange is now Bursa Malaysia
    "KSE": "XKRX",  # Assuming KSE refers to Korea Exchange
    "KOSDAQ": "KOSDAQ",
    "Tokyo": "XTKS",  # Tokyo Stock Exchange
    "NZSE": "XNZE",  # New Zealand Stock Exchange, now NZX
    "Nasdaq": "XNAS",
    "Copenhagen": "XCSE",  # Copenhagen Stock Exchange, part of Nasdaq Nordic
    "NASDAQ": "XNAS",
    "NASDAQ Capital Market": "XNAS",
    "Other OTC": "OTC",
    "NASDAQ Global Market": "XNAS",
    "São Paulo": "B3",  # São Paulo Stock Exchange, now B3
    "Buenos Aires": "XBUE",
    "Toronto Stock Exchange": "XTSE",
    "NEO": "NEO",  # NEO Exchange in Canada
    "New York Stock Exchange": "XNYS",
    "New York Stock Exchange Arca": "ARCA",
    "NASDAQ Global Select": "XNAS",
    "American Stock Exchange": "XASE",  # Now part of NYSE American
    "BATS": "BATS",  # Now part of Cboe Global Markets
    "Toronto Stock Exchange Ventures": "TSXV",  # It's actually the TSX Venture Exchange
    "Cboe US": "CBOE",
    "Thailand": "XBKK",  # Stock Exchange of Thailand
    "CBOE BZX": "BATS",  # Cboe BZX Exchange, Inc.
    "Canadian Securities Exchange": "CNSX",
    "Mexico": "XMEX",  # Bolsa Mexicana de Valores
    "Cboe CA": "CBOE",  # Cboe Canada
    "Stuttgart": "XSTU",
    "Frankfurt Stock Exchange": "XFRA",
    "Frankfurt": "XFRA",
    "TSXV": "XTSX",  # TSX Venture Exchange
    "Berlin": "XBER",
    "Hamburg": "XHAM",
    "Santiago": "XSGO",  # Santiago Stock Exchange
    "Canadian Sec": "CNSX",  # Canadian Securities Exchange
    "Munich": "XMUN",
    "London Stock Exchange": "XLON",
    "IOB": "IOB",  # International Order Book, part of the London Stock Exchange
    "International Order Book": "IOB",
    "Dusseldorf": "XDUS",
    "Irish": "XDUB",  # Irish Stock Exchange, now Euronext Dublin
    "Johannesburg": "XJSE",
    "Madrid Stock Exchange": "XMAD",
    "Milan": "XMIL",  # Borsa Italiana, part of Euronext
    "Paris": "XPAR",  # Euronext Paris
    "Amsterdam": "XAMS",  # Euronext Amsterdam
    "Vienna": "XWBO",  # Wiener Börse
    "Brussels": "XBRU",  # Euronext Brussels
    "Lisbon": "XLIS",  # Euronext Lisbon
    "XETRA": "XETR",
    "Swiss Exchange": "XSWX",
    "Stockholm Stock Exchange": "XSTO",  # Now part of Nasdaq Nordic
    "Helsinki": "XHEL",  # Nasdaq Helsinki
    "Iceland": "XICE",  # Nasdaq Iceland
    "Cboe Europe": "CBOE",  # Cboe Europe Equities
    "Aquis AQSE": "AQSE",  # Aquis Stock Exchange
    "Nordic Growth Market": "XNGM",
    "Budapest": "XBUD",  # Budapest Stock Exchange
    "Istanbul Stock Exchange": "XIST",  # Now Borsa İstanbul
    "Warsaw Stock Exchange": "XWAR",
    "Tel Aviv": "XTAE",
    "Oslo Stock Exchange": "XOSL",
    "Athens": "XATH",  # Athens Stock Exchange
    "Prague": "XPRA",  # Prague Stock Exchange
    "Bombay Stock Exchange": "XBOM",
    "Saudi": "XSAU",  # Saudi Stock Exchange (Tadawul)
    "EGX": "XCAI",  # Egyptian Exchange
    "Dubai": "XDFM",  # Dubai Financial Market
    "Riga": "XRIS",  # Nasdaq Riga
    "BSE": "XBOM",  # Bombay Stock Exchange
    "Kuwait": "XKUW",
    "National Stock Exchange of India": "XNSE",
    "Qatar": "DSM",  # Qatar Stock Exchange
    "Shenzhen": "XSHE",
    "Shanghai": "XSHG",
    "HKSE": "XHKG",  # Hong Kong Stock Exchange
    "Taipei Exchange": "TWO",  # Taipei Exchange
    "Taiwan": "XTAI",  # Taiwan Stock Exchange
    "Moscow Stock Exchange": "MOEX",  # Moscow Exchange
}
