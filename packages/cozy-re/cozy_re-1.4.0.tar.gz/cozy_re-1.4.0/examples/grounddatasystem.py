import cozy
import angr
import claripy

proj_prepatched = cozy.project.Project("test_programs/GroundDataSystem/libscience-0_powerpc-e500.so")
proj_postpatched = cozy.project.Project("test_programs/GroundDataSystem/libscience-0_powerpc-e500-badpatch-2.so")

MAX_BUFF_SIZE = 64
buff_contents = claripy.BVS('buff_contents', MAX_BUFF_SIZE * 8)
len_arg = claripy.BVS('len', 32)

class to_hex(angr.SimProcedure):
    def run(self, input_bytes, count, output_buff, outbuff_size):
        self.state.globals['hex_bytes'] = input_bytes
        self.state.globals['hex_count'] = self.state.solver.max(count)

class printf(angr.SimProcedure):
    def run(self):
        input_bytes = self.state.globals['hex_bytes']
        count = self.state.globals['hex_count']
        printed_bytes = self.state.memory.load(input_bytes, count)
        cozy.side_effect.perform(self.state, "printf", printed_bytes)

def run(proj: cozy.project.Project):
    proj.hook_symbol('to_hex', to_hex)
    proj.hook_symbol('printf', printf)

    sess = proj.session('processSciencePacket')

    buff_addr = sess.malloc(MAX_BUFF_SIZE)
    sess.store(buff_addr, buff_contents)

    sess.add_constraints(len_arg.SGE(0))
    sess.add_constraints(len_arg.SLT(MAX_BUFF_SIZE))

    args = [buff_addr, len_arg]

    return sess.run(args)

results_prepatched = run(proj_prepatched)
results_postpatched = run(proj_postpatched)

comparison_results = cozy.analysis.Comparison(results_prepatched, results_postpatched)

cozy.execution_graph.visualize_comparison(proj_prepatched, proj_postpatched,
                                          results_prepatched, results_postpatched,
                                          comparison_results,
                                          include_actions=False,
                                          include_side_effects=True,
                                          args={"buff_contents": buff_contents, "len_arg": len_arg},
                                          num_examples=2, open_browser=True)