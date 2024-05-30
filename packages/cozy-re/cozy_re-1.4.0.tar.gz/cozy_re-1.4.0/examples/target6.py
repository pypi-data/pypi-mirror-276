import cozy
import archinfo

proj_prepatched = cozy.project.Project("test_programs/amp_target6_hackathon/CM2350_KeplersLaw_Unpatched.xcal",
                                       load_options={'main_opts': {"backend": "blob"}, 'arch': archinfo.arch_from_id("ppc32")})

