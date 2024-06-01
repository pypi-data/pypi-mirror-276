from __future__ import annotations

from abc import abstractmethod
from decimal import Decimal
from enum import Enum
from typing import Any, cast

from eth_abi.abi import encode as encode_abi
from eth_typing import HexStr
from eth_utils.abi import collapse_if_tuple
from pydantic import BaseModel, Field
from web3 import Web3
from web3.auto import w3

from jam_sdk.constants import HASH_HOOKS_ABI, NATIVE_TOKEN_ADDRESS


# TODO: move below funs somewhere else without resulting in circular imports
def decode_token_transfers(token_transfers: str) -> list[JamCommand]:
    return [JamCommand(token_transfers[i * 2 : i * 2 + 2]) for i in range(1, int(len(token_transfers) / 2))]


def merge_tokens(tokens: list[TokenAmount]) -> list[TokenAmount]:
    """
    Combine split tokens

    Args:
        tokens (list[TokenAmount]): list of tokens

    Returns:
        _type_: merged tokens
    """
    merged_tokens: dict[str, TokenAmount] = {}
    for token in tokens:
        if token.address in merged_tokens and token.amount:
            current_amount = merged_tokens[token.address].amount
            if current_amount:
                merged_tokens[token.address].amount = current_amount + token.amount
        else:
            merged_tokens[token.address] = TokenAmount(
                address=token.address, amount=token.amount, usd_price=token.usd_price
            )
    return list(merged_tokens.values())


class ApprovalType(Enum):
    Standard = "Standard"
    Permit = "Permit"
    Permit2 = "Permit2"


class OrderType(Enum):
    OneToOne = "121"
    OneToMany = "12M"
    ManyToOne = "M21"
    ManyToMany = "M2M"


class JamCommand(Enum):
    SIMPLE_TRANSFER = "00"
    PERMIT2_TRANSFER = "01"
    CALL_PERMIT_THEN_TRANSFER = "02"
    CALL_PERMIT2_THEN_TRANSFER = "03"
    NATIVE_TRANSFER = "04"
    NFT_ERC721_TRANSFER = "05"
    NFT_ERC1155_TRANSFER = "06"


class BaseMessage(BaseModel):
    @abstractmethod
    def to_ws(self) -> dict: ...

    @staticmethod
    @abstractmethod
    def from_ws(data: dict) -> Any: ...


class TokenAmount(BaseMessage):
    address: str
    amount: int | None
    usd_price: float | None

    def to_ws(self) -> dict:
        return {
            "address": self.address,
            "amount": str(self.amount) if self.amount else None,
            "usd_price": self.usd_price,
        }

    @staticmethod
    def from_ws(data: dict) -> TokenAmount:
        return TokenAmount(
            address=data["address"],
            amount=(int(data["amount"]) if "amount" in data and data["amount"] is not None else None),
            usd_price=data["usd_price"],
        )


class TokenAmountResponse(BaseMessage):
    address: str
    amount: int

    def to_ws(self) -> dict:
        return {"address": self.address, "amount": str(self.amount) if self.amount else None}

    @staticmethod
    def from_ws(data: dict) -> TokenAmountResponse:
        return TokenAmountResponse(
            address=data["address"],
            amount=(int(data["amount"])),
        )


class InteractionData(BaseModel):
    result: bool
    to: str
    value: int
    data: str

    def to_ws(self) -> dict:
        return {
            "result": self.result,
            "to": self.to,
            "value": str(self.value),
            "data": self.data,
        }

    @staticmethod
    def from_ws(data: dict) -> InteractionData:
        return InteractionData(
            result=data["result"],
            to=data["to"],
            value=int(data["value"]),
            data=data["data"],
        )

    def abi_encode(self) -> bytes:
        return encode_abi(
            ["bool", "address", "uint256", "bytes"],
            [self.result, self.to, self.value, Web3.to_bytes(hexstr=HexStr(self.data))],
        )


class AllHooks(BaseModel):
    before_settle: list[InteractionData]
    after_settle: list[InteractionData]

    def hash_hooks(self) -> str:
        def flatten_hooks(h: InteractionData) -> tuple[bool, str, int, str]:
            return h.result, h.to, h.value, h.data

        if len(self.after_settle) == 0 and len(self.before_settle) == 0:
            return "0x0000000000000000000000000000000000000000000000000000000000000000"

        hooks = [[flatten_hooks(h) for h in self.before_settle], [flatten_hooks(h) for h in self.after_settle]]
        args_types = [collapse_if_tuple(cast(dict[str, Any], arg)) for arg in HASH_HOOKS_ABI["inputs"]]
        hooks_encoded = w3.codec.encode(args_types, [hooks])
        keccak_hash = w3.keccak(primitive=hooks_encoded)
        return keccak_hash.hex()

    def to_blockchain_args(self) -> list[list[dict[str, Any]]]:
        return [
            [interaction.to_ws() for interaction in self.before_settle],
            [interaction.to_ws() for interaction in self.after_settle],
        ]


class InteractionDetails(BaseModel):
    data: InteractionData
    gas: int

    def to_ws(self) -> dict:
        return {
            "data": self.data.to_ws(),
            "gas": self.gas,
        }

    @staticmethod
    def from_ws(data: dict) -> InteractionDetails:
        return InteractionDetails(
            data=InteractionData.from_ws(data["data"]),
            gas=data["gas"],
        )


class QuoteRequest(BaseMessage):
    order_type: OrderType
    quote_id: str
    base_settle_gas: int
    approval_type: ApprovalType
    taker: str
    receiver: str
    expiry: int
    nonce: int
    hooks: AllHooks
    hooks_hash: str
    slippage: Decimal
    sell_tokens: list[TokenAmount]
    buy_tokens: list[TokenAmount]
    sell_token_transfers: str
    buy_token_transfers: str
    native_token_price: float
    source: str | None = Field(default=None)
    exclude_fee: bool = False
    gasless: bool = Field(exclude=True)

    @property
    def usd_prices(self) -> dict[str, float]:
        prices = {}
        for token in self.sell_tokens + self.buy_tokens:
            if token.usd_price:
                prices[token.address] = token.usd_price

        prices[NATIVE_TOKEN_ADDRESS] = self.native_token_price
        return prices

    def to_ws(self) -> dict:
        data = self.model_dump()
        data["order_type"] = self.order_type.value
        data["hooks"] = self.hooks.to_blockchain_args()
        data["approval_type"] = self.approval_type.value
        data["sell_tokens"] = [token.to_ws() for token in self.sell_tokens]
        data["buy_tokens"] = [token.to_ws() for token in self.buy_tokens]
        data["nonce"] = str(self.nonce)
        data["slippage"] = float(self.slippage)
        return data

    @staticmethod
    def from_ws(data: dict) -> QuoteRequest:
        msg_data: dict[str, Any] = data["msg"]
        match data["msg_topic"]:
            case "quote":
                gasless = True
            case "taker_quote":
                gasless = False
            case _:
                raise ValueError(f"Invalid message topic: {data['msg_topic']}")

        return QuoteRequest(
            order_type=OrderType(msg_data["order_type"]),
            quote_id=msg_data["quote_id"],
            base_settle_gas=msg_data["base_settle_gas"],
            approval_type=ApprovalType(msg_data["approval_type"]),
            taker=msg_data["taker"],
            receiver=msg_data["receiver"],
            expiry=msg_data["expiry"],
            nonce=int(msg_data["nonce"]),
            hooks=AllHooks(
                before_settle=[InteractionData.from_ws(interaction) for interaction in msg_data["hooks"][0]],
                after_settle=[InteractionData.from_ws(interaction) for interaction in msg_data["hooks"][1]],
            ),
            hooks_hash=msg_data["hooks_hash"],
            slippage=Decimal(msg_data["slippage"]),
            buy_tokens=[TokenAmount.from_ws(token) for token in msg_data["buy_tokens"]],
            sell_tokens=[TokenAmount.from_ws(token) for token in msg_data["sell_tokens"]],
            sell_token_transfers=msg_data["sell_token_transfers"],
            buy_token_transfers=msg_data["buy_token_transfers"],
            native_token_price=msg_data["native_token_price"],
            exclude_fee=bool(msg_data.get("exclude_fee")),
            gasless=gasless,
            source=data.get("source"),
        )

    @property
    def order_sell_tokens(self) -> list[TokenAmount]:
        """
        tokens formatted as required for the jam order object
        """
        return merge_tokens(self.sell_tokens)

    @property
    def order_buy_tokens(self) -> list[TokenAmount]:
        """
        tokens formatted as required for the jam order object
        """
        return merge_tokens(self.buy_tokens)

    def decode_sell_token_transfers(self) -> list[JamCommand]:
        return decode_token_transfers(self.sell_token_transfers)


class QuoteResponse(BaseMessage):
    quote_id: str  # Quote ID of the request
    amounts: list[TokenAmountResponse]  # Output amounts
    fee: int  # Estimated fee in native token
    executor: str

    def to_ws(self) -> dict:
        return {
            "quote_id": self.quote_id,
            "amounts": [amount.to_ws() for amount in self.amounts],
            "fee": str(self.fee),
            "executor": self.executor,
        }

    @staticmethod
    def from_ws(msg: dict[str, Any]) -> QuoteResponse:
        amounts: list[TokenAmountResponse] = []
        for amount in msg["amounts"]:
            amounts.append(TokenAmountResponse(address=amount["address"], amount=int(amount["amount"])))
        return QuoteResponse(
            quote_id=msg["quote_id"],
            amounts=amounts,
            fee=int(msg["fee"]),
            executor=msg["executor"],
        )


class TakerQuoteResponse(QuoteResponse):
    interactions: list[InteractionDetails]
    solver_data: SolverData

    def to_ws(self) -> dict:
        return {
            "quote_id": self.quote_id,
            "amounts": [amount.to_ws() for amount in self.amounts],
            "fee": str(self.fee),
            "executor": self.executor,
            "interactions": [interaction.to_ws() for interaction in self.interactions] if self.interactions else None,
            "solver_data": self.solver_data.model_dump(),
        }

    @staticmethod
    def from_ws(msg: dict[str, Any]) -> TakerQuoteResponse:
        amounts: list[TokenAmountResponse] = []
        for amount in msg["amounts"]:
            amounts.append(TokenAmountResponse(address=amount["address"], amount=int(amount["amount"])))
        return TakerQuoteResponse(
            quote_id=msg["quote_id"],
            amounts=amounts,
            fee=int(msg["fee"]),
            executor=msg["executor"],
            interactions=[InteractionDetails.from_ws(interaction) for interaction in msg["interactions"]],
            solver_data=SolverData(**msg["solver_data"]),
        )


class SignatureType(Enum):
    NONE = 0
    EIP712 = 1
    EIP1271 = 2
    ETHSIGN = 3

    @staticmethod
    def from_str(name: str) -> SignatureType:
        return SignatureType[name]

    def to_str(self) -> str:
        return str(self.name)


class Signature(BaseMessage):
    signature_type: SignatureType
    signature_bytes: str

    def to_ws(self) -> dict:
        return {
            "signature_type": self.signature_type.to_str(),
            "signature_bytes": self.signature_bytes,
        }

    @staticmethod
    def from_ws(data: dict) -> Signature:
        return Signature(
            signature_type=SignatureType.from_str(data["signature_type"]),
            signature_bytes=data["signature_bytes"],
        )

    def to_blockchain_args(self) -> dict:
        return {"signatureType": self.signature_type.value, "signatureBytes": self.signature_bytes}


class PermitsInfo(BaseModel):
    signature: str
    deadline: int
    token_addresses: list[str]  # only for Permit2, for Permit it's []
    token_nonces: list[int]  # only for Permit2, for Permit it's []

    def to_ws(self) -> dict:
        return {
            "signature": self.signature,
            "deadline": str(self.deadline),
            "token_addresses": self.token_addresses,
            "token_nonces": [str(nonce) for nonce in self.token_nonces],
        }

    @staticmethod
    def from_ws(data: dict) -> PermitsInfo:
        return PermitsInfo(
            signature=data["signature"],
            deadline=int(data["deadline"]),
            token_addresses=data["token_addresses"],
            token_nonces=[int(nonce) for nonce in data["token_nonces"]],
        )


class SolverData(BaseModel):
    balance_recipient: str
    cur_fill_percent: int = 10000

    def to_blockchain_args(self) -> dict:
        return {"balanceRecipient": self.balance_recipient, "curFillPercent": self.cur_fill_percent}


class ExecuteRequest(BaseMessage):
    quote_id: str
    signature: Signature
    min_amounts: list[TokenAmountResponse]  # Slippage applied amounts
    permits_info: PermitsInfo | None = None

    def to_ws(self) -> dict:
        data = {
            "quote_id": self.quote_id,
            "signature": self.signature.to_ws(),
            "min_amounts": [amount.to_ws() for amount in self.min_amounts],
        }
        if self.permits_info:
            data["permits_info"] = self.permits_info.to_ws()
        return data

    @staticmethod
    def from_ws(data: dict) -> ExecuteRequest:
        permits_info = PermitsInfo.from_ws(data["permits_info"]) if "permits_info" in data else None
        min_amounts = [TokenAmountResponse.from_ws(amount) for amount in data["min_amounts"]]
        return ExecuteRequest(
            quote_id=data["quote_id"],
            signature=Signature.from_ws(data["signature"]),
            min_amounts=min_amounts,
            permits_info=permits_info,
        )

    def get_permits_blockchain_args(self, approval_type: ApprovalType) -> dict | None:
        if approval_type == ApprovalType.Permit and self.permits_info:
            return {
                "permitSignatures": [self.permits_info.signature],
                "signatureBytesPermit2": "0x",
                "noncesPermit2": [],
                "deadline": self.permits_info.deadline,
            }
        elif approval_type == ApprovalType.Permit2 and self.permits_info:
            return {
                "permitSignatures": [],
                "signatureBytesPermit2": self.permits_info.signature,
                "noncesPermit2": self.permits_info.token_nonces,
                "deadline": self.permits_info.deadline,
            }
        return None


class ExecuteResponse(BaseMessage):
    quote_id: str

    def to_ws(self) -> dict:
        return {"quote_id": self.quote_id}

    @staticmethod
    def from_ws(data: dict) -> ExecuteResponse:
        return ExecuteResponse(quote_id=data["quote_id"])


class QuoteErrorType(Enum):
    Unavailable = "unavailable"  # Unavailable to provide quotes
    NotSupported = "not_supported"  # Type of order or tokens not supported
    GasExceedsSize = "gas_exceeds_size"  # Order size is too small to cover fee
    Unknown = "unknown"  # Unknown error
    Timeout = "timeout"  # Solver took too long to respond


class ExecuteErrorType(Enum):
    Reject = "reject"  # Rejected executing the order
    Timeout = "timeout"  # Solver took too long to respond


class BaseError(BaseMessage):
    quote_id: str
    error_type: Enum
    error_message: str | None

    def to_ws(self) -> dict:
        return {
            "quote_id": self.quote_id,
            "error_type": self.error_type.value,
            "error_msg": self.error_message,
        }


class QuoteError(BaseError):
    error_type: QuoteErrorType

    @staticmethod
    def from_ws(data: dict) -> QuoteError:
        return QuoteError(
            quote_id=data["quote_id"], error_type=QuoteErrorType(data["error_type"]), error_message=data["error_msg"]
        )


class ExecuteError(BaseError):
    error_type: ExecuteErrorType

    @staticmethod
    def from_ws(data: dict) -> ExecuteError:
        return ExecuteError(
            quote_id=data["quote_id"], error_type=ExecuteErrorType(data["error_type"]), error_message=data["error_msg"]
        )


class CachedQuote(BaseModel):
    chain_id: int
    request: QuoteRequest
    response: QuoteResponse


class SolverConnection(BaseModel):
    name: str
    auth: str
    url: str
