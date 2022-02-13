from collections import Counter
from datetime import datetime, timedelta
from typing import List

import pandas as pd

from config import TABLE_COLUMNS
from user import DummyUser, SecuritySavvyUser, EasilyDeceivedUser, AverageUser, User

import random


class Organization:
    """Class for a hypothetical customer organization."""

    def __init__(self, n_users: int, n_simulations: int, training_interval_days: int) -> None:
        """Init the object."""
        self.n_users = n_users
        self.n_simulations = n_simulations
        self.training_interval_days = training_interval_days
        self.users = self._populate_organization()
        assert all(
            issubclass(type(user), User) for user in self.users
        ), "Please create your users as subclasses of the abstract User class."

    def _populate_organization(self) -> List:
        # TODO(Task 2):
        # 1. import your own user types created in Task 1 from the user.py module
        # 2. change this to populate the organization with your own user types
        # 3. change the distribution from uniform to something a bit more realistic
        """
        My organization will be 70% AverageUser, 20% SecuritySavvyUser,
        5% EasilyDeceivedUser, and 5% DummyUser.
        """
        users = []
        user_type_list = ["Average", "SecuritySavvy", "EasilyDeceived", "Dummy"]
        for i in range(self.n_users):
            # choose user type according to the distribution defined above
            random_user_type = random.choices(user_type_list, weights=(70, 20, 5, 5), k=1)
            if random_user_type == "Average":
                users.append(AverageUser())
            elif random_user_type == "SecuritySavvy":
                users.append(SecuritySavvyUser())
            elif random_user_type == "EasilyDeceived":
                users.append(EasilyDeceivedUser())
            else:
                users.append(DummyUser())
        return users

    def do_training(self) -> None:
        """Train organization with Hoxhunt simulations."""
        for i in range(self.n_simulations):
            timestamp = datetime.now() + timedelta(days=self.training_interval_days * i)
            for user in self.users:
                user.complete_simulation(timestamp=timestamp)

    def get_result(self) -> pd.DataFrame:
        """Fetch the results of training."""
        org_history = []
        for user in self.users:
            org_history += user.history
        return pd.DataFrame(org_history, columns=TABLE_COLUMNS)

    def __repr__(self) -> str:
        """Update the representation of a class object."""
        user_names = [user.name for user in self.users]
        name, amount = Counter(user_names).most_common(1)[0]
        return (
            f"Organization(n_users={self.n_users}, n_simulations={self.n_simulations}, "
            f"training_interval_days={self.training_interval_days}, "
            f"random_fact=The most common name in your organization is {name}, "
            f"there are {amount} of them... I wonder who's the best performer 🤔)"
        )
