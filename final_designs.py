import data_import
import graphing

#The final designs after iteration. First the constant thickness one:
#test_unscaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [ 0.0028076928753693084, 0.0038648013451746885,  0.0028076928753693084, 0.0038648013451746885], 'partially_constant', 26, 3.624271793503936e-05, scaled_thickness=False)
#graphing.plot_MOS_graph(test_unscaled_wingbox)

test_unscaled_rounded_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [ 0.0029, 0.0039,  0.0029, 0.0039], 'partially_constant', 26, 3.7e-05, scaled_thickness=False)
#graphing.plot_MOS_graph(test_unscaled_rounded_wingbox)
#test_unscaled_rounded_wingbox.weight()
#graphing.shear_flow_plot(test_unscaled_rounded_wingbox)
if __name__=='__main__':
    import column_buckling
    ribs = column_buckling.generate_rib_spacing(test_unscaled_rounded_wingbox, True)
    graphing.plot_MOS_graph(test_unscaled_rounded_wingbox, ribs)



#THe final design after iteration, here the variable thickness one
#test_scaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0009140942779731522, 0.001263453670307925, 0.0009140942779731522, 0.001263453670307925], 'partially_constant', 28, 3.0285835970395364e-05, scaled_thickness=True)
#graphing.plot_MOS_graph(test_scaled_wingbox)

test_scaled_rounded_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0009, 0.0013, 0.0009, 0.0013], 'partially_constant', 28, 3.4e-05, scaled_thickness=True)
#graphing.plot_MOS_graph(test_scaled_rounded_wingbox)
#test_scaled_rounded_wingbox.weight()
#graphing.shear_flow_plot(test_scaled_rounded_wingbox)
if __name__=='__main__':
    import column_buckling
    ribs = column_buckling.generate_rib_spacing(test_scaled_rounded_wingbox, True)
    graphing.plot_MOS_graph(test_scaled_rounded_wingbox, ribs)