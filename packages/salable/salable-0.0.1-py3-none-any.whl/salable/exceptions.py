class SalableSDKError(Exception):
    """Base class for all SDK errors."""
    pass

class AuthenticationError(SalableSDKError):
    """Raised when authentication fails."""
    pass

class ProductError(SalableSDKError):
    """Raised when there is an issue with product operations."""
    pass

class PlanError(SalableSDKError):
    """Raised when there is an issue with plan operations."""
    pass

class LicenseError(SalableSDKError):
    """Raised when there is an issue with license operations."""
    pass

class PaymentLinkError(SalableSDKError):
    """Raised when there is an issue with payment link generation."""
    pass