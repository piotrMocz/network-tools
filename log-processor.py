import matplotlib.pyplot as plt
import numpy as np
import os
from string import strip

LOGS_DIR = '/home/moczur/Dev/social_traffic/.logs'


def parse_line(line):
    timestamp, usr_id, msg_type = map(strip, line.split(", "))[:3]
    timestamp = int(timestamp.split(".")[0])
    r = 1 if msg_type == 'R' else 0
    s = 1 if msg_type == 'S' else 0
    cc = 1 if msg_type == 'CC' else 0
    return timestamp, {
        #  'uid': [usr_id],
        'R': r, 'S': s, 'CC': cc}


def combine_infos(info1, info2):
    return {'R': info1['R'] + info2['R'],
            'S': info1['S'] + info2['S'],
            'CC': info1['CC'] + info2['CC']}


def read_log(file_path):
    time_series = {}

    with open(file_path, 'r') as logfile:
        for line in logfile.readlines():
            timestamp, msg_info = parse_line(line)

            if timestamp in time_series:
                time_series[timestamp] = combine_infos(time_series[timestamp], msg_info)
            else:
                time_series[timestamp] = msg_info

    return time_series


def combine_time_series(ts1, ts2):
    for timestamp2, msg_info2 in ts2.iteritems():
        if timestamp2 in ts1:
            ts1[timestamp2] = combine_infos(ts1[timestamp2], msg_info2)
        else:
            ts1[timestamp2] = msg_info2

    return ts1


def load_logs():
    print "Loading the logs..."
    logs = {}

    for f in os.listdir(LOGS_DIR):
        file_path = os.path.join(LOGS_DIR, f)
        time_series = read_log(file_path)
        logs = combine_time_series(logs, time_series)

    return logs


def compute_logs(logs):
    print "Computing stats..."
    N = len(logs)
    rs = np.zeros(N)
    ss = np.zeros(N)
    ccs = np.zeros(N)

    idx = 0
    for info in logs.itervalues():
        rs[idx] = info['R']
        ss[idx] = info['S']
        ccs[idx] = info['CC']

        idx += 1

    rs_pref = np.cumsum(rs)
    ss_pref = np.cumsum(ss)
    ccs_pref = np.cumsum(ccs)

    return {'R': (rs, rs_pref),
            'S': (ss, ss_pref),
            'CC': (ccs, ccs_pref)}


def dump_logs(logs, dump_file):
    print "Dumping logs to file..."
    with open(dump_file, 'w+') as f:
        for t, info in logs.iteritems():
            f.write("{0}, {1}\n".format(t, info))

    print "Finished dumping the logs!"


def process_logs(received=True, sent=True, created=True, linear=True, cumulative=True):
    logs = load_logs()
    results = compute_logs(logs)
    dump_logs(logs, "logs.txt")

    rs, rs_pref = results['R']
    ss, ss_pref = results['S']
    ccs, ccs_pref = results['CC']

    xs = np.arange(len(logs))

    if linear:
        print "Plotting linear..."
        plt.figure(figsize=(10, 8), dpi=120)
        plt.subplot(1, 1, 1)

        if received:
            plt.plot(xs, rs, 'b^-', label='Received')
        if sent:
            plt.plot(xs, ss, 'gv-', label='Sent')
        if created:
            plt.plot(xs, ccs, 'ro-', label='Created')

        plt.legend(loc='best')
        plt.xlabel('Time')
        plt.ylabel('No of requests')
        plt.title('Social network actions time series')
        plt.savefig('plot.png')
        plt.close()

    if cumulative:
        print "Plotting cumulative..."
        plt.figure(figsize=(10, 8), dpi=120)
        plt.subplot(1, 1, 1)

        if received:
            plt.plot(xs, rs_pref, 'b^-', label='Received')
        if sent:
            plt.plot(xs, ss_pref, 'gv-', label='Sent')
        if created:
            plt.plot(xs, ccs_pref, 'ro-', label='Created')

        plt.legend(loc='best')
        plt.xlabel('Time')
        plt.ylabel('No of requests')
        plt.title('Social network actions time series [cumulative]')
        plt.savefig('plot_pref.png')
        plt.close()

    print "Finished the log processing!"

if __name__ == '__main__':
    print "Processing..."
    process_logs()
