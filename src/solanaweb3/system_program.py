"""Library to interface with system programs."""
from __future__ import annotations

from typing import Any, List, NamedTuple, Union

from solanaweb3.instruction import InstructionLayout, decode_data, encode_data
from solanaweb3.publickey import PublicKey
from solanaweb3.transaction import AccountMeta, Transaction, TransactionInstruction

# Instruction Indices
_CREATE = 0
_ASSIGN = 1
_TRANSFER = 2
_CREATE_WITH_SEED = 3
_ADVANCE_NONCE_ACCOUNT = 4
_WITHDRAW_NONCE_ACCOUNT = 5
_INITIALZE_NONCE_ACCOUNT = 6
_AUTHORIZE_NONCE_ACCOUNT = 7
_ALLOCATE = 8
_ALLOCATE_WITH_SEED = 9
_ASSIGN_WITH_SEED = 10


# Instruction Params
class CreateAccountParams(NamedTuple):
    """Create account system transaction params.

    :param from_pubkey: PublicKey

    :param new_account_pubkey: PublicKey

    :param lamports: int

    :param space: int

    :param program_id: PublicKey
    """

    from_pubkey: PublicKey
    new_account_pubkey: PublicKey
    lamports: int
    space: int
    program_id: PublicKey


class TransferParams(NamedTuple):
    """Transfer system transaction params.

    :param from_pubkey: PublicKey

    :param to_pubkey: PublicKey

    :param lamports: int
    """

    from_pubkey: PublicKey
    to_pubkey: PublicKey
    lamports: int


class AssignParams(NamedTuple):
    """Assign system transaction params.

    :param account_pubkey: PublicKey

    :param program_id: PublicKey
    """

    account_pubkey: PublicKey
    program_id: PublicKey


class CreateAccountWithSeedParams(NamedTuple):
    """Create account with seed system transaction params.

    :param from_pubkey: PublicKey

    :param new_account_pubkey: PublicKey

    :param base_pubkey: PublicKey

    :param seed: str

    :param lamports: int

    :param space: int

    :param program_id: PublicKey
    """

    from_pubkey: PublicKey
    new_account_pubkey: PublicKey
    base_pubkey: PublicKey
    seed: str
    lamports: int
    space: int
    program_id: PublicKey


class CreateNonceAccountParams(NamedTuple):
    """Create nonce account system transaction params.

    :param from_pubkey: PublicKey

    :param nonce_pubkey: PublicKey

    :param authorized_pubkey: PublicKey

    :param lamports: int
    """

    from_pubkey: PublicKey
    nonce_pubkey: PublicKey
    authorized_pubkey: PublicKey
    lamports: int


class CreateNonceAccountWithSeedParams(NamedTuple):
    """Create nonce account with seed system transaction params.

    :param from_pubkey: PublicKey

    :param nonce_pubkey: PublicKey

    :param authorized_pubkey: PublicKey

    :param lamports: int

    :param base_pubkey: PublicKey

    :param seed: str
    """

    from_pubkey: PublicKey
    nonce_pubkey: PublicKey
    authorized_pubkey: PublicKey
    lamports: int
    base_pubkey: PublicKey
    seed: str


class InitializeNonceParams(NamedTuple):
    """Initialize nonce account system instruction params.

    :param nonce_pubkey: PublicKey

    :param authorized_pubkey: PublicKey
    """

    nonce_pubkey: PublicKey
    authorized_pubkey: PublicKey


class AdvanceNonceParams(NamedTuple):
    """Advance nonce account system instruction params.

    :param nonce_pubkey: PublicKey

    :param authorized_pubkey: PublicKey
    """

    nonce_pubkey: PublicKey
    authorized_pubkey: PublicKey


class WithdrawNonceParams(NamedTuple):
    """Withdraw nonce account system transaction params.

    :param nonce_pubkey: PublicKey

    :param authorized_pubkey: PublicKey

    :param to_pubkey: PublicKey

    :param lamports: int
    """

    nonce_pubkey: PublicKey
    authorized_pubkey: PublicKey
    to_pubkey: PublicKey
    lamports: int


class AuthorizeNonceParams(NamedTuple):
    """Authorize nonce account system transaction params.

    :param nonce_pubkey: PublicKey

    :param authorized_pubkey: PublicKey

    :param new_authorized_pubkey: PublicKey
    """

    nonce_pubkey: PublicKey
    authorized_pubkey: PublicKey
    new_authorized_pubkey: PublicKey


class AllocateParams(NamedTuple):
    """Allocate account with seed system transaction params.

    :param account_pubkey: PublicKey

    :param space: int
    """

    account_pubkey: PublicKey
    space: int


class AllocateWithSeedParams(NamedTuple):
    """Allocate account with seed system transaction params.

    :param account_pubkey: PublicKey

    :param base_pubkey: PublicKey

    :param seed: str

    :param space: int

    :param program_id: PublicKey
    """

    account_pubkey: PublicKey
    base_pubkey: PublicKey
    seed: str
    space: int
    program_id: PublicKey


class AssignWithSeedParams(NamedTuple):
    """Assign account with seed system transaction params.

    :param account_pubkey: PublicKey

    :param base_pubkey: PublicKey

    :param seed: str

    :param program_id: PublicKey
    """

    account_pubkey: PublicKey
    base_pubkey: PublicKey
    seed: str
    program_id: PublicKey


SYSTEM_INSTRUCTION_LAYOUTS: List[InstructionLayout] = [
    InstructionLayout(idx=_CREATE, fmt="<Iqq32s"),
    InstructionLayout(idx=_ASSIGN, fmt="<I32s"),
    InstructionLayout(idx=_TRANSFER, fmt="<Iq"),
    InstructionLayout(idx=_CREATE_WITH_SEED, fmt=""),
    InstructionLayout(idx=_ADVANCE_NONCE_ACCOUNT, fmt="<I"),
    InstructionLayout(idx=_WITHDRAW_NONCE_ACCOUNT, fmt="<Iq"),
    InstructionLayout(idx=_INITIALZE_NONCE_ACCOUNT, fmt="<I32s"),
    InstructionLayout(idx=_AUTHORIZE_NONCE_ACCOUNT, fmt="<I32s"),
    InstructionLayout(idx=_ALLOCATE, fmt="<I32s"),
    InstructionLayout(idx=_ALLOCATE_WITH_SEED, fmt=""),
    InstructionLayout(idx=_ASSIGN_WITH_SEED, fmt=""),
]


class SystemInstruction:
    """System Instruction class to decode transaction instruction data."""

    @staticmethod
    def __check_key_length(keys: List[Any], expected_length: int) -> None:
        if len(keys) < expected_length:
            raise ValueError(f"invalid instruction: found {len(keys)} keys, expected at least {expected_length}")

    @staticmethod
    def __check_program_id(program_id: PublicKey) -> None:
        if program_id != SystemProgram.program_id():
            raise ValueError("invalid instruction: programId is not SystemProgram")

    @staticmethod
    def decode_instruction_layout(instructoin: TransactionInstruction) -> InstructionLayout:
        """Decode a system instruction and retrieve the instruction layout."""
        raise NotImplementedError("decode_instruction_layout not implemented")

    @staticmethod
    def decode_create_account(instruction: TransactionInstruction) -> CreateAccountParams:
        """Decode a create account system instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_create_account not implemented")

    @staticmethod
    def decode_transfer(instruction: TransactionInstruction) -> TransferParams:
        """Decode a transfer system instruction and retrieve the instruction params."""
        SystemInstruction.__check_program_id(instruction.program_id)
        SystemInstruction.__check_key_length(instruction.keys, 2)

        layout = SYSTEM_INSTRUCTION_LAYOUTS[_TRANSFER]
        data = decode_data(layout, instruction.data)

        return TransferParams(
            from_pubkey=instruction.keys[0].pubkey, to_pubkey=instruction.keys[1].pubkey, lamports=data[1]
        )

    @staticmethod
    def decode_allocate(instruction: TransactionInstruction) -> AllocateParams:
        """Decode an allocate system instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_allocate not implemented")

    @staticmethod
    def decode_allocate_with_seed(instruction: TransactionInstruction) -> AllocateWithSeedParams:
        """Decode an allocate with seed system instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_allocate_with_seed not implemented")

    @staticmethod
    def decode_assign(instruction: TransactionInstruction) -> AssignParams:
        """Decode an assign system instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_assign not implemented")

    @staticmethod
    def decode_assign_with_seed(instruction: TransactionInstruction) -> AssignWithSeedParams:
        """Decode an assign system with seed instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_assign_with_seed not implemented")

    @staticmethod
    def decode_create_with_seed(instruction: TransactionInstruction) -> CreateAccountWithSeedParams:
        """Decode a create account with seed system instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_create_with_seed not implemented")

    @staticmethod
    def decode_nonce_initialize(instruction: TransactionInstruction) -> InitializeNonceParams:
        """Decode a nonce initialize system instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_nonce_initialize not implemented")

    @staticmethod
    def decode_nonce_advance(instruction: TransactionInstruction) -> AdvanceNonceParams:
        """Decode a nonce advance system instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_nonce_advance not implemented")

    @staticmethod
    def decode_nonce_withdraw(instruction: TransactionInstruction) -> WithdrawNonceParams:
        """Decode a nonce withdraw system instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_nonce_withdraw not implemented")

    @staticmethod
    def decode_nonce_authorize(instruction: TransactionInstruction) -> AuthorizeNonceParams:
        """Decode a nonce authorize system instruction and retrieve the instruction params."""
        raise NotImplementedError("decode_nonce_authorize not implemented")


class SystemProgram:
    """Factory class for transactions to interact with the System program."""

    @staticmethod
    def program_id() -> PublicKey:
        """Public key that identifies the System program."""
        return PublicKey("11111111111111111111111111111111")

    @staticmethod
    def create_account(param: CreateAccountParams) -> Transaction:
        """Generate a Transaction that creates a new account."""
        raise NotImplementedError("create_account not implemented")

    @staticmethod
    def assign(params: Union[AssignParams, AssignWithSeedParams]) -> Transaction:
        """Generate a Transaction that assigns an account to a program."""
        raise NotImplementedError("assign not implemented")

    @staticmethod
    def transfer(params: TransferParams) -> Transaction:
        """Generate a Transaction that transfers lamports from one account to another."""
        layout = SYSTEM_INSTRUCTION_LAYOUTS[_TRANSFER]
        data = encode_data(layout, params.lamports)

        txn = Transaction()
        txn.add(
            TransactionInstruction(
                keys=[
                    AccountMeta(pubkey=params.from_pubkey, is_signer=True, is_writable=True),
                    AccountMeta(pubkey=params.to_pubkey, is_signer=False, is_writable=True),
                ],
                program_id=SystemProgram.program_id(),
                data=data,
            )
        )
        return txn

    @staticmethod
    def create_account_with_seed(params: CreateAccountWithSeedParams) -> Transaction:
        """Generate a Transaction that creates a new account at an address."""
        raise NotImplementedError("create_account_with_seed not implemented")

    @staticmethod
    def create_nonce_account(param: Union[CreateNonceAccountParams, CreateAccountWithSeedParams]) -> Transaction:
        """Generate a Transaction that creates a new Nonce account."""
        raise NotImplementedError("create_nonce_account_params not implemented")

    @staticmethod
    def nonce_initialization(param: InitializeNonceParams) -> TransactionInstruction:
        """Generate an instruction to initialize a Nonce account."""
        raise NotImplementedError("nonce_initialization not implemented")

    @staticmethod
    def nonce_advance(param: AdvanceNonceParams) -> TransactionInstruction:
        """Generate an instruction to advance the nonce in a Nonce account."""
        raise NotImplementedError("nonce advance not implemented")

    @staticmethod
    def nonce_withdraw(param: WithdrawNonceParams) -> Transaction:
        """Generate a Transaction that withdraws lamports from a Nonce account."""
        raise NotImplementedError("nonce_withdraw not implemented")

    @staticmethod
    def nonce_authorize(param: AuthorizeNonceParams) -> Transaction:
        """Generate a Transaction that authorizes a new PublicKey as the authority on a Nonce account."""
        raise NotImplementedError("nonce_authorize not implemented")

    @staticmethod
    def allocate(param: Union[AllocateParams, AllocateWithSeedParams]) -> Transaction:
        """Generate a Transaction that allocates space in an account without funding."""
        raise NotImplementedError("allocate not implemented")
