*********
Changelog
*********

0.5.4 -- 2020-01-01
===================

* Minor cleanup.
* Lots of docs updates.

0.5.3 -- 2019-12-16
===================

bugfixes
--------

* Fix ``Pass`` type stub to include ``Result``.
  `#61 <https://github.com/mattsb42/rhodes/issues/61>`_
* Fix ``ContextPath`` to allow indexing inside of ``Map.Item.Value``.
  `#62 <https://github.com/mattsb42/rhodes/issues/62>`_

0.5.2 -- 2019-12-10
===================

* Fixed incorrect kw-only split for ``AwsStepFunctions`` type signature.
  `#55 <https://github.com/mattsb42/rhodes/issues/55>`_
* Fixed too-strict type restrictions.
  `#54 <https://github.com/mattsb42/rhodes/issues/54>`_
  `#56 <https://github.com/mattsb42/rhodes/issues/56>`_


0.5.1 -- 2019-12-09
===================

* Fixed ``setup.py`` to package type stubs.

0.5.0 -- 2019-12-09
===================

* **BREAKING CHANGE:** ``AwsLambda`` now requires ``Payload`` to be a ``Parameters`` instance.
* ``AwsStepFunctions`` no longer allows the definition of an execution name.

   * NOTE: This is only *not* a breaking change because ``AwsStepFunctions`` was fundamentally broken before.

* **BREAKING CHANGE:** ``AwsBatch`` now required ``Parameters`` to be a ``Parameters`` instance.
* **BREAKING CHANGE:** All parameters for ``State`` classes other than ``title`` are now keyword-only.
  `#47 <https://github.com/mattsb42/rhodes/issues/47>`_
* **BREAKING CHANGE:** Most parameters are now keyword-only.
  `#47 <https://github.com/mattsb42/rhodes/issues/47>`_
* Added explicit local defaults for common State fields:
  `#50 <https://github.com/mattsb42/rhodes/issues/50>`_

    * ``InputPath``
    * ``OutputPath``
    * ``ResultPath``

features
--------

* Add ``State.promote`` method for states that support ``ResultPath``.
  `#32 <https://github.com/mattsb42/rhodes/issues/32>`_

bugfixes
--------

* Fixed ``AwsStepFunctions`` parameters names.
  `#45 <https://github.com/mattsb42/rhodes/issues/45>`_

0.4.0 -- 2019-12-03
===================

* **BREAKING CHANGE:** Renamed ``State.name`` to ``State.title``
  `#38 <https://github.com/mattsb42/rhodes/issues/38>`_

0.3.1 -- 2019-11-24
===================

* Add support for "comparing" VariablePath instances to Enum members
  `#29 <https://github.com/mattsb42/rhodes/pull/29>`_
* Add support for troposphere objects as resource values
  `#33 <https://github.com/mattsb42/rhodes/pull/33>`_
* Initial implementation of context object helper
  `#34 <https://github.com/mattsb42/rhodes/pull/34>`_

0.3.0 -- 2019-11-19
===================

* Add preliminary service integration helpers
  `#27 <https://github.com/mattsb42/rhodes/pull/27>`_

0.2.1 -- 2019-11-18
===================

* Updated docs and added examples.

0.2.0 -- 2019-11-17
===================

* **BREAKING CHANGE:** Renamed ``ChoiceRule.then_`` to ``ChoiceRule.then``
  `#12 <https://github.com/mattsb42/rhodes/issues/12>`_
* **BREAKING CHANGE:** Reworked ``Variable`` into ``JsonPath`` and ``VariablePath``
  `#3 <https://github.com/mattsb42/rhodes/issues/3>`_
  `#10 <https://github.com/mattsb42/rhodes/issues/10>`_
  `#11 <https://github.com/mattsb42/rhodes/issues/11>`_

0.1.0 -- 2019-11-14
===================

Initial alpha release.

Includes:

* Basic state/machine construction
* Improved ergonomics for state machines.
* Improved ergonomics for Choice, Task, and Parallel states.
