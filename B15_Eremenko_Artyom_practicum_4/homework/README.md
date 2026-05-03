# Домашнее задание "DFS с postvisit методом"

## Постановка задачи

Реализовать обход графа в глубину без использования рекурсии с вызовами previsit и postvisit методов. Более конкретно, необходимо реализовать метод `DfsViaLifoQueueWithPostvisit.run()` в файле `dfs_with_postvisit.py`. 

## Ожидаемый результат

Заполненный файл `dfs_with_postvisit.py`, запускаемый без ошибок из корня репозитория
```bash
$ python practicum_4/homework/dfs_with_postvisit.py
```

# Домашнее задание "Алгоритм Дейкстры"

## Постановка задачи

Реализовать алгоритм Дейкстры в файле `dijkstra.py`. Более конкретно, необходимо реализовать метод `DijkstraAlgorithm.run()`. 

## Ожидаемый результат

Заполненный файл `dijkstra.py`, запускаемый без ошибок из корня репозитория
```bash
$ python practicum_4/homework/dijkstra.py
```

## Необходимая теория

Алгоритм Дейкстры решает задачу поиска кратчайших путей на взвешенном графе. При работе алгоритма поддерживается очередь доступных к добавлению ребер. На конкретной итерации добавляется ребро с наименьшим значением веса. После этого в рамках той же итерации добавляются ребра, связанные с вновь добавленной вершиной.

![graph from maze](images/graph_from_maze_dijkstra_1.svg)

![graph from maze](images/graph_from_maze_dijkstra_2.svg)

![graph from maze](images/graph_from_maze_dijkstra_3.svg)

![graph from maze](images/graph_from_maze_dijkstra_4.svg)

![graph from maze](images/graph_from_maze_dijkstra_5.svg)

Как и любой другой алгоритм обхода графа, алгоритм Дейкстры строит дерево обхода. В данном случае оно будет деревом кратчайших путем на взвешенном графе с неотрицательными весами.

![graph from maze](images/graph_from_maze_dijkstra_tree.svg)
