#!/usr/bin/env python

from mininet.log import setLogLevel, info
from minindn.wifi.minindnwifi import MinindnAdhoc #MinindnAdhocクラスを利用する方針で。
#from mininet.wifi.node import Station
#from mininet.wifi.link import wmediumd, adhoc
from mininet.net import Mininet
from mininet.util import quietRun

from minindn.apps.nfd import Nfd
from minindn.apps.nlsr import Nlsr
from minindn.apps.app_manager import AppManager
#from minindn.apps.appmanager import AppManager

def cleanUp():
    "Mini-NDNとMininetの古いプロセスをすべてクリアする"
    quietRun('sudo mn -c')

def run_adhoc_experiment():
    "2つのノード間でNDNアドホック通信を確立する"
    info("*** 実験環境のクリーンアップ\n")
    cleanUp()

    net = MinindnAdhoc()

    net.start()


    info("*** ホストの追加\n")
    sta1 = net.addStation('sta1',
                          mac='00:00:00:00:00:01',
                          ip='10.0.0.1/8')
    sta2 = net.addStation('sta2',
                          mac='00:00:00:00:00:02',
                          ip='10.0.0.2/8')
    # 位置の設定
    sta1.params['position'] = '10,20,0'
    sta2.params['position'] = '30,20,0'
    
    info("*** Ad-hocリンクの作成\n")
    net.addLink(sta1, sta2,
                cls=adhoc,
                intf='sta1-wlan0',
                ssid='adhocNet',
                mode='g',
                channel=5,
                delay='10ms',
                bw=100)
    
    net.build()
    net.start()

    info("*** NDNコンポーネントの開始\n")
    nfds = AppManager(net, net.stations, Nfd)
    
    # NLSRの隣接ノードを手動で定義
    faceDict = {'sta1': [('sta2', 1)], 'sta2': [('sta1', 1)]}
    nlsrs = AppManager(net, net.stations, Nlsr, faceDict=faceDict)
    nlsrs.start()

    info("*** ミニネットCLIの開始\n")
    # ここで ndnping の実行と検証を行う
    
    info("*** 実験の終了\n")
    # net.stop() # CLIを終了するまで実行を停止しない

if __name__ == '__main__':
    setLogLevel('info')
    run_adhoc_experiment()