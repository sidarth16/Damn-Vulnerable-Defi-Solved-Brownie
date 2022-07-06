import pytest
import brownie
from brownie import DamnValuableTokenSnapshot, SimpleGovernance, SelfiePool
from brownie import AttackRewarder
from brownie import accounts , Wei , exceptions, chain

deployer, attacker = None, None

# Pool has 1M * 10**18 tokens
TOKEN_INITIAL_SUPPLY = Wei('2_000_000 ether')
TOKENS_IN_POOL = Wei('1500000 ether')  

#--  [ SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE ] --#
@pytest.fixture(scope="module")
def contracts():

    global deployer, attacker
    deployer, attacker = accounts[0:2]

    contracts = {}

    token =  DamnValuableTokenSnapshot.deploy(TOKEN_INITIAL_SUPPLY, {"from":deployer})
    governance =  SimpleGovernance.deploy(token.address, {"from":deployer})
    pool = SelfiePool.deploy(token.address, governance.address, {"from":deployer})

    # Set initial token balance of the pool offering flash loans
    token.transfer(pool.address, TOKENS_IN_POOL, {"from":deployer})

    assert token.balanceOf(pool.address) == TOKENS_IN_POOL

    contracts['token'] = tokens
    contracts["governance"] = governance
    contracts["pool"] = pool

    yield contracts

#     #---  [ SUCCESS CONDITIONS ]  ---#
    
#     # Only one round should have taken place
#     assert rewarderPool.roundNumber() == '3'

#      # Users should get neglegible rewards this round
#     for user in users:
#         rewarderPool.distributeRewards({"from":user})
#         rewards = rewardToken.balanceOf(user.address)
        
#     # The difference between current and previous rewards balance should be lower than 0.01 tokens
#     delta = rewards - Wei('25 ether')
#     assert  delta < Wei(1e16)
        
#     # Rewards must have been issued to the attacker account
#     assert rewardToken.totalSupply() > Wei('100 ether')
#     rewards = rewardToken.balanceOf(attacker.address)
        
#     # The amount of rewards earned should be really close to 100 tokens
#     delta = Wei('100 ether') - (rewards)
#     assert delta < Wei(1e17)
    
#     # Attacker finishes with zero DVT tokens in balance
#     assert liquidityToken.balanceOf(attacker.address) == ('0')


def test_selfie_challenge(contracts):
    #-- [ CODE YOUR EXPLOIT HERE ] ---#
    pass
    #_________________________________#
