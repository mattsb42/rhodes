*************
Simple Choice
*************

This example shows a simple state machine containing
a single `Choice`_ state that maps to
a small number of terminal states.

The ``enums`` version demonstrates how Enum members
can be used rather than just primitive values.

.. _Choice: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-choice-state.html

.. uml::

   start

   if ($.value == "A") then (yes)
      :ResultA;
      stop
   else if ($.value == "B") then (yes)
      :ResultB1;
      :ResultB2;
      stop
   else
      #red:Unknown;
      end
   endif


.. tabs::

   .. tab:: basic

      .. tabs::

         .. tab:: python

            .. literalinclude:: ../../examples/src/simple_choice.py
               :language: python

         .. tab:: json

            .. literalinclude:: ../../examples/src/simple_choice.json
               :language: json

   .. tab:: enums

      .. tabs::

         .. tab:: python

            .. literalinclude:: ../../examples/src/simple_choice_with_enums.py
               :language: python

         .. tab:: json

            .. literalinclude:: ../../examples/src/simple_choice_with_enums.json
               :language: json
