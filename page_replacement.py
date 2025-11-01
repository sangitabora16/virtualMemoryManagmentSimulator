class ReplacementPolicy:
    @staticmethod
    def FIFO(frames, usage, page):
        if -1 in frames:
            return frames.index(-1)
        return frames.index(usage[0])  # Evict the oldest page in usage

    @staticmethod
    def LRU(frames, usage, page):
        if -1 in frames:
            return frames.index(-1)
        for p in usage:
            if p in frames:
                return frames.index(p)  # Evict the least recently used

    @staticmethod
    def Optimal(frames, usage, page):
        if -1 in frames:
            return frames.index(-1)

        # Predict future usage of each page currently in frame
        future = usage[1:]  # current page is at usage[0]
        farthest_use = {}

        for f in frames:
            if f in future:
                farthest_use[f] = future.index(f)
            else:
                return frames.index(f)  # Not used again, best candidate

        farthest_page = max(farthest_use, key=farthest_use.get)
        return frames.index(farthest_page)