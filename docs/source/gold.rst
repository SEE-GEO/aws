Setup for computations
======================

We will make use of the gold servers for the simulations. The addresses
of the servers are

.. code::

  gold<i>.rss.chalmers.se

for i in [2, 3, 4, 5, 6, 7]. Each server has 4 cores, so we can run 24
simulations in parallel. To run simulations in parallel distributed on the six
machines we are using the (`IPyParallel
<https://ipyparallel.readthedocs.io/en/latest/index.html>`_) package.

Overview
--------

The IPyParallel infrastructure consists of a controller and a hub running on the
local machine and several engines running on the remote machines (in our case
the gold server). The hub manages communication between engines and controller
and should not be of concern for us. To execute code on the engines, a Python
script running on the local machine can connect to the controller and send tasks
for execution on the remote engines.

The AWS simulations will not require direct interaction with the IPyParallel
controller but it may be good to have an overview over the general computational
setup.

Preparing access to the remote machines
---------------------------------------

For IPyParallel to be able to connect to the remote machines, it needs to be
able ssh into them without entering a password. For this you need to enable
ssh key-based authentication, by copying your public key to any of the machines.

Generating an SSH key
^^^^^^^^^^^^^^^^^^^^^
If you are unsure whether you already have a SSH key, follow the steps described
`here
<https://help.github.com/en/enterprise/2.17/user/github/authenticating-to-github/checking-for-existing-ssh-keys>_`
and `here
<https://help.github.com/en/enterprise/2.17/user/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>_`
to find out whether you have already generated a key and if not generate a new one.
Keep in mind to leave the pass phrase empty in case you are generating a new key.

Copying you key to the gold machines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To copy  the ssh key to the gold machines run

.. code::

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
servers. To use it, you will need to copy the profile file to your local
:code:`~/.ipython` directory:

.. code::

    cp -r /home/simonpf/.ipython/profile_gold ~/.ipython



Starting the controller and engines
-----------------------------------

To start the IPyParallel hub, controller and engines, we use the :code:`ipcluster`
command.

.. code::

   ipcluster start --profile=gold --ip=* --debug
  
The :code:`--debug` flag is not strictly required and produces quite a lot of output
but especially in the beginning it can be helpful to see what's happening. Since
you want to keep this process alive as long as the simulations are running it
is a good idea to run in a :code:`tmux` session.

It can be convenient to define an alias to start the IPyParallel cluster in tmux:

.. code::

  alias start_gold_cluster="tmux new-session -d -s gold_cluster 'ipcluster start --profile=gold --ip=* --debug'


