# rest-api-development

CS5331 Assignment 1 Project Reference Repository

## Instructions

Your objective is to implement a web application that provides the endpoints
specified here: https://cs5331-assignments.github.io/rest-api-development/.

The project has been packaged in an easy to set-up docker container with the
skeleton code implemented in Python Flask. You are not restricted in terms of
which language, web stack, or database you desire to use. However, please note
that very limited support can be given to those who decide to veer off the
beaten path.

You may be required to modify the following files/directories:

- Dockerfile - contains the environment setup scripts to ensure a homogenous
  development environment
- src/ - contains the front-end code in `html` and the skeleton Flask API code
  in `service`
- img/ - contains images used for this README

Assuming you're developing on an Ubuntu 16.04 machine, the quick instructions
to get up and running are:

```
# Install Docker

sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce

# Verify Docker Works

sudo docker run hello-world

# Run the skeleton implementation

sudo ./run.sh
```

(Docker CE installation instructions are from this
[link](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository).)

**Please consult your assignment hand-out for detailed setup information.**

## Grading

The implementation will be graded in an automated fashion on an Ubuntu 16.04
virtual machine by building the docker container found in your repository and
running it. The grading script will interact with your API.

The following ports are expected to be accessible:

1. 80, on which static HTML content, including the front-end, is served.
2. 8080, on which the API is exposed.

To verify this, please run the following commands:

```
sudo ./run.sh
```

On a different window:

```
curl http://localhost:80
curl http://localhost:8080
```

If a response is received, you're good to go.

**Please replace the details below with information relevant to your team.**

## Screenshots

Please replace the example screenshots with screenshots of your completed
project. Feel free to include more than one.

![Sample Screenshot](./img/samplescreenshot.png)

## Administration and Evaluation

Please fill out this section with details relevant to your team.

### Team Members

1. LAU Wee You
2. LEE Zi Shan
3. SIA Wei Kiat Jason
4. ZHOU Zhi Zhong

### Short Answer Questions

#### Question 1: Briefly describe the web technology stack used in your implementation.

Answer: Please replace this sentence with your answer.

#### Question 2: Are there any security considerations your team thought about?

Answer: Please replace this sentence with your answer.

#### Question 3: Are there any improvements you would make to the API specification to improve the security of the web application?

Answer: Please replace this sentence with your answer.

#### Question 4: Are there any additional features you would like to highlight?

Answer: Please replace this sentence with your answer.

#### Question 5: Is your web application vulnerable? If yes, how and why? If not, what measures did you take to secure it?

Answer: Please replace this sentence with your answer.

#### Feedback: Is there any other feedback you would like to give?

Answer: Please replace this sentence with your answer.

### Declaration

#### Please declare your individual contributions to the assignment:

1. LAU Wee You
    - Implemented z
2. LEE Zi Shan
    - Implemented z
3. SIA Wei Kiat Jason
    - Implemented z
4. ZHOU Zhi Zhong
    - Implemented z



/* Actual Document Starts Here*/

Database Schema

Table
users {
  username: varchar (255) not null,
  fullname: varchar (255) not null,
  salt: varchar (255) not null,
  hashed_password: varchar (255) not null,
  age: int not null
}

diary_entries {
  id: int primary key auto increment, 
  title: varchar (255) not null,
  author: varchar (255) not null,
  publish_date: datetime not null, 
  public: boolean not null, 
  text: text

}

members {
  name: varchar (255) not null
}