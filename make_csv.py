import fileinput
import re

RE = re.compile(r"[a-zA-Z]{3} \d\d \d\d:\d\d:\d\d ([0-9]+\.[0-9]+) .... ([0-9A-Za-z]{3}) ")

all_events = {}

all_times = []


count = 0

with open("copy.txt", "w") as backup:
  with open("crtd.txt", "w") as crtd:
    for line in fileinput.input(mode="rb"):
      try:
        line = line.decode("utf-8")
        backup.write(line)
        crtd.write(line[16:])
        m = RE.match(line)
        if m:
          #print(m.groups())
          timestamp, e = m.groups()
          l = all_events.get(e, [])
          l.append(timestamp)
          all_events[e] = l
          all_times.append( (timestamp, e) )    

          
        else:
          print("ignoring:", line.strip())
          pass  
      except UnicodeDecodeError as e:
        print("Unicode error in line",str(count))
        print(e)
        backup.write("### Error ###\n")
      
      count += 1
      #if count > 100:
      #  break
    
all_keys = list(all_events.keys())
all_keys.sort()

with open("data.csv", "w") as f:

  f.write('"Time";'+";".join( [ '"'+x+'"' for x in all_keys ]  )+"\n")
  last_t = 0
  for t,e in all_times:
    tval = float(t)
    
    if last_t > 0:
      delta = tval - last_t
      if delta > 1000:
        # something's wrong? skip this one...
        print("Error? Time delta very high:", str(delta), "Skipping:", t, e)
        continue
    last_t = tval
  
    row = [t] + (len(all_keys)*["0"])
    row[all_keys.index(e) + 1] = "1"
    f.write(";".join(row)+"\n")
    
with open("plot.txt", "w") as f:
  f.write('''set terminal png notransparent interlace size 640,480
             set datafile separator ";"
             set key autotitle columnheader\n
             ''')
  for i in range(len(all_keys)):
    f.write('set output "'+all_keys[i]+'.png"\n')
    f.write('plot "data.csv" using 1:'+str(i+2)+' with lines\n')
  
  
    
    

