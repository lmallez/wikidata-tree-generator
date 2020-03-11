#!/usr/bin/env python3

from MainModule import MainModule

main = MainModule()

main.tree_builder.build_tree('Q9696')
main.gedcom_exporter.export('../out/jfk.ged')

print(main.database.cache)
