import cozy
import cozy.analysis as analysis
from cozy.project import Project
import claripy

a_sym = claripy.BVS("a", 32)
b_sym = claripy.BVS("b", 32)
c_sym = claripy.BVS("c", 32)
args = [a_sym, b_sym, c_sym]

def run(proj):
    proj.add_prototype("flt_3", "int flt_3(unsigned int a, unsigned int b, unsigned int c)")
    sess = proj.session("flt_3")
    return sess.run(args)

proj = Project("test_programs/flt/flt")
results = run(proj)
comparison_results = analysis.Comparison(results, results)

print("\nComparison Results:\n")
print(comparison_results.report(args))

cozy.execution_graph.visualize_comparison(proj, proj, results, results, comparison_results, args=args,
                                          num_examples=2, open_browser=True)