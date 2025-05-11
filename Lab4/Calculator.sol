// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Calculator {
    function add(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b;
    }

    function subtract(uint256 a, uint256 b) public pure returns (uint256) {
        require(a >= b, "Subtraction underflow");
        return a - b;
    }

    function multiply(uint256 a, uint256 b) public pure returns (uint256) {
        return a * b;
    }

    function divide(uint256 a, uint256 b) public pure returns (uint256) {
        require(b > 0, "Division by zero");
        return a / b;
    }

    function exponent(uint256 a, uint256 b) public pure returns (uint256) {
        if (b == 0) return 1;
        return a ** b;
    }

    function remainder(uint256 a, uint256 b) public pure returns (uint256) {
        require(b > 0, "Division by zero");
        return a % b;
    }

    function square(uint256 a) public pure returns (uint256) {
        return a * a;
    }

    function absoluteValue(int256 a) public pure returns (uint256) {
        return a >= 0 ? uint256(a) : uint256(-a);
    }

    function max(uint256 a, uint256 b) public pure returns (uint256) {
        return a >= b ? a : b;
    }

    function min(uint256 a, uint256 b) public pure returns (uint256) {
        return a <= b ? a : b;
    }
}
