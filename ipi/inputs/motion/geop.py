"""Deals with creating the ensembles class.

Copyright (C) 2013, Joshua More and Michele Ceriotti

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http.//www.gnu.org/licenses/>.

Inputs created by Michele Ceriotti and Benjamin Helfrecht, 2015

Classes:
   InputGeop: Deals with creating the Geop object from a file, and
      writing the checkpoints.
"""

import numpy as np
import ipi.engine.initializer
from ipi.engine.motion import *
from ipi.utils.inputvalue import *
from ipi.inputs.thermostats import *
from ipi.inputs.initializer import *
from ipi.utils.units import *

__all__ = ['InputGeop']

class InputGeop(InputDictionary):
    """Geometry optimization options.

    Contains options related with geometry optimization, such as method,
    thresholds, linear search strategy, etc.

    """

    attribs={"mode"  : (InputAttribute, {"dtype"   : str, "default": "lbfgs",
                                    "help"    : "The geometry optimization algorithm to be used",
                                    "options" : ['sd', 'cg', 'bfgs', 'bfgstrm','lbfgs']}) }
    
    # options of the method (mostly tolerances)
    fields = { "ls_options" : ( InputDictionary, {"dtype" : [float, int, float, float],
                              "help" : """"Options for line search methods. Includes:
                              tolerance: stopping tolerance for the search,
                              iter: the maximum number of iterations,
                              step: initial step for bracketing,
                              adaptive: whether to update initial step.
                              """,
                              "options"  : ["tolerance", "iter", "step", "adaptive"],
                              "default"  : [1e-6, 100, 1e-3, 1.0],
                              "dimension": ["energy", "undefined", "length", "undefined" ] }),
                "tolerances" : ( InputDictionary, {"dtype" : float,
                              "options"  : [ "energy", "force", "position" ],
                              "default"  : [ 1e-8, 1e-8, 1e-8 ],
                              "help"     : "Convergence criteria for optimization.",
                              "dimension": [ "energy", "force", "length" ] }),     
                "biggest_step": (InputValue, {"dtype" : float,
                              "default"  : 100.0,
                              "help"     : "The maximum step size for (L)-BFGS line minimizations."}),
                "corrections_lbfgs" : (InputValue, {"dtype" : int,
                              "default"  : 5,
                              "help"     : "The number of past vectors to store for L-BFGS."}),
                # re-start parameters, estimate hessian, etc.
                "old_pos": (InputArray, {"dtype" : float,
                              "default"  : input_default(factory=np.zeros, args = (0,)),
                              "help"     : "The previous positions in an optimization step.",
                              "dimension": "length"}),
                "old_pot": (InputArray, {"dtype" : float,
                              "default"  : input_default(factory=np.zeros, args = (0,)),
                              "help"     : "The previous potential energy in an optimization step.",
                              "dimension": "energy"}),
                "old_force": (InputArray, {"dtype" : float,
                              "default"  : input_default(factory=np.zeros, args = (0,)),
                              "help"     : "The previous force in an optimization step.",
                              "dimension": "force"}),
                "old_direction": (InputArray, {"dtype" : float,
                              "default"  : input_default(factory=np.zeros, args = (0,)),
                              "help"     : "The previous direction in a CG or SD optimization."}),
                "invhessian_bfgs" : (InputArray, {"dtype" : float,
                              "default"  : input_default(factory=np.eye, args = (0,)),
                              "help"     : "Approximate inverse Hessian for BFGS, if known."}),
                "hessian_trm" : (InputArray, {"dtype" : float,
                              "default"  : input_default(factory=np.eye, args = (0,)),
                              "help"     : "Approximate Hessian for trm, if known."}),
                "tr_trm": (InputArray, {"dtype" : float,
                               "default"  : input_default(factory=np.zeros, args = (0,)),
                               "help"     : "The trust radius in trm.",
                               "dimension": "length"}),
                "qlist_lbfgs" : (InputArray, {"dtype" : float,
                              "default"  : input_default(factory=np.zeros, args = (0,)),
                              "help"     : "List of previous position differences for L-BFGS, if known."}),
                "glist_lbfgs" : (InputArray, {"dtype" : float,
                              "default"  : input_default(factory=np.zeros, args = (0,)),
                              "help"     : "List of previous gradient differences for L-BFGS, if known."})
                }

    dynamic = {  }

    default_help = "TODO EXPLAIN WHAT THIS IS"
    default_label = "GEOP"

    def store(self, geop):
        if geop == {}: 
            return


        self.mode.store(geop.mode)
        self.tolerances.store(geop.tolerances)

        if geop.mode == "bfgs":
              self.old_direction.store(geop.old_d)
              self.invhessian_bfgs.store(geop.invhessian)
              self.biggest_step.store(geop.big_step)
        elif geop.mode == "bfgstrm":
              self.hessian_trm.store(geop.hessian)
              self.tr_trm.store(geop.tr)
              self.biggest_step.store(geop.big_step)
        elif geop.mode == "lbfgs":
              self.qlist_lbfgs.store(geop.qlist)
              self.glist_lbfgs.store(geop.glist)
              self.corrections_lbfgs.store(geop.corrections)
              self.biggest_step.store(geop.big_step)
              self.old_force.store(geop.old_f)
        elif geop.mode == "sd":
              self.ls_options.store(geop.ls_options)
        elif geop.mode == "cg":
              self.old_direction.store(geop.old_d)
              self.ls_options.store(geop.ls_options)
              self.old_force.store(geop.old_f)





    def fetch(self):
        rv = super(InputGeop,self).fetch()
        rv["mode"] = self.mode.fetch()
        return rv
