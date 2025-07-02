This project aims to create a conversational AI assistant named "Neo-Sama" that is designed to be "helpful" The development is heavily inspired by vedal and his work, with a focus on creating an engaging and informative conversation experience.

the defalt model is gemma3:1b, and will use gemma3 (they change alot) if more then 10 gb of ram and this will work with some Chain-of-thought (CoT) models ex deepseek r1

requirements.txt is not updated much so be worend

on mac you need to run with sudo

example audio of a suroke
<audio controls>
  <source src="suroke.wav" type="audio/wav"> 
  <a href="suroke.wav">Download audio</a>
</audio>

we have discord bot suport you need to add your token to .env.example and rename it to .env and run discord_bot.py
it works with 11 labs if you fell like it

## License
Neo-sama  © 2025 by DJkitty &amp; chris is licensed under CC BY-NC-ND 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/


pipreqs . --ignore .venv
