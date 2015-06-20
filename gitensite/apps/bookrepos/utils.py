#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
import logging
import time

from github3 import login

from gitensite.apps.bookrepos.models import GitHubAuthToken
# from .forms import BookRepoForm
# from .models import BookRepo
from .interfaces import GithubToBookRepoInterface
from .models import BookRepo

logger = logging.getLogger(__name__)

class GitHubOrg(object):
    """docstring for GitHubOrg"""
    def __init__(self, arg):
        super(GitHubOrg, self).__init__()
        self.arg = arg

class CommitTree():
    """
    Takes a github3.py Tree and provides interfaces
    http://github3py.readthedocs.org/en/latest/git.html#github3.git.Tree
    """
    def __init__(self, tree):
        self.tree = tree
        self.dict = self.tree.as_dict()

class BookRepoGenerator():
    def __init__(self):
        self.gh = self.get_or_create_auth()
        self.check_ratelimit()
        self.org = self.gh.organization('gitenberg')

    def check_ratelimit(self):
        # Check to see if we have enough ratelimits to continue, or if we
        # should wait until timestamp
        self.rates = self.gh.rate_limit()
        logger.debug("\tGitHub api allocation {0}".format(self.rates['resources']['core']['remaining']))
        logger.debug("\t{0} seconds until refresh".format(
            self.rates['resources']['core']['reset'] -
            int(time.time())
        ))
        # if rates['resources']['core']['remaining'] < 10000:
        #     # TODO: wait until
        #     reset = rates['resources']['core']['reset']
        #     now = calendar.timegm(datetime.datetime.utcnow())
        #     import ipdb; ipdb.set_trace()  # XXX BREAKPOINT

    def get_or_create_auth(self):
        try:
            gh_token = GitHubAuthToken.objects.get(id=1)
            gh = login(token=gh_token.token)
            logger.debug("Recovered gh token from db, used that to log in.")
        except GitHubAuthToken.DoesNotExist:
            self.stdout.write('GitHub Token not found, try running make_github_token')
            self.stdout.write('I need to log into your account:')

            gh = login(raw_input("username:"), password=getpass.getpass())

        return gh

    def run(self, save=True, max_count=100):

        # Find the latest BookRepo we updated in the db, and get its etag
        latest_updated_book_repo = BookRepo.objects.order_by('-updated_at')[0]
        logger.debug("Latest updated book: {0}".format(latest_updated_book_repo))
        latest_etag = latest_updated_book_repo.etag

        """ Bad news,
        etag doesn't paginate each `number` bounded request to org.repositories()
        so we don't need to check etag in the db.
        """
        # https://developer.github.com/v3/#rate-limiting
        # Check on each run of run to see if we have >100 rate limits remaining
        # if we do not, fetch the timestamp for when we can begin again

        # if not latest_etag:
        #     logger.debug("Latest etag: {0}. providing that to org.repositories()".format(latest_etag))
        #     repo_iterator = self.org.repositories(etag=latest_etag)
        # else:
            # iterate over
            # logger.debug("we have an etag to iterate from with {0}".format(repo_iterator))

        repo_iterator = self.org.repositories()
        for repo in repo_iterator:

            logger.debug("We have a repo from our iterator to digest")
            self.etag = repo_iterator.etag
            # TODO: fetch existing book as update form

            # Create an object that manages transfering data from a
            # Github3.Repo to a models.BookRepo
            interface = GithubToBookRepoInterface(repo, self.etag)
            book_repo = interface.fulfill()
            print interface
            book_repo.save()

        self.run()
