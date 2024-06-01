gb_changepoint stands for "Graph-Based Changepoint" and provides, as the name suggests, methods for graph-based changepoint detection. So far, this package includes three main modules: gbTests, gbChangepoint1, and gbChangepoint2.  
  
gbTests performs a two sample test on a valid similarity graph.  
gbChangepoint1 locates a single changepoint for a valid similarity graph.  
gbChangepoint2 locates a change interval (not a single point) for a valid similarity graph. That is, it locates a section of contigous time points where the underlying distribution changed.