library(visNetwork)
library(igraph)
edges<-unique(read.csv('edge_list.csv'))
nodes<-unique(read.csv('node_list.csv'))
#nodes <- data.frame(id=unique(c(as.character(edges$from),as.character(edges$to))))
nodes$label = gsub("[0-9]*$","",nodes$id)
nodes$group = nodes$label
nodes$title = paste0("<p>", gsub("(.{50,}?)\\s", "\\1<br>", nodes$title),"</p>")
nodes$shape = 'circle'
net<-visNetwork(nodes, edges, height = "700px", width = "100%") %>% visEdges(arrows ="to") %>% 
visOptions(highlightNearest = TRUE, nodesIdSelection = TRUE) %>%visLegend()  %>% visInteraction(navigationButtons = TRUE) %>% visIgraphLayout()

visSave(net,"graph_view.html",selfcontained = FALSE)