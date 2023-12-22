#coding: utf-8
from fuzzywuzzy import process
from colorama import init,Fore
import time,logging,os,sys
init(autoreset=True)
access={"server":5,"admin":4,"player":3,"spectators":2,"banned":1}
logger = logging.getLogger(name='r')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
# 写到文件
file_handler = logging.FileHandler(f"./logs/{time.strftime('%Y.%m.%d_%H.%M.%S.log')}")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# 写到屏幕
screen_handler = logging.StreamHandler()
screen_handler.setLevel(logging.INFO)
screen_handler.setFormatter(formatter)

players=[["Server",access.get("server"),"127.0.0.1"]] # [[玩家名,权限级,IP],别的玩家]
logging.basicConfig(filemode="a",level=logging.INFO,format=f'{Fore.LIGHTMAGENTA_EX} %(asctime)s {Fore.RESET}- {Fore.CYAN} %(levelname)s {Fore.RESET}: {Fore.LIGHTYELLOW_EX}%(message)s', datefmt='%y-%b-%d %H:%M:%S') # 设置logger格式

class game:
    server_running=True
    paint=[[i, j, "#FFFFFF"] for j in range(1024) for i in range(1024)]
    def command_interpreter(prompt):
        print(f"{Fore.LIGHTYELLOW_EX}Welcome to kris's draw & guess game server!\n{Fore.CYAN}this is game command interpreter, use 'help' command to get help.\n{Fore.LIGHTRED_EX}Current Time: {time.strftime('%Y-%m-%d.%H:%M:%S')}\n")
        while game.server_running==True:
            try:
                command=str(input(prompt))
                commands.execute("Server",command)
                if players[0][0] != "Server":
                    logging.error(f"Server offline.")
                    game.stop()
            except TypeError as err:
                if command != "":
                    logging.error(f"The parameter error or command {command} does not exist.")
                    detect=process.extractOne(command, commands.command_access.keys())
                    if detect[1] >= 85:
                        logging.warning(f"did you mean {detect[0]}...?")
            except KeyboardInterrupt:
                game.stop()
    def stop():
        sys.exit(0)

class commands:
    command_access = {"execute": 1, "kick": 4, "stop": 5, "modify_access":5, "get_commands": 1, "clean_logs": 4, "help": 1, "list": 1, "player_access": 5} # 指令权限等级
    alias = {"clean": "clean_log"} # 指令别名
    def execute(executer,command):
        for player in players:
            if player[0] == executer:
                compile=command.split(" ") # 以第一个参数为主命令，空格为参数
                try:
                    if player[1] >= commands.command_access.get(compile[0]):
                        logging.info(f"Player {player[0]}({player[1]}) executed command {command}({commands.command_access.get(compile[0])})")
                        exec(f"commands.{compile[0]}({(','.join(compile[1:]))})")
                        break
                    else:
                        logging.warning(f"Access denied: Player {player[0]}({player[1]}) executed command {command}({commands.command_access.get(command)})") # 权限不足
                except:
                    compile[0]=commands.alias.get(compile[0])
                    if player[1] >= commands.command_access.get(compile[0]):
                        logging.info(f"Player {player[0]}({player[1]}) executed command {command}({commands.command_access.get(compile[0])})")
                        exec(f"commands.{compile[0]}({(','.join(compile[1:]))})")
                        break
                    else:
                        logging.warning(f"Access denied: Player {player[0]}({player[1]}) executed command {command}({commands.command_access.get(command)})") # 权限不足

    def kick(player_name):
        for player in players:
            if player[0] == player_name:
                logging.info(f"Kicked {player_name}({player[2]})")
                player.remove(player_name)
                return
        logging.warning("Player Not Found")

    def stop(delay=0):
        if delay != 0:
            logging.warning(f"Game server will stop after {delay} seconds.")
        else:
            logging.warning(f"Game server stopping.")
        game.server_running = False
        time.sleep(delay)
        game.stop()

    def modify_access(command, new_access):
        if new_access > 5:
            logging.error("maximum access level(5) exceeded.")
            return
        elif new_access < 1:
            logging.error("minimum access level(1) exceeded.")
        logging.warning(f"Modifyed {command} access to {new_access}")
        commands.command_access[command]=new_access

    def get_commands():
        commands_list= [method for method in dir(commands) if not method.startswith('__') and callable(getattr(commands, method))]
        for command in commands_list:
            if command.startswith("_"):
                commands_list.remove(commands_list.index(command))
        logging.info(f"Command list: {','.join(commands_list)}")

    def clean_logs():
        logging.warning("Remove all log files from ./logs/ directory.")
        folder_path = './logs/'  # 指定文件夹路径
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)  # 获取文件路径
            if os.path.isfile(file_path):  # 判断是否为文件
                try:
                    os.remove(file_path)  # 删除文件
                except PermissionError:
                    pass

    def help(command=""):
        if command == "":
            print(f"{Fore.LIGHTGREEN_EX}Use 'get_commands' command to get command list. \nServer's access will be 5(maximum), if you are using server interpreter, you can execute all commands here.")
        else:
            if command == "get_commands":
                print("Usage: get_commands\nReturn: None\nRaise: None\n")
            elif command == "clean_logs":
                print("Usage: clean_logs\nReturn: None\nRaise: PermissionError(Catched)\n")
            elif command == "modify_access":
                print("Usage: modify_access 'function' level\nReturn: None\nRaise: TypeError(When you forget to add a quote)")
            elif command == "stop":
                print("Usage: stop delay\nReturn: None\nRaise: None")
            elif command == "kick":
                print("Usage: kick 'player_id'\nReturn: None\nRaise: ValueError(When ID is invalid)")
            elif command == "player_access":
                print("Usage: player_access 'player_id' 'new_access'\nReturn: None\nRaise: None")

    def list():
        lists=[]
        for player in players:
            lists.append(player[0])
        logging.info(f"Server players: {','.join(lists)}")

    def player_access(player, access_):
        for player_ in players:
            if player_[0] == player:
                new_access=access.get(access_)
                if new_access == None:
                    logging.warning(f"Access level {access_} not found. access list: {access}")
                else:
                    logging.info(f"Player {player_[0]}'s access updated to {access_}")
                    player_[1]=new_access
                return

game.command_interpreter(">>> ")