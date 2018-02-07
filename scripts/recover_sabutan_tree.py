#!/usr/bin/env python
"""
Recover the tree relationship from a sabutan tree hierarchy file.
"""

from sys           import argv,stdin,stdout,stderr,exit
from sabutan_parse import read_sabutan_tree_file

def usage(s=None):
	message = """
usage: cat sabutan_tree_file | recover_sabutan_tree [options]
  --show=preorder        list the tree in pre-order
                         (this is the default)
  --show=leafgroups      list all leaf groups
  --show=height          for each node, list max distance to a leaf, and number
                         of descendants
  --show:subtree=<node>  create a listing file for a node and its descendants
  --filespec=<spec>      spec describing how node names are to be output; for
                         example /usr/nwu253/sabutan/compressed/{name}.rrr.bf"""

	if (s == None): exit (message)
	else:           exit ("%s\n%s" % (s,message))


def main():

	# parse the command line

	showWhat = "pre order"
	fileSpec = None

	for arg in argv[1:]:
		if ("=" in arg):
			argVal = arg.split("=",1)[1]

		if (arg == "--show=preorder"):
			showWhat = "pre order"
		elif (arg == "--show=leafgroups"):
			showWhat = "leaf groups"
		elif (arg == "--show=height"):
			showWhat = "height etc"
		elif (arg.startswith("--show:subtree=")) or (arg.startswith("--subtree=")):
			showWhat = "subtree"
			nodeName = argVal
		elif (arg.startswith("--filespec=")):
			if ("{name}" not in argVal):
				usage("filespec MUST contain {name}\n(in \"%s\"" % arg)
			fileSpec = argVal
		elif (arg.startswith("--")):
			usage("unrecognized option: %s" % arg)
		else:
			usage("unrecognized option: %s" % arg)

	# process the tree

	forest = read_sabutan_tree_file(stdin)
	assert (len(forest) != 0), "input has no tree"

	for tree in forest:
		if (showWhat == "pre order"):
			tree.list_pre_order()
		elif (showWhat == "leaf groups"):
			tree.list_leaf_groups()
		elif (showWhat == "height etc"):
			tree.compute_height_etc()
			tree.list_height_etc()
		elif (showWhat == "subtree"):
			nameToNode = tree.build_dict()
			assert (nodeName in nameToNode), \
			       "unknown node: \"%s\"" % nodeName
			subtree = nameToNode[nodeName]
			subtree.list_pre_order(fileSpec=fileSpec)
		else:
			assert (False), \
			       "internal error: unknown operation \"%s\"" % showWhat




if __name__ == "__main__": main()
