# FixChat
Are you tired of being a dry chatter? Are you interested in other persons chats but can't express your self so you chat dry and the others think you aren't interested? Well i have the same problem. This is a begin of a new project i am going to make. It uses an llm to train your chatting in a phone looking gui. Fully made in python and usses ollama  

# Today 19-02-2026  
I finaly Finished my prototype V1.0.  
It runs fully local with ollama with qwen3-vl:8b  
I made it so once ran it opens a pygame window. Looks a bit like a phone.  
Before the guy pops up there are the chat name that you still have to select in the terminal. There are already a few random chat names i wrote my self so if you leave chat name empty it will select an random name that i wrote.  
Then you will have to select an random gender. There are random genders so if you leave that also blank it will select one of the preloaded genders i could think of.  
There is an Analyze Button on the top left what that does it will put all the logs thru the same ai model nad will say what you could do beter on your side of the text's
So like an diagnostics. That will be saved in two different filles one will be an simple .txt fille and the other one will be spat out in an cvs format.  

# Run
For the script to run you will need all the Library's installed  
```bash
pip install ollama pygame
```
Also i use the ollama Qwen3-vl:8b model but feel free to use what you want. But i think that if you might go lower like 1b it will feel worse definitely the diagnostics.  
Make sure you have ollama installed.  
How to download the model
```bash
ollama pull qwen3-vl:8b #but you can always use your own preffered model
```
# Linux
This is how to run the script and how to use it.
```bash
#make sure you have everything you need.
git clone https://github.com/ermwhatesigma/FixChat
cd FixChat
#if you didn't install pygame or ollama for python also run this real quick
pip install ollama pygame
python FixChatV1-0.py
#If you have python3 just put 3 in the end of python
```
This will run the script. But like i said before the pygame wi

# Open AI script
The open ai script runs on windows and linux. It uses the free api keys from the open router.  
How to run it  
```bash
git clone https://github.com/ermwhatesigma/FixChat
cd FixChat #First we need to save the api keys with the api key saver
python OpenAI-api-save.py
```
Then you put your own api key you pulled from openRouter in the script that will save it in the file format.  
You can select in the begin of the script how many different api keys you want.  
Then you put your first api key and the the others if you have others.  
After you saved the api keys with the script you just ruin the main script  
Get your free api key https://openrouter.ai/
```bash
#make sure you have openai installed
pip install openai
python FixChatV1-0-OpenAI.py #after you saved the main api keys
```
Thats all to run the api keys script in python.  
# Genai script
You can get the free api key in https://aistudio.google.com/  

Setting up the api keys. You will have to run
Then you will have to sellect option 2 and then you sellect how many api keys and thats it.
```bash
python All-API-saver.py
```
Then run the script thats all
```bash
#make sure you have genai installed
pip install google-genai
python FixChatV1-0-Google.py
```
ndow pops up you will have to set the chat name in the terminal and also the gender of the ai.  
Leave them blank for an random choice that i tought of.
# Example
Here is an usage of the script  
[![Watch the video](https://img.youtube.com/vi/hjp1usZjRTs/0.jpg)](https://www.youtube.com/watch?v=hjp1usZjRTs)
# Conclusion
I also wanna make this project for phone like on an android to start with.  
The project on the phone will use api keys. I will and try to make 2 different android versions. One for open ai free api keys and the other one with google free api keys.
The api keys will be saved in the phone itself so you won't need to retype them the whole time. Also on the phone apk file i won't make a server for it i am to broke for it.  
So no api keys will be saved online only localy. You would also be able to select from different ai models on the phone from like open ai and google.  
If the requests are stopped with one api key you could just use one from another gmail account for free.  
But first i gota make the free api script work on PC python so i have an insight on how i could make it look like.  
That is my goal. Support will be praised, more like positive comments
