import os

import os
for file in os.listdir("./"):
    if file.endswith(".ini"):
        print(os.path.join("./", file))