# Manual of DO processing
browseVignettes("GOSemSim")
rm(list = ls())

# Import dataset
library(readxl)
datasheet <- read_excel("D:/Semester 6/Proyek Network Analysis/breast-cancer-network/data/1684561103-DOID-unique-1006.xlsx")

# Preprocessing DOID
library(DOSE)
a <- datasheet$`DOID`
a <- a[!is.na(a)]
a <- a[! a %in% c('-')]
a

# Use doSim function to measure similarity
s <- doSim(a, a, measure = "Rel")
s <- data.frame(s)

# Write the result to Excel format
library(openxlsx)

# For writing a data.frame or list of data.frames to an xlsx file
write.xlsx(s, 'D:/Semester 6/Proyek Network Analysis/breast-cancer-network/data/adjmatrix-Rel.xlsx')
