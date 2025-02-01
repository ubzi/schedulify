class Task:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration

class Dependency:
    def __init__(self, dependent_task: Task, prereq_task: Task):
        self.dependent_task = dependent_task
        self.prereq_task = prereq_task


begin = Task("begin", 4)
a = Task("a", 3)
b = Task("b", 4)
e = Task("e", 1)
g = Task("g", 2)
c = Task("c", 3)
h = Task("h", 7)
d = Task("d", 5)
p = Task("p", 4)
f = Task("f", 6)
q = Task("q", 2)
end = Task("end", 3)

tasks = [a, b, c, d, e, f, g, h, p, q, begin, end]

d0 = Dependency(begin, None)
d1 = Dependency(a, begin)
d2 = Dependency(b, begin)
d3 = Dependency(e, begin)
d4 = Dependency(g, a)
d5 = Dependency(g, e)
d6 = Dependency(c, a)
d7 = Dependency(c, g)
d8 = Dependency(c, b)
d9 = Dependency(h, g)
d10 = Dependency(d, c)
d11 = Dependency(p, d)
d12 = Dependency(p, c)
d13 = Dependency(p, h)
d14 = Dependency(f, d)
d15 = Dependency(q, p)
d16 = Dependency(q, h)
d17 = Dependency(end, f)
d18 = Dependency(end, q)
d19 = Dependency(end, p)

dependencies = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19]