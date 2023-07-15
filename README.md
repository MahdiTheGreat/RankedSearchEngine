# RankedSearchEngine

In this project, we want to expand the information retrieval model and represent the documents in vector form so that we can rank the search results based on their relevance to the user's query. In this way, a numerical vector is extracted from each document, which is the representation of that document in the vector space, and these vectors are stored. When receiving a query, first create the vector corresponding to that query in the same vector space, and then, using a suitable similarity criterion, compare the numeric vector of the query with the vector of all documents in the vector space.
and finally, the output results are sorted based on the degree of similarity. Various methods can be used to increase the response speed of the information retrieval model, which are described in detail below.

# Document modeling in vector space
In the previous project, after extracting the tokens, the information was stored in the form of a dictionary and a location index.
In this section, the aim is to represent the documents in vector space. Using the tf-idf weighting method, 
a numerical vector will be calculated for each document, and finally, each document will be represented as a vector 
containing the weights of all the words in that document. Calculating the weight of each word t in document d by having 
the set of all documents D is calculated using the following equation:

![image](https://github.com/MahdiTheGreat/RankedSearchEngine/assets/47212121/af39be8b-3a44-4dd7-a41c-cb2bf34ad54e)


where f_t,d is the number of repetitions of the word t in document d and n_t is the number of documents in which the word t appears. More details of this method are given in chapter 6 of the reference book. In the above vector representation, zero weight is considered for a word that does not exist in a document, and therefore many elements of the calculated vectors will be zero. To save memory, instead of considering a full numeric vector for each document, where many elements are zero, we can store the word weights in different documents in the same post lists. At the time of answering the user's question (which will be explained further) and at the same time as searching for words in the postings list, we can also fetch the weight of the words in different documents, and in this way, only the non-zero elements of the document vectors are stored and processed.

# Answering the question in vector space
With the user's question, the special vector of the question is extracted (the weight of the words in the question is calculated), and then, using the similarity criterion, it is tried to find the documents that have the most similarity (the least distance) to the input question. The results are then displayed in order of similarity. Various distance measures can be considered for this task, the simplest of which is the cosine similarity between vectors, which calculates the angle between two vectors. This criterion is defined as follows:

![image](https://github.com/MahdiTheGreat/RankedSearchEngine/assets/47212121/06acfe6f-7f2a-4fe3-92a3-e2236b4300d2)

To increase response time, we can use the Index elimination technique to not calculate cosine similarity with documents that will score zero. Finally, to display a page of query results, it is enough to select K documents that are most similar to the query.

# Increasing the speed of query processing

By using the Index elimination technique, the problem of high response time in the previous step is solved to some extent, but the response time is still not acceptable for many applications. In order to increase the speed of processing and response, we can use Champion lists before a query is raised and in order to do that, during the document processing stage, a list of the most relevant documents related to each term is kept in a separate list. To implement this section, after creating the spatial-inverted index( which we use to calculate tf-idf weights as well), we create the Champion lists and compare only the query vector with the document vector obtained by searching the Champion list and displaying k related documents. More details of this method are given in chapter 7 of the book, "An Introduction To Information Retrieval" by Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze.





