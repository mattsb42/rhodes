######
Rhodes
######

.. image:: https://img.shields.io/pypi/v/rhodes.svg
   :target: https://pypi.python.org/pypi/rhodes
   :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/rhodes.svg
   :target: https://pypi.python.org/pypi/rhodes
   :alt: Supported Python Versions

.. image:: https://img.shields.io/badge/code_style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code style: black

.. image:: https://readthedocs.org/projects/rhodes/badge/
   :target: https://rhodes.readthedocs.io/
   :alt: Documentation Status

.. image:: https://travis-ci.org/mattsb42/rhodes.svg?branch=master
   :target: https://travis-ci.org/mattsb42/rhodes
   :alt: Travis CI Test Status


Rhodes is a library designed to make creating `AWS Step Functions`_ state machines
simple and less error prone.
Rhodes is designed to integrate tightly with `Troposphere`_ to provide a seamless experience
for building state machines in your `AWS CloudFormation`_ templates.

For some examples of what this looks like, check out the `examples`_.

.. important::

    This project is a work in progress and is not ready for production use.
    The low-level API is unlikely to change,
    but the higher-level helper APIs might as I find better patterns.


.. _AWS Step Functions: https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html
.. _AWS CloudFormation: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html
.. _Troposphere: https://troposphere.readthedocs.io
.. _examples: https://github.com/mattsb42/rhodes/tree/master/examples/src
