import data_import
import graphing
print(0.0009140942779731522/0.0028076928753693084)

#The final designs after iteration. First the constant thickness one:
test_unscaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [ 0.0028076928753693084, 0.0038648013451746885,  0.0028076928753693084, 0.0038648013451746885], 'partially_constant', 26, 3.624271793503936e-05, scaled_thickness=False)
graphing.plot_MOS_graph(test_unscaled_wingbox)

#test_unscaled_rounded_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [ 0.0019, 0.0035,  0.0019, 0.0035], 'partially_constant', 42, 1.03e-05, scaled_thickness=False)
#graphing.plot_MOS_graph(test_unscaled_rounded_wingbox)




#THe final design after iteration, here the variable thickness one
test_scaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0009140942779731522, 0.001263453670307925, 0.0009140942779731522, 0.001263453670307925], 'partially_constant', 28, 3.0285835970395364e-05, scaled_thickness=True)
graphing.plot_MOS_graph(test_scaled_wingbox)



