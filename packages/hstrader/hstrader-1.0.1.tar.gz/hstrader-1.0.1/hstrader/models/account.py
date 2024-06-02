from .base import BaseModel
from .enums import AccountStatus, AccountType, KycStatus, TradeType



class Identity(BaseModel):

    id: int = None
    account_id: int = None
    first_name: str = None
    middle_name: str = None
    family_name: str = None
    country_of_citizenship: str = None
    date_of_birth: int = None
    country_of_birth: str = None
    current_country_residence: str = None
    address_line: str = None
    funding_source: int = None
    documents: str = None
    agreements: str = None
    recovery_contact: str = None
    note: str = None
    telephone: str = None
    mobile: str = None
    tel_pw: str = None
    po_box: str = None
    fax: str = None
    email: str = None
    city: str = None
    status: str = None
    created_at: int = None
    updated_at: int = None
    created_by: int = None
    updated_by: int = None


class Account(BaseModel):

    role_id: int = None
    trade_type: TradeType = None
    balance: float = None
    currency_digits: int = None
    user_id: str = None
    user_password: str = None
    account_type: AccountType = None
    created_by: int = None
    free_margin: float = None
    liabilities: float = None
    margin_level: float = None
    # role : Role =None
    status: AccountStatus = None
    blocked_profit: float = None
    used_margin: float = None
    floating_profit: float = None
    margin_maintenance: float = None
    client_secret: str = None
    created_at: int = None
    credit: float = None
    margin_initial: float = None
    currency: str = None
    favourite: bool = None
    relized_profit: float = None
    assets: float = None
    broker_id: int = None
    profit: float = None
    client_id: str = None
    kyc_results: KycStatus = None
    leverage: int = None
    updated_by: int = None
    # code_expiry : str =None
    investor_password: str = None
    equity: float = None
    change_password_code: str = None
    group_id: int = None
    id: int = None
    identity: Identity = None
    updated_at: int = None
