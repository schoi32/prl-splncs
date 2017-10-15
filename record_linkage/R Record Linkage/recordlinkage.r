# Author: Yongheng Lin
# Contributor: Sou-Cheng Choi
# Date: May 27, 2016 -- Aug 3, 2017
# Reference: Choi, Sou-Cheng T., Yongheng Lin, and Edward Mulrow. "Comparison of Public-Domain Software and Services for Probabilistic Record Linkage and Address Standardization,” Towards Integrative Machine Learning and Knowledge Extraction, Springer LNAI 10344, 2017. To appear. PDF available at http://tinyurl.com/ydxbjww4

suppressMessages(library(RecordLinkage))

data(RLdata10000)

system.time({ rpairs = compare.dedup(RLdata10000, identity = identity.RLdata10000) })
system.time({ rpairs = epiWeights(rpairs) })

res = epiClassify(rpairs, 0.53)
summary(res)
