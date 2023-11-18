“电影关系图”实例将电影、电影导演、演员之间的复杂网状关系作为蓝本，使用Neo4j创建三者关系的图结构

创建图数据：将电影、导演、演员等图数据导入Neo4j数据库中

cypher语句：

```cypher
CREATE (TheMatrix:Movie {title:'The Matrix', released:1999, tagline:'Welcome to the Real World'})
CREATE (Keanu:Person {name:'Keanu Reeves', born:1964})
CREATE (Carrie:Person {name:'Carrie-Anne Moss', born:1967})
CREATE (Laurence:Person {name:'Laurence Fishburne', born:1961})
CREATE (Hugo:Person {name:'Hugo Weaving', born:1960})
CREATE (LillyW:Person {name:'Lilly Wachowski', born:1967})
CREATE (LanaW:Person {name:'Lana Wachowski', born:1965})
CREATE (JoelS:Person {name:'Joel Silver', born:1952})
CREATE
  (Keanu)-[:ACTED_IN {roles:['Neo']}]->(TheMatrix),
  (Carrie)-[:ACTED_IN {roles:['Trinity']}]->(TheMatrix),
  (Laurence)-[:ACTED_IN {roles:['Morpheus']}]->(TheMatrix),
  (Hugo)-[:ACTED_IN {roles:['Agent Smith']}]->(TheMatrix),
  (LillyW)-[:DIRECTED]->(TheMatrix),
  (LanaW)-[:DIRECTED]->(TheMatrix),
  (JoelS)-[:PRODUCED]->(TheMatrix)
```

每个cypher的意思如下，但是要整体运行，否则他们的关系不会连在前面8句中创建的节点上，因为最后面的7句运用到了前面CREATE时的变量，比如：最后一行JoelS变量就是对应的第8行的JoelS。单独运行也会产生关系，但是节点是Neo4j自动生成的，只有一个id。这个查询ACTED_IN类型的关系，上面的绿色和蓝色为整体运行cypher产生的，底下的全红是单独运行产生的，点击中间红点，可以看见左下角只有Neo4j自己生成的id(138)。



下面每步骤为单独运行和解释cypher：

1. 创建电影节点

```cypher
CREATE (TheMatrix:Movie {title:'The Matrix', released:1999, tagline:'Welcome to the Real World'})
```

此cypher语句使用CREATE指令创建了一个Movie节点。这个节点带有3个属性，{title:'The Matrix', released:1999, tagline:'Welcome to the Real World'}，分别代表电影标题，发行时间，宣传词。btw：The Matrix（黑客帝国）带你进入程序世界，程序员必看电影。单独运行完之后则创建了一个节点

2. 创建人物节点

```cypher
CREATE (Keanu:Person {name:'Keanu Reeves', born:1964})
CREATE (Carrie:Person {name:'Carrie-Anne Moss', born:1967})
CREATE (Laurence:Person {name:'Laurence Fishburne', born:1961})
CREATE (Hugo:Person {name:'Hugo Weaving', born:1960})
CREATE (LillyW:Person {name:'Lilly Wachowski', born:1967})
CREATE (LanaW:Person {name:'Lana Wachowski', born:1965})
CREATE (JoelS:Person {name:'Joel Silver', born:1952})
```

3. 创建演员导演关系

```cypher
CREATE
  (Keanu)-[:ACTED_IN {roles:['Neo']}]->(TheMatrix),
  (Carrie)-[:ACTED_IN {roles:['Trinity']}]->(TheMatrix),
  (Laurence)-[:ACTED_IN {roles:['Morpheus']}]->(TheMatrix),
  (Hugo)-[:ACTED_IN {roles:['Agent Smith']}]->(TheMatrix),
  (LillyW)-[:DIRECTED]->(TheMatrix),
  (LanaW)-[:DIRECTED]->(TheMatrix),
  (JoelS)-[:PRODUCED]->(TheMatrix)
```

 CREATE下面前4行创建演员与电影的关系，后3句创建导演与电影的关系。

(Keanu)-[:ACTED_IN {roles:['Neo']}]->(TheMatrix)的意思是演员Keanu在电影TheMatrix中扮演Neo角色roles:['Neo']。

(LillyW)-[:DIRECTED]->(TheMatrix)的意思是LillyW导演了[:DIRECTED]电影TheMatrix。





## 作业一

运行整体cypher图数据结构创建完成后，查找人员

1. 查找名为Carrie-Anne Moss的人

   ```
   match (n:Person{name:"Carrie-Anne Moss"} )return n
   ```
   
   
   
2. 查询谁导演了The Matrix

```
match (n:Movie{title:"The Matrix"})-[r:PRODUCED]-(n2:Person)
return n2.name
```



## 作业二

执行 movie_full_info.txt中的cypher语句

查询1950年之前出生的演员

```
match (n:Person)
where n.born<1950
return n.name ,n.born
```

查询 "Sleepless in Seattle" 电影的演员有哪些

```
match (n:Movie{title:"Sleepless in Seattle"})-[r:ACTED_IN]-(P:Person)
return P.name
```

查询 "Tom Hanks" 出演哪些电影

```
match (n:Person{name:"Tom Hanks"})-[r:ACTED_IN]-(M:Movie)
return M.title
```

查询"Hoffa" 电影中最年轻的演员，导演

```
match(M:Movie{title:"Hoffa"})-[r:ACTED_IN]-(P:Person)
return P.born,P.name
order by P.born desc LIMIT 1
```

