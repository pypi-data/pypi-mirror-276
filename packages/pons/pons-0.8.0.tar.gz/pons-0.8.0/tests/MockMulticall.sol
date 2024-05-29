pragma solidity >=0.8.0 <0.9.0;


contract MockMulticall {
    struct Call3 {
        address target;
        bool allowFailure;
        bytes callData;
    }

    struct Result {
        bool success;
        bytes returnData;
    }

    uint256 public v1;

    constructor() {
        v1 = 666;
    }

    function aggregate3(Call3[] calldata calls) public payable returns (Result[] memory returnData) {
        uint256 length = calls.length;
        Call3 calldata calli;
        returnData = new Result[](length);

        for (uint256 i = 0; i < length; i++) {
            Result memory result = returnData[i];
            calli = calls[i];
            (result.success, result.returnData) = calli.target.call(calli.callData);
        }
    }

    function test(uint256 x) public returns (uint256) {
        if (x == 1) {
            v1 = x + 1;
        }
        return v1;
    }
}
