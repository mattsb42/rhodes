***************
Simple Parallel
***************

This example demonstrates creating a simple state machine
containing a single `Parallel`_ state that runs some `Task`_ states.

.. _Parallel: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-parallel-state.html
.. _Task: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-task-state.html

.. uml::

   start
   fork
      :LookupAddress;
   fork again
      :LookupPhone;
   endfork
   stop

.. tabs::

   .. tab:: python

      .. literalinclude:: ../../examples/src/simple_parallel.py
         :language: python

   .. tab:: json

      .. literalinclude:: ../../examples/src/simple_parallel.json
         :language: json
