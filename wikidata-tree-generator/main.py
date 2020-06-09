#!/usr/bin/env python3

from MainModule import MainModule

main = MainModule()

id = 'Q82339'

main.config.max_prof = 1000
main.config.max_thread = 1000

main.ancestors_tree_builder.compute(id)
main.entity_filler.process()

main.exporter.export('../out/{}.ged'.format(id))
