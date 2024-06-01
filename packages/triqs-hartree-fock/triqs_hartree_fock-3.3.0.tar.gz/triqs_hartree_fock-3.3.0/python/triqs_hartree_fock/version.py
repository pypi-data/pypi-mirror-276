# Copyright (c) 2022 Simons Foundation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You may obtain a copy of the License at
#     https:#www.gnu.org/licenses/gpl-3.0.txt
#
# Authors: Jonathan Karp, Alexander Hampel, Nils Wentzell, Hugo U. R. Strand, Olivier Parcollet

version = "3.3.0"
triqs_hash = "d7868de5b996d2fc756f53ec924b2ce0c2a163db"
triqs_hartree_fock_hash = "6e6ea1330bb3712528ea1415e3df61591d7eb021"

def show_version():
  print("\nYou are using triqs_hartree_fock version %s\n"%version)

def show_git_hash():
  print("\nYou are using triqs_hartree_fock git hash %s based on triqs git hash %s\n"%("6e6ea1330bb3712528ea1415e3df61591d7eb021", triqs_hash))
