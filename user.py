import random
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import names

from simulation import SIMULATION_OUTCOMES, SimulationResult


class User(metaclass=ABCMeta):
    """The abstract baseclass for a user, please don't use this directly.

    Create your own subclass(es) with a '_get_simulation_outcome' private method.

    DummyUser is an example of how to do this.
    """

    def __init__(self, type: str = "Base") -> None:
        """Init the object."""
        self.id: str = uuid4().hex
        self.type: str = type
        self.name: str = names.get_first_name()
        self.history: List[Optional[SimulationResult]] = []

    @abstractmethod
    def _get_simulation_outcome() -> str:
        """Implement this method in your own subclass.

        It should always return one of the possible SIMULATION_OUTCOMES
        """
        pass

    def complete_simulation(self, timestamp: datetime) -> None:
        """Complete a simulation and store it in the user's history."""
        outcome = self._get_simulation_outcome()
        assert (
            outcome in SIMULATION_OUTCOMES
        ), "The outcome from your logic is not a valid simulation outcome."

        self.history.append(
            SimulationResult(
                timestamp=datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S"),
                user_id=self.id,
                type=self.type,
                name=self.name,
                outcome=outcome,
            )
        )

    @property
    def simulations_completed(self) -> int:
        """Return amount of simulations user has completed."""
        return len(self.history)

    def __repr__(self) -> str:
        """Update the representation of a class object."""
        return (
            f"User(id={self.id}, name={self.name}, type={self.type} "
            f"simulations_completed={self.simulations_completed})"
        )


# TODO(Task 1): Implement your own user classes.
# All classes should be inherited from the above User class.
# See the DummyUser class below user for an example.
class DummyUser(User):
    """Dummy user class."""

    def __init__(self) -> None:
        """Init the object."""
        super(DummyUser, self).__init__(type="Dummy")

    def _get_simulation_outcome(self) -> str:
        """
        Implement a dummy simulation completion logic.

        Please write your own classes and make the logic smarter! :)
        """
        # In your solution, tweak this logic to mimick your chosen user types instead
        # of picking a random simulation outcome
        return random.choice(SIMULATION_OUTCOMES)

class SecuritySavvyUser(User):
    """User class for the security savvy users."""

    def __init__(self) -> None:
        """Init the object."""
        super(SecuritySavvyUser, self).__init__(type="SecuritySavvy")

    def _get_simulation_outcome(self) -> str:
        """
        A security savvy user really cares about cybersecurity.
        These people almost never miss a Hoxhunt training email
        and can respond to almost all of them accurately.
        """
        # 98% success, 1% miss, 1% fail
        return random.choices(SIMULATION_OUTCOMES, weights=(98, 1, 1))[0]

class EasilyDeceivedUser(User):
    """User class for the easily deceived users."""

    def __init__(self) -> None:
        """Init the object."""
        super(EasilyDeceivedUser, self).__init__(type="EasilyDeceivedUser")

    def _get_simulation_outcome(self) -> str:
        """
        An easily deceived user is easily tricked by Hoxhunt training
        emails. Some of them have already been victims of a real
        phishing attack. These are people who need to be helped quickly.
        """
        # 10% success, 10% miss, 80% fail
        return random.choices(SIMULATION_OUTCOMES, weights=(10, 10, 80))[0]

class AverageUser(User):
    """User class for the average users."""

    def __init__(self) -> None:
        """Init the object."""
        super(AverageUser, self).__init__(type="AverageUser")

    def _get_simulation_outcome(self) -> str:
        """
        An average user knows about phishing emails, but they do not
        take active part in cybersecurity training. Once they are up
        to it, they can detect most phishing emails. Sorry Hoxhunt devs,
        but these are the "average" people I've seen in my life.
        """
        # 35% success, 60% miss, 5% fail
        return random.choices(SIMULATION_OUTCOMES, weights=(35, 60, 5))[0]
