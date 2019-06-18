
import sys
import clang.cindex
import collections

def process_ast(cursor):
    type_kinds = {
            clang.cindex.TypeKind.RECORD: "record",
            clang.cindex.TypeKind.FUNCTIONPROTO: "function"
            }

    cursor_kinds = {
            clang.cindex.CursorKind.TRANSLATION_UNIT: "unit",
            clang.cindex.CursorKind.CLASS_DECL: "class",
            clang.cindex.CursorKind.CONSTRUCTOR: "method",
            clang.cindex.CursorKind.DESTRUCTOR: "method",
            clang.cindex.CursorKind.CXX_METHOD: "method_impl",
            clang.cindex.CursorKind.FIELD_DECL: "field",
            clang.cindex.CursorKind.CALL_EXPR: "call",
            clang.cindex.CursorKind.DECL_REF_EXPR: "var_ref",
            clang.cindex.CursorKind.VAR_DECL: "var",
            clang.cindex.CursorKind.TYPE_REF: "type",
            clang.cindex.CursorKind.MEMBER_REF_EXPR: "member_ref",
            clang.cindex.CursorKind.FUNCTION_DECL: "function",
            clang.cindex.CursorKind.CALL_EXPR: "call"
            }

    def process_cursor(cursor, parent_entry):
        kind = cursor_kinds.get(cursor.kind)
        if kind:
            new_entry = {
                    "kind": kind,
                    "name": cursor.spelling,
                    "start": cursor.extent.start.line,
                    "end": cursor.extent.end.line,
                    "children": []
                    }

            type_kind = type_kinds.get(cursor.type.kind)
            if type_kind:
                new_entry["type"] = type_kind

            parent_entry["children"].append(new_entry)
            return new_entry
        else:
            return None

    def build_entries(cursor, parent_entry, level = 0):
        new_entry = process_cursor(cursor, parent_entry)
        if new_entry:
            parent_entry = new_entry

        for child in cursor.get_children():
            build_entries(child, parent_entry, level+1)

    root = {"kind": "root", "name": "root", "start": 0, "end": 0, "children":[]}
    build_entries(cursor, root)
    return root

def print_entries(entries):
    def print_ast(root, level = 0):
        print "{}{}".format( level * "  ", ", ".join(["{}:{}".format(k,v) for k,v in root.items() if k != "children"]) )
        for child in root["children"]:
            print_ast(child, level+1)

    print_ast(entries)

def process_entries(entries, class_name):
    methods = set()
    fields = set()
    used_by = collections.defaultdict(set)
    using = collections.defaultdict(set)

    def xpath(entry, path):
        def is_matching(entry, sub_path):
            if not sub_path:
                return True

            constraints = sub_path.split("&")
            for c in constraints:
                key_value = c.split("=")
                k = key_value[0]
                v = key_value[1]
                if k in entry:
                    if entry[k] != v:
                        return False
                else:
                    return False
            return True

        def capture(entry, levels):
            if is_matching(entry, levels[0]):
                if len(levels) == 1:
                    return [entry]
                else:
                    captured = []
                    for child in entry["children"]:
                        captured += capture(child, levels[1:])
                    return captured
            else:
                return []

        levels = path.split("/")
        return capture(entry, levels)

    def process_method_impl(method):
        method_name = method["name"]

        for call in xpath(method, "/kind=call"):
            if not xpath(call, "/kind=member_ref/kind=member_ref&type=record"):
                call_name = call["name"]
                methods.add(call_name)
                using[method_name].add(call_name)
                used_by[call_name].add(method_name)

        for field in xpath(method, "/kind=member_ref"):
            field_name = field["name"]
            fields.add(field_name)
            using[method_name].add(field_name)
            used_by[field_name].add(method_name)

    for struct in xpath(entries, "kind=root/kind=unit/kind=class&name="+class_name):
        for field in xpath(struct, "/kind=field"):
            fields.add( field["name"] )

        for method in xpath(struct, "/kind=method_impl"):
            methods.add( method["name"] )
            process_method_impl(method)

    for method in xpath(entries, "kind=root/kind=unit/kind=method_impl"):
        if xpath(method, "/kind=type&name=class "+class_name):
            methods.add( method["name"] )
            process_method_impl(method)

    return (methods, fields, used_by, using)

def print_set(usage):
    for k, v in usage.items():
        print " ", k
        for r in v:
            print "   ", r

if __name__ == '__main__':
    clang.cindex.Config.set_library_file('/usr/lib/x86_64-linux-gnu/libclang-7.so.1')
    compile_db = clang.cindex.CompilationDatabase.fromDirectory('/media/benoit/Data/Projects/linux_study/linux_kernel_study/runtime')
    index = clang.cindex.Index.create()

    source = sys.argv[1]

    compile_cmds = compile_db.getCompileCommands(source)
    if not compile_cmds:
        sys.exit(0)
    compile_args = [a for a in compile_cmds[0].arguments if not a.startswith("-f") and not a.startswith("-m") and not a.startswith("-O")][1:-3]

    tu = index.parse(source, args=compile_args)
    # for f in tu.get_includes():
        # print '\t'*f.depth, f.include.name

    root = process_ast(tu.cursor)

    print_entries(root)
    print

    methods, fields, used_by, using = process_entries(root, "scheduler_tick")
    print methods
    print fields
    print "\nused_by:"
    print_set(used_by)
    print "\nusing:"
    print_set(using)

