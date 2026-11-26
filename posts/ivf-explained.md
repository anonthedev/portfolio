---
title: What is IVF?
date: 2026-11-26
description: IVF stands for inverted file. It speeds up vector search by skipping most of the vectors.
---

**IVF** stands for ***inverted file***. It speeds up vector search by skipping most of the vectors. But before getting into all that, let's look at what vector search is.

## What is vector search?
If you search a PDF, you are looking for the exact words. That is **keyword search**. **Vector search** matches by *meaning*.

You split the source into chunks and turn each chunk into a vector. You turn the query into a vector too. How that conversion works deserves its own post, so I'm not going to cover it here.

That vector stands for the meaning of the chunk. Two vectors that point the same way are similar, because the distance I use is the *angle* between them. How long the vectors are does not change the score. Take the query vector and find the chunk vectors with the smallest angle to it. Those chunks are the closest in meaning.

Scoring the query against every vector is exact. That full scan is also the slow part. The rest of this post is about how IVF skips most of those scores. Now let's get into what IVF is all about.

## How IVF works, at a high level
IVF speeds up the search process by searching through only selected vectors. The selection is based on clustering and then creating an inverted list of the vectors. We take all the vectors and partition them into different clusters. Then we only search the clusters whose centroids are closest to the query vector. That way, we can cut down the number of vectors that need to be searched by a massive amount. But this comes at a cost of **recall**: you can miss some of the nearest vectors, because they might be sitting at the edge of a cluster or in some other cluster that we didn't search.

Technically, the two phases are called the **indexing** phase and the **query** phase. Indexing is where you build the clusters and the inverted index.

## The clustering part
IVF searches fewer vectors because it divides them into clusters. It uses **k-means clustering** to split the vector space into regions called **Voronoi cells**. A Voronoi cell is the region of space that is closer to one centroid than to any other centroid. The **centroid** represents the cluster, and it is the *mean* of the vectors in that cluster.

k-means finds the centroids in a loop:
1. It starts with random guesses for the centroids.
2. It assigns every vector to the closest centroid.
3. It moves each centroid to the mean of the vectors assigned to it.
4. It repeats steps 2 and 3 until the assignments stop changing.

At that point, we have our clusters.

The **objective function** measures how good the clusters are, and k-means tries to make it as small as possible. It is the sum of the squared distances from each vector to its own centroid. A small sum means the vectors sit close to their centroids. A big sum means the clusters are spread out. So, *the smaller, the better*. We rarely get to say that, but that's the case here.

In my implementation, I used the angle between vectors as my distance, so I <u>normalize every vector to length 1 before clustering</u>. Without that step, k-means groups vectors by straight-line distance, and straight-line distance is not the same as angle.

The ***k*** in k-means clustering, meaning how many clusters the vector space should be divided into, is very important. It directly affects the cost and how efficient querying will be later on. In practice, setting *k* anywhere from **4 × √n to 16 × √n** works well, where *n* is the number of vectors in the vector space.

## The indexing part
Now that we have our clusters, we need a data structure that tells us which vectors each centroid holds. Right now, we can only answer *"Which cluster is this vector assigned to?"* After we build the inverted index, we can answer *"Which vectors are in this cluster?"*, and that is the question a search needs. This flip gives IVF its name: **inverted file**.

The index stores the list of centroids. For each centroid, it stores a list of the vector IDs in that cluster. Most implementations also store each cluster's vectors next to each other in memory, so scanning one cluster is fast. At query time, we open the lists of the clusters we picked and skip every other cluster.

## The querying part
Now for the part that saves you time: querying. Querying finds the vectors most similar to your query, so you first turn the query into a vector too.

A flat index compares the query against every vector. At query time, IVF compares the query vector against the centroids first. Then it searches only the vectors inside the closest clusters.

The catch is deciding how many clusters to search. That number is called **nprobe**. With nprobe set to 6, IVF searches the vectors in the 6 closest clusters and skips the rest. A higher nprobe finds more of the true nearest neighbours but searches more slowly. A lower nprobe is faster but can miss neighbours that sit just across a cluster boundary. <u>You pick nprobe by measuring recall and latency on your own data.</u>

*nprobe* depends on many factors, like how well the data is clustered, the number of centroids, etc. That's why, as I mentioned above, picking the correct *k* for clustering is very important.

## The boundary problem
Each vector belongs to **one cluster only**. IVF first searches the cluster whose centroid is closest to the query. A vector just across the boundary, in the next cluster, can be closer to the query than most of the vectors IVF scans. If the query lands near that boundary, its nearest neighbour may be in the next cell. With nprobe set to 1, IVF never opens that cell and misses the neighbour.

**Raising nprobe is the main fix.** Each extra cluster covers more of the space around the query, so IVF also scans the neighbours just across a boundary. Every added cluster costs more time. With 1,000 clusters and nprobe set to 10, IVF scans about **1%** of the vectors. With nprobe set to 100, it scans about **10%**.

There are two other fixes:
- **Store boundary vectors in more than one cluster.** This uses more memory but needs a smaller nprobe.
- **Use fewer, bigger clusters.** Fewer vectors sit near an edge, but each cluster takes longer to scan.

## How dimensionality affects IVF
Embedding models output vectors with hundreds or thousands of dimensions. At that size, the distance from a query to its nearest vector and the distance to its farthest vector get closer together. Near and far vectors become harder to tell apart.

This hurts IVF in two ways:
1. **k-means finds weaker clusters**, because each vector is only a little closer to one centroid than to the others.
2. **More vectors sit near a boundary**, so the query's true neighbours spread across more clusters.

To keep the same recall at a higher dimension, you need a <u>higher nprobe</u>.

Each comparison also gets slower, because a distance takes one multiplication per dimension. Scoring a 1,536-dimension vector costs **four times** as much as scoring a 384-dimension one. This applies to both the centroid comparisons and the cluster scans.

Text embeddings make the problem smaller. They don't fill their space evenly. They group around topics, so k-means finds useful clusters even at 1,536 dimensions. If search is still too slow, lower the dimension with **PCA** or use an embedding model with shorter vectors. Both cost a small amount of accuracy.

## My implementation
I built IVF from scratch in Go as part of **vecsearch**, my implementation of different vector search algorithms. You can find the code here: [github.com/anonthedev/vecsearch](https://github.com/anonthedev/vecsearch)