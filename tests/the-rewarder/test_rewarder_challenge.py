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
    
    # Only one round should have taken place
    assert rewarderPool.roundNumber() == '3'

     # Users should get neglegible rewards this round
    for user in users:
        rewarderPool.distributeRewards({"from":user})
        rewards = rewardToken.balanceOf(user.address)
        
        # The difference between current and previous rewards balance should be lower than 0.01 tokens
        delta = rewards - Wei('25')
        assert  delta < 10**16
        expect(delta).to.be.lt(ethers.utils.parseUnits('1', 16))
        console.log("\n----[ delta 1 passed ]----\n")

        
        // Rewards must have been issued to the attacker account
        expect(await this.rewardToken.totalSupply()).to.be.gt(ethers.utils.parseEther('100'));
        console.log("\n----[ Total Rewards passed ]----\n")
        let rewards = await this.rewardToken.balanceOf(attacker.address);
        
        // The amount of rewards earned should be really close to 100 tokens
        let delta = ethers.utils.parseEther('100').sub(rewards);
        expect(delta).to.be.lt(ethers.utils.parseUnits('1', 17));
        console.log("\n----[ Delta 2 passed ]----\n")
        
        // Attacker finishes with zero DVT tokens in balance
        expect(await this.liquidityToken.balanceOf(attacker.address)).to.eq('0');


def test_truster_challenge(contracts):
    #-- [ CODE YOUR EXPLOIT HERE ] ---#
    #_________________________________#
