# GitSearch CLI 

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Gitsearch CLI is a github search tool that enables people to search
repositories and get various information about them using Github API

## Features

- Search Github Repositories by given string
- Sort data in ascending or descending order
- Ignore desired repositories by name


## Project Installation

### Without Docker

Gitsearch CLI requires [Python3](https://www.python.org/) v3.6+ to run.

Instructions to install the dependencies and start the CLI.

```sh
cd gitsearch
pip install --editable .
gitsearch --help
```
> Note: Use gitsearch ---help to make sure that everything worked as desired

> Note: you can use `cli_test.py` file located in the tests folder to test project against various test cases

## Docker

Gitsearch CLI is very easy to install and deploy in a Docker container.

```sh
cd gitsearch
docker build -t gitsearch --rm .
```
This will create the gitsearch image and pull in the necessary dependencies.

Once done, run the Docker image as seen in the example
```sh
docker run -t -i gitsearch -r arg_name
```


Verify the deployment by running test search query of your desired repository.

```sh
docker run -t -i gitsearch -r teststr
```
# How to use 

GitHub CLI is a simple app that can be used to receive Github repositories search information. It enables people to get various information about them using Github API

> Note! Gitsearch CLI displays data in table, which is RESPONSIVE to the user's terminal size, as long as user does not use docker, since docker uses simulated terminal and there is no way determinig size of terminal in this case.

</br>


### CLI call example



</br>

## Example 1:

</br>

Gitsearch CLI acceepts several arguments, let's start with the:
```-r, --reponame```
> Note! this is a required argument, which can be used to enter a search string


Let's provide data to the argument 😎

```
gitsearch -r repo_name
```

```
docker run -t -i gitsearch -r repo_name
```
In this case API will return: 

![Example 1](/assets/img/example1.png "First Example")
</br>
> At the end of the screen, for pagination purposes, two options are promoted for a page navigation

 - Use UP, DOWN arrow keys to navigate throught pages

 - Input desired page number by pressing to ":" + page number

![Example 1 continuation](/assets/img/example1_cont.png "First Example continuation")

## Example 2:

</br>

To sort data one can use:
```-s, --sort```

> this is a optional argument, which can be used to sort data by name in ascending or descending order 


Let's provide data to the argument 😎

```
gitsearch -r repo_name -s asc
```
```
docker run -t -i gitsearch -r repo_name -s asc
```

In this case API will return sorted data ascending order: 

![Example 2](/assets/img/example2.png "Second Example")
</br>

#### let's try to sort data in descending order
```
gitsearch -r repo_name -s desc
```
```
docker run -t -i gitsearch -r repo_name -s desc
```

Which will give us
</br>

![Example 2 continuation](/assets/img/example2_cont.png "Second Example")

</br>
Data sorted in descending order

</br>


## Example 3:

</br>

We also can ignore some repositories by using:
```-i, --ignore```

> this is a optional argument, which can be used to ignore data by name, or by list of the names

> Note! if you want to ignore multiple repositories, you can use "," as a delimiter

Example
- ```gitsearch -r repo_name -i name1,name2```

Let's provide data to the argument 😎

For example, if we want to ignore let's say first two elements of the data:

![Example 3](/assets/img/example3_1.png "Third Example")
</br>

We run the command:

```
gitsearch -r repo_name -i repokemon,meta-learning-lstm
```
```
docker run -t -i gitsearch -r repo_name -i repokemon,meta-learning-lstm
```

Which will result in:


![Example 2](/assets/img/example3_2.png "Second Example")
</br>

</br>

## License

MIT

**Free Software, Hell Yeah!**