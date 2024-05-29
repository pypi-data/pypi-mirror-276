from pathlib import Path

import pytest

from pons import (
    Address,
    Constructor,
    ContractABI,
    Method,
    Mutability,
    abi,
    compile_contract_file,
)
from pons._contract import DeployedContract


@pytest.fixture
def compiled_contracts():
    path = Path(__file__).resolve().parent / "MockMulticall.sol"
    yield compile_contract_file(path)


async def test_multicall(session, root_signer, compiled_contracts):
    mock = compiled_contracts["MockMulticall"]

    dmock = await session.deploy(root_signer, mock.constructor())

    Call3 = abi.struct(target=abi.address, allowFailure=abi.bool, callData=abi.bytes())

    Result = abi.struct(success=abi.bool, returnData=abi.bytes())

    ABI = ContractABI(
        methods=[
            Method(
                name="aggregate3",
                mutability=Mutability.PAYABLE,
                inputs=dict(calls=Call3[...]),
                outputs=Result[...],
            ),
            Method(
                name="test",
                mutability=Mutability.NONPAYABLE,
                inputs=dict(x=abi.uint(256)),
                outputs=abi.uint(256),
            ),
            Method(
                name="v1",
                mutability=Mutability.VIEW,
                inputs={},
                outputs=abi.uint(256),
            ),
        ],
    )

    dmock = DeployedContract(ABI, dmock.address)

    call1 = [dmock.address, True, dmock.abi.method.test(1).data_bytes]
    call2 = [dmock.address, True, dmock.abi.method.test(2).data_bytes]

    result = await session.eth_call(dmock.method.aggregate3([call1, call2]))
    print(dmock.abi.method.test.decode_output(result[0]["returnData"]))

    print("v1 = ", await session.eth_call(dmock.method.v1()))
    print(await session.eth_call(dmock.method.test(1)))
    print("v1 = ", await session.eth_call(dmock.method.v1()))
    await session.transact(root_signer, dmock.method.test(1))
    print("v1 = ", await session.eth_call(dmock.method.v1()))
