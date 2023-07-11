# RankedSearchEngine

In this project, we want to expand the information retrieval model and represent the documents in vector form so that we can rank the search results based on their relevance to the user's query. In this way, a numerical vector is extracted from each document, which is the representation of that document in the vector space, and these vectors are stored. When receiving a query, first create the vector corresponding to that query in the same vector space, and then, using a suitable similarity criterion, compare the numeric vector of the query with the vector of all documents in the vector space.
and finally the output results are sorted based on the degree of similarity. To increase the response speed of the information retrieval model, various methods can be used, which are described in detail below.

# Document modeling in vector space
In the previous project, after extracting the tokens, the information was stored in the form of a dictionary and a location index.
In this section, the aim is to represent the documents in the vector space. Using the tf-idf weighting method, 
a numerical vector will be calculated for each document, and finally each document will be represented as a vector 
containing the weights of all the words in that document. Calculating the weight of each word t in a document d by having 
the set of all documents D is calculated using the following equation:

![image](https://github.com/MahdiTheGreat/RankedSearchEngine/assets/47212121/8e489bf2-2b27-4f92-9a95-1b6f0420c455)

where f_t,d is the number of repetitions of the word t in document d and n_t is the number of documents in which the word t appears. More details of this method are given in chapter 6 of the reference book. In the above vector representation, zero weight is considered for a word that does not exist in a document, and therefore many elements of the calculated vectors will be zero. To save memory, instead of considering a full numeric vector for each document, where many elements are zero, we can store the word weights in different documents in the same post lists. At the time of answering the user's question (which will be explained further) and the same time as searching for words in the postings list, we can also fetch the weight of the words in different documents and in this way only the non-zero elements of the document vectors are stored and processed.
