import fnmatch
import logilab.astng
from logilab.astng.exceptions import (InferenceError, ASTNGError,
                                      NotFoundError, UnresolvableName)
from logilab.astng import CallFunc
import sys
import os
from collections import defaultdict
from print_dependency_tree import print_from_file

b = logilab.astng.builder.ASTNGBuilder()
m = logilab.astng.manager.ASTNGManager()

dep_map = defaultdict(list)
q = list()
cache = {}

def getkey(node):
    key = ""
    if isinstance(node, CallFunc) and not hasattr(node, 'name'):
        #this is lamda definition
        key = 'lambda' + "_" + str(node.lineno) + "_" + str(node.col_offset)
    else:
        key = node.name

    if isinstance(node.parent, CallFunc) and not hasattr(node.parent, 'name'):
        key = key + "_" + 'lambda'
    else:
        if not hasattr(node.parent, 'name'):
            key = key + "_" + '_no_name_'
        else:
            key = key + "_" + node.parent.name

    return key

def append_to_list(node, target_node, **kwargs):
    ctx = kwargs['module_source']
    lineno = kwargs['lineno']
    dep_map[getkey(target_node)].append((getkey(node), ctx, lineno))

    if (getkey(node) not in dep_map):
        if (isinstance(node, CallFunc) and not hasattr(node, 'name')):
            return #lambda function, dont go searching for dependencies
        if (not hasattr(node.parent, 'name')):
            return #typically if parent does not have a name, this node is not
            #reference else where

        q.append(node)
        dep_map[getkey(node)] = list()
    else:
        #print 'Skipping node=', node
        pass

class DependencyVisitor(object):

    def _get_cache_key_attr(self, node, module_name):
        return ",".join([node.attrname, str(node.tolineno), str(node.fromlineno),
                          str(node.col_offset), module_name])

    def visit_CallFunc(self, node, target_node, **kwargs):
        pass  #we need a noop on this

    def visit_Getattr(self, node, target_node, **kwargs):
        #print 'in getattr ,', node.__dict__
        #print node.expr.name, node.attrname, target_node.name,
        #target_node.parent.name
        try:
            key = self._get_cache_key_attr(node, kwargs["module_source"])
            if (key in cache):
                types = cache[key]
            else:
                types = [n.name for n in node.expr.infer()]
                cache[key] = types
        except UnresolvableName as e:
            return #unable to resolve name, for certain nodes like func
        except InferenceError as e:
            return

        #print 'types=', types
        if (target_node.name == node.attrname and target_node.parent.name in types):
            #print target_node.name, ' = ', node.attrname
            kwargs['lineno'] = node.lineno,
            append_to_list(node.frame(), target_node, **kwargs)

    def visit_Name(self, node, target_node, **kwargs):
        try:
            key = ",".join([node.name, str(node.tolineno), str(node.fromlineno),
                            str(node.col_offset), kwargs["module_source"]])
            if (key in cache):
                infered_list = cache[key]
            else:
                infered_list = [(n.name, n.parent.name) for n in list(node.infer()) if
                                hasattr(n, 'name') and hasattr(n.parent, 'name')]
                cache[key] = infered_list
        except UnresolvableName as e:
            return #unable to resolve name, for certain nodes like func
        except InferenceError as e:
            return

        if ((target_node.name, target_node.parent.name) in infered_list):
            kwargs['lineno'] = node.lineno,
            append_to_list(node.frame(), target_node, **kwargs)

def walk(root, target_node, visitor, **kwargs):
    for w in root.get_children():
        visit(w, target_node, visitor, **kwargs)
        walk(w, target_node, visitor, **kwargs)

def generic_visitor(node, target_node, **kwargs):
    #print '----In generic function===', type(node), kwargs["module_source"], node
    #print node.name if hasattr(node, "name") else ""
    #print node.parent.name if (hasattr(node, "is_method") and node.is_method()) else ""a
    pass

def visit(node, target_node, visitor, **kwargs):
    #print node.__dict__
    func = getattr(visitor, "visit_" + node.__class__.__name__, generic_visitor)
    #print "calling =", func, "for =", node.__class__.__name__
    func(node, target_node, **kwargs)

def parsefile(fname, target_node, visitor):
    #root = b.string_build(open(fname).read())
    root = m.astng_from_file(fname)
    kwargs = defaultdict(str)
    kwargs['module_source'] = fname
    walk(root, target_node, visitor, **kwargs)

def get_dependencies_of(node):
    root_path = '.'
    pattern = "*.py"
    d = DependencyVisitor()

    #parsefile("./sample.py", node, d)
    for root, dirs, files in os.walk(root_path):
        if "test" not in root:
            for filename in fnmatch.filter(files, pattern):
                parsefile(os.path.join(root, filename), node, d)

def init_q(name, module_name, file_ctx):
    root = m.astng_from_module_name(module_name, file_ctx)
    q.append(root[name])

def start_search():
    while (q):
        n = q.pop(0)
        #print 'get dependency for ', n.name, n #, n.__dict__
        get_dependencies_of(n)

def save_result(filename):
    import pickle

    # for k, v in dep_map.iteritems():
    #     print k, v

    pickle.dump(dep_map, open(filename, "w"))

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print "python.py parser.py <object_name> <file_name> <file_src>"
    else:
        #print sys.argv
        name, module_name, file_ctx = sys.argv[1], sys.argv[2], sys.argv[3]
        init_q(name, module_name, file_ctx)
        start_search()
        save_result("./dependency_list")
        print_from_file()
