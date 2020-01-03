************
Contributing
************

Where to Start?
===============

Want to help but you're not sure where to start?
Check our issues for ``help wanted`` or ``good first issue`` labels.

Nothing there? Examples and documentation are always a great place to start!
If you're confused about something, chances are a lot of other people are too.
If you can offer a clearer way of explaining something
or an example that highlights what you were trying to figure out,
that's a great way to contribute!

Development Workflow
--------------------

All development should start and end with the ``development`` branch.
We create all releases from the ``master`` branch,
but no human should ever touch that branch.

If you forget, don't worry!
``master`` should never be far behind ``development``
so you probably won't have any conflicts if you start from ``master``
and our army of bots will make sure that your pull requests end up in the right place. :)

Development Environment
=======================

All of our checks and tests can be run locally using ``tox``.
Just ``pipx install tox`` or ``pip install --user -r ci-requirements.txt`` to get set up.

Once you have ``tox`` installed,
check out the `config file <https://github.com/mattsb42/rhodes/tree/development/tox.ini>`_
for information on the various test environments.

For more information on ``tox``,
see the `tox docs <https://tox.readthedocs.io/en/latest/index.html>`_.

Submitting Changes
==================

When you're ready to submit your changes,
open up a pull request against the ``development`` branch.

Operations
==========

Ok, so that's cool and all, but how does all of that work???

We use a variety of GitHub Apps and Action workflows to manage this repo:

Repo Management
---------------

* `settings <https://github.com/mattsb42/rhodes/tree/development/.github/settings.yml>`_ :
  We use `probot settings <https://probot.github.io/apps/settings/>`_ to manage most repository settings.
* `branch-switcher <https://github.com/mattsb42/rhodes/tree/development/.github/branch-switcher.yml>`_ :
  We use `probot branch switcher <https://probot.github.io/apps/branch-switcher/>`_ to make sure that
  all pull requests end up with the correct target.
* `apply-pr-labels <https://github.com/mattsb42/rhodes/tree/development/.github/workflows/apply-pr-labels.yaml>`_
  Some of our automation relies on labels being applied to pull requests.
  This workflow takes care of applying those labels.
* `promote <https://github.com/mattsb42/rhodes/tree/development/.github/workflows/promote.yaml>`_
  Every time a pull request is merged into ``development``,
  this workflow automatically creates a pull request promoting those changes to ``master``.
  If a pull request already exists, it will simply be updated as you would expect.
* `automerge <https://github.com/mattsb42/rhodes/tree/development/.github/workflows/automerge.yaml>`_
  Our branch protection rules define our requirements for a pull request to be accepted.
  If those requirements are met, this workflow merges those changes.
* `publish <https://github.com/mattsb42/rhodes/tree/development/.github/workflows/publish.yaml>`_
  Libraries are not terribly useful if they are not published to the appropriate package indexes.
  This workflow takes any published GitHub releases, packages them, and publishes them to PyPI.

Pull Requests and Testing
-------------------------

* `static-analysis <https://github.com/mattsb42/rhodes/tree/development/.github/workflows/static-analysis.yaml>`_ :
  We check all pull requests with a variety of static analysis tools
  to ensure the safety, consistency, and quality of our codebase.
  This also means that computers (not humans!) will complain if you don't have formatting/etc quite right. :)
* `local-tests <https://github.com/mattsb42/rhodes/tree/development/.github/workflows/local-tests.yaml>`_ :
  We run our local (unit and functional) tests on every pull request.
* `integration-tests <https://github.com/mattsb42/rhodes/tree/development/.github/workflows/integration-tests.yaml>`_ :
  Because they require credentials that are difficult to share,
  we only run our integration tests on promotion pull requests from ``development`` to ``master``.
  If you want to run these tests for yourself locally, though, you can!
  Like all of our other tests, our integration tests are all managed through ``tox``.
