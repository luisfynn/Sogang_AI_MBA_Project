#install.packages("dplyr")
#install.packages('tidyr")
library(dplyr)
library(httr)
library(tidyverse)
library(jsonlite) # fromJSON()

#전처리
retail<-read.csv("train.csv", header = T)
str(retail)

#데이터는 서울특별시 742285건, 부산광역시 474268건, 총 1216553건
retail %>% filter(city =="서울특별시") %>% 
  count()

retail %>% filter(city =="부산광역시") %>% 
  count()

#서울, 부산 데이터 중 서울 데이터만 선택
retail_seoul<-retail %>%
  filter(city == "서울특별시")

#2017년 데이터만 추출
#갯수 91364개
retail_seoul %>% 
  mutate(transaction_year_month = lubridate::parse_date_time(transaction_year_month, "Ym"),
         year = lubridate::year(transaction_year_month)) %>% 
  filter(year == "2017") %>% 
  count()

retail_seoul<-retail_seoul %>% 
  mutate(transaction_year_month = lubridate::parse_date_time(transaction_year_month, "Ym"),
         year = lubridate::year(transaction_year_month)) %>% 
  filter(year == "2017")

##################################################################################################
#1st
#Geo coding(카카오맵을 이용해서, 아파트위치의 위도,경도,지역구 추출)
KAKAO_MAP_API_KEY ="19207f22aaab012c605a0aa82887cd70" #<나의 KEY 입력>
result = data.frame()
address_list <- retail_seoul$addr_kr

#------------------------------------------------------------------------------#
# #run loop
for(i in 82650:86000)
{
  res <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/address.json',
      query = list(query = address_list[i]),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  #print(x=res)
  coord <- res %>% content(as = 'text') %>% fromJSON()

  Latitude <- coord$documents$x
  Hardness <- coord$documents$y
  Rejion <- coord$documents$address_name

  #2개 이상으로 주소가 검색되는 현상 방지
  Latitude<-Latitude[1]
  Hardness<-Hardness[1]
  Rejion<-Rejion[1]

  #Latitude /Harness /Rejion 이 Null 이면 pass
  if(is.null(Latitude) || is.null(Hardness) || is.null(Rejion)
     || is.na(Latitude) || is.na(Hardness) || is.na(Rejion)){
    bigMarket05 <- NA
    bigMarket10 <- NA
    bigMarket15 <- NA
    hospital05 <- NA
    hospital10 <- NA
    hospital15 <- NA

    kid05 <- NA
    kid10 <- NA
    kid15 <- NA
    movie05 <- NA
    movie10 <- NA
    movie15 <- NA
    office05 <- NA
    office10 <- NA
    office15 <- NA
    school05 <- NA
    school10 <- NA
    school15 <- NA
    subway05 <- NA
    subway10 <- NA
    subway15 <- NA
    Latitude <- NA
    Hardness <- NA
    Rejion  <- NA
    row_temp <- cbind(Latitude, Hardness, Rejion)
    row_temp <- cbind(row_temp, bigMarket05, bigMarket10, bigMarket15)
    row_temp <- cbind(row_temp, hospital05, hospital10, hospital15)
    row_temp <- cbind(row_temp, kid05, kid10, kid15)
    row_temp <- cbind(row_temp, movie05, movie10, movie15)
    row_temp <- cbind(row_temp, office05, office10, office15)
    row_temp <- cbind(row_temp, school05, school10, school15)
    row_temp <- cbind(row_temp, subway05, subway10, subway15)
    result = rbind(result, row_temp)
    print(paste(i, "is skipped"))
    next
  }

  row_temp = cbind(Latitude, Hardness, Rejion)

  #대형마트------------------------------------------------------------------
  #0.5km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket05)

  #1km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket10)

  #1.5km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket15)


  #학교------------------------------------------------------------------
  #0.5km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school05)

  #1km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school10)

  #1.5km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school15)


  #지하철------------------------------------------------------------------
  #0.5km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway05)

  #1km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway10)

  #1.5km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway15)

  #병원------------------------------------------------------------------
  #0.5km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital05)

  #1km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital10)

  #1.5km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital15)


  #문화시설 ------------------------------------------------------------------
  #0.5km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie05)

  #1km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie10)

  #1.5km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie15)

  #유치원/어린이집 ------------------------------------------------------------------
  #0.5km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid05)

  #1km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid10)

  #1.5km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid15)

  #관공서 ------------------------------------------------------------------
  #0.5km 이내 관공서수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office05)

  #1km 이내 관공서 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office10)

  #1.5km 이내 관공서 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office15)

  result = rbind(result, row_temp)
  print(paste(i, "is finished"))
}

#82650~86000
final_data_82650_86000<-cbind(retail_seoul[82650:86000, ], result)
write.csv(final_data_82650_86000, "finalData_82650_86000.csv", fileEncoding = 'cp949')

###############################################################################################
#2nd
#Geo coding(카카오맵을 이용해서, 아파트위치의 위도,경도,지역구 추출)
KAKAO_MAP_API_KEY ="54770038e915f4697298f89487238b3d" #<나의 KEY 입력>
result = data.frame()
address_list <- retail_seoul$addr_kr

#------------------------------------------------------------------------------#
# #run loop
for(i in 86001:90000)
{
  res <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/address.json',
      query = list(query = address_list[i]),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  #print(x=res)
  coord <- res %>% content(as = 'text') %>% fromJSON()
  
  Latitude <- coord$documents$x
  Hardness <- coord$documents$y
  Rejion <- coord$documents$address_name

  #2개 이상으로 주소가 검색되는 현상 방지
  Latitude<-Latitude[1]
  Hardness<-Hardness[1]
  Rejion<-Rejion[1]
  
  #Latitude /Harness /Rejion 이 Null 이면 pass
  if(is.null(Latitude) || is.null(Hardness) || is.null(Rejion)
     || is.na(Latitude) || is.na(Hardness) || is.na(Rejion)){
    bigMarket05 <- NA
    bigMarket10 <- NA
    bigMarket15 <- NA
    hospital05 <- NA
    hospital10 <- NA
    hospital15 <- NA    
    
    kid05 <- NA
    kid10 <- NA
    kid15 <- NA
    movie05 <- NA
    movie10 <- NA
    movie15 <- NA   
    office05 <- NA
    office10 <- NA
    office15 <- NA
    school05 <- NA
    school10 <- NA
    school15 <- NA
    subway05 <- NA
    subway10 <- NA
    subway15 <- NA
    Latitude <- NA
    Hardness <- NA
    Rejion  <- NA
    row_temp <- cbind(Latitude, Hardness, Rejion)   
    row_temp <- cbind(row_temp, bigMarket05, bigMarket10, bigMarket15)
    row_temp <- cbind(row_temp, hospital05, hospital10, hospital15) 
    row_temp <- cbind(row_temp, kid05, kid10, kid15) 
    row_temp <- cbind(row_temp, movie05, movie10, movie15) 
    row_temp <- cbind(row_temp, office05, office10, office15) 
    row_temp <- cbind(row_temp, school05, school10, school15) 
    row_temp <- cbind(row_temp, subway05, subway10, subway15) 
    result = rbind(result, row_temp) 
    print(paste(i, "is skipped"))
    next
  }
  
  row_temp = cbind(Latitude, Hardness, Rejion)    
  
  #대형마트------------------------------------------------------------------
  #0.5km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket05)
  
  #1km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket10)
  
  #1.5km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket15)
  
  
  #학교------------------------------------------------------------------
  #0.5km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school05)
  
  #1km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school10)
  
  #1.5km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school15)
  
  
  #지하철------------------------------------------------------------------
  #0.5km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway05)
  
  #1km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway10)
  
  #1.5km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway15)
  
  #병원------------------------------------------------------------------
  #0.5km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital05)
  
  #1km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital10)
  
  #1.5km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital15)
  
  
  #문화시설 ------------------------------------------------------------------
  #0.5km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie05)
  
  #1km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie10)
  
  #1.5km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie15)
  
  #유치원/어린이집 ------------------------------------------------------------------
  #0.5km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid05)
  
  #1km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid10)
  
  #1.5km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid15)
  
  #관공서 ------------------------------------------------------------------
  #0.5km 이내 관공서수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office05)
  
  #1km 이내 관공서 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office10)
  
  #1.5km 이내 관공서 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office15)
  
  result = rbind(result, row_temp) 
  print(paste(i, "is finished"))
}

#86001~90000
final_data_86001_90000<-cbind(retail_seoul[86001:90000, ], result)
write.csv(final_data_86001_90000, "finalData_86001_90000.csv", fileEncoding = 'cp949')

###############################################################################################
#3th
#Geo coding(카카오맵을 이용해서, 아파트위치의 위도,경도,지역구 추출)
KAKAO_MAP_API_KEY ="5e79c1f88e3a0ae9c5f6111fb0b69e81" #<나의 KEY 입력>
result = data.frame()
address_list <- retail_seoul$addr_kr

#------------------------------------------------------------------------------#
# #run loop
for(i in 62001:66000)
{
  res <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/address.json',
      query = list(query = address_list[i]),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  #print(x=res)
  coord <- res %>% content(as = 'text') %>% fromJSON()
  
  Latitude <- coord$documents$x
  Hardness <- coord$documents$y
  Rejion <- coord$documents$address_name

  #2개 이상으로 주소가 검색되는 현상 방지
  Latitude<-Latitude[1]
  Hardness<-Hardness[1]
  Rejion<-Rejion[1]
  
  #Latitude /Harness /Rejion 이 Null 이면 pass
  if(is.null(Latitude) || is.null(Hardness) || is.null(Rejion)
     || is.na(Latitude) || is.na(Hardness) || is.na(Rejion)){
    bigMarket05 <- NA
    bigMarket10 <- NA
    bigMarket15 <- NA
    hospital05 <- NA
    hospital10 <- NA
    hospital15 <- NA    
    
    kid05 <- NA
    kid10 <- NA
    kid15 <- NA
    movie05 <- NA
    movie10 <- NA
    movie15 <- NA   
    office05 <- NA
    office10 <- NA
    office15 <- NA
    school05 <- NA
    school10 <- NA
    school15 <- NA
    subway05 <- NA
    subway10 <- NA
    subway15 <- NA
    Latitude <- NA
    Hardness <- NA
    Rejion  <- NA
    row_temp <- cbind(Latitude, Hardness, Rejion)   
    row_temp <- cbind(row_temp, bigMarket05, bigMarket10, bigMarket15)
    row_temp <- cbind(row_temp, hospital05, hospital10, hospital15) 
    row_temp <- cbind(row_temp, kid05, kid10, kid15) 
    row_temp <- cbind(row_temp, movie05, movie10, movie15) 
    row_temp <- cbind(row_temp, office05, office10, office15) 
    row_temp <- cbind(row_temp, school05, school10, school15) 
    row_temp <- cbind(row_temp, subway05, subway10, subway15) 
    result = rbind(result, row_temp) 
    print(paste(i, "is skipped"))
    next
  }
  
  row_temp = cbind(Latitude, Hardness, Rejion)    
  
  #https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-keyword-request-query-category-group-code
  # MT1	대형마트
  # CS2	편의점
  # PS3	어린이집, 유치원
  # SC4	학교
  # AC5	학원
  # PK6	주차장
  # OL7	주유소, 충전소
  # SW8	지하철역
  # BK9	은행
  # CT1	문화시설
  # AG2	중개업소
  # PO3	공공기관
  # AT4	관광명소
  # AD5	숙박
  # FD6	음식점
  # CE7	카페
  # HP8	병원
  # PM9	약국
  
  #대형마트------------------------------------------------------------------
  #0.5km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket05)
  
  #1km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket10)
  
  #1.5km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket15)
  
  
  #학교------------------------------------------------------------------
  #0.5km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school05)
  
  #1km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school10)
  
  #1.5km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school15)
  
  
  #지하철------------------------------------------------------------------
  #0.5km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway05)
  
  #1km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway10)
  
  #1.5km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway15)
  
  #병원------------------------------------------------------------------
  #0.5km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital05)
  
  #1km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital10)
  
  #1.5km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital15)
  
  
  #문화시설 ------------------------------------------------------------------
  #0.5km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie05)
  
  #1km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie10)
  
  #1.5km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie15)
  
  #유치원/어린이집 ------------------------------------------------------------------
  #0.5km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid05)
  
  #1km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid10)
  
  #1.5km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid15)
  
  #관공서 ------------------------------------------------------------------
  #0.5km 이내 관공서수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office05)
  
  #1km 이내 관공서 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office10)
  
  #1.5km 이내 관공서 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office15)
  
  result = rbind(result, row_temp) 
  print(paste(i, "is finished"))
}

#62001~66000
final_data_62001_66000<-cbind(retail_seoul[62001:66000, ], result)
write.csv(final_data_62001_66000, "finalData_62001_66000.csv", fileEncoding = 'cp949')

###############################################################################################
#4th
#Geo coding(카카오맵을 이용해서, 아파트위치의 위도,경도,지역구 추출)
KAKAO_MAP_API_KEY ="7d289c7f29e01896386021952fc5ab73" #<나의 KEY 입력>
result = data.frame()
address_list <- retail_seoul$addr_kr

#------------------------------------------------------------------------------#
# #run loop
for(i in 70001:74000)
{
  res <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/address.json',
      query = list(query = address_list[i]),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  #print(x=res)
  coord <- res %>% content(as = 'text') %>% fromJSON()
  
  Latitude <- coord$documents$x
  Hardness <- coord$documents$y
  Rejion <- coord$documents$address_name
  
  #2개 이상으로 주소가 검색되는 현상 방지
  Latitude<-Latitude[1]
  Hardness<-Hardness[1]
  Rejion<-Rejion[1]
  
  #Latitude /Harness /Rejion 이 Null 이면 pass
  if(is.null(Latitude) || is.null(Hardness) || is.null(Rejion)
     || is.na(Latitude) || is.na(Hardness) || is.na(Rejion)){
    bigMarket05 <- NA
    bigMarket10 <- NA
    bigMarket15 <- NA
    hospital05 <- NA
    hospital10 <- NA
    hospital15 <- NA    
    
    kid05 <- NA
    kid10 <- NA
    kid15 <- NA
    movie05 <- NA
    movie10 <- NA
    movie15 <- NA   
    office05 <- NA
    office10 <- NA
    office15 <- NA
    school05 <- NA
    school10 <- NA
    school15 <- NA
    subway05 <- NA
    subway10 <- NA
    subway15 <- NA
    Latitude <- NA
    Hardness <- NA
    Rejion  <- NA
    row_temp <- cbind(Latitude, Hardness, Rejion)   
    row_temp <- cbind(row_temp, bigMarket05, bigMarket10, bigMarket15)
    row_temp <- cbind(row_temp, hospital05, hospital10, hospital15) 
    row_temp <- cbind(row_temp, kid05, kid10, kid15) 
    row_temp <- cbind(row_temp, movie05, movie10, movie15) 
    row_temp <- cbind(row_temp, office05, office10, office15) 
    row_temp <- cbind(row_temp, school05, school10, school15) 
    row_temp <- cbind(row_temp, subway05, subway10, subway15) 
    result = rbind(result, row_temp) 
    print(paste(i, "is skipped"))
    next
  }
  
  row_temp = cbind(Latitude, Hardness, Rejion)    
  
  #https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-keyword-request-query-category-group-code
  # MT1	대형마트
  # CS2	편의점
  # PS3	어린이집, 유치원
  # SC4	학교
  # AC5	학원
  # PK6	주차장
  # OL7	주유소, 충전소
  # SW8	지하철역
  # BK9	은행
  # CT1	문화시설
  # AG2	중개업소
  # PO3	공공기관
  # AT4	관광명소
  # AD5	숙박
  # FD6	음식점
  # CE7	카페
  # HP8	병원
  # PM9	약국
  
  #대형마트------------------------------------------------------------------
  #0.5km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket05)
  
  #1km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket10)
  
  #1.5km 이내 대형마트 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "MT1", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  bigMarket15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, bigMarket15)
  
  
  #학교------------------------------------------------------------------
  #0.5km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school05)
  
  #1km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school10)
  
  #1.5km 이내 학교 총 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SC4", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  school15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, school15)
  
  
  #지하철------------------------------------------------------------------
  #0.5km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway05)
  
  #1km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway10)
  
  #1.5km 이내 지하철 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "SW8", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  subway15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, subway15)
  
  #병원------------------------------------------------------------------
  #0.5km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital05)
  
  #1km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital10)
  
  #1.5km 이내 병원 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "HP8", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  hospital15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, hospital15)
  
  
  #문화시설 ------------------------------------------------------------------
  #0.5km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie05)
  
  #1km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie10)
  
  #1.5km 이내 문화 시설 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "CT1", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  movie15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, movie15)
  
  #유치원/어린이집 ------------------------------------------------------------------
  #0.5km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid05)
  
  #1km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid10)
  
  #1.5km 이내 유치원/어린이집 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PS3", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  kid15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, kid15)
  
  #관공서 ------------------------------------------------------------------
  #0.5km 이내 관공서수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office05 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office05)
  
  #1km 이내 관공서 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "1000"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office10 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office10)
  
  #1.5km 이내 관공서 수
  place <-
    GET(
      url = 'https://dapi.kakao.com/v2/local/search/category.json',
      query = list(x = Latitude, y = Hardness, category_group_code = "PO3", radius = "1500"),
      add_headers(Authorization = paste0("KakaoAK ",
                                         KAKAO_MAP_API_KEY))
    )
  cplaceCoord <- place %>% content(as = 'text') %>% fromJSON()
  office15 <-cplaceCoord$meta$total_count
  row_temp <- cbind(row_temp, office15)
  
  result = rbind(result, row_temp) 
  print(paste(i, "is finished"))
}

#70001~74000
final_data_70001_74000<-cbind(retail_seoul[70001:74000, ], result)
write.csv(final_data_70001_74000, "finalData_70001_74000.csv", fileEncoding = 'cp949')