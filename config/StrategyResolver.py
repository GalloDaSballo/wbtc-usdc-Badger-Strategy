from helpers.StrategyCoreResolver import StrategyCoreResolver
from rich.console import Console
from brownie import interface

console = Console()


class StrategyResolver(StrategyCoreResolver):
    def hook_after_confirm_withdraw(self, before, after, params):
        """
            Specifies extra check for ordinary operation on withdrawal
            Use this to verify that balances in the get_strategy_destinations are properly set
        """
        assert after.balances("want", "staking_rewards") < before.balances(
            "want", "staking_rewards")

    def hook_after_confirm_deposit(self, before, after, params):
        """
            Specifies extra check for ordinary operation on deposit
            Use this to verify that balances in the get_strategy_destinations are properly set
        """
        assert after.balances("want", "strategy") == 0

    def hook_after_earn(self, before, after, params):
        """
            Specifies extra check for ordinary operation on earn
            Use this to verify that balances in the get_strategy_destinations are properly set
        """
        assert after.balances("want", "staking_rewards") > before.balances(
            "want", "staking_rewards")

    def confirm_harvest(self, before, after, tx):
        """
            Verfies that the Harvest produced yield and fees
        """
        console.print("=== Compare Harvest ===")
        self.manager.printCompare(before, after)
        self.confirm_harvest_state(before, after, tx)

        valueGained = after.get("sett.pricePerFullShare") > before.get(
            "sett.pricePerFullShare"
        )

        # Strategist should earn if fee is enabled and value was generated
        if before.get("strategy.performanceFeeStrategist") > 0 and valueGained:
            assert after.balances("want", "strategist") > before.balances(
                "want", "strategist"
            )

        # Strategist should earn if fee is enabled and value was generated
        if before.get("strategy.performanceFeeGovernance") > 0 and valueGained:
            assert after.balances("want", "governanceRewards") > before.balances(
                "want", "governanceRewards"
            )

    def confirm_tend(self, before, after, tx):
        """
        Tend Should;
        - Increase the number of staked tended tokens in the strategy-specific mechanism
        - Reduce the number of tended tokens in the Strategy to zero

        (Strategy Must Implement)
        """
        # print("strategy.balanceOfWant")
        # print(before.get("strategy.balanceOfWant"))

        if (before.get("strategy.balanceOfWant") > 0):
            assert after.get("strategy.balanceOfWant") == 0

            assert after.get("strategy.balanceOfPool") > before.get(
                "strategy.balanceOfPool")

    def get_strategy_destinations(self):
        """
        Track balances for all strategy implementations
        (Strategy Must Implement)
        """
        strategy = self.manager.strategy
        return {
            "reward": strategy.reward(),
            "want": strategy.want(),
            "staking_rewards": strategy.STAKING_REWARDS(),
        }

    def add_balances_snap(self, calls, entities):
        super().add_balances_snap(calls, entities)
        strategy = self.manager.strategy

        usdc = interface.IERC20(strategy.usdc())
        wbtc = interface.IERC20(strategy.wbtc())
        weth = interface.IERC20(strategy.weth())
        quick = interface.IERC20(strategy.reward()) # QUICK

        calls = self.add_entity_balances_for_tokens(calls, "usdc", usdc, entities)
        calls = self.add_entity_balances_for_tokens(calls, "wbtc", wbtc, entities)
        calls = self.add_entity_balances_for_tokens(calls, "weth", weth, entities)
        calls = self.add_entity_balances_for_tokens(calls, "quick", quick, entities)

        return calls

    def confirm_harvest_state(self, before, after, tx):
        key = "Harvest"
        if key in tx.events:
            event = tx.events[key][0]
            keys = [
                "harvested",
            ]
            for key in keys:
                assert key in event

            console.print("[blue]== harvest() Harvest State ==[/blue]")
            self.printState(event, keys)

    def printState(self, event, keys):
        for key in keys:
            print(key, ": ", event[key])

