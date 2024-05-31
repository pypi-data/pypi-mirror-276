*****
Usage
*****

Who is this for
===============

This particular package is most likely to be useful for people either
developing algorithms for techniques for KEPs, or setting kep_solver for use
within an organisation with specific requirements. A sample web interface is
viewable at https://kep-web.optimalmatching.com, and the code for said
interface is at https://gitlab.com/wpettersson/kep_web.

Installing
==========

This package is available via pip, and requires Python 3.9 at least. To install
it, I recommend using a Python virtual environment (see `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ for an easy-to-use introduction) and then running ``pip install kep_solver``

Reading and inspecting instances
================================

File IO functionality is available in the :doc:`kep_solver.fileio` module. The
following code should read in any supported file format.
::

    from kep_solver.fileio import read_file
    instance = read_file("instance.json")

Instances can be analysed for a number of properties, as can the Donor and
Recipient entities they contain. These are documented in :doc:`kep_solver.entities`.
::

    print(f"This instance has {len(instance.recipients())} recipients")

Analysing the compatibility graph
=================================

The underlying compatibility graph can be accessed by creating a
:ref:`compatibility graph` object as follows. Specifics are documented in
:doc:`kep_solver.graph`.
::

    graph = CompatibilityGraph(instance)
    cycles = graph.findCycles(maxCycleLength)
    chains = graph.findChains(maxChainLength)
    print(f"There are {len(cycles)} cycles and {len(chains)} chains")


Using different models
======================

Different IP models can be used for solving KEP instances, and kep\_solver currently supports two such models: the :class:`kep_solver.models.CycleAndChainFormulation` [Abraham07]_ [Roth07]_ and :class:`kep_solver.models.PICEF` [Dickerson16]_. PICEF is currently significantly faster for longer chain lengths, but not all objectives are able to be used with PICEF. As such, the cycle and chain formulation is still the default. An example using PICEF is given below.
::

    from kep_solver.models import PICEF
    model = PICEF(
                  instance,
                  objectives,
                  maxChainLength=chain_length,
                  maxCycleLength=cycle_length,
                 )
    solution, model_times, numSols = model.solve()

You can also create a :class:`kep_solver.pool.Pool` that uses :class:`kep_solver.models.PICEF` by default.
::

    from kep_solver.pool import Pool
    from kep_solver.model import TransplantCount
    pool = Pool(
                objectives=[TransplantCount()],
                maxCycleLength=3,
                maxChainLength=6,
                description="My PICEF Pool",
                model=PICEF,
               )
    solution, model = pool.solve_single(instance)


As mentioned above, not all objectives are compatible with PICEF. If you see an exception stating that "Edge value is not defined for this objective", then this indicates that the objective cannot be used with PICEF as the model.
