# Bombsquad Modded Server 
A modded server script for [Bombsquad](https://github.com/efroemling/ballistica) game engine (API 9).

## FEATURES
* **Administrative roles and tools:**
  - Special roles with chat commands.
  - Special tags for each roles.
  - 
* **Stats system:**
  - A system to show leaderboard players ranking em based on points
  - Provides stats of players e.g kills, games played, deaths, e.t.c.
  - 
* **Currency system:**
  - Advanced and updated currency system
  - Buy vip commands or vip roles
  - Buy special tags or effects
  - 

* **Effects and Tags:**
  - Plenty of cool special effects to choose from
  - Customize your own tag
  - 
* **Commands:**
  - Chat commands for owners, admins, and vips
  - 
* **Discord:**
  - Full discord bot integration
  - Owners can give roles, effects, and tags all from discord
  - Transfer currency to other users
  - Stream live stats from game to discord
  - Slash commands included
  - 
* *This was made with mobile so the codes might be a bit junky*

## VERSION
* **1.0 beta**

## INSTALLATION
1. Create Ec2 server with popular cloud hosting services like Aws, Oracle, Digiocean, e.t.c.
2. Make an instance(Ubuntu 22+).
4. Update packages and install python
   ```bash
   sudo apt update && sudo apt install -y software-properties-common
   sudo add-apt-repository -y ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install -y python 3.11  
5. clone scripts
   ```bash
   git clone https://github.com/itsre3/bombsquad-server

   # Give file permisions
   cd Bombsquad-server
   chmod 777 bombsquad_server
   chmod 777 config.toml
   chmod 777 dist/bombsquad_headless
6. Edit config.toml and settings.json in (dist/ba_root/mods)
7. ```bash
    ./bombsquad_server
8. Ur server should be up and running if you did all right.


## Note
* Currently, it only works on x86 system.
* Might get some weird prints on running, just ignore. Like I said, it’s not a perfect art but I did my best Xd.
* This will constantly get update and in its beta phase.
* Made proudly with my mobile phone.
* If you have ideas or cool addons, please join [this discord](https://discord.gg/bombsquad-community-server-588424129972142123), tag @itsre3 and I’ll get to ya.
* **Want server scripts flawless and better than this, check [this out](https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server)**

## CREDITS
* **ME**
* **My TECNO Phone**
