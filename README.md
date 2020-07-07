# buddhashand

Buddha's hand is a simple streaming ETL tool that provides a rich set of functionalities with the ability to easily extend its' features. The general useability can be described as follows. 

## Sub-components
Buddha's hand is decomposed into three sections:
* InputProvider handles the reading the input source on a per record basis. 
* Transform  Transform allows the user to modify, reduce or extend the incoming input record.
* OutputHandler takes the transformed record and "persists" it to the persistent storage.  Although the term persistence is used here, but there is no reason why the output handlder could not behave more like a dispatcher.  For example, dispatching to a messaging queue. 

By decoupling the sub-components, following benefits are realized:
* Code is localized, smaller and therefore, easier to author and debug.
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
- HDFS
- Hive
- Messaging Queue (As an inputprovider, this is an interesting case, since the tool runs infinitely)


## Use of Expression Parser
Transform sub-component is responsible for making the transformation on the input record. Transformation is made rich by using the [SimpleEval](https://github.com/danthedeckie/simpleeval) parser. Benefits are:

* uses natural python code. So, easy to write and test. 
* offers the richness of the expression parsing.
* offers extensiblity.

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


# Running Buddha's Hand:

python3 main.py -m /my/bh/config/test1.json




