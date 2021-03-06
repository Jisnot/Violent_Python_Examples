# _*_coding:utf8-
import dpkt
import optparse
import socket

THRESH = 1000

def findDownload(pcap):
    for ts,buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            tcp = ip.data
            http = dpkt.http.Request(tcp.data)
            if http.method == 'GET':
                uri = http.uri.lower()
                if '.zip' in uri and 'loic' in uri:
                    print '[!] ' + src + ' Download LOIC'
        except:
            print '[-] Not Find'

def findHivemind(pcap):
    for ts,buf in pcap:
        try:
            eth= dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            sport = tcp.sport
            if dport == 6667:
                if '!lazor' in tcp.data.lower():
                    print '[!] DDos Hivemind issued by: ' + src
                    print '[+] Target CMD: ' + tcp.data

            if sport == 6667:
                if '!lazor' in tcp.data.lower():
                    print '[!] DDos Hivemind issued by: ' + src
                    print '[+] Target CMD: ' + tcp.data

        except:
            pass


def findAttcak(pcap):
    pktCount = {}
    for ts,buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            if dport == 80:
                stream = src + ';' + dst
                if pktCount.has_key(stream):
                    pktCount[stream] = pktCount[stream] + 1
                else:
                    pktCount[stream] =1
        except:
            pass

    for stream in pktCount:
        pktsSent = pktCount[stream]
        if pktsSent > THRESH:
            src = stream.split(':')[0]
            dst = stream.split(':')[1]
            print '[+] ' + src + ' attacked ' + dst + ' with ' + str(pktsSent) + ' pkts.'
def main():
    global THRESH
    parser = optparse.OptionParser('usage%prog ' + '-p <pcap file> -t <thresh>')
    parser.add_option('-p',dest = 'pcapFile',type='string',help = 'specify pcap filename')
    parser.add_option('-t',dest = 'thresh',type='int',help = 'specify threshold count')
    (options,args) = parser.parse_args()
    pcapFile = options.pcapFile
    thresh = options.thresh
    if pcapFile is None:
        print parser.usage
        exit(0)
    if thresh is not None:
        THRESH = thresh
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    findDownload(pcap)
    findHivemind(pcap)
    findHivemind(pcap)

if __name__ == '__main__':
    main()


