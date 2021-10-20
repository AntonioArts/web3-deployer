// SPDX-Licence-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // init with 0
    uint256 favoriteNumber;

    struct People {
        string name;
        uint256 favoriteNumber;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retreive() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_name, _favoriteNumber));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
