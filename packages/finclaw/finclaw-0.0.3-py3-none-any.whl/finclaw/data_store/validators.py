from finclaw.vendor import SUPPORTED_VENDORS


def validate_vendor(vendor):
    if vendor not in SUPPORTED_VENDORS:
        raise ValueError(f"Vendor: {vendor} is not yet supported")
