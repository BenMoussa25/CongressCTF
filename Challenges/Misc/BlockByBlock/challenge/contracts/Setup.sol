// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Cyber.sol";

contract Setup {
    Cyber public challengeInstance;

    constructor() payable {
        challengeInstance = new Cyber{value: 1 ether}();
    }

    function isSolved() public view returns (bool) {
        return false;
    }

}