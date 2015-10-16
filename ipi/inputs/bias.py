"""Creates objects that compose and apply forces."""

# This file is part of i-PI.
# i-PI Copyright (C) 2014-2015 i-PI developers
# See the "licenses" directory for full license information.


from copy import copy

from ipi.engine.bias import *
from ipi.utils.inputvalue import *


__all__ = ['InputBias', 'InputBiasComponent']


class InputBiasComponent(InputValue):
   """BiasComponent input class.

   Uses the forcefield object whose name is specified as the value of the
   field (matching one of the forcefields defined in the simulation tag)
   to compute one component of the force acting on the ring polymer.


   Attributes:
      nbeads: The number of beads that the forcefield will be evaluated on.
      weight: A scaling factor for the contribution from this forcefield.
      name: The name of the forcefield.
   """

   attribs = { "nbeads" : ( InputAttribute, { "dtype"   : int,
                                         "default" : 0,
                                         "help"    : "If the forcefield is to be evaluated on a contracted ring polymer, this gives the number of beads that are used. If not specified, the forcefield will be evaluated on the full ring polymer." } ),
               "weight" : ( InputAttribute, { "dtype"   : float,
                                         "default" : 1.0,
                                         "help"    : "A scaling factor for this forcefield, to be applied before adding the force calculated by this forcefield to the total force." } ),
               "name" : ( InputAttribute, { "dtype" : str,
                                          "default" : "",
                                          "help" : "An optional name to refer to this force component." } )
            }

   default_help = "The class that deals with how each forcefield contributes to the overall potential, force and virial calculation."
   default_label = "FORCECOMPONENT"

   def __init__(self, help=None, dimension=None, units=None, default=None, dtype=None):
      """Initializes InputBiasComponent.

      Just calls the parent initialization function with appropriate arguments.
      """

      super(InputBiasComponent,self).__init__(dtype=str, dimension=dimension, default=default, help=help)

   def store(self, forceb):
      """Takes a BiasComponent instance and stores a minimal
      representation of it.

      Args:
         forceb: A BiasComponent object.
      """

      super(InputBiasComponent,self).store(forceb.ffield)
      self.nbeads.store(forceb.nbeads)
      self.weight.store(forceb.weight)
      self.name.store(forceb.name)

   def fetch(self):
      """Creates a BiasComponent object.

      Returns:
         A BiasComponent object.
      """

      val=super(InputBiasComponent,self).fetch()
      return BiasComponent(ffield=val, nbeads=self.nbeads.fetch(), weight=self.weight.fetch(), name=self.name.fetch())

   def check(self):
      """Checks for optional parameters."""

      super(InputBiasComponent,self).check()
      if self.nbeads.fetch() < 0:
         raise ValueError("The forces must be evaluated over a positive number of beads.")


class InputBias(Input):
   """Deals with creating all the forcefield objects required in the
   simulation.

   Dynamic fields:
      socket: Socket object to create the server socket.
   """

   #At the moment only socket driver codes implemented, other types
   #could be used in principle
   dynamic = {  "force" : (InputBiasComponent, { "help" : InputBiasComponent.default_help } )
            }

   default_help = "Deals with creating all the necessary forcefield objects."
   default_label = "FORCES"

   def fetch(self):
      """Returns a list of the output objects included in this dynamic
      container.

      Returns:
         A list of tuples, with each tuple being of the form ('type', 'object'),
         where 'type' is the type of forcefield, and 'object' is a
      """

      super(InputBias, self).fetch()
      flist = [ f.fetch() for (n, f) in self.extra ]
      return flist

   def store(self, flist):
      """Stores a list of the output objects, creating a sequence of
      dynamic containers.

      Args:
         flist: A list of tuples, with each tuple being of the form
         ('type', 'object') where 'type' is the type of forcefield
         and 'object' is a forcefield object of that type.
      """

      super(InputBias, self).store()
      self.extra = []

      for el in flist:
         iff = InputBiasComponent()
         iff.store(el)
         self.extra.append(("force", iff))
