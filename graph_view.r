library(visNetwork)
library(igraph)
edges<-unique(read.csv('C:/skp/phd/UIPS/edge_list.csv'))
nodes<-unique(read.csv('C:/skp/phd/UIPS/node_list.csv'))
#nodes <- data.frame(id=unique(c(as.character(edges$from),as.character(edges$to))))
nodes$label = gsub("[0-9]*$","",nodes$id)
nodes$group = nodes$label
nodes$title = paste0("<p>",nodes$title,"</p>")
net<-visNetwork(nodes, edges, height = "700px", width = "100%") %>% visEdges(arrows ="to") %>% visOptions(highlightNearest = TRUE, nodesIdSelection = TRUE) %>%visLegend() #%>% visIgraphLayout() 

visSave(net,"C:/skp/phd/UIPS/graph_view.html",selfcontained = FALSE)