# Linear Regression predicts linear relationship between two variables

setwd("~/Desktop/edu/R-lang/")
rawData <- read.csv("linear.csv", header=T)

head(rawData, 10)
linModel <- lm(y~x, data = rawData)

attributes(linModel) 
linModel$na.action
linModel$coefficients

# Predicting New Value based on our model
predict(linModel, data.frame(x = 1))

plot(y ~ x, data = rawData,
     xlab = "X",
     ylab = "Y",
     main = "Plot"
)

abline(linModel, col = "green", lwd = 1)