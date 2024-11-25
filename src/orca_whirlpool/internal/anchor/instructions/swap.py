from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID
from spl.memo.constants import MEMO_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class SwapArgs(typing.TypedDict):
    amount: int
    other_amount_threshold: int
    sqrt_price_limit: int
    amount_specified_is_input: bool
    a_to_b: bool


class SwapArgsV2(typing.TypedDict):
    amount: int
    other_amount_threshold: int
    sqrt_price_limit: int
    amount_specified_is_input: bool
    a_to_b: bool
    remaining_accounts_info: dict


layout = borsh.CStruct(
    "amount" / borsh.U64,
    "other_amount_threshold" / borsh.U64,
    "sqrt_price_limit" / borsh.U128,
    "amount_specified_is_input" / borsh.Bool,
    "a_to_b" / borsh.Bool,
)


class SwapAccounts(typing.TypedDict):
    token_authority: Pubkey
    whirlpool: Pubkey
    token_owner_account_a: Pubkey
    token_vault_a: Pubkey
    token_owner_account_b: Pubkey
    token_vault_b: Pubkey
    tick_array0: Pubkey
    tick_array1: Pubkey
    tick_array2: Pubkey
    oracle: Pubkey


class SwapAccountsV2(typing.TypedDict):
    token_program_a: Pubkey
    token_program_b: Pubkey
    memo_program: Pubkey
    token_authority: Pubkey
    whirlpool: Pubkey
    token_mint_a: Pubkey
    token_mint_b: Pubkey
    token_owner_account_a: Pubkey
    token_vault_a: Pubkey
    token_owner_account_b: Pubkey
    token_vault_b: Pubkey
    tick_array0: Pubkey
    tick_array1: Pubkey
    tick_array2: Pubkey
    oracle: Pubkey


def swap(
    args: SwapArgs,
    accounts: SwapAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["whirlpool"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["token_owner_account_a"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_vault_a"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_owner_account_b"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_vault_b"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["tick_array0"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["tick_array1"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["tick_array2"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xf8\xc6\x9e\x91\xe1u\x87\xc8"
    encoded_args = layout.build(
        {
            "amount": args["amount"],
            "other_amount_threshold": args["other_amount_threshold"],
            "sqrt_price_limit": args["sqrt_price_limit"],
            "amount_specified_is_input": args["amount_specified_is_input"],
            "a_to_b": args["a_to_b"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)


def swap_v2(
    args: SwapArgsV2,
    accounts: SwapAccountsV2,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["token_program_a"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["token_program_b"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=MEMO_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["whirlpool"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["token_mint_a"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_mint_b"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_owner_account_a"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_vault_a"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_owner_account_b"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_vault_b"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["tick_array0"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["tick_array1"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["tick_array2"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b'+\x04\xed\x0b\x1a\xc9\x1eb'
    encoded_args = layout.build(
        {
            "amount": args["amount"],
            "other_amount_threshold": args["other_amount_threshold"],
            "sqrt_price_limit": args["sqrt_price_limit"],
            "amount_specified_is_input": args["amount_specified_is_input"],
            "a_to_b": args["a_to_b"]
            #,
            #"remaining_account_info": args['remaining_accounts_info']
        }
    )
    data = identifier + encoded_args + b'\x00' # last part \x00 is remaining_account_info encoder which I just hardcode it
    return Instruction(program_id, data, keys)
