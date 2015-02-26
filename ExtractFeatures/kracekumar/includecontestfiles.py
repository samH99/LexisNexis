import glob
import os
import time
import string


header_value = """\
=============================
Programming Contest Solutions
=============================

The following project page contains the solutions to some programming contest
problems.

"""
footer_value = """

**Last Updated:** |today|
"""

date_file_list = []

template_value = """
*$filename* - $lastmodified

.. literalinclude:: ../$fileloc
   :language: c
   :tab-width: 4

----
"""

uthcodepath = '/home/senthil/uthcode/'

cfiles = glob.glob(uthcodepath + 'contests/topcoder/*.cpp')
for each in cfiles:
    stats = os.stat(each)
    last_modified_date = time.localtime(stats[8])
    date_file_tuple = last_modified_date, each
    date_file_list.append(date_file_tuple)

date_file_list.sort()
date_file_list.reverse()

content = []
for item in date_file_list:
    s = string.Template(template_value)
    filename_value = item[1].split('/')[-1]
    fileloc_value = item[1].replace(uthcodepath,'')
    lastmodified_value = time.strftime("On %d %b,%Y.",item[0])
    o = s.substitute(fileloc=fileloc_value,
            filename=filename_value,
            lastmodified=lastmodified_value)
    content.append(o)


content = ''.join(content)

fobject = open(uthcodepath + 'source/contests.rst','w')
fobject.write(header_value)
fobject.write(content)
fobject.write(footer_value)
fobject.close()
