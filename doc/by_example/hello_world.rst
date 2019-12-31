***********
Hello World
***********

This example shows a very simple state machine,
with a single state that invokes a Lambda Function `Task`_ state.

The ``troposphere`` version demonstrates how
`Troposphere`_ objects can be passed as references
rather than having to provide a string value.

.. _Task: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-task-state.html
.. _Troposphere: https://troposphere.readthedocs.io

.. uml::

   start
   :Hello World;
   stop

.. tabs::

   .. tab:: basic

      .. tabs::

         .. tab:: python

            .. literalinclude:: ../../examples/src/hello_world.py
               :language: python

         .. tab:: json

            .. literalinclude:: ../../examples/src/hello_world.json
               :language: json

   .. tab:: troposphere

      .. tabs::

         .. tab:: python

            .. literalinclude:: ../../examples/src/hello_world_troposphere_direct.py
               :language: python

         .. tab:: json

            .. literalinclude:: ../../examples/src/hello_world_troposphere_direct.json
               :language: json
