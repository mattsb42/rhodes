***********
Three Tasks
***********

This example demonstrates a simple state machine
composes of three serially executed `Task`_ states
with no branching.

.. _Task: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-task-state.html


.. uml::

   start
   :TaskOne;
   :TaskTwo;
   :TaskThree;
   stop

.. tabs::

   .. tab:: python

      .. literalinclude:: ../../examples/src/three_tasks.py
         :language: python

   .. tab:: json

      .. literalinclude:: ../../examples/src/three_tasks.json
         :language: json
