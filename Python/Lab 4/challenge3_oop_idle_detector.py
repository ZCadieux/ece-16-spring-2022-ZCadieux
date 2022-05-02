from ECE16Lib.IdleDetector import IdleDetector

det = IdleDetector("COM4", 115200)
det.detectIdle()