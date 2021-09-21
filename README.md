# StarPins

Use channel pins as a managed starboard.

## Installation

You will need to install `poetry` to run this bot locally for levelopment, but running in docker is preferred for production deployment.

Poetry can be installed using the following command:

- Windows: `py -3 -m pip install poetry`.
- Linux/Mac: `python3 -m pip install poetry`.

To install the dependencies you can then run `poetry install` in the folder you cloned the repository to.

You need to copy `.env.example` to `.env` and fill in the appropriate values.

To run the bot run `poetry run task start` or `docker-compose up` to run with docker.

## Usage

To configure the starboard for a channel, navigate to the channel you wish to configure and enter the command 
`sp!setup`.
![image](https://user-images.githubusercontent.com/39353605/134232894-7c251819-b387-407e-81ed-c5126185a42b.png)

<hr/>

For more advanced config, you can use use the args `sp!setup [channel] [emoji] [count]` to setup the channel 
of the starboard, which emoji is used, and number of emojies required to be starred.
![image](https://user-images.githubusercontent.com/39353605/134234339-0b859ff1-bc67-47de-8a96-f09bbc336354.png)

<hr/>

To remove the channel from being tracked by the starboard, use the command `sp!remove` in the desired channel.
(You can optionally pass the channel to be removed as an argument).
![image](https://user-images.githubusercontent.com/39353605/134233009-ebb38fd8-d74e-4bf0-87ae-47fc00d6f4ee.png)
