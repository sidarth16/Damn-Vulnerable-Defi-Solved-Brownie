import pytest
import brownie
from brownie import Exchange, DamnValuableNFT, TrustfulOracle, TrustfulOracleInitializer
from brownie import accounts , Wei , exceptions


print('Compromised challenge :')

sources = [
        '0xA73209FB1a42495120166736362A1DfA9F95A105',
        '0xe92401A4d3af5E446d93D11EEc806b1462b39D15',
        '0x81A5D6E50C214044bE44cA0CB057fe119097850c'
    ]

deployer, attacker = None, None
EXCHANGE_INITIAL_ETH_BALANCE = Wei('9990 ether')
INITIAL_NFT_PRICE = Wei('999 ether')


@pytest.fixture(scope="module")
def contracts():
    #-- SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE --#
    global deployer, attacker
    deployer, attacker= accounts[0:2]

    contracts = {}

    pool = NaiveReceiverLenderPool.deploy( {"from":deployer} )
    receiver =  FlashLoanReceiver.deploy( pool.address, {"from":deployer} )
    attackNaiveReceiver = AttackNaiveReceiver.deploy(pool.address, {"from":attacker} )

    # Funding Pool and receiver contracts with initial Ether
    deployer.transfer(to=pool, amount=ETHER_IN_POOL)
    deployer.transfer(to=receiver, amount=ETHER_IN_RECEIVER)

    assert pool.balance() == ETHER_IN_POOL
    assert receiver.balance() == ETHER_IN_RECEIVER
    assert pool.fixedFee() == Wei('1 ether')

    contracts['receiver'] = receiver
    contracts['pool'] = pool
    contracts['attackNaiveReceiver'] = attackNaiveReceiver

    yield contracts
