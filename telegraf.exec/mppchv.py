import os

measurement = 'mppchv'

mppchv_text = '/misc/subdata/MPPC_HV/mppcbias_summary.txt'

if __name__ == '__main__':
  hv_set = []
  hv_mon = []
  i_mon = []
  temp = []
  ch_name = []
  ch_state = []
  with open(mppchv_text, 'r') as f:
    lines = f.readlines()
    for line in lines:
      columns = line.split()
      if len(columns) == 2:
        host = columns[0]
        if columns[0] == "192.168.30.81":
          device = 'bft'
          if columns[1] =="ON":
            state = 1
          elif columns[1] == "OFF":
            state = 0
          else:
            state = -1
          board_state = state
          print(f'{measurement},device={device},channel=board status={board_state}')
      if len(columns) == 8:
        if columns[1] =="ON":
          state = 1
        elif columns[1] == "OFF":
          state = 0
        else:
          state = -1
        hv_set.append(columns[4])
        hv_mon.append(columns[5])
        i_mon.append(columns[6])
        temp.append(columns[7])
        ch_name.append(device + columns[0])
        ch_state.append(state)
        print(f'{measurement},device={device},channel={columns[0]} status={state},hv_set={columns[4]},hv_mon={columns[5]},i_mon={columns[6]},temp={columns[7]}')
