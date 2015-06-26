#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time

from .interfaces import GithubToBookRepoInterface
from .interfaces import GHSearchBookRepo
from .models import BookRepo
from .models import GitHubAuthToken

logger = logging.getLogger(__name__)

class CommitTree():
    """
    Takes a github3.py Tree and provides interfaces
    http://github3py.readthedocs.org/en/latest/git.html#github3.git.Tree
    """
    def __init__(self, tree):
        self.tree = tree
        self.dict = self.tree.as_dict()


class SearchAllRepos():
    def __init__(self):
        self.gh = GitHubAuthToken.get_token_or_login()
        self.check_ratelimit()

    def check_ratelimit(self):
        """ Check to see if we have enough ratelimits to continue, or if we
        should wait until timestamp
        Check on each run of run to see if we have >100 rate limits remaining
        if we do not, fetch the timestamp for when we can begin again """
        # TODO: break if not enough ratelimits remaining
        self.rates = self.gh.rate_limit()
        logger.debug("\tGitHub api allocation {0}".format(self.rates['resources']['core']['remaining']))
        logger.debug("\t{0} seconds until refresh".format(
            self.rates['resources']['core']['reset'] -
            int(time.time())
        ))

    def run(self):
        for repo in self.gh.repositories_by('gitenberg'):
            interface = GHSearchBookRepo(repo)
            interface.fulfill()
            logger.debug(interface)


class BookRepoGenerator():
    def __init__(self, start=1, count=10):
        self.gh = GitHubAuthToken.get_token_or_login()
        self.check_ratelimit()

    def get_bookrepo(self, pg_id):
        """ takes `pg_id` a PG book id
        searches github for that id
        returns github repository object """
        search_prefix = "user:GITenberg"
        search_id = "_{}".format(pg_id)
        search_str = " ".join([search_prefix, search_id])

        result_iterator = self.gh.search_repositories(search_str)
        result = result_iterator.next()  # fetching the first result from search
        logger.debug(result)
        return result.repository


    def run(self):
        for pg_id in self.todo:
            repo = self.get_bookrepo(pg_id)

            logger.debug("We have a repo from our iterator to digest")
            # Create an object that manages transfering data from a
            # Github3.Repo to a models.BookRepo
            interface = GithubToBookRepoInterface(repo)
            book_repo = interface.fulfill()
            logger.debug(interface)
            book_repo.save()

        self.run()


def get_latest_etag():
    # Not using this at the moment.
    latest_updated_book_repo = BookRepo.objects.order_by('-updated_at')[0]
    logger.debug("Latest updated book: {0}".format(latest_updated_book_repo))
    latest_etag = latest_updated_book_repo.etag
    return latest_etag
