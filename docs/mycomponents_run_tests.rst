Run All Tests
=============

Now you are ready to run the tests for components you just built as well as
the components in the ``insights_examples`` directory...

.. code-block:: shell

   (env)[userone@hostone ~]$ cd ~/work/insights-core-tutorials
   (env)[userone@hostone insights-core-tutorials]$ pytest

This will run the tests for the components you created in ``mycomponents`` as well as the components
provided in the ``insights_examples`` directory.

If you would like to run only the tests in your newly created ``mycomponents`` directory run
the following...

.. code-block:: shell

   (env)[userone@hostone ~]$ cd ~/work/insights-core-tutorials
   (env)[userone@hostone insights-core-tutorials]$ pytest -k mycomponents
