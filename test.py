from cloudpathlib import CloudPath
from pathlib import Path

r = CloudPath("gs://test/dir1/test.txt")
print(r.bucket)