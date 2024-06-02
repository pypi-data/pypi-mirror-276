# Finclaw

Finclaw is a dedicated tool designed to fetch and
update price data for various assets from multiple vendors.
It has been designed to provide uniform data interface across multiple vendors.

### Principles
- Don't use new libraries unless they are accepted by the industry
- Longevity and simplicity over shortness and complexity

### Vendors supported

- Finnhub
- FMP
- TwelveData


### Running on local
#### Setting up env variables
Before you start fetching data, you need to set up environment variables.

```text
IMAGE=None

TRADE_ENGINE_DATA=./data
FINNHUB_API=x

# FMP creds
FMP_API_KEY=None
# Twelvedata creds
TWELVEDATA_API_KEY=None

# Kraken creds
KRAKEN_API_KEY=None
KRAKEN_API_SECRET=None
```

### Example usage
```bash
# Load environment variables defined in .env file
source ./tools/load_env.sh
finclaw grab --start 2023-08-13 --end 2023-09-04 --frequency 1 --include-information p --vendor fmp --market TO
```

```bash
# Pull data for all stocks and store into path specified by TRADE_ENGINE_DATA variable
finclaw grab --start 2023-08-13 --end 2023-09-04 \
--frequency 1 --include-information p --vendor fmp --market TO
```

```bash
# Pull data for RY.TO symbol and store it in S3 bucket
finclaw grab --start 2024-01-18 --end 2024-01-19 \
--frequency 1  --market TO -ic p -v fmp -s RY.TO \
--storage-type s3 --bucket-name my-financial-datalake-bucket --region us-east-1
```

## (WIP) Infra Setup 
- When creating a job definition make sure the user is marked as Priveleged else it will fail with mount error
```text
VolumeDriver.Create: mounting volume failed: b'mount.nfs4: access denied by server while mounting 127.0.0.1:/'
```