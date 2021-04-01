# Import R packages needed for the UI
library(shiny)
library(shinycssloaders)
library(DT)
library(shinydashboard)
library(plotly)
library(shinythemes)
library(shinyalert)

# Begin UI for the R + reticulate example app

navbarPage("Recommandation Playlist Spotify",
           tabPanel(
             "",
             fluidPage(
             theme = shinytheme('darkly'),
             includeCSS("styles.css"),),
                    tags$head(
                      tags$style(type = 'text/css', '.navbar { background-color: #262626;
                                               font-family: Arial;
                                               font-size: 13px;
                                               color: #088A08; }',
                                 
                                 '.navbar-dropdown { background-color: #262626;
                                                    font-family: Arial;
                                                    font-size: 13px;
                                                    color: #088A08; }')),
                    #tags$style(HTML(".shiny-output-error-validation{color: blue;}"))),
                    pageWithSidebar(
                      headerPanel(''),
                      sidebarPanel(width = 3,
                                   helpText("Sélectionnez les caractéristiques de votre playlist idéale"),
                                   h2("  Ambiance"),
                                   selectInput("energy", "Énergie",
                                               c("Musique très énergique"="tres_oui",
                                                 "Musique énergique" = "oui",
                                                 "Peu importe"="peu_importe",
                                                 "Musique neutre" = "neutre",
                                                 "Musique calme"= "non",
                                                 "Musique très calme"="tres_non"
                                               ),
                                               selected="peu_importe"),
                                   
                                   selectInput("danceability", "Danse",
                                               c("Musique dansante" = "oui",
                                                 "Musique un peu dansante" = "neutre",
                                                 "Peu importe"="peu_importe",
                                                 "Musique non dansante" = "pas_du_tout"
                                               ),
                                               selected="peu_importe"),
                                   
                                 
                                   selectInput("valence", "Mood",
                                               c("Plutôt joyeux" = "joyeuse",
                                                 "Peu importe"="peu_importe",
                                                 "Neutre" = "neutre",
                                                 "Plutôt triste"= "triste"
                                               ),
                                               selected="peu_importe"),
                                   
                                   h2("  Spécificités"),
                                   
                                   selectInput("acousticness", "Type d'instruments",
                                               c("Instuments acoustiques" = "acoustiques",
                                                 "Majorité d'instruments acoustiques" = "majorite_acoustiques",
                                                 "Peu importe" ="peu_importe",
                                                 "Peu d'instruments acoustiques"="melange",
                                                 "Pas d'instruments acoustiques" = "majorite_electronique"),
                                               selected="peu_importe"),
                                   
                                   selectInput("instrumentalness", "Paroles",
                                               c("Musiques sans paroles" = "sans_paroles",
                                                 "Musiques majoritairement sans paroles" = "majorite_sans_paroles",
                                                 "Peu importe"="peu_importe",
                                                 "Musiques avec paroles" = "avec_paroles"
                                               ),
                                               selected="peu_importe"),
                                   
                                   checkboxInput("top", "Inclure les musiques du top 50", FALSE)
                      ),
                      
####################################################################################################################@                      
                      mainPanel(
                        tabBox(
                          title = uiOutput('titre_choix1'),
                          width=6,
                          id = "tabset1", 
                          tabPanel("Lecteur",br(),uiOutput('lien1'),br()),
                          tabPanel("Infos",br(),tableOutput('tableau1'),
                                   plotlyOutput("plot1", height = '250px'),br()
                          )
                        ),
                        
                        tabBox(
                          title = uiOutput('titre_choix2'),
                          width=6,
                          id = "tabset2", 
                          tabPanel("Lecteur",br(),uiOutput('lien2'),br()),
                          tabPanel("Infos",br(),tableOutput('tableau2'),
                                   plotlyOutput("plot2", height = '250px'),br()
                          )
                        ),
                        
                        tabBox(
                          title = uiOutput('titre_choix3'),
                          width=6,
                          # The id lets us use input$tabset1 on the server to find the current tab
                          id = "tabset3", 
                          tabPanel("Lecteur",br(),uiOutput('lien3'),br()),
                          tabPanel("Infos",br(),tableOutput('tableau3'),
                                   plotlyOutput("plot3", height = '250px'),br()
                          )
                        ),
                        
                        tabBox(
                          title = uiOutput('titre_choix4'),
                          width=6,
                          # The id lets us use input$tabset4 on the server to find the current tab
                          id = "tabset4", 
                          tabPanel("Lecteur",br(),uiOutput('lien4'),br()),
                          tabPanel("Infos",br(),tableOutput('tableau4'),
                                   plotlyOutput("plot4", height = '250px'),br()
                          )
                        ),
                        
                        tabBox(
                          title = uiOutput('titre_choix5'),
                          width=6,
                          # The id lets us use input$tabset5 on the server to find the current tab
                          id = "tabset5", 
                          tabPanel("Lecteur",br(),uiOutput('lien5'),br()),
                          tabPanel("Infos",br(),tableOutput('tableau5'),
                                   plotlyOutput("plot5", height = '250px'),br()
                          )
                        ),
                        
                        tabBox(
                          title = uiOutput('titre_choix6'),
                          width=6,
                          # The id lets us use input$tabset6 on the server to find the current tab
                          id = "tabset6", 
                          tabPanel("Lecteur",br(),uiOutput('lien6'),br()),
                          tabPanel("Infos",br(),tableOutput('tableau6'),
                                   plotlyOutput("plot6", height = '250px'),br()
                          )
                        ),
                        
                        tabBox(
                          title = uiOutput('titre_choix7'),
                          width=6,
                          # The id lets us use input$tabset7 on the server to find the current tab
                          id = "tabset7", 
                          tabPanel("Lecteur",br(),uiOutput('lien7'),br()),
                          tabPanel("Infos",br(),tableOutput('tableau7'),
                                   plotlyOutput("plot7", height = '250px'),br()
                          )
                        ),
                        
                        tabBox(
                          title = uiOutput('titre_choix8'),
                          width=6,
                          # The id lets us use input$tabset7 on the server to find the current tab
                          id = "tabset8", 
                          tabPanel("Lecteur",br(),uiOutput('lien8'),br()),
                          tabPanel("Infos",br(),tableOutput('tableau8'),
                                   plotlyOutput("plot8", height = '250px'),br()
                          )
                        )
                        
                        
           
))))



