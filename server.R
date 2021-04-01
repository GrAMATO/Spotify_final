# Import R packages needed for the app here:
library(shiny)
library(DT)
library(RColorBrewer)
library(lubridate)
library(reticulate)
library(dplyr)
library(readr)
library(shinyalert)

# Define any Python packages needed for the app here:
PYTHON_DEPENDENCIES = c('pip', 'numpy','pandas')

# Begin app server
shinyServer(function(input, output) {
  
  # ------------------ App virtualenv setup (Do not edit) ------------------- #
  
  virtualenv_dir = Sys.getenv('VIRTUALENV_NAME')
  python_path = Sys.getenv('PYTHON_PATH')
  
  # Create virtual env and install dependencies
  reticulate::virtualenv_create(envname = virtualenv_dir, python = python_path)
  reticulate::virtualenv_install(virtualenv_dir, packages = PYTHON_DEPENDENCIES, ignore_installed=TRUE)
  reticulate::use_virtualenv(virtualenv_dir, required = T)
  
  # ------------------ App server logic (Edit anything below) --------------- #
  
  plot_cols <- brewer.pal(11, 'Spectral')
  
  # Import python functions to R

  #reticulate::
  source_python('opti.py')
  
  moyennes_playlists <- read_csv('moyennes_playlists.csv')
  data_playlists <- read_csv("data_playlists.csv")
  data_analyse <- read_csv("data_analyse.csv")
  data_tracks_final <- read_csv("data_tracks_final.csv")
  
  # Generate the requested distribution
  data <- reactive({
    df <- final_opti(input$valence, input$danceability, input$energy,
               input$acousticness,"peu_importe", input$instrumentalness)
    df <- df%>%filter(!grepl('Learn', names))
    if (input$top==FALSE){df <- df%>%filter(!grepl('Top', names))}
    return(df)
  })
  

  output$dff <- renderDataTable(data())
  
  reactive(if(nrow(data())<1){
  shinyalert(
    title = "",
    text = "Votre demande est trop incohérente, veuillez réessayer avec des attentes plus réalistes",
    size = "s", 
    closeOnEsc = TRUE,
    closeOnClickOutside = TRUE,
    html = FALSE,
    type = "warning",
    showConfirmButton = FALSE,
    showCancelButton = TRUE,
    cancelButtonText = "Retour",
    timer = 0,
    imageUrl = "",
    animation = FALSE
  )})
  
  ########
  url_choix1 <- reactive({return(as.character(paste0(substr(data()[1,2], start = 1, stop = 25),"embed",substr(data()[1,2], start = 25, stop = 60))))})
  
  code_choix1 <- reactive(paste0("<p style='text-align: center;'><iframe src='",url_choix1(),"' width='350' height='500' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><p>"))
  
  output$lien1 <- renderUI(HTML(code_choix1( )))
  
  tableau_choix1 <- reactive({
    data_chosen <- data_tracks_final%>%
      filter(playlist_id==data()[1,3])%>%
      inner_join(.,data_analyse,by = c("track_id" = "id"))%>%
      inner_join(.,data_playlists,by=c("playlist_id"="id"))%>%
      rename("Nom_de_la_Playlist"=names)%>%
      rename("Description"=description)
    
    return(t(data.frame("Titre"=data_chosen[1,25],
                 "Description"=data_chosen[1,26],
                 "Durée"=round(seconds_to_period(sum(data_chosen$duration_ms)/1000),0),
                 "Nombre_de_musiques"=nrow(data_chosen),
                 "Artists_récurrents"="Artists récurents à récupérer",
                 "Popularité"=paste0(round(mean(data_chosen$popularity),2),"/100"))))})
  
  
  output$tableau1 <- renderTable(tableau_choix1(),
                               rownames = TRUE,
                               colnames = FALSE,
                               striped = TRUE, bordered = TRUE,hover = TRUE)
  
  output$titre_choix1 <- renderUI(as.character(tableau_choix1()[1,1]))
  
  
  output$plot1 <- renderPlotly(plot_ly(
                                type = 'scatterpolar',
                                r = as.vector(t(data()[1,5:10])),
                                theta = c('Ambiance positive','Musique dansante','Musique énergique', 'Musique acoustique', 'Paroles parlées', 'Absence de paroles'),
                                fill = 'toself') %>%
                                layout(
                                      polar = list(
                                        radialaxis = list(
                                          visible = T,
                                          range = c(0,1))),
                                      showlegend = F))
  

  ########
  
  url_choix2 <- reactive({return(as.character(paste0(substr(data()[2,2], start = 1, stop = 25),"embed",substr(data()[2,2], start = 25, stop = 60))))})
  
  code_choix2 <- reactive(paste0("<p style='text-align: center;'><iframe src='",url_choix2(),"' width='350' height='500' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><p>"))
  
  output$lien2 <- renderUI(HTML(code_choix2( )))
  
  tableau_choix2 <- reactive({
    data_chosen <- data_tracks_final%>%
      filter(playlist_id==data()[2,3])%>%
      inner_join(.,data_analyse,by = c("track_id" = "id"))%>%
      inner_join(.,data_playlists,by=c("playlist_id"="id"))%>%
      rename("Nom_de_la_Playlist"=names)%>%
      rename("Description"=description)
    
    return(t(data.frame("Titre"=data_chosen[2,25],
                        "Description"=data_chosen[2,26],
                        "Durée"=round(seconds_to_period(sum(data_chosen$duration_ms)/1000),0),
                        "Nombre_de_musiques"=nrow(data_chosen), 
                        "Artists_récurrents"="Artists récurents à récupérer",
                        "Popularité"=paste0(round(mean(data_chosen$popularity),2),"/100"))))})
  
  
  output$tableau2 <- renderTable(tableau_choix2(),
                                 rownames = TRUE,
                                 colnames = FALSE,
                                 striped = TRUE, bordered = TRUE,hover = TRUE)
  
  output$titre_choix2 <- renderUI(as.character(tableau_choix2()[1,1]))
  
  
  output$plot2 <- renderPlotly(plot_ly(
    type = 'scatterpolar',
    r = as.vector(t(data()[2,5:10])),
    theta = c('Ambiance positive','Musique dansante','Musique énergique', 'Musique acoustique', 'Paroles parlées', 'Absence de paroles'),
    fill = 'toself') %>%
      layout(
        polar = list(
          radialaxis = list(
            visible = T,
            range = c(0,1))),
        showlegend = F))
  
  ####
  url_choix3 <- reactive({return(as.character(paste0(substr(data()[3,2], start = 1, stop = 25),"embed",substr(data()[3,2], start = 25, stop = 60))))})
  
  code_choix3 <- reactive(paste0("<p style='text-align: center;'><iframe src='",url_choix3(),"' width='350' height='500' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><p>"))
  
  output$lien3 <- renderUI(HTML(code_choix3( )))
  
  tableau_choix3 <- reactive({
    data_chosen <- data_tracks_final%>%
      filter(playlist_id==data()[3,3])%>%
      inner_join(.,data_analyse,by = c("track_id" = "id"))%>%
      inner_join(.,data_playlists,by=c("playlist_id"="id"))%>%
      rename("Nom_de_la_Playlist"=names)%>%
      rename("Description"=description)
    
    return(t(data.frame("Titre"=data_chosen[3,25],
                        "Description"=data_chosen[3,26],
                        "Durée"=round(seconds_to_period(sum(data_chosen$duration_ms)/1000),0),
                        "Nombre_de_musiques"=nrow(data_chosen), 
                        "Artists_récurrents"="Artists récurents à récupérer",
                        "Popularité"=paste0(round(mean(data_chosen$popularity),2),"/100"))))})
  
  
  output$tableau3 <- renderTable(tableau_choix3(),
                                 rownames = TRUE,
                                 colnames = FALSE,
                                 striped = TRUE, bordered = TRUE,hover = TRUE)
  
  output$titre_choix3 <- renderUI(as.character(tableau_choix3()[1,1]))
  
  
  output$plot3 <- renderPlotly(plot_ly(
    type = 'scatterpolar',
    r = as.vector(t(data()[3,5:10])),
    theta = c('Ambiance positive','Musique dansante','Musique énergique', 'Musique acoustique', 'Paroles parlées', 'Absence de paroles'),
    fill = 'toself') %>%
      layout(
        polar = list(
          radialaxis = list(
            visible = T,
            range = c(0,1))),
        showlegend = F))
  
####
  
  url_choix4 <- reactive({return(as.character(paste0(substr(data()[4,2], start = 1, stop = 25),"embed",substr(data()[4,2], start = 25, stop = 60))))})
  
  code_choix4 <- reactive(paste0("<p style='text-align: center;'><iframe src='",url_choix4(),"' width='350' height='500' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><p>"))
  
  output$lien4 <- renderUI(HTML(code_choix4( )))
  
  tableau_choix4 <- reactive({
    data_chosen <- data_tracks_final%>%
      filter(playlist_id==data()[4,3])%>%
      inner_join(.,data_analyse,by = c("track_id" = "id"))%>%
      inner_join(.,data_playlists,by=c("playlist_id"="id"))%>%
      rename("Nom_de_la_Playlist"=names)%>%
      rename("Description"=description)
    
    return(t(data.frame("Titre"=data_chosen[4,25],
                        "Description"=data_chosen[4,26],
                        "Durée"=round(seconds_to_period(sum(data_chosen$duration_ms)/1000),0),
                        "Nombre_de_musiques"=nrow(data_chosen), 
                        "Artists_récurrents"="Artists récurents à récupérer",
                        "Popularité"=paste0(round(mean(data_chosen$popularity),2),"/100"))))})
  
  
  output$tableau4 <- renderTable(tableau_choix4(),
                                 rownames = TRUE,
                                 colnames = FALSE,
                                 striped = TRUE, bordered = TRUE,hover = TRUE)
  
  output$titre_choix4 <- renderUI(as.character(tableau_choix4()[1,1]))
  
  
  output$plot4 <- renderPlotly(plot_ly(
    type = 'scatterpolar',
    r = as.vector(t(data()[4,5:10])),
    theta = c('Ambiance positive','Musique dansante','Musique énergique', 'Musique acoustique', 'Paroles parlées', 'Absence de paroles'),
    fill = 'toself') %>%
      layout(
        polar = list(
          radialaxis = list(
            visible = T,
            range = c(0,1))),
        showlegend = F))
  
 ####
  
  url_choix5 <- reactive({return(as.character(paste0(substr(data()[5,2], start = 1, stop = 25),"embed",substr(data()[5,2], start = 25, stop = 60))))})
  
  code_choix5 <- reactive(paste0("<p style='text-align: center;'><iframe src='",url_choix5(),"' width='350' height='500' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><p>"))
  
  output$lien5 <- renderUI(HTML(code_choix5( )))
  
  tableau_choix5 <- reactive({
    data_chosen <- data_tracks_final%>%
      filter(playlist_id==data()[5,3])%>%
      inner_join(.,data_analyse,by = c("track_id" = "id"))%>%
      inner_join(.,data_playlists,by=c("playlist_id"="id"))%>%
      rename("Nom_de_la_Playlist"=names)%>%
      rename("Description"=description)
    
    return(t(data.frame("Titre"=data_chosen[5,25],
                        "Description"=data_chosen[5,26],
                        "Durée"=round(seconds_to_period(sum(data_chosen$duration_ms)/1000),0),
                        "Nombre_de_musiques"=nrow(data_chosen), 
                        "Artists_récurrents"="Artists récurents à récupérer",
                        "Popularité"=paste0(round(mean(data_chosen$popularity),2),"/100"))))})
  
  
  output$tableau5 <- renderTable(tableau_choix5(),
                                 rownames = TRUE,
                                 colnames = FALSE,
                                 striped = TRUE, bordered = TRUE,hover = TRUE)
  
  output$titre_choix5 <- renderUI(as.character(tableau_choix5()[1,1]))
  
  
  output$plot5 <- renderPlotly(plot_ly(
    type = 'scatterpolar',
    r = as.vector(t(data()[5,5:10])),
    theta = c('Ambiance positive','Musique dansante','Musique énergique', 'Musique acoustique', 'Paroles parlées', 'Absence de paroles'),
    fill = 'toself') %>%
      layout(
        polar = list(
          radialaxis = list(
            visible = T,
            range = c(0,1))),
        showlegend = F))
  
  #######
  
  url_choix6 <- reactive({return(as.character(paste0(substr(data()[6,2], start = 1, stop = 25),"embed",substr(data()[6,2], start = 25, stop = 60))))})
  
  code_choix6 <- reactive(paste0("<p style='text-align: center;'><iframe src='",url_choix6(),"' width='350' height='500' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><p>"))
  
  output$lien6 <- renderUI(HTML(code_choix6( )))
  
  tableau_choix6 <- reactive({
    data_chosen <- data_tracks_final%>%
      filter(playlist_id==data()[6,3])%>%
      inner_join(.,data_analyse,by = c("track_id" = "id"))%>%
      inner_join(.,data_playlists,by=c("playlist_id"="id"))%>%
      rename("Nom_de_la_Playlist"=names)%>%
      rename("Description"=description)
    
    return(t(data.frame("Titre"=data_chosen[6,25],
                        "Description"=data_chosen[6,26],
                        "Durée"=round(seconds_to_period(sum(data_chosen$duration_ms)/1000),0),
                        "Nombre_de_musiques"=nrow(data_chosen), 
                        "Artists_récurrents"="Artists récurents à récupérer",
                        "Popularité"=paste0(round(mean(data_chosen$popularity),2),"/100"))))})
  
  
  output$tableau6 <- renderTable(tableau_choix6(),
                                 rownames = TRUE,
                                 colnames = FALSE,
                                 striped = TRUE, bordered = TRUE,hover = TRUE)
  
  output$titre_choix6 <- renderUI(as.character(tableau_choix6()[1,1]))
  
  
  output$plot6 <- renderPlotly(plot_ly(
    type = 'scatterpolar',
    r = as.vector(t(data()[6,5:10])),
    theta = c('Ambiance positive','Musique dansante','Musique énergique', 'Musique acoustique', 'Paroles parlées', 'Absence de paroles'),
    fill = 'toself') %>%
      layout(
        polar = list(
          radialaxis = list(
            visible = T,
            range = c(0,1))),
        showlegend = F))
  
  #######
  
  url_choix7 <- reactive({return(as.character(paste0(substr(data()[7,2], start = 1, stop = 25),"embed",substr(data()[7,2], start = 25, stop = 60))))})
  
  code_choix7 <- reactive(paste0("<p style='text-align: center;'><iframe src='",url_choix7(),"' width='350' height='500' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><p>"))
  
  output$lien7 <- renderUI(HTML(code_choix7( )))
  
  tableau_choix7 <- reactive({
    data_chosen <- data_tracks_final%>%
      filter(playlist_id==data()[7,3])%>%
      inner_join(.,data_analyse,by = c("track_id" = "id"))%>%
      inner_join(.,data_playlists,by=c("playlist_id"="id"))%>%
      rename("Nom_de_la_Playlist"=names)%>%
      rename("Description"=description)
    
    return(t(data.frame("Titre"=data_chosen[7,25],
                        "Description"=data_chosen[7,26],
                        "Durée"=round(seconds_to_period(sum(data_chosen$duration_ms)/1000),0),
                        "Nombre_de_musiques"=nrow(data_chosen), 
                        "Artists_récurrents"="Artists récurents à récupérer",
                        "Popularité"=paste0(round(mean(data_chosen$popularity),2),"/100"))))})
  
  
  output$tableau7 <- renderTable(tableau_choix7(),
                                 rownames = TRUE,
                                 colnames = FALSE,
                                 striped = TRUE, bordered = TRUE,hover = TRUE)
  
  output$titre_choix7 <- renderUI(as.character(tableau_choix7()[1,1]))
  
  
  output$plot7 <- renderPlotly(plot_ly(
    type = 'scatterpolar',
    r = as.vector(t(data()[7,5:10])),
    theta = c('Ambiance positive','Musique dansante','Musique énergique', 'Musique acoustique', 'Paroles parlées', 'Absence de paroles'),
    fill = 'toself') %>%
      layout(
        polar = list(
          radialaxis = list(
            visible = T,
            range = c(0,1))),
        showlegend = F))
  
  ######
  
  url_choix8 <- reactive({return(as.character(paste0(substr(data()[8,2], start = 1, stop = 25),"embed",substr(data()[8,2], start = 25, stop = 60))))})
  
  code_choix8 <- reactive(paste0("<p style='text-align: center;'><iframe src='",url_choix8(),"' width='350' height='500' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><p>"))
  
  output$lien8 <- renderUI(HTML(code_choix8( )))
  
  tableau_choix8 <- reactive({
    data_chosen <- data_tracks_final%>%
      filter(playlist_id==data()[8,3])%>%
      inner_join(.,data_analyse,by = c("track_id" = "id"))%>%
      inner_join(.,data_playlists,by=c("playlist_id"="id"))%>%
      rename("Nom_de_la_Playlist"=names)%>%
      rename("Description"=description)
    
    return(t(data.frame("Titre"=data_chosen[8,25],
                        "Description"=data_chosen[8,26],
                        "Durée"=round(seconds_to_period(sum(data_chosen$duration_ms)/1000),0),
                        "Nombre_de_musiques"=nrow(data_chosen), 
                        "Artists_récurrents"="Artists récurents à récupérer",
                        "Popularité"=paste0(round(mean(data_chosen$popularity),2),"/100"))))})
  
  
  output$tableau8 <- renderTable(tableau_choix8(),
                                 rownames = TRUE,
                                 colnames = FALSE,
                                 striped = TRUE, bordered = TRUE,hover = TRUE)
  
  output$titre_choix8 <- renderUI(as.character(tableau_choix8()[1,1]))
  
  
  output$plot8 <- renderPlotly(plot_ly(
    type = 'scatterpolar',
    r = as.vector(t(data()[8,5:10])),
    theta = c('Ambiance positive','Musique dansante','Musique énergique', 'Musique acoustique', 'Paroles parlées', 'Absence de paroles'),
    fill = 'toself') %>%
      layout(
        polar = list(
          radialaxis = list(
            visible = T,
            range = c(0,1))),
        showlegend = F))


})
