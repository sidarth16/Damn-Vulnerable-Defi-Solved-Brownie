import pytest
import brownie
from brownie import FlashLoanerPool, TheRewarderPool, DamnValuableToken, RewardToken, AccountingToken
from brownie import AttackRewarder
from brownie import accounts , Wei , exceptions, chain

deployer, alice, bob, charlie, david, attacker = None, None, None, None, None, None
users = [alice, bob, charlie, david]

# Pool has 1M * 10**18 tokens
TOKENS_IN_LENDER_POOL = Wei('1_000_000 ether')  

#--  [ SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE ] --#
@pytest.fixture(scope="module")
def contracts():

    global deployer, alice, bob, charlie, david, attacker, users
    deployer, alice, bob, charlie, david, attacker = accounts[0:6]

    contracts = {}

    liquidityToken =  DamnValuableToken.deploy({"from":deployer})
    flashLoanPool =  FlashLoanerPool.deploy(liquidityToken.address, {"from":deployer})

    # Set initial token balance of the pool offering flash loans
    liquidityToken.transfer(flashLoanPool.address, TOKENS_IN_LENDER_POOL, {"from":deployer})

    rewarderPool =  TheRewarderPool.deploy(liquidityToken.address, {"from":deployer})
    rewardToken =  RewardToken.attach(rewarderPool.rewardToken(), {"from":deployer})
    accountingToken =  AccountingToken.attach(rewarderPool.accToken(), {"from":deployer})

    # Alice, Bob, Charlie and David deposit 100 tokens each
    for user in users: 
        amount = Wei('100 ether')
        liquidityToken.transfer(user.address, amount, {"from":deployer})
        liquidityToken.approve(rewarderPool.address, amount, {"from":user})
        rewarderPool.deposit(amount, {"from":user})
        assert accountingToken.balanceOf(user.address) == amount
    assert accountingToken.totalSupply() == Wei('400 ether')
    assert rewardToken.totalSupply() == '0'

    chain.sleep(5 * 24 * 60 * 60)
    chain.mine(1)
          
    # Each depositor gets 25 reward tokens
    for user in users:
        rewarderPool.distributeRewards({"from":user})
        assert rewardToken.balanceOf(user.address) == Wei('25 ether')
    assert rewardToken.totalSupply() == Wei('100 ether')

    # Attacker starts with zero DVT tokens in balance
    assert liquidityToken.balanceOf(attacker.address) == '0'
    
    # Two rounds should have occurred so far
    assert rewarderPool.roundNumber() == '2'

    contracts['liquidityToken'] = liquidityToken
    contracts["flashLoanPool"] = flashLoanPool
    contracts["rewarderPool"] = rewarderPool
    contracts['rewardToken'] = rewardToken
    contracts['AccountingToken'] = accountingToken

    yield contracts

    #---  [ SUCCESS CONDITIONS ]  ---#
    # Attacker has taken all tokens from the pool
    assert token.balanceOf(attacker.address) == TOKENS_IN_POOL
    assert token.balanceOf(pool.address) == '0'


def test_truster_challenge(contracts):
    #-- [ CODE YOUR EXPLOIT HERE ] ---#
    #_________________________________#
