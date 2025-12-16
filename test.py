import data_import
import graphing
print(.0020421020391436155/.0006572158442155239)

#The final designs after iteration. First the constant thickness one:
test_unscaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [ 0.0018923258935710516, 0.003417513470019843,  0.0018923258935710516, 0.003417513470019843], 'partially_constant', 42, 1.0232949682472236e-05, scaled_thickness=False)
graphing.plot_MOS_graph(test_unscaled_wingbox)

#test_unscaled_rounded_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [ 0.0019, 0.0035,  0.0019, 0.0035], 'partially_constant', 42, 1.03e-05, scaled_thickness=False)
#graphing.plot_MOS_graph(test_unscaled_rounded_wingbox)




#THe final design after iteration, here the variable thickness one
#test_scaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0006572158442155239, 0.0011401876353445486, 0.0006572158442155239, 0.0011401876353445486], 'partially_constant', 4, 1.0487964101566806e-05, scaled_thickness=True)
#graphing.plot_MOS_graph(test_scaled_wingbox)



