import unittest
from unittest.mock import MagicMock

from bot.utils import checks
from bot.utils.checks import InWhitelistCheckFailure
from tests.helpers import MockContext, MockRole


class ChecksTests(unittest.TestCase):
    """Tests the check functions defined in `bot.checks`."""

    def setUp(self):
        self.ctx = MockContext()

    def test_with_role_check_without_guild(self):
        """`with_role_check` returns `False` if `Context.guild` is None."""
        self.ctx.guild = None
        self.assertFalse(checks.with_role_check(self.ctx))

    def test_with_role_check_without_required_roles(self):
        """`with_role_check` returns `False` if `Context.author` lacks the required role."""
        self.ctx.author.roles = []
        self.assertFalse(checks.with_role_check(self.ctx))

    def test_with_role_check_with_guild_and_required_role(self):
        """`with_role_check` returns `True` if `Context.author` has the required role."""
        self.ctx.author.roles.append(MockRole(id=10))
        self.assertTrue(checks.with_role_check(self.ctx, 10))

    def test_without_role_check_without_guild(self):
        """`without_role_check` should return `False` when `Context.guild` is None."""
        self.ctx.guild = None
        self.assertFalse(checks.without_role_check(self.ctx))

    def test_without_role_check_returns_false_with_unwanted_role(self):
        """`without_role_check` returns `False` if `Context.author` has unwanted role."""
        role_id = 42
        self.ctx.author.roles.append(MockRole(id=role_id))
        self.assertFalse(checks.without_role_check(self.ctx, role_id))

    def test_without_role_check_returns_true_without_unwanted_role(self):
        """`without_role_check` returns `True` if `Context.author` does not have unwanted role."""
        role_id = 42
        self.ctx.author.roles.append(MockRole(id=role_id))
        self.assertTrue(checks.without_role_check(self.ctx, role_id + 10))

    def test_in_whitelist_check_correct_channel(self):
        """`in_whitelist_check` returns `True` if `Context.channel.id` is in the channel list."""
        channel_id = 3
        self.ctx.channel.id = channel_id
        self.assertTrue(checks.in_whitelist_check(self.ctx, [channel_id]))

    def test_in_whitelist_check_incorrect_channel(self):
        """`in_whitelist_check` raises InWhitelistCheckFailure if there's no channel match."""
        self.ctx.channel.id = 3
        with self.assertRaises(InWhitelistCheckFailure):
            checks.in_whitelist_check(self.ctx, [4])

    def test_in_whitelist_check_correct_category(self):
        """`in_whitelist_check` returns `True` if `Context.channel.category_id` is in the category list."""
        category_id = 3
        self.ctx.channel.category_id = category_id
        self.assertTrue(checks.in_whitelist_check(self.ctx, categories=[category_id]))

    def test_in_whitelist_check_incorrect_category(self):
        """`in_whitelist_check` raises InWhitelistCheckFailure if there's no category match."""
        self.ctx.channel.category_id = 3
        with self.assertRaises(InWhitelistCheckFailure):
            checks.in_whitelist_check(self.ctx, categories=[4])

    def test_in_whitelist_check_correct_role(self):
        """`in_whitelist_check` returns `True` if any of the `Context.author.roles` are in the roles list."""
        self.ctx.author.roles = (MagicMock(id=1), MagicMock(id=2))
        self.assertTrue(checks.in_whitelist_check(self.ctx, roles=[2, 6]))

    def test_in_whitelist_check_incorrect_role(self):
        """`in_whitelist_check` raises InWhitelistCheckFailure if there's no role match."""
        self.ctx.author.roles = (MagicMock(id=1), MagicMock(id=2))
        with self.assertRaises(InWhitelistCheckFailure):
            checks.in_whitelist_check(self.ctx, roles=[4])

    def test_in_whitelist_check_fail_silently(self):
        """`in_whitelist_check` test no exception raised if `fail_silently` is `True`"""
        self.assertFalse(checks.in_whitelist_check(self.ctx, roles=[2, 6], fail_silently=True))

    def test_in_whitelist_check_complex(self):
        """`in_whitelist_check` test with multiple parameters"""
        self.ctx.author.roles = (MagicMock(id=1), MagicMock(id=2))
        self.ctx.channel.category_id = 3
        self.ctx.channel.id = 5
        self.assertTrue(checks.in_whitelist_check(self.ctx, channels=[1], categories=[8], roles=[2]))
