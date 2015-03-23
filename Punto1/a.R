library(httr)
library(XML)
library(tidyr)
library(dplyr)
library(ggplot2)

#Escribir aqui el directorio en el que se quieren guardar los diferentes archivos, por default se deja el working directory
#mydirectory <- "/Users/caldasrivera/Dropbox/UniAndes/Semestres\ Acade\314\201micos/Septimo\ Semestre/Metodos\ Computacionales/Tareas/Tarea4/Punto1"
mydirectory <- getwd()

get_dataframe <- function(city){
  search_url <- paste("http://data.giss.nasa.gov/cgi-bin/gistemp/find_station.cgi?dt=1&ds=14&name=", city, sep = "", collapse = NULL)
  search_page <- GET(search_url, user_agent("Chrome"), set_cookies("MeWant" = "cookies"))
  search_page <- as(content(search_page), "character")
  lines <- strsplit(x = search_page, split = "\n")
  lines <- grep(city, lines[[1]], fixed = TRUE, value=TRUE)
  index_start <- gregexpr(pattern = 'id=',lines)
  index_stop <- gregexpr(pattern = '&amp',lines)
  id <- substr(lines, index_start[[1]][1] + 3, index_stop[[1]][1]-1)
  data_url <- paste("http://data.giss.nasa.gov/tmp/gistemp/STATIONS/tmp_", id, "_14_0/station.txt",  sep = "", collapse = NULL)
  useless_url <- paste("http://data.giss.nasa.gov/cgi-bin/gistemp/show_station.cgi?id=", id, "&dt=1&ds=14",  sep = "", collapse = NULL)
  data_useless <- GET(useless_url[1], user_agent("Chrome"))
  filename <- paste(city, ".txt", sep = "", collapse = NULL)
  filename <- paste(mydirectory,filename, sep = "/", collapse = NULL)
  data_ok <- GET(data_url[1], user_agent("Chrome"), write_disk(filename, overwrite = TRUE))
  mydata <- read.table(filename, header = TRUE)
  mydata <- dplyr::select(mydata, YEAR, JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC)
  mydata <- tidyr::gather(mydata, "MONTH", "TEMPERATURE", 2:13)
  if(city != 'Calipuerto')
    mydata$CITY <- city
  else
    mydata$CITY <- 'Cali'
  mydata <- dplyr::mutate(mydata, DATE = as.Date(paste(YEAR, MONTH, "1", sep = "-", collapse = NULL), format="%Y-%b-%d"))
  file.remove(filename)
  return(mydata)
}

cities <- c('Bogota', 'Calipuerto', 'Barranquilla', 'Bucaramanga', 'Ipiales')
big_dataframe <- get_dataframe(cities[1])

for(i in 2:length(cities)){
  big_dataframe <- dplyr::bind_rows(big_dataframe, get_dataframe(cities[i]))
}

write.csv(x = big_dataframe, file = paste(mydirectory, "temperaturas.csv", sep = "/", collapse = NULL))

big_dataframe <- dplyr::filter(big_dataframe, TEMPERATURE != 999.9)
title <- "Temperature in Colombian cities\n1968-2015"
plot1 <- ggplot(big_dataframe, aes(x = DATE, y = TEMPERATURE, colour = CITY)) + geom_line( ) + ggtitle(title) + ylab(expression("Temperature ("*~degree*C*")")) + xlab("Year") 
plot2 <- ggplot(big_dataframe, aes(x = DATE, y = TEMPERATURE)) + geom_line(colour="#F8A21B") + ggtitle(title) + facet_wrap(~ CITY, scales = "free_x", ncol=2) + ylab(expression("Temperature ("*~degree*C*")")) + xlab("Year") 
                                                            
ggsave(filename=paste(mydirectory, "calidadarticuloweb.png", sep = "/", collapse = NULL), width = 7.38, height = 7.36, plot1);
ggsave(filename=paste(mydirectory, "calidadarticuloimpreso.png", sep = "/", collapse = NULL), width = 7.38, height = 7.36, plot2);

