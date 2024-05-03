FinalData <-read.csv("2차 전처리/Retail_FinalData.csv", header = T, fileEncoding = "cp949")
tail(FinalData)
str(FinalData)
OrderedData<-FinalData[order(FinalData$index),]

tail(OrderedData)
write.csv(OrderedData, "OrderedFinal91365=4", fileEncoding = 'cp949')
