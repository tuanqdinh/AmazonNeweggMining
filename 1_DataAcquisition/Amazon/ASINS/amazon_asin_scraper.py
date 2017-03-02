import csv
import random
from lxml import html  
import json
import requests
import json,re
from dateutil import parser as dateparser
from time import sleep
from random import shuffle
import os


def ParseProducts(bnode, page):
	amazon_url = "http://www.amazon.com/b/?ie=UTF8&node="+bnode+"&page="+str(page)

	useragents = [	#'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
			##'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41', 
			#'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',  
			##'Googlebot/2.1 (+http://www.google.com/bot.html)',
			#'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'
			"Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
			"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
			"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
			"Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0",
			"Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
			"Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
			"Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
			"Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
			"Mozilla/2.02E (Win95; U)",
			"Mozilla/3.01Gold (Win95; I)",
			"Mozilla/4.8 [en] (Windows NT 5.1; U)",
			"Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
			"Opera/7.50 (Windows XP; U)",
			"Opera/7.50 (Windows ME; U) [en]",
			"Opera/7.51 (Windows NT 5.1; U) [en]",
			"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.0",
			"Opera/9.25 (Windows NT 6.0; U; en)",
			"Opera/9.80 (Windows NT 5.2; U; en) Presto/2.2.15 Version/10.10",
			"Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10",
			"Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
			"Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.2b) Gecko/20021001 Phoenix/0.2",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.23) Gecko/20090825 SeaMonkey/1.1.18",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser; Avant Browser; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Beamrise/17.2.0.9 Chrome/17.0.939.0 Safari/535.8",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1",
			"Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0",
			"Mozilla/5.0 (Windows NT 6.2; rv:19.0) Gecko/20121129 Firefox/19.0",
			"Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0",
			"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0",
			"iTunes/9.0.2 (Windows; N)",
			"Mozilla/5.0 (compatible; Konqueror/4.5; Windows) KHTML/4.5.4 (like Gecko)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Maxthon 2.0)",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML like Gecko) Maxthon/4.0.0.2000 Chrome/22.0.1229.79 Safari/537.1",
			"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/5.0)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; WOW64; Trident/5.0)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0)",
			"Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
			"Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C)",
			"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.7.62 Version/11.01",
			"Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
			"Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.16",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.12 Safari/537.36 OPR/14.0.1116.4",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.29 Safari/537.36 OPR/15.0.1147.24 (Edition Next)",
			"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36 OPR/18.0.1284.49",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36 OPR/19.0.1326.56",
			"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
			"Mozilla/5.0 (Windows; U; Windows NT 6.2; es-US ) AppleWebKit/540.0 (KHTML like Gecko) Version/6.0 Safari/8900.00",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
			"Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20120422 Firefox/12.0 SeaMonkey/2.9",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.79 Safari/537.4",
			"Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
			"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
			"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0",
			"Mozilla/4.0 (compatible; MSIE 5.15; Mac_PowerPC)",
			"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.15",
			"Opera/9.0 (Macintosh; PPC Mac OS X; U; en)",
			"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/85.8",
			"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8",
			"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fr-fr) AppleWebKit/312.5 (KHTML, like Gecko) Safari/312.3",
			"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Camino/2.2.1",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre Camino/2.2a1pre",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.31 (KHTML like Gecko) Chrome/26.0.1410.63 Safari/537.31",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 1083) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:20.0) Gecko/20100101 Firefox/20.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0",
			"iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)",
			"iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0.112941",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0",
			"Opera/9.20 (Macintosh; Intel Mac OS X; U; en)",
			"Opera/9.64 (Macintosh; PPC Mac OS X; U; en) Presto/2.1.1",
			"Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.6.30 Version/10.61",
			"Opera/9.80 (Macintosh; Intel Mac OS X 10.4.11; U; en) Presto/2.7.62 Version/11.00",
			"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; de-de) AppleWebKit/534.15  (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7; en-us) AppleWebKit/534.20.8 (KHTML, like Gecko) Version/5.1 Safari/534.20.8",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.26.17 (KHTML like Gecko) Version/6.0.2 Safari/536.26.17",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.5; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
			"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.0.13.81_10003810) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true",
			"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.4 (KHTML, like Gecko) Chrome/4.0.237.0 Safari/532.4 Debian",
			"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.277.0 Safari/532.8",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15",
			"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.613.0 Chrome/10.0.613.0 Safari/534.15",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1",
			"Mozilla/5.0 Slackware/13.37 (X11; U; Linux x86_64; en-US) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41",
			"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.825.0 Chrome/14.0.825.0 Safari/535.1",
			"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2",
			"Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Epiphany/1.2.5",
			"Mozilla/5.0 (X11; U; Linux i586; en-US; rv:1.7.3) Gecko/20040924 Epiphany/1.4.4 (Ubuntu)",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.6) Gecko/20040614 Firefox/0.8",
			"Mozilla/5.0 (X11; U; Linux x86_64; sv-SE; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060309 Ubuntu/9.10 (karmic) Firefox/3.0.11",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090803 Ubuntu/9.04 (jaunty) Shiretoko/3.5.2",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091107 Firefox/3.5.5",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Linux Mint/8 (Helena) Firefox/3.5.3",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9",
			"Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8",
			"Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre",
			"Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20100101 Firefox/4.2a1pre",
			"Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0",
			"Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0",
			"Mozilla/5.0 (X11; Linux x86_64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1",
			"Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0",
			"Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0",
			"Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0 ",
			"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1",
			"Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Galeon/1.3.14",
			"Mozilla/5.0 (X11; U; Linux ppc; en-US; rv:1.8.1.13) Gecko/20080313 Iceape/1.1.9 (Debian-1.1.9-5)",
			"Mozilla/5.0 (X11; U; Linux i686; pt-PT; rv:1.9.2.3) Gecko/20100402 Iceweasel/3.6.3 (like Firefox/3.6.3) GTB7.0",
			"Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Iceweasel/5.0",
			"Mozilla/5.0 (X11; Linux i686; rv:6.0a2) Gecko/20110615 Firefox/6.0a2 Iceweasel/6.0a2",
			"Konqueror/3.0-rc4; (Konqueror/3.0-rc4; i686 Linux;;datecode)",
			"Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.6.8-gentoo-r3; X11;",
			"Mozilla/5.0 (compatible; Konqueror/3.5; Linux 2.6.30-7.dmz.1-liquorix-686; X11) KHTML/3.5.10 (like Gecko) (Debian package 4:3.5.10.dfsg.1-1 b1)",
			"Mozilla/5.0 (compatible; Konqueror/3.5; Linux; en_US) KHTML/3.5.6 (like Gecko) (Kubuntu)",
			"Mozilla/5.0 (X11; Linux x86_64; en-US; rv:2.0b2pre) Gecko/20100712 Minefield/4.0b2pre",
			"Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7",
			"MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.17) Gecko/20110123 SeaMonkey/2.0.12",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061024 Firefox/2.0 (Swiftfox)",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
			"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.56 Safari/537.4",
			"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1478.0 Safari/537.36",
			"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.22 (KHTML like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22",
			"Mozilla/4.0 (compatible; Dillo 3.0)",
			"Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) lt-GtkLauncher",
			"Mozilla/5.0 (X11; Linux i686; rv:16.0) Gecko/20100101 Firefox/16.0",
			"Mozilla/5.0 (X11; U; Linux i686; rv:19.0) Gecko/20100101 Slackware/13 Firefox/19.0",
			"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0",
			"Mozilla/5.0 (X11; Linux i686; rv:20.0) Gecko/20100101 Firefox/20.0",
			"Mozilla/5.0 (X11; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0",
			"Mozilla/5.0 (X11; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Galeon/2.0.6 (Ubuntu 2.0.6-2)",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.16) Gecko/20080716 (Gentoo) Galeon/2.0.6",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8",
			"Mozilla/5.0 (X11; Linux i686; rv:14.0) Gecko/20100101 Firefox/14.0.1 Iceweasel/14.0.1",
			"Mozilla/5.0 (X11; Linux x86_64; rv:15.0) Gecko/20120724 Debian Iceweasel/15.02",
			"Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0 Iceweasel/19.0.2",
			"Mozilla/5.0 (compatible; Konqueror/4.2; Linux) KHTML/4.2.4 (like Gecko) Slackware/13.0",
			"Mozilla/5.0 (compatible; Konqueror/4.3; Linux) KHTML/4.3.1 (like Gecko) Fedora/4.3.1-3.fc11",
			"Mozilla/5.0 (compatible; Konqueror/4.4; Linux) KHTML/4.4.1 (like Gecko) Fedora/4.4.1-1.fc12",
			"Mozilla/5.0 (compatible; Konqueror/4.4; Linux 2.6.32-22-generic; X11; en_US) KHTML/4.4.3 (like Gecko) Kubuntu",
			"Mozilla/5.0 (compatible; Konqueror/4.4; Linux 2.6.32-22-generic; X11; en_US) KHTML/4.4.3 (like Gecko) Kubuntu",
			"Mozilla/5.0 (X11; Linux 3.8-6.dmz.1-liquorix-686) KHTML/4.8.4 (like Gecko) Konqueror/4.8",
			"Mozilla/5.0 (X11; Linux) KHTML/4.9.1 (like Gecko) Konqueror/4.9",
			"Midori/0.1.10 (X11; Linux i686; U; en-us) WebKit/(531).(2) ",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330",
			"Opera/9.64 (X11; Linux i686; U; Linux Mint; nb) Presto/2.1.1",
			"Opera/9.80 (X11; Linux i686; U; en) Presto/2.2.15 Version/10.10",
			"Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00",
			"Opera/9.80 (X11; Linux i686) Presto/2.12.388 Version/12.16",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.166 Safari/537.36 OPR/20.0.1396.73172",
			"Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) QupZilla/1.2.0 Safari/534.34",
			"Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
			"Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20120502 Firefox/12.0 SeaMonkey/2.9.1",
			"Mozilla/5.0 (X11; U; Linux x86_64; us; rv:1.9.1.19) Gecko/20110430 shadowfox/7.0 (like Firefox/7.0",
			"Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.2.3) Gecko/20100406 Firefox/3.6.3 (Swiftfox)",
			"Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0",
			"Mozilla/5.0 (X11; U; OpenBSD i386; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.359.0 Safari/533.3",
			"Mozilla/5.0 (X11; U; FreeBSD x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16",
			"Mozilla/5.0 (X11; U; SunOS sun4m; en-US; rv:1.4b) Gecko/20030517 Mozilla Firebird/0.6",
			"Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.6) Gecko/20040406 Galeon/1.3.15",
			"Mozilla/5.0 (compatible; Konqueror/3.5; NetBSD 4.0_RC3; X11) KHTML/3.5.7 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/3.5; SunOS) KHTML/3.5.1 (like Gecko)",
			"Mozilla/5.0 (X11; U; FreeBSD; i386; en-US; rv:1.7) Gecko",
			"Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)",
			"Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)",
			"Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/536.5 (KHTML like Gecko) Chrome/19.0.1084.56 Safari/536.5",
			"Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.79 Safari/537.4",
			"Mozilla/5.0 (X11; U; OpenBSD arm; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0",
			"Mozilla/5.0 (X11; U; FreeBSD amd64; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0",
			"Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.9.1b3) Gecko/20090429 Firefox/3.1b3",
			"Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.1) Gecko/20090702 Firefox/3.5",
			"Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8",
			"Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0",
			"Mozilla/5.0 (compatible; Konqueror/4.1; DragonFly) KHTML/4.1.4 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/4.1; OpenBSD) KHTML/4.1.4 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/4.5; NetBSD 5.0.2; X11; amd64; en_US) KHTML/4.5.4 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/4.5; FreeBSD) KHTML/4.5.4 (like Gecko)",
			"Mozilla/5.0 (X11; U; NetBSD amd64; en-US; rv:1.9.2.15) Gecko/20110308 Namoroka/3.6.15",
			"Opera/9.80 (X11; FreeBSD 8.1-RELEASE i386; Edition Next) Presto/2.12.388 Version/12.10",
			"Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.8.1.12) Gecko/20080303 SeaMonkey/1.1.8"
			]
	
	session = requests.Session()
	a = requests.adapters.HTTPAdapter(max_retries=10)
	b = requests.adapters.HTTPAdapter(max_retries=10)
	session.mount('http://', a)
	session.mount('https://', b)
	

	headers = {'User-Agent': useragents[random.randint(0, 257)]}
	print(headers)
	page = session.get(amazon_url,headers = headers).text

	parser = html.fromstring(page)

	XPATH_ASIN = '//li[contains(@class, "s-result-item")]/@data-asin'

	asins = parser.xpath(XPATH_ASIN)
	# print asins
	asin_string = ""
	for asin in asins:
		asin_string = asin_string + asin + "\n"
	# print asin_string
	return asin_string



def ReadBrowseNodes():
	BnodesList = [
		
	'172500', # desktop memory
	'229189', # desktop cpus
	'1292116011', # internal solid state drives

	'12097479011', # over ear
	'12097480011', # on ear
	'12097478011', # ear bud

	'300189', # wireless routers
	'1161760', # power supplies
	'572238', # computer cases
	'1254762011', # desktop internal harddrives
	'595048', # all external harddrives; portable and desktop
	'3151491', # usb flashdrives
	'402051011', # gaming keyboard
	'1048424', # all motherboards; intel and amd
	'172648', # laser printers
	'11036491', # mice
	
	'402052011', # PC gaming mice
	'405592011', # Mac gaming mice

	'11036281', # cpu fans
	'2998409011', # heat sinks
	'3015422011', # liquid cooling
	'13896615011', # traditional laptops
	'13896609011', # 2 in 1 laptops
	'284823', # sound cards # only until page 20
	'202505011' # hdmi cables
	]
	shuffled_pages = {}

	for bnode in BnodesList:
		shuffled_pages[bnode] = [[x] for x in range(66,69)]
		#shuffle(shuffled_pages[bnode])		
		shuffled_pages[bnode].reverse()
		
		# print(shuffled_pages[bnode])
	for i in range(66,69):
		print("Iteration: "+ str(i))
		for bnode in BnodesList:
			extracted_data = ""
		
			bnode_page = shuffled_pages[bnode].pop()

			print("Node: " + str(bnode))
			print("Page: " + str(bnode_page[0]))

			extracted_data = extracted_data + ParseProducts(bnode, bnode_page[0])

			# print(extracted_data)
			filename = "bnode/"+bnode+"/"+bnode+ "_"+str(bnode_page[0]) + ".txt"
			# f=open(filename,'w')
			# json.dump(extracted_data,f,indent=4)
			with open(filename, "w") as f:
				f.write(extracted_data)
			sleep(random.randint(20,30))

if __name__ == '__main__':
	ReadBrowseNodes()
