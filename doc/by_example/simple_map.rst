**********
Simple Map
**********

This example demonstrates using the `Map`_ state
to run a `Task`_ over every member of a part of
the state machine data.

.. _Map: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-map-state.html
.. _Task: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-task-state.html

.. uml::

   start
   :ValidateAll ($.shipped);
   fork
      :Validate ($.shipped[0]);
   fork again
      :Validate ($.shipped[1]);
   fork again
      :Validate ($.shipped[2]);
   endfork
   stop

.. tabs::

   .. tab:: python

      .. literalinclude:: ../../examples/src/simple_map.py
         :language: python

   .. tab:: json

      .. literalinclude:: ../../examples/src/simple_map.json
         :language: json
