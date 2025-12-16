import data_import
import graphing
print(.0020421020391436155/.0006572158442155239)

#The final designs after iteration. First the constant thickness one:
test_unscaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0020421020391436155, 0.0034692189338491365, 0.0020421020391436155, 0.0034692189338491365], 'partially_constant', 4, 1.4314458878848655e-05, scaled_thickness=False)
test_unscaled_wingbox.weight()
graphing.plot_MOS_graph(test_unscaled_wingbox)

#THe final design after iteration, here the variable thickness one
test_scaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0006572158442155239, 0.0011401876353445486, 0.0006572158442155239, 0.0011401876353445486], 'partially_constant', 4, 1.0487964101566806e-05, scaled_thickness=True)
test_scaled_wingbox.weight()
graphing.plot_MOS_graph(test_scaled_wingbox)



