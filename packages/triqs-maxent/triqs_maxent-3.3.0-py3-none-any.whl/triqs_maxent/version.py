################################################################################
#
# TRIQS: a Toolbox for Research in Interacting Quantum Systems
#
# Copyright (C) 2016-2018, N. Wentzell
# Copyright (C) 2018-2019, Simons Foundation
#   author: N. Wentzell
#
# TRIQS is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# TRIQS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# TRIQS. If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

version = "3.3.0"
triqs_hash = "d7868de5b996d2fc756f53ec924b2ce0c2a163db"
triqs_maxent_hash = "9231875d4382c81854dd4e98170d792c75ab08e8"

def show_version():
  print("\nYou are using triqs_maxent version %s\n"%version)

def show_git_hash():
  print("\nYou are using triqs_maxent git hash %s based on triqs git hash %s\n"%("9231875d4382c81854dd4e98170d792c75ab08e8", triqs_hash))
