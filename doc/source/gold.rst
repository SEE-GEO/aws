Setup
=====

We will make use of the gold servers for the simulations. The addresses
of the servers are

.. code-block:: none

  gold<i>.rss.chalmers.se

for i in [2, 3, 4, 5, 6, 7]. Each server has 4 cores, so we can run 24
simulations in parallel. To run simulations in parallel distributed on the six
machines we are using the `IPyParallel
<https://ipyparallel.readthedocs.io/en/latest/index.html>`_ package.

Overview
--------

The AWS simulations require only minimal interaction with the IPyParallel
package but it is still good to have an overview over the general computational
architecture to understand which steps are required to start the simulations.

The IPyParallel infrastructure consists of a controller and a hub running on the
local machine and several engines running on the remote machines (in our case
the gold server). The hub manages communication between engines and controller
but should not be of further concern for us. Our main interaction will be with
the controller. We will use a Python script running on the local machine to the controller
and execute tasks on the remote engines.

Running simulations on the gold cluster thus always involves two steps:

1. Start the IPyParallel controller hub and engines.
2. Run a Python script to connect to the controller and execute code
   on the engines.

Preparing access to the remote machines
---------------------------------------

For IPyParallel to be able to connect to the remote machines, it needs to be
able to ssh into them without a password. For this you need to enable ssh
key-based authentication, by copying your public key to the machines.

Generating an SSH key
^^^^^^^^^^^^^^^^^^^^^

If you are unsure whether you already have a SSH key, follow the steps described
`here
<https://help.github.com/en/enterprise/2.17/user/github/authenticating-to-github/checking-for-existing-ssh-keys>`_
and `here
<https://help.github.com/en/enterprise/2.17/user/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_
to find out whether you have already generated a key and if not generate a new one.
Keep in mind to leave the pass phrase empty in case you are generating a new key.

Copying you key to the gold machines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To copy  the ssh key to the gold machines run

.. code-block:: none

   ssh-copy-id <username>@gold2.rss.chalmers.se

Since the machines run on a shared file system it should be sufficient to copy the
key to only one of them.

You should now be able to login to any of the gold machines without entering
your password.

Copying the IPyParallel profile
-------------------------------
..
The information which tells IPyParallel to which machines to connect is stored
in a profile. I have setup a :code:`gold` profile to use to connect to the gold
servers. To use it, you will need to copy the profile folder to your local
:code:`~/.ipython` directory:

.. code-block:: none

    cp -r /home/simonpf/.ipython/profile_gold ~/.ipython



Starting the controller and engines
-----------------------------------

To start the IPyParallel hub, controller and engines, we use the :code:`ipcluster`
command.

.. code-block:: none

   ipcluster start --profile=gold --ip=* --debug
  
The :code:`--debug` flag is not strictly required and produces quite a lot of output
but especially in the beginning it can be helpful to see what's happening. Since
you want to keep this process alive as long as the simulations are running it
is a good idea to run in a :code:`tmux` session.

It can be convenient to define an alias to start the IPyParallel cluster in tmux:

.. code-block:: none

  alias start_gold_cluster="tmux new-session -d -s gold_cluster 'ipcluster start --profile=gold --ip=* --debug'


