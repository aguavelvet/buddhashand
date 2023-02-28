# Buddhashand

Buddha's hand is a simple streaming ETL tool that provides a rich set of functionalities with the ability to easily extend its' features.  This tool was originally written in Java.  I have decided to reimplement using Python, as python is faster to implement than Java.  In the near future, minimally, I will include Java Interfaces.

## Why [Buddha's hand](https://en.wikipedia.org/wiki/Buddha%27s_hand)?
A while back, in a project, all the component names were based on citrus fruits. For example, API-Gateway was called Lemon, the database server was called Grape Fruit, etc.  Buddha's hand is a citrus fruit predominantly available in Asia.  As this fruit has many finger like segments, it was thought to be an appropriate name because thish tool could also extend it's use in many different areas.

The general useability can be described as follows. 

## Sub-components
Buddha's hand is decomposed into three sections:
* InputProvider handles the reading the input source on a per record basis. Currenlty supports:
  	* Athena
  	* csv
	* http (TBD)
	* line based input
	* mongodb
	* mysql
	* psycopg2
	* range (useful for template generation)

* Transform  Transform allows the user to modify, reduce or extend the incoming input record.
* OutputHandler takes the transformed record and "persists" it to the persistent storage.  Although the term persistence is used here, but there is no reason why the output handlder could not behave more like a dispatcher.  For example, dispatching to a messaging queue. 

By decoupling the sub-components, following benefits are realized:
* Code is localized, smaller and therefore, easier to author and debug.See [csv input provider](https://github.com/aguavelvet/buddhashand/blob/master/src/input/csv_input_provider.py)
* Easier to integrate new code (say a new Input Provider)
* Any addition to the project extends it's functionality significantly.

For example, suppose we have the following input providers and output handlers:

| InputProvider       | OutputHandler |
| ------------------- | ------------- |
| CSV                 | CSV           |
| SQL                 | JSON          |

There are 4 combination of potential use cases. (CSV->CSV), {CSV->JSON), (JSON->CSV), (JSON->JSON).  Or I x O use cases, where I is the number of Input Providers and O is the number of Output providers.  If I = 5 and O = 6, we have a signficant coverages in the persistenct stores. 

### Possible InputProviders and OutputHandlers

- HTTP (Provided that Http Response is handed with records.
- NoSQL
- SQL (Output Handler could be micro-batching for performance)
- HDFS
- Hive
- Messaging Queue (As an inputprovider, this is an interesting case, since the tool runs infinitely)


## Use of Expression Parser
Transform sub-component is responsible for making the transformation on the input record. Transformation is made rich by using the [SimpleEval](https://github.com/danthedeckie/simpleeval) parser. Benefits are:

* uses natural python code. So, easy to write and test. 
* offers the richness of the expression parsing.
* offers extensiblity, through registration of functions and operators.

### Extensibility
SimpleEval allows the user to register user defined functions and operators.  By registering these functions, it allows significant degree of freedom in the desired outcome. See [functors.py](https://github.com/aguavelvet/buddhashand/blob/master/src/transform/functors.py) for examples. 



## Configuration File

Buddha's hand is driven by a json based configuration file. See [test1.json](https://github.com/aguavelvet/buddhashand/blob/master/test/test1.json) as an example.


### Notes on test1.json 
test1.json shows the flexibility of the use of SimpleEval in the transform section. In particular:
* Product, ProductType, Price are symbols resolved at run time for each record.
* All tokens are considered to be strings.  
* Hence, *mult* function was introduced to convert the string to float for the calculation


Given the input file test1.csv:

| ID  | ProductType |  Product  |  Price  |
| --- | ----------- | --------- | ------- |
|1|  fruit| apple|10|
|2|  fruit| orange|15|
|3|  fruit| pear|  8|
|4|  fruit| cherry| 15|
|5|  fruit| banana| 5|
|6|  vegetable| broccoli | 10|
|7|  vegetable| cauliflower| 10|
|8|  vegetable| green onions| 3|
|9|  vegetable| potato| 4|
|10| vegetable| tomato| 6|

Applying teh test1.json results in:

|Name|Price|On Sale|Sale Price|
| ---- | ----- | ------- | ----- |
|apple|10|False|10|
|orange|15|False|15|
|pear|8|False|8|
|cherry|15|True|19.5|
|banana|5|False|5|
|broccoli|10|False|10|
|cauliflower|10|False|10|
|green onions|3|False|3|
|potato|4|False|4|
|tomato|6|False|6|



### Notes on test2.json
I have added a prefilter for test2.json. We now filter in only the fruits. 

|Name|Price|On Sale|Sale Price|
| ---- | ----- | ------- | ----- |
|apple|10|False|10|
|orange|15|False|15|
|pear|8|False|8|
|cherry|15|True|9.0|
|banana|5|False|5|


### Notes on test3.json

Example of output with prefilter persisting to JSON format.

```json
{
    "comment" : "Buddha's hand samaple manifest directive. Buddhas hand is a simple streaming 'ETL' with decoupled Input, Transform and Output. By decoupling thes sub-components, we gain a tremendous amount of flexibility.  Moreover, because they are decoupled, we also reduce code complexity which results in easier to maintain code base. Secondly, any new providers (input and output) increases functionality of the code base. ",

    
    "input" : {
	"comment" : "simple csv input provider. Since each of the steps are decoupled, it is very easy to isolate different types of providers. Fewer lines of code makes it also easier to debug.", 
	"type" : "CSV",
	"input" : "/home/kirby/dev/projects/buddhashand/test/test1.csv",
	"delimiter" : ","
    },
    
    "transform": {
	"comment" : "transform here like map/reduce.  But Does not have to be.  Note that Product and Price are runtime variables that are resolved for each record.  Note also that the expression is natural python code snippet, which is very easily testable for correctness.  Lastly, 'mult' is a user defined functor. We need this method because the parser types all tokens as strings.  So, we need to convert $Price and '1.3' to numbers.",
	"type" : "default",
	"prefilter" : "ProductType == 'fruit'",
	"transform" : {
	    "Name" : "Product",
	    "Price"   : "Price",
	    "On Sale" : "True if ProductType == 'fruit' and Product == 'cherry' else False",
	    "Sale Price" : "mult(Price,0.6) if Product == 'cherry' else Price"
	}
    },
    
    "output" : {
	"type" : "JSON",
	"output" : "/home/kirby/dev/projects/buddhashand/test/test3.out.json"
    }
}
```

### Notes on [test4.mysql.json](https://github.com/aguavelvet/buddhashand/blob/master/test/test4.mysql.json)

This configuration shows a simple mysql input provider --> CSV output.
Note that the SELECT statement is "SELECT * FROM PRODUCT".  We could have easily made it to be:  "SELECT * FROM PRODUCT WHERE ProductType = 'fruit'
It's made more generic so you can see the prefilter capability of the transform section. Prefilter is useful, if we encounter a usecase that is difficult to express in SQL.

Also note that the output is persisted as a JSON output.

```
[
 {    "Name": "apple",     "Price": 10.0,    "On Sale": false,   "Sale Price": 10.0},
 {    "Name": "orange",    "Price": 15.0,    "On Sale": false,   "Sale Price": 15.0},
 {    "Name": "pear",      "Price": 8.0,     "On Sale": false,   "Sale Price": 8.0},
 {    "Name": "cherry",    "Price": 15.0,    "On Sale": true,    "Sale Price": 9.0},
 {    "Name": "banana",    "Price": 5.0,     "On Sale": false,   "Sale Price": 5.0}
]
```



### Notes on [test5.mysql.json](https://github.com/aguavelvet/buddhashand/blob/master/test/test5.mongodb.json)

This configuration file provides MongoDB input provider example persisted to CSV file.
Input script to mongodb is [here](https://github.com/aguavelvet/buddhashand/blob/master/test/test5.mongody.py). For all intent and purpose, this example is interesting because it contains a Profit and Loss vector, with 252 PnL entries.  These entries are used to compute VaR95 and Volatility, hooked in the transform section.  

The output is a simple [CSV file](https://github.com/aguavelvet/buddhashand/blob/master/test/test5.out.csv)



# Control Flow:

```
BuddahsHand.process() 
    InputProvider.start () 
        for each record from InputProvider:
            InputHandler.handle(record)
                orec = Transform.transform (record)
                OutputHandler.handle (orec)
           
    InputProvider.done () 
        InputProvider.done()
        OutputHandler.done()
```

# Running Buddha's Hand:

```
    python3 main.py -m /my/bh/config/test1.json
```


# Performance:
Performance of Buddha's hand was never measured, neither for this implementation or the the original Java version.  There two reason for that:
* BH was used as an enabling tool and not used in a mission critical setting.
* In the production setting, nothing stood out that required attention

## Memory
Since this is a streaming tool, it has very small memory foot print.  

## CPU
This tool uses a expression parser. Therefore, performance is not that great. For each record, expression parser is executed multiple times.  Having said that, BH is a IO bound tool. Therefore, optimizing the expression parser code will not significantly increase the overall performance.

Having said that, if optimization is desired, one could fold in desired expressions into a registered function.  For example, suppose you have the following expression:
``` a*b*ln(a,b) ```
You could write a function called foo that encapsulates the expression:
```foo(a,b)

def foo(a,b):
    return a*b*ln(a,b)

```

# Blue Skying


### Buddha's Hand chaining.  
As one can chain map/reduce functionality,  We can also perform the same using multiple Buddha's hands.

- Define Http Server Input Provider  (1/2 day developing time, using Flask)
- Define Http Client Output Provider ( 2 hours development time)

We now have a Transformation service that dispatches the transformation down the chain.  In a docker container, this chaining service could be easily deployed across a cloud environment.

### Buddha's Hand as a multiplexor. 

- Define Http Ouput Provider (Clients) that can connect to multiple servers. (1/2 day development)
- Configure transform to bucketize the input record.  Something like ``` uuencode (ID) % N ```  Where N is the number of Http Clients. 

### Refernce Key checker
Since the expression parser allows us to register functions, there is no reason why we could not take advantage of this feature. One area where the functions could be used is to load foreign keys.  
- On start up, load foreign keys from the database (1/2 day)
- define ref_check(foreign_key) method.

### Work Flow Service
The idea is to use the expression parser hooks to execute a set of tasks to solve a problem, using the mathematical rule of precendence and works entirely on side effects. It's a bit far fetched, but I see no reason why it could not work. W will an example to illustrate how a work flow service could work.

We want to execute the following expression:

```
     report (simulate (load_db(dsname) + partition(dsname) ) ~+ (market_data(bus_date))))
```

**Input:**
a single tuple that defines the parameter to a work flow.  (For example, dataset name, business date, runtime,  etc)

**Output:**

a tuple that shows each step that was executed, success fail status.

**Transform:**
executes the expression where:
- report is an aggregation service running on a node in a cluster somewhere.
- load_db is a tool that extracts data from the database
- partition is a bucketizing tool.
- market_data is a tool that grabs the market data for a given date.
- ~+ is a parallelize symbol. It will execute LHS at the same time as RHS.

Firstly, we note that the expression would adhere to the arithmatic rule of precedence. So, '()' are grouped.  Of course, *,/,+,- followign their precedence rule, although it doesn't really make a lot of sense in this context.

We make no assumptions that these are in process tasks. In other words, these services could be a client/server call accessing any other service that might be available in the network.

Then, according the the expression execution:

- simulate and market_data would execute in parallel
- Simulate:
	- load_db runs and loads data from the database. 
	- partition the loaded data.
- Market_data 
	- runs parallel to Simulate
- report waits until both simulate and market data finshes it's run.  

```
def parallelize (lhs, rhs):
    t1 = thread.start_new_thread (lhs) 
    t2 = thread.start_new_thread (rhs)
    t1.join ()
    t2.join ()
```

**Cool Factor:**  11
**Flexibility:** 10
**Usefulness:**  ?


# Conclusion
Buddhas hand is a simple tool that has many potential uses. It's configurability and ease of adding new features makes it a tool that can add value in many settings.  Personally, I think it would be a good tool in a data transformation area.  I welcome your comments.

Thanks.  Kirby


