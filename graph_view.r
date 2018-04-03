"C:/Program Files/R/R-3.3.2/bin/Rscript"
library(visNetwork)
library(igraph)
edges<-read.csv('C:/skp/phd/UIPS/edge_list.csv')
nodes <- data.frame(id=unique(c(as.character(edges$from),as.character(edges$to))))
nodes$label = gsub("[0-9]*$","",nodes$id)
nodes$title = paste0("<p>",nodes$label,"</p>")
net<-visNetwork(nodes, edges, height = "700px", width = "100%") %>% visEdges(arrows ="to") %>% visIgraphLayout() 
visSave(net,"C:/skp/phd/UIPS/graph_view.html",selfcontained = FALSE)