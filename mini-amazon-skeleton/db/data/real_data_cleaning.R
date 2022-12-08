library(tidyverse)



finance <-  read.csv('itpas2-2.txt',sep = "|",header = FALSE) 
colnames(finance) <- c("CMTE_ID","AMNDT_IND","RPT_TP","TRANSACTION_PGI","IMAGE_NUM","TRANSACTION_TP",
                                         "ENTITY_TP","NAME","CITY","STATE","ZIP_CODE","EMPLOYER","OCCUPATION","TRANSACTION_DT","TRANSACTION_AMT","OTHER_ID",
                                         "CAND_ID","TRAN_ID","FILE_NUM","MEMO_CD","MEMO_TEXT","SUB_ID")
candidate <- read.csv('cn.txt',sep = '|', header = FALSE)
colnames(candidate) <- c("CAND_ID","CAND_NAME","CAND_PTY_AFFILIATION","CAND_ELECTION_YR","CAND_OFFICE_ST","CAND_OFFICE","CAND_OFFICE_DISTRICT",
                         "CAND_ICI","CAND_STATUS","CAND_PCC","CAND_ST1","CAND_ST2","CAND_CITY","CAND_ST","CAND_ZIP")
c("CAND_ID","CAND_NAME","CAND_ICI","PTY_CD","CAND_PTY_AFFILIATION","TTL_RECEIPTS","TRANS_FROM_AUTH","TTL_DISB","TRANS_TO_AUTH","COH_BOP",
  "COH_COP","CAND_CONTRIB","CAND_LOANS","OTHER_LOANS","")
results <- read.csv('webl06.txt',sep='|',header=FALSE) %>% 
  select('V1','V24','V25')
 
Issues <- c("Abortion","Gun Rights","Taxes","Foreign Policy","Jobs","Civil Liberties","Big Business")
big_daddy <- inner_join(finance,candidate,by='CAND_ID') %>% 
  right_join(results,by=c("CAND_ID" = "V1")) %>% 
  rename("GEN_ELECTION" = "V24","GEN_ELECTION_PERCENT" = "V25") %>% 
  filter(CAND_OFFICE == "S", GEN_ELECTION != "", GEN_ELECTION_PERCENT != "", NAME != "", TRANSACTION_AMT > 1000, row_number() %% 3 != 1) %>% 
  select(NAME,CAND_OFFICE_ST,TRANSACTION_AMT,CAND_ID,CAND_NAME,CAND_PTY_AFFILIATION,GEN_ELECTION,GEN_ELECTION_PERCENT) %>% 
  mutate(Issues = sample(Issues,n(),replace = TRUE))

write.csv(big_daddy,'real_correlation_data.csv') 
