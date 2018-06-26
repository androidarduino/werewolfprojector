#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
import os.path
import random
from pygame import mixer

mixer.init()

class Logic(object):
    # this should be loaded from config file
    m = { "img_1": "ww1.png", "img_2": "ww2.png", "img_3": "ww3.png", "img_4": "ww4.png", "img_5": "ww5.png", "img_6": "ww6.png", "img_7": "ww7.png", "img_8": "ww8.png", "img_9": "ww9.png", "img_10": "ww10.png", "img_11": "ww11.png", "img_12": "ww12.png", "name_1": "周忆沁", "name_2": "学弟", "name_3": "冬冬", "name_4": "齐康", "name_5": "李森南", "name_6": "Zhen Xia", "name_7": "雲上小竹", "name_11": "张翔", "name_9": "Haohao", "name_10": "想当狼", "name_8": "时间静止", "name_12": "陈可梁" }
    masterVolumn = 0.5

    def processCmd(self, s):
        items = re.split(",|\s", s)
        print items
        verb = items[-1]
        nums = items[:-1]
        print "verb: ", verb, "players:",  nums
        home = ["home", "clear", "back", "h", "b", "c", "q"]
            #TODO:
            # more verbs:
        jj = ["jianjie", "jj", "简介", "介绍", "intro", "introduction"]
        fy = ["fayan", "fy", "speech", "talk", "发言", "说话"]
        zb = ["zb", "zibao", "自爆", "爆", "bao"]
        sj = ["sj", "shangjing", "上警", "竞选", "jx", "elect"]
        ts = ["ts", "tuishui", "tc", "tuichu", "退水", "退出", "quit", "withdraw"]
        yy = ["yy", "yiyan", "遗言", "lastwords"]
        fb = ["fb", "fanbai", "翻白", "是白痴", "白痴翻牌", "白痴", "bc", "fbc", "baichi", "shibaichi", "idiot"]
        fq = ["fq", "fanqiang", "翻枪", "是猎人", "猎人", "hunter", "flr", "lr", "qiang"]
        sw = ["sw", "siwang", "beidao", "chuju", "cj", "bd", "死亡", "被刀", "出局", "die", "killed", "kill"]
        fh = ["fh", "fuhuo", "live", "alive", "复活", "活", "huo"]
        tp = ["tp", "toupiao", "vote", "投票"]
        dx = ["dx", "dangxuan", "sherrif", "police", "dxjz", "jz", "dangxuanjingzhang", "jingzhang", "当选", "当选警长"]
        js = ["js", "jiashi", "jia", "加时", "bonus"]
        night = ["hy", "jrhy", "night", "dark"]
        wake = ["wake", "tll", "tl", "wakeup", "day", "stop"]
        effect = ["ohyeah", "win", "rowboat", "failed", "applause"]
        stop = ["s", "ting", "stop", "nosound"]
        openning = ["start"]
        # conveniencing sugar command, type a number, start speech
        if (verb.isdigit()):
            return "dlg_speech: " + verb
        for n in nums:
            try:
                num = int(n)
            except ValueError:
                num = 0
            if (num < 1 or num > 12):
                continue

            # picture changing event
            self.pic(verb, sw, "out.png", num)
            self.pic(verb, zb, "explode.png", num)
            self.pic(verb, sj, "election.png", num)
            self.pic(verb, ts, "withdraw.png", num)
            self.pic(verb, fb, "idiot.png", num)
            self.pic(verb, fq, "hunter.png", num)
            # display dialog with timer
            if (verb.lower() in fy):
                return "dlg_speech: " + str(num)
            if (verb.lower() in yy):
                return "dlg_lastwords: " + str(num)
            # live is a special case
            if (verb.lower() in fh):
                self.live(num)
            # introduction needs some special work
            if (verb.lower() in jj):
                return "dlg_intro: " + str(num)

        # other control words without numbers
        if (verb.lower() in js):
            self.playSound("levelup.mp3", 0.2)
            return "bonus"
        if (verb.lower() in tp):
            return "dlg_vote"
        if (verb.lower() in home):
            return "home"
        # crawn is a special case
        if (verb.lower() in dx):
            self.crown("sherrif.png", num)
        if (verb.lower() in night):
            # play a random bgm
            bgm = os.listdir(os.curdir + "/bgm")
            bgm.remove(".DS_Store")
            song = random.choice(bgm)
            print "selecting a music to play", song
            self.playSound("./bgm/" + song, 0.2)
            return "night"
        if (verb.lower() in wake):
            self.stopSound()
            return "day"
        if (verb.lower() in effect):
            mixer.music.fadeout(1000)
            self.playSound(verb.lower() + ".mp3", 0.2)
        if (verb.lower() in openning):
            mixer.music.fadeout(1000)
            self.playSound(verb.lower() + ".mp3", 1)
        if (verb.lower() in stop):
            mixer.music.stop()
        if (verb.lower() == "volup"):
            self.masterVolumn += 0.1
        if (verb.lower() == "voldown"):
            self.masterVolumn -= 0.1

        # write to disk to remember state
        self.write()
        return self.status()

    def pic(self, verb, words, text, num):
        sounds = {"explode.png": "explode.mp3", "idiot.png":"idiot.mp3", "hunter.png": "hunter.mp3"}
        if (verb.lower() in words):
            print text, ": ", num
            key = "img_" + str(num)
            self.m[key] = text
            if text in sounds:
                self.playSound(sounds[text])

    def light(self):
        s = list("bbbbbbbbbbbbbbbbbbbb")
        jzhm = 0
        img2char = {"election.png":"s", "out.png": "b", "ww1.png": "g", "wolf.png": "b", "idiot.png": "w", "hunter.png": "b", "explode.png": "b", "sherrif.png": "s", "withdraw.png": "y", "ww2.png": "g", "ww3.png": "g", "ww4.png": "g", "ww5.png": "g", "ww6.png": "g", "ww7.png": "g", "ww8.png": "g", "ww9.png": "g", "ww10.png": "g", "ww11.png": "g", "ww12.png": "g", "ww13.png": "g", "ww14.png": "g", "ww15.png": "g"}
        for player in self.m:
            [prefix, num] = player.split("_");
            if prefix == "img":
                s[int(num) - 1] = img2char[self.m[player]]
            if prefix == "addon":
                jzhm = int(num)
        print "sherrif is: ", jzhm
        if (jzhm > 0):
            s[jzhm - 1] = "r"
        return "".join(s)

    def playSound(self, file, volumn=1):
        if (not os.path.isfile(file)):
            return
        #TODO: play sound of file, create a dictionary
        # mode: [remind, finish, explode, NIGHT_MUSIC, idiot, hunter, extra_time, OTHERS]
        #sound_len = mixer.Sound(file).get_length()
        mixer.music.stop()
        try:
            mixer.music.load(file)
        except:
            return
        # control volumn
        mixer.music.set_volume(volumn * self.masterVolumn)
        mixer.music.play()
        print "playing sound"

    def stopSound(self):
        mixer.music.fadeout(1000)

    def nothing(self, num):
        print "todo..."

    def crown(self, pic, num):
        print "crown: ", num
        key = "addon_" + str(num)
        for k, v in self.m.items():
            if k.startswith("addon_"):
                del self.m[k]
        self.m[key] = pic

    def live(self, num):
        print "live: ", num
        key = "img_" + str(num)
        self.m[key] = "ww" + str(num) + ".png"

    def status(self):
        s = ""
        for k in self.m:
            s = s + k + " " + self.m[k] + "\n"
        return s

    def write(self):
        file = open("status.txt", "w")
        file.write(self.status())

