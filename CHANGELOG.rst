*********
Changelog
*********

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
