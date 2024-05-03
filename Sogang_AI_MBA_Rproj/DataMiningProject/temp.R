x<-c(3,3,4,5,6,6,7,8,8,9)
y<-c(9,5,12,9,14,16,22,18,24,22)

xmean<-mean(x)
xmean
ymean<-mean(y)
ymean

sum((y-ymean)*(x-xmean))
sum((x-xmean)^2)
sum((y-ymean)*(x-xmean))/sum((x-xmean)^2)

pchisq(38.615, df = 2, lower.tail = F)^2
pt(38.615, df =1, lower.tail = F)^2

pchisq(38.615, df = 1, lower.tail =F)
pf(38.615, 1, 8, lower.tail =F)


sqrt(2.7408)

pt(6.214, df = 8, lower.tail = F)*2
sqrt(63.653/8)
pf(38.62, 1, 8, lower.tail =F)
