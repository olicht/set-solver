from config import *

if video:
	import set_video
	set_video.main()
else:
	import tests
	tests.main()
